""" module:: xcp.client
    :platform: Any
    :synopsis: XCP Client originally called Master specification
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
import time
from queue import Queue, Empty
from threading import Thread
from enum import IntEnum
from typing import Union

from xcp.transport import XcpOnCan, XcpTransport
from xcp.protocol import XCP_PROTOCOL_VERSION, PacketIdFromServer, concat_connect_command, \
    ConnectMode, StdCmd, concat_disconnect_command, concat_get_comm_mode_info, \
    concat_get_status_command, ComModeBasicFlag, concat_clear_daq_list, concat_set_daq_ptr, \
    concat_write_daq, DaqListMode, concat_set_daq_list_mode, parse_packet_from_server, concat_get_daq_list_mode, \
    DaqStartStopMode, concat_start_stop_daq_list, concat_start_stop_daq_sync, concat_get_daq_clock, concat_read_daq, \
    XcpTimeout, XcpTrueTimeout, concat_sync, XcpErrorSyncCmd, raise_for_error, concat_get_daq_processor_info, \
    concat_get_daq_resolution_info, concat_get_server_id, concat_get_daq_id, concat_set_daq_id, TransportLayerCmdCAN


class XcpClientState(IntEnum):
    Init = 0
    NotConnected = 1
    Connected = 2


class XcpClient:
    """
    This class represents the XCP Master which is the client side of XCP.
    """

    def __init__(self, transport: Union[XcpTransport, XcpOnCan]):
        """
        Constructor

        :param transport: A xcp transport instance.
        """
        self._logger = logging.getLogger(__name__)
        self.timeouts = {"t1": 0.1,
                         "t2": 0.1,
                         "t3": 0.1,
                         "t4": 0.1,
                         "t5": 0.1,
                         "t6": 0.1,
                         "t7": 0.1,
                         }  # The timeouts t1 - t7, these are to be taken from ASAM MCD file (.A2L)
        self._state = None
        self._protocol_layer_version = XCP_PROTOCOL_VERSION
        self._endianess = "little"

        self.state = XcpClientState.Init
        self.rx_queue = Queue()
        self.rx_handler = Thread(target=self.handle_rx)
        self.rx_handler.daemon = True
        self.transport = transport
        # do some init
        self.state = XcpClientState.NotConnected
        self.rx_handler.start()

    @property
    def state(self) -> XcpClientState:
        return self._state

    @state.setter
    def state(self, value: XcpClientState) -> None:
        self._state = value

    @property
    def endianess(self):
        return self._endianess

    @endianess.setter
    def endianess(self, value):
        self._logger.info("Set Endianess to '{0}'".format(value))
        self._endianess = value

    def handle_rx(self):
        """
        The thread handling incoming communication.

        It feeds into local receive queue where request mechanism checks for responses.
        :TODO: This method will not work once DAQ is implemented. DAQ needs a separate queue or hook.
        :return: Nothing.
        """
        while True:
            data = self.transport.recv()
            try:
                packet_id = PacketIdFromServer(data[0])
            except ValueError:
                pass
            else:
                assert packet_id
                self.rx_queue.put(data)

    def _request(self, req: Union[bytes, bytearray], timeout: float) -> dict:
        """
        A single shot request / response mechanism that can return either
        a response, a timeout, or will raises an error.

        :param req: The request.
        :type req: bytes, bytearray
        :return: The response.
        :rtype: dict
        :raises XcpTimeout, XcpEvent
        """
        cmd = StdCmd(req[0])
        sub_cmd = None
        if cmd == StdCmd.TransportLayerCmd:
            sub_cmd = TransportLayerCmdCAN(req[1])
        self.transport.send(req)
        try:
            resp = parse_packet_from_server(cmd=cmd,
                                            data=self.rx_queue.get(timeout=timeout),
                                            endianess=self.endianess,
                                            sub_cmd=sub_cmd)
        except Empty:
            raise XcpTimeout
        raise_for_error(resp)
        return resp

    def request(self, req: Union[bytes, bytearray], retry_cnt: int = 2) -> dict:
        """
        Send a request to the server and handle the request / response mechanism

        :param req: The request.
        :type req: bytes, bytearray
        :param retry_cnt: The retry count. In case of timeout t1, xcp tries again.
        :type retry_cnt: int
        :return: The response.
        :rtype: dict
        """
        timeout = self.timeouts.get("t1")
        cmd = StdCmd(req[0])
        for i in range(retry_cnt):
            try:
                resp = self._request(req=req,
                                     timeout=timeout)
            except XcpTimeout:
                # do the pre-action and the action according to xcp spec
                # keep it simple, just wait t7 and then sync
                if cmd != StdCmd.Sync:
                    self._logger.debug("Trigger sync after timeout.")
                    time.sleep(self.timeouts.get("t7"))
                    try:
                        self.request(req=concat_sync(), retry_cnt=2)
                    except XcpErrorSyncCmd:
                        continue
            else:
                return resp
        raise XcpTrueTimeout

    def connect(self, mode: ConnectMode = ConnectMode.Normal) -> dict:
        """
        Connect to server.

        :param mode: The connection mode.
        :type mode: ConnectMode
        :return: The response.
        :rtype: dict
        """
        resp = self.request(req=concat_connect_command(mode=mode))
        self.on_connect_response(resp=resp)
        return resp

    def on_connect_response(self, resp: dict) -> None:
        """
        A hook to react on connect response.

        :param resp: The response.
        :type resp: dict
        :return: Nothing.
        """
        if ComModeBasicFlag.MSBFirst in resp.get("com_mode_basic_flags"):
            self.endianess = "big"

    def disconnect(self):
        """
        Disconnect from server.

        :return: The response which is just an ack.
        :rtype: dict.
        """
        return self.request(req=concat_disconnect_command())

    def get_status(self):
        """
        Get the session status from server.

        :return: The response.
        :rtype: dict
        """
        resp = self.request(req=concat_get_status_command())
        self.on_get_status_response(resp=resp)
        return resp

    def on_get_status_response(self, resp: dict) -> None:
        """
        A hook to react on get status response.

        :param resp: The response.
        :type resp: dict
        :return: Nothing.
        """
        pass

    def get_comm_mode_info(self):
        """
        Get the comm mode info from server.

        :return: The response.
        :rtype: dict
        """
        resp = self.request(req=concat_get_comm_mode_info())
        self.on_get_comm_mode_info_response(resp=resp)
        return resp

    def on_get_comm_mode_info_response(self, resp: dict) -> None:
        """
        A hook to react on get comm mode info response.

        :param resp: The response.
        :type resp: dict
        :return: Nothing.
        """
        pass

    def clear_daq_list(self, daq_list: int):
        resp = self.request(req=concat_clear_daq_list(daq_list=daq_list, endianess=self.endianess))
        return resp

    def set_daq_ptr(self, daq_list: int, odt_list: int, odt_elem: int):
        resp = self.request(req=concat_set_daq_ptr(daq_list=daq_list, odt_list=odt_list, odt_elem=odt_elem,
                                                   endianess=self.endianess))
        return resp

    def write_daq(self, bit_offset: int, size: int, ext: int, addr: int):
        resp = self.request(req=concat_write_daq(bit_offset=bit_offset, size=size, ext=ext, addr=addr,
                                                 endianess=self.endianess))
        return resp

    def set_daq_list_mode(self, mode: DaqListMode, daq_list: int, chan: int, prescaler: int,
                          prio: int):
        resp = self.request(req=concat_set_daq_list_mode(daq_list=daq_list, mode=mode, chan=chan,
                                                         prescaler=prescaler, prio=prio, endianess=self.endianess))
        return resp

    def get_daq_list_mode(self, daq_list: int):
        resp = self.request(req=concat_get_daq_list_mode(daq_list=daq_list, endianess=self.endianess))
        return resp

    def start_stop_daq_list(self, daq_list: int, mode: DaqStartStopMode):
        resp = self.request(req=concat_start_stop_daq_list(daq_list=daq_list, mode=mode, endianess=self.endianess))
        return resp

    def start_stop_daq_sync(self, mode: DaqStartStopMode):
        resp = self.request(req=concat_start_stop_daq_sync(mode=mode))
        return resp

    def get_daq_clock(self):
        resp = self.request(req=concat_get_daq_clock())
        return resp

    def read_daq(self):
        resp = self.request(req=concat_read_daq())
        return resp

    def get_daq_processor_info(self):
        resp = self.request(req=concat_get_daq_processor_info())
        return resp

    def get_daq_resolution_info(self):
        resp = self.request(req=concat_get_daq_resolution_info())
        return resp

    def get_server_id(self, invert_echo: bool = False):
        resp = self.request(req=concat_get_server_id(invert_echo=invert_echo))
        return resp

    def get_daq_id(self, daq_list: int):
        resp = self.request(req=concat_get_daq_id(daq_list=daq_list,
                                                  endianess=self.endianess))
        return resp

    def set_daq_id(self, daq_list: int, can_id: int):
        resp = self.request(req=concat_set_daq_id(daq_list=daq_list,
                                                  can_id=can_id,
                                                  endianess=self.endianess))
        return resp
