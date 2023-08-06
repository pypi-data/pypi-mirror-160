""" module:: xcp.slave
    :platform: Any
    :synopsis: XCP Server originally called Slave in specification
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
from threading import Thread
from enum import IntEnum
from typing import Union

from xcp.daq import DaqTable, OdtElem, DaqProcessor
from xcp.transport import XcpOnCan, XcpTransport
from xcp.protocol import parse_packet_from_client, StdCmd, concat_connect_response, ResourceFlag, ComModeBasicFlag, \
    XCP_PROTOCOL_VERSION, concat_response_packet, SessionStatus, ProtectionStatus, concat_status_response, \
    concat_comm_mode_info_response, ComModeOptional, ErrCode, concat_error_packet, concat_get_daq_list_mode_response, \
    concat_start_stop_daq_list_response, concat_get_daq_clock_response, concat_read_daq_response, \
    concat_get_daq_processor_info_response, concat_get_daq_resolution_info_response, concat_get_server_id_response, \
    concat_get_daq_id_response, TransportLayerCmdCAN


class XcpServerState(IntEnum):
    Init = 0
    NotConnected = 1
    Connected = 2


class XcpServer:
    """
    This class represents the XCP Slave which is the server side of XCP.
    This implementation is, for now intended to work as a mock to test the client side.
    Therefore implementation only includes standard / non-optional services.
    The resume Mode is also omitted for now.
    """

    def __init__(self,
                 transport: Union[XcpTransport, XcpOnCan],
                 endianess: str = "big"):
        """
        Constructor

        :param transport: A xcp transport instance.
        :type transport: XcpOnCan
        :param endianess: The endianess to use for built-in int-bytes conversion.
        :type endianess: str
        """
        self._logger = logging.getLogger(__name__)
        self._state = XcpServerState.Init
        self._resource = ResourceFlag(0)
        self._endianess = endianess
        self._com_mode_basic = ComModeBasicFlag(0)
        if self.endianess == "big":
            self._com_mode_basic |= ComModeBasicFlag.MSBFirst
        self._max_cto = 8
        self._max_dto = 8
        self._protocol_layer_version = XCP_PROTOCOL_VERSION
        self._session_status = SessionStatus(0)
        self._protection_status = ProtectionStatus(0)
        self._session_config_id = 0

        self._com_mode_optional = ComModeOptional(0)
        self._max_bs = 255
        self._min_st = 0
        self._queue_size = 255
        self._xcp_driver_version = 1.1  # what version should be here - Autosar Driver Version ?!

        self._daq_processor = DaqProcessor(daq_table=DaqTable(daq_table_length=10,
                                                              daq_list_length=10,
                                                              odt_list_length=10))

        self.cmd_handler_mapping = {StdCmd.Connect: self.on_connect,
                                    StdCmd.Disconnect: self.on_disconnect,
                                    StdCmd.GetStatus: self.on_get_status,
                                    StdCmd.GetCommModeInfo: self.on_get_comm_mode_info,
                                    StdCmd.Sync: self.on_sync,
                                    StdCmd.ClearDaqList: self.on_clear_daq_list_config,
                                    StdCmd.SetDaqPtr: self.on_set_daq_ptr,
                                    StdCmd.WriteDaq: self.on_write_daq,
                                    StdCmd.SetDaqListMode: self.on_set_daq_list_mode,
                                    StdCmd.GetDaqListMode: self.on_get_daq_list_mode,
                                    StdCmd.StartStopDaqList: self.on_start_stop_daq_list,
                                    StdCmd.StartStopSync: self.on_start_stop_sync,
                                    StdCmd.GetDaqClock: self.on_get_daq_clock,
                                    StdCmd.ReadDaq: self.on_read_daq,
                                    StdCmd.GetDaqProcessorInfo: self.on_get_daq_processor_info,
                                    StdCmd.GetDaqResolutionInfo: self.on_get_daq_resolution_info,
                                    StdCmd.TransportLayerCmd: self.on_transport_layer_command,
                                    }

        self.rx_handler = Thread(target=self.handle_rx)
        self.rx_handler.daemon = True
        self.transport = transport
        # do some init
        self.state = XcpServerState.NotConnected
        self.rx_handler.start()

    @property
    def state(self) -> XcpServerState:
        return self._state

    @state.setter
    def state(self, value: XcpServerState) -> None:
        if self._state != value:
            self._logger.info("State Change {0} -> {1}".format(self._state.name, value.name))
            self._state = value

    @property
    def resource(self):
        return self._resource

    @property
    def com_mode_basic(self):
        return self._com_mode_basic

    @property
    def max_cto(self):
        return self._max_cto

    @property
    def max_dto(self):
        return self._max_dto

    @property
    def protocol_layer_version(self):
        return self._protocol_layer_version

    @property
    def protection_status(self):
        return self._protection_status

    @property
    def session_status(self):
        return self._session_status

    @property
    def session_config_id(self):
        return self._session_config_id

    @property
    def endianess(self):
        return self._endianess

    @property
    def com_mode_optional(self):
        return self._com_mode_optional

    @property
    def max_bs(self):
        return self._max_bs

    @property
    def min_st(self):
        return self._min_st

    @property
    def queue_size(self):
        return self._queue_size

    @property
    def xcp_driver_version(self):
        return self._xcp_driver_version

    @property
    def daq_table(self):
        return self._daq_processor.daq_table

    def handle_rx(self):
        """
        The thread handling incoming communication.

        It reacts on the commands from a client.
        :return: Nothing.
        """
        while True:
            data = self.transport.recv()
            req = parse_packet_from_client(data=data, endianess=self.endianess)
            command = req.get("packet_id")
            handler = self.cmd_handler_mapping.get(command)
            if handler is not None and callable(handler):
                self._logger.debug("Handling Command {0}".format(command.name))
                handler(req)
            else:
                self._logger.error("Unhandled Command {0}".format(command.name))

    def on_connect(self, req: dict) -> None:
        """
        Connect

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Connect")
        data = concat_response_packet(command_response_data=concat_connect_response(
            resource=self.resource,
            com_mode_basic=self.com_mode_basic,
            max_cto=self.max_cto,
            max_dto=self.max_dto,
            protocol_layer_version=self.protocol_layer_version,
            transport_layer_version=self.transport.transport_layer_version,
        ))
        self.transport.send(data=data)
        self.state = XcpServerState.Connected

    def on_disconnect(self, req: dict) -> None:
        """
        Disconnect

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Disconnect")
        self.transport.send(concat_response_packet())
        self.state = XcpServerState.NotConnected

    def on_get_status(self, req: dict):
        """
        Get Status

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Get Status")
        self.transport.send(
            concat_response_packet(command_response_data=concat_status_response(
                session_status=self.session_status,
                resource_protection_status=self.protection_status,
                session_config_id=self.session_config_id,
                endianess=self.endianess
            )))

    def on_get_comm_mode_info(self, req: dict):
        """
        Get Comm Mode Info

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Comm Mode Info")
        self.transport.send(
            concat_response_packet(command_response_data=concat_comm_mode_info_response(
                comm_mode_optional=self.com_mode_optional,
                max_bs=self.max_bs,
                min_st=self.min_st,
                queue_size=self.queue_size,
                xcp_driver_version=self.xcp_driver_version,
            )))

    def on_sync(self, req: dict):
        """
        Sync

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Sync")
        self.transport.send(
            concat_error_packet(error_code=ErrCode.CmdSync,
                                ))

    def on_clear_daq_list_config(self, req: dict):
        """
        Clear daq list config

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Clear Daq List Config")
        self.transport.send(concat_response_packet())

    def on_set_daq_ptr(self, req: dict):
        """
        Set daq ptr

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Set Daq Ptr")

        try:
            self.daq_table.set_ptr(daq_list_idx=req.get("daq_list"),
                                   odt_list_idx=req.get("odt_list"),
                                   odt_elem_idx=req.get("odt_elem")
                                   )
        except IndexError:
            self._logger.error("IndexError while setting dag ptr to {0}".format(req))
            self.transport.send(concat_error_packet(error_code=ErrCode.OutOfRange))
        else:
            self.transport.send(concat_response_packet())

    def on_write_daq(self, req: dict):
        """
        Write daq

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Write Daq")
        self.transport.send(concat_response_packet())
        self.daq_table.write(value=OdtElem(addr=req.get("addr"),
                                           bit_offset=req.get("bit_offset"),
                                           ext=req.get("ext"),
                                           size=req.get("size")))

    def on_set_daq_list_mode(self, req: dict):
        """
        Set daq list mode

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Set Daq list mode")
        self.transport.send(concat_response_packet())

    def on_get_daq_list_mode(self, req: dict):
        """
        Get daq list mode

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Get Daq list mode")
        daq_list_data = self.daq_table.elems[req.get("daq_list")]
        self.transport.send(
            concat_response_packet(command_response_data=concat_get_daq_list_mode_response(
                mode=daq_list_data.mode,
                prescaler=daq_list_data.mode,
                chan=daq_list_data.chan,
                prio=daq_list_data.prio,
                endianess=self.endianess
            )))

    def on_start_stop_daq_list(self, req: dict):
        self._logger.debug("Start / Stop Daq list")
        daq_list_data = self.daq_table.elems[req.get("daq_list")]
        self.transport.send(
            concat_response_packet(command_response_data=concat_start_stop_daq_list_response(
                first_pid=daq_list_data.first_pid
            )))

    def on_start_stop_sync(self, req: dict):
        self._logger.debug("Start / Stop Sync")
        self.transport.send(concat_response_packet())

    def on_get_daq_clock(self, req: dict):
        self._logger.debug("Get Daq Clock")
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_get_daq_clock_response(
                    self.get_timestamp(),
                    endianess=self.endianess
                )))

    def get_timestamp(self) -> int:
        return 0

    def on_read_daq(self, req: dict):
        """
        Read Daq

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Read Daq")
        elem = self.daq_table.read()
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_read_daq_response(addr=elem.addr,
                                                               size=elem.size,
                                                               ext=elem.ext,
                                                               bit_offset=elem.bit_offset,
                                                               endianess=self.endianess
                                                               )))

    def on_get_daq_processor_info(self, req: dict):
        """
        Get Daq Processor Info

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Get Daq Processor Info")
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_get_daq_processor_info_response(
                    daq_property=self._daq_processor.daq_properties,
                    min_daq=self._daq_processor.min_daq,
                    max_daq=self._daq_processor.max_daq,
                    daq_key_byte_opt=self._daq_processor.daq_key_byte_opt,
                    daq_key_byte_id_type=self._daq_processor.daq_key_byte_id_type,
                    daq_key_byte_addr_ext=self._daq_processor.daq_key_byte_addr_ext,
                    max_event_chan=self._daq_processor.max_event_chan,
                    endianess=self.endianess
                )))

    def on_get_daq_resolution_info(self, req: dict):
        """
        Get Daq Processor Info

        :param req: The request message
        :return: Nothing.
        """
        self._logger.debug("Get Daq Resolution Info")
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_get_daq_resolution_info_response(
                    daq_granularity=self._daq_processor.daq_granularity,
                    daq_max_elem_size=self._daq_processor.daq_max_elem_size,
                    stim_granularity=self._daq_processor.stim_granularity,
                    stim_max_elem_size=self._daq_processor.stim_max_elem_size,
                    timestamp_resolution=self._daq_processor.timestamp_resolution,
                    timestamp_size=self._daq_processor.timestamp_size,
                    timestamp_fixed=self._daq_processor.timestamp_fixed,
                    timestamp_ticks=self._daq_processor.timestamp_ticks,
                    endianess=self.endianess
                )))

    def on_get_server_id(self, req: dict):
        """
        Get Server Id

        :param req: The request message
        :return: Nothing.
        """
        invert_echo = req.get("invert_echo")
        can_id = 0x1234  # TODO: get this can_id from transport
        self._logger.debug("Get Server Id, Invert echo {0}, can_id {1}".format(invert_echo, can_id))
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_get_server_id_response(
                    can_id=can_id,
                    invert_echo=invert_echo,
                    endianess=self.endianess
                )))

    def on_get_daq_id(self, req: dict):
        """
        Get Daq Id

        :param req: The request message
        :return: Nothing.
        """
        can_id = self._daq_processor.get_can_id_for_daq_list(daq_list=req.get("daq_list"))
        fixed = False
        self._logger.debug("Get Daq Id, fixed {0}, can_id {1}".format(fixed, can_id))
        self.transport.send(
            concat_response_packet(
                command_response_data=concat_get_daq_id_response(
                    can_id=can_id,
                    fixed=fixed,
                    endianess=self.endianess
                )))

    def on_set_daq_id(self, req: dict):
        """
        Set Daq Id

        :param req: The request message
        :return: Nothing.
        """
        self._daq_processor.set_can_id_for_daq_list(daq_list=req.get("daq_list"),
                                                    can_id=req.get("can_id"))
        self._logger.debug("Set Daq Id, list {daq_list}, can_id {can_id}".format_map(req))
        self.transport.send(concat_response_packet())

    def on_transport_layer_command(self, req: dict):
        """
        On Transport Layer command

        :param req: The request message
        :return: Nothing.
        """
        subcmd_mapping = {
            TransportLayerCmdCAN.GetSlaveId: self.on_get_server_id,
            TransportLayerCmdCAN.GetDaqId: self.on_get_daq_id,
            TransportLayerCmdCAN.SetDaqId: self.on_set_daq_id,
        }
        action = subcmd_mapping.get(req.get("sub_command"))
        if action is not None and callable(action):
            action(req)
