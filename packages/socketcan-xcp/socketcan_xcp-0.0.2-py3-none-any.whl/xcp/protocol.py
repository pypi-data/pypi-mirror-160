""" module:: xcp.protocol
    :platform: Any
    :synopsis: XCP Protocol Layer
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3

    Note: XCP is a point to point communication protocol from a XCP Master to a XCP slave.
          The protocol strictly distinguishes Command Code meanings by direction.
          The Command Codes, i.e. bytes that switch program flow are present in both with different meaning.
"""

from enum import IntEnum, IntFlag, unique
from typing import Optional, Union

import logging

LOGGER = logging.getLogger(__name__)

XCP_PROTOCOL_VERSION = 0x10


class SessionStatus(IntFlag):
    StoreCalReq = 1
    StoreDaqReq = 4
    ClearDaqReq = 8
    DaqRunning = 0x40
    Resume = 0x80


class ProtectionStatus(IntFlag):
    CalibrationAndPagingIsProtected = 1
    DaqIsProtected = 4
    StimIsProtected = 8
    ProgrammingIsProtected = 0x10


class ResourceFlag(IntFlag):
    CalibrationAndPagingSupported = 1
    DaqSupported = 4
    StimSupported = 8
    ProgrammingSupported = 16


class ComModeBasicFlag(IntFlag):
    MSBFirst = 1
    AddressGranularity0 = 2
    AddressGranularity1 = 4
    SlaveBlockModeAvailable = 64
    MoreTypesAvailable = 128


class ComModeOptional(IntFlag):
    MasterBlockMode = 1
    InterleavedMode = 2


class DaqListMode(IntFlag):
    Selected = 1
    Direction = 2
    TimeStamp = 0x10
    PidOff = 0x20
    Running = 0x40
    Resume = 0x80


class DaqStartStopMode(IntEnum):
    Stop = 0
    Start = 1
    Select = 2


class Granularity(IntEnum):
    """
    A local / non-protocol enum for convenience
    may be removed later if a better solution presents itself.
    """
    Byte = 0
    Word = 1
    DoubleWord = 2
    Reserved = 3


class DaqProperty(IntFlag):
    DynamicDaqListSuported = 1
    PrescalerSupported = 2
    ResumeSupported = 4
    BitStimSupported = 8
    TimestampSupported = 0x10
    PidOffSupported = 0x20
    OverloadMsb = 0x40
    OverloadEvent = 0x80


class DaqKeyByteOptimisation(IntEnum):
    Default = 0
    OdtType16 = 1
    OdtType32 = 2
    OdtType64 = 3
    OdtTypeAlign = 4
    OdtMaxEntrySize = 5


class DaqKeyByteAddrExtention(IntEnum):
    Free = 0  # CanBeDifferentInsideSameOdt
    OdtFixed = 1  # MustBeIdenticalInsideSameOdt
    NotAllowed = 2
    DaqFixed = 3  # MustBeIdenticalInsideSameDaq


class DaqKeyByteIdentificaitonType(IntEnum):
    AbsoluteOdt = 0
    RelativeOdtAbsoluteDaqByte = 1
    RelativeOdtAbsoluteDaqWord = 2
    RelativeOdtAbsoluteDaqWordAligned = 3


@unique
class ErrCode(IntEnum):
    CmdSync = 0  # Not an Error

    CmdBusy = 0x10
    DaqActive = 0x11
    PgmActive = 0x12

    CmdUnknown = 0x20
    CmdSyntax = 0x21
    OutOfRange = 0x22
    WriteProtected = 0x23
    AccessDenied = 0x24
    AccessLocked = 0x25
    PageNotValid = 0x26
    ModeNotValid = 0x27
    SegmentNotValid = 0x28
    Sequence = 0x29
    DaqConfig = 0x2A

    MemoryOverflow = 0x30
    Generic = 0x31
    Verify = 0x32


ERR_CODE_SEVERITY = {
    ErrCode.CmdSync: 0,
    ErrCode.CmdBusy: 2,
    ErrCode.DaqActive: 2,
    ErrCode.PgmActive: 2,
    ErrCode.CmdUnknown: 2,
    ErrCode.CmdSyntax: 2,
    ErrCode.OutOfRange: 2,
    ErrCode.WriteProtected: 2,
    ErrCode.AccessDenied: 2,
    ErrCode.AccessLocked: 2,
    ErrCode.PageNotValid: 2,
    ErrCode.ModeNotValid: 2,
    ErrCode.SegmentNotValid: 2,
    ErrCode.Sequence: 2,
    ErrCode.DaqConfig: 2,
    ErrCode.MemoryOverflow: 2,
    ErrCode.Generic: 2,
    ErrCode.Verify: 3
}


def get_severity_by_err_code(error_code: ErrCode) -> Optional[int]:
    return ERR_CODE_SEVERITY.get(error_code)


@unique
class EvCode(IntEnum):
    ResumeMode = 0  # Slave starting in RESUME mode
    ClearDAQ = 1  # DAQ conf in NvM is cleared
    StoreDAW = 2  # DAQ conf stored in NvM
    StoreCAL = 3  # CAL stored in NvM
    CmdPending = 5  # Slave requests restart timeout
    DAQOverload = 6  # DAQ processor overload
    SessionTerminated = 7  # Session terminated by slave device
    User = 0xFE  # User defined event
    Transport = 0xFF  # Transport layer specific event


EV_CODE_SEVERITY = {
    EvCode.ResumeMode: 0,
    EvCode.ClearDAQ: 0,
    EvCode.StoreDAW: 0,
    EvCode.StoreCAL: 0,
    EvCode.CmdPending: 1,
    EvCode.DAQOverload: 1,
    EvCode.SessionTerminated: 3,
    EvCode.User: 0,
}


def get_severity_by_ev_code(ev_code: EvCode) -> Optional[int]:
    return EV_CODE_SEVERITY.get(ev_code)


class ConnectMode(IntEnum):
    Normal = 0
    User = 1


class ServCodes(IntEnum):
    Reset = 0
    Text = 1


@unique
class StdCmd(IntEnum):
    Connect = 0xFF
    Disconnect = 0xFE
    GetStatus = 0xFD
    Sync = 0xFC

    GetCommModeInfo = 0xFB
    GetId = 0xFA
    SetRequest = 0xF9
    GetSeed = 0xF8
    Unlock = 0xF7
    SetMta = 0xF6
    Upload = 0xF5
    ShortUpload = 0xF4
    BuildChecksum = 0xF3
    TransportLayerCmd = 0xF2
    UserCmd = 0xF1

    Download = 0xF0
    DownloadNext = 0xEF
    DownloadMax = 0xEE
    ShortDownload = 0xED
    ModifyBits = 0xEC

    SetCalPage = 0xEB
    GetCalPage = 0xEA

    GetPagProcessorInfo = 0xE9
    GetSegmentInfo = 0xE8
    GetPageInfo = 0xE7
    SetSegmentMode = 0xE6
    GetSegmentMode = 0xE5
    CopyCalPage = 0xE4

    ClearDaqList = 0xE3
    SetDaqPtr = 0xE2
    WriteDaq = 0xE1
    SetDaqListMode = 0xE0
    GetDaqListMode = 0xDF
    StartStopDaqList = 0xDE
    StartStopSync = 0xDD

    GetDaqClock = 0xDC
    ReadDaq = 0xDB

    GetDaqProcessorInfo = 0xDA
    GetDaqResolutionInfo = 0xD9


@unique
class TransportLayerCmdCAN(IntEnum):
    GetSlaveId = 0xFF
    GetDaqId = 0xFE
    SetDaqId = 0xFD


@unique
class PacketIdFromServer(IntEnum):
    Response = 0xFF
    Error = 0xFE
    Event = 0xFD
    ServiceRequest = 0xFC


def parse_connect_response(data: bytes, endianess: str) -> dict:
    """
    Parse the connect response data.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess. Not used here!
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """
    resource, com_mode_basic, max_cto = data[1:4]
    resource_flags = ResourceFlag(resource)
    com_mode_basic_flags = ComModeBasicFlag(com_mode_basic)
    granularity = Granularity((com_mode_basic >> 1) & 0x3)
    endianess_ = "little"
    if ComModeBasicFlag.MSBFirst in com_mode_basic_flags:
        endianess_ = "big"
    max_dto = int.from_bytes(data[4:6], endianess_)
    protocol_layer_version, transport_layer_version = data[6:8]

    return {"resource_flags": resource_flags,
            "com_mode_basic_flags": com_mode_basic_flags,
            "granularity": granularity,
            "max_cto": max_cto,
            "max_dto": max_dto,
            "protocol_layer_version": protocol_layer_version,
            "transport_layer_version": transport_layer_version
            }


def parse_get_status_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse the get status response data.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """
    return dict(session_status=SessionStatus(data[1]),
                protection_status=ProtectionStatus(data[2]),
                session_config_id=int.from_bytes(data[4:6], endianess))


def parse_get_comm_mode_info(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse the get status response data.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """

    return dict(comm_mode_optional=ComModeOptional(data[2]),
                max_bs=data[4],
                min_st=data[5] / 10000,
                queue_size=data[6],
                xcp_driver_version=float("{0}.{1}".format(data[7] >> 4, data[7] & 0xF)),
                )


def parse_get_daq_list_mode(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse the get daq list mode response data.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """
    return dict(mode=DaqListMode(data[1]), chan=int.from_bytes(data[4:6], endianess), prescaler=data[6], prio=data[7])


def parse_start_stop_daq_list(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse the start stop daq list response data.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """
    return dict(first_pid=data[1])


def parse_get_daq_clock(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a get daq clock response.

    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :return: The contents as a dictionary.
    :rtype dict
    """
    return dict(timestamp=int.from_bytes(data[4:8], endianess))


def parse_read_daq_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a read daq command response.

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(bit_offset=data[1], size=data[2], ext=data[3],
                addr=int.from_bytes(data[4:8], endianess))


def parse_get_daq_processor_info_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a read daq response.

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """

    return dict(daq_property=DaqProperty(data[1]),
                max_daq=int.from_bytes(data[2:4], endianess),
                max_event_chan=int.from_bytes(data[4:6], endianess),
                min_daq=data[6],
                daq_key_byte_opt=DaqKeyByteOptimisation(data[7] & 0xF),
                daq_key_byte_addr_ext=DaqKeyByteAddrExtention((data[7] >> 4) & 0x3),
                daq_key_byte_addr_id_type=DaqKeyByteIdentificaitonType((data[7] >> 6) & 0x3),
                )


def parse_get_daq_resolution_info_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a read daq response.

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(daq_granularity=data[1],
                daq_max_elem_size=data[2],
                stim_granularity=data[3],
                stim_max_elem_size=data[4],
                timestamp_size=(data[5] & 0x7),
                timestamp_fixed=bool((data[5] >> 3) & 0x1),
                timestamp_resolution=(data[5] >> 4) & 0xF,
                timestamp_ticks=int.from_bytes(data[6:8], endianess)
                )


def parse_get_server_id_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a get server id response.

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pattern=data[1:4],
                can_id=int.from_bytes(data[4:8], endianess)
                )


def parse_get_daq_id_response(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a get daq id response.

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(fixed=bool(data[1]),
                can_id=int.from_bytes(data[4:8], endianess)
                )


TRANSPORT_LAYER_CMD_TO_RESPONSE_PARSER_MAPPING = {
    TransportLayerCmdCAN.GetSlaveId: parse_get_server_id_response,
    TransportLayerCmdCAN.GetDaqId: parse_get_daq_id_response,

}

#
# def parse_transport_layer_cmd_response(sub_cmd: TransportLayerCmdCAN,
#                                        data: bytes,
#                                        endianess: str) -> dict:
#     """
#     Parse a transport layer command response packet.
#
#     :param sub_cmd: The sub command in case of transport layer command.
#     :type sub_cmd: TransportLayerCmdCAN
#     :param data: The response data.
#     :type data: bytes
#     :param endianess: The endianess.
#     :type endianess: str
#     :return: A dictionary with the values.
#     :rtype: dict
#     """
#     ret = {}
#     parser = TRANSPORT_LAYER_CMD_TO_RESPONSE_PARSER_MAPPING.get(sub_cmd)
#     if parser is not None and callable(parser):
#         ret.update(parser(data=data,
#                           endianess=endianess))
#     return ret


CMD_TO_RESPONSE_PARSER_MAPPING = {
    StdCmd.Connect: parse_connect_response,
    StdCmd.GetStatus: parse_get_status_response,
    StdCmd.GetCommModeInfo: parse_get_comm_mode_info,
    StdCmd.GetDaqListMode: parse_get_daq_list_mode,
    StdCmd.StartStopDaqList: parse_start_stop_daq_list,
    StdCmd.GetDaqClock: parse_get_daq_clock,
    StdCmd.ReadDaq: parse_read_daq_response,
    StdCmd.GetDaqProcessorInfo: parse_get_daq_processor_info_response,
    StdCmd.GetDaqResolutionInfo: parse_get_daq_resolution_info_response,
}


def parse_response_packet(cmd: StdCmd,
                          data: bytes,
                          endianess: str,
                          sub_cmd: Optional[TransportLayerCmdCAN] = None,
                          ) -> dict:
    """
    Parse a response packet.

    :param cmd: The command which this response is for.
    :type cmd: StdCmd
    :param data: The response data.
    :type data: bytes
    :param endianess: The endianess.
    :type endianess: str
    :param sub_cmd: The sub command in case of transport layer command.
    :type sub_cmd: TransportLayerCmdCAN
    :return: A dictionary with the values.
    :rtype: dict
    """
    ret = {}
    parser = CMD_TO_RESPONSE_PARSER_MAPPING.get(cmd)
    if parser is not None and callable(parser):
        ret.update(parser(data=data,
                          endianess=endianess))
    elif cmd == StdCmd.TransportLayerCmd:
        assert sub_cmd is not None
        parser = TRANSPORT_LAYER_CMD_TO_RESPONSE_PARSER_MAPPING.get(sub_cmd)
        LOGGER.debug(parser)
        if parser is not None and callable(parser):
            ret.update(parser(data=data,
                              endianess=endianess))

    return ret


def parse_error_packet(data: bytes) -> dict:
    """
    Parse an error packet.

    :param data: The packet data.
    :type data: bytes
    :return: A dictionary with the values.
    :rtype: dict
    """
    error_code = ErrCode(data[1])
    ret = dict(error_code=error_code,
               severety=get_severity_by_err_code(error_code=error_code),
               optional=data[2:])
    return ret


def parse_event_packet(data: bytes) -> dict:
    """
    Parse an event packet.

    :param data: The packet data.
    :type data: bytes
    :return: A dictionary with the values.
    :rtype: dict
    """
    ev_code = EvCode(data[1])
    ret = dict(ev_code=ev_code,
               severety=get_severity_by_ev_code(ev_code=ev_code),
               optional=data[2:])
    return ret


def parse_service_packet(data: bytes) -> dict:
    """
    Parse a service packet.

    :param data: The packet data.
    :type data: bytes
    :return: A dictionary with the values.
    :rtype: dict
    """
    ret = dict(serv_code=ServCodes(data[1]),
               optional=data[2:])
    return ret


def parse_packet_from_server(cmd: StdCmd,
                             data: Union[bytes, bytearray],
                             endianess: str,
                             sub_cmd: Optional[TransportLayerCmdCAN] = None,
                             ) -> dict:
    """
    Parse a packet from the server.

    :param cmd: The command which this response is for.
    :type cmd: StdCmd
    :param data: The response data.
    :type data: bytes,bytearray
    :param endianess: The endianess.
    :type endianess: str
    :param sub_cmd: The sub command in case of transport layer command.
    :type sub_cmd: TransportLayerCmdCAN
    :return: A dictionary with the values.
    :rtype: dict
    """
    ret = {"raw": data}
    try:
        packet_id = PacketIdFromServer(data[0])
    except ValueError:
        # likely a daq packet
        pass
    else:
        ret.update({"packet_id": packet_id})
        if packet_id == PacketIdFromServer.Response:
            ret.update(parse_response_packet(cmd=cmd,
                                             data=data,
                                             endianess=endianess,
                                             sub_cmd=sub_cmd))
        elif packet_id == PacketIdFromServer.Error:
            ret.update(parse_error_packet(data=data))
        elif packet_id == PacketIdFromServer.Event:
            ret.update(parse_event_packet(data=data))
        elif packet_id == PacketIdFromServer.ServiceRequest:
            ret.update(parse_service_packet(data=data))
    return ret


def concat_connect_command(mode: ConnectMode = ConnectMode.Normal) -> bytes:
    """
    Concat the connect command message.

    :param mode: The defined Mode
    :type mode: ConnectMode
    :return: The message bytes.
    :type: bytes
    """
    return bytes((StdCmd.Connect, mode))


def parse_connect_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a connect command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little (unused in this parser).
    :type endianess: str
    :return: A dictionary.
    :rtype: dict(pid=StdCmd, mode=ConnectMode)
    """
    return dict(pid=StdCmd(data[0]), mode=ConnectMode(data[1]))


def parse_clear_daq_list_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a clear daq list command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), daq_list=int.from_bytes(data[2:4], endianess))


def parse_set_daq_ptr_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a set daq ptr command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), daq_list=int.from_bytes(data[2:4], endianess), odt_list=data[4], odt_elem=data[5])


def parse_write_daq_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a write daq command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), bit_offset=data[1], size=data[2], ext=data[3],
                addr=int.from_bytes(data[4:8], endianess))


def parse_set_daq_list_mode_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a set daq list mode command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), mode=DaqListMode(data[1]), daq_list=int.from_bytes(data[2:4], endianess),
                chan=int.from_bytes(data[4:6], endianess), prescaler=data[6], prio=data[7])


def parse_get_daq_list_mode_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a get daq list mode command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), daq_list=int.from_bytes(data[2:4], endianess))


def parse_start_stop_daq_list_command(data: bytes, endianess: str = "big") -> dict:
    """
    Parse a start stop daq list command message

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pid=StdCmd(data[0]), mode=DaqStartStopMode(data[1]), daq_list=int.from_bytes(data[2:4], endianess))


def parse_get_server_id(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse get server id command. (CAN only)

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(pattern=data[2:5], invert_echo=bool(data[5]))


def parse_get_daq_id(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a get daq id command. (CAN only)

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(daq_list=int.from_bytes(data[2:4], endianess))


def parse_set_daq_id(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a set daq id command. (CAN only)

    :param data: The data bytes.
    :type data: bytes
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype:
    """
    return dict(daq_list=int.from_bytes(data[2:4], endianess),
                can_id=int.from_bytes(data[2:4], endianess))


TRANSPORT_LAYER_CMD_TO_PARSER_MAPPING = {
    TransportLayerCmdCAN.GetSlaveId: parse_get_server_id,
    TransportLayerCmdCAN.GetDaqId: parse_get_daq_id,
    TransportLayerCmdCAN.SetDaqId: parse_set_daq_id,
}


def parse_transport_layer_command(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a transport layer command.

    :param data: The message data.
    :type data: bytes, bytearray
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype: dict
    """
    sub_cmd = TransportLayerCmdCAN(data[1])
    parser = TRANSPORT_LAYER_CMD_TO_PARSER_MAPPING.get(sub_cmd)
    ret = {"sub_command": sub_cmd,
           }
    if parser is not None and callable(parser):
        ret.update(parser(data=data, endianess=endianess))
    return ret


PACKET_ID_TO_PARSER_MAPPING = {
    StdCmd.Connect: parse_connect_command,
    StdCmd.ClearDaqList: parse_clear_daq_list_command,
    StdCmd.SetDaqPtr: parse_set_daq_ptr_command,
    StdCmd.WriteDaq: parse_write_daq_command,
    StdCmd.SetDaqListMode: parse_set_daq_list_mode_command,
    StdCmd.GetDaqListMode: parse_get_daq_list_mode_command,
    StdCmd.StartStopDaqList: parse_start_stop_daq_list_command,
    StdCmd.TransportLayerCmd: parse_transport_layer_command,
}


def parse_packet_from_client(data: Union[bytes, bytearray], endianess: str) -> dict:
    """
    Parse a message from client to server.

    This can be a Command Transfer Object (CTO) or a Data Transfer Object (DTO).
    The message is a CTO, if the first byte, the packet id is in the range for
    standard commands. Otherwise it must be a DTO. For this direction, a CTO is
    a command (CMD) and a DTO is a data stimulation (STIM).

    :param data: The message data.
    :type data: bytes, bytearray
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: A dictionary.
    :rtype: dict
    """
    try:
        packet_id = StdCmd(data[0])
    except ValueError:
        # is a DTO
        ret = {"packet_id": data[0],
               "packet_type": "DTO",
               "packet_data": data[1:]}
    else:
        # is a CTO
        parser = PACKET_ID_TO_PARSER_MAPPING.get(packet_id)
        ret = {"packet_id": packet_id,
               "packet_type": "CTO"}
        if parser is not None and callable(parser):
            ret.update(parser(data=data, endianess=endianess))
    return ret


def concat_response_packet(command_response_data: Optional[Union[bytes, bytearray]] = None) -> bytearray:
    """
    Concat the response packet

    :param command_response_data: The
    :return:
    """
    ret = bytearray((PacketIdFromServer.Response,))
    if command_response_data is not None:
        ret.extend(command_response_data)
    return ret


def concat_connect_response(resource: ResourceFlag,
                            com_mode_basic: ComModeBasicFlag,
                            max_cto: int,
                            max_dto: int,
                            protocol_layer_version: int = 1,
                            transport_layer_version: int = 1
                            ) -> bytes:
    """
    Concat the connect response message.

    :param resource: The resource flags.
    :type resource: ResourceFlag
    :param com_mode_basic: The com mode basic flags.
    :type com_mode_basic: ComModeBasicFlag
    :param max_cto: Max bytes of command transfer object (CTO)
    :type max_cto: int
    :param max_dto: Max bytes of data transfer object (DTO)
    :type max_dto: int
    :param protocol_layer_version: Protocol Major Version
    :type protocol_layer_version: int
    :param transport_layer_version: Transport Layer Major Version
    :type transport_layer_version: int
    :return: The message as bytes.
    :rtype: bytes
    """
    data = bytearray((resource, com_mode_basic, max_cto))
    endianess_ = "little"
    if ComModeBasicFlag.MSBFirst in com_mode_basic:
        endianess_ = "big"
    data.extend(max_dto.to_bytes(2, endianess_))
    data.extend((protocol_layer_version, transport_layer_version))
    return bytes(data)


def concat_disconnect_command() -> bytes:
    """
    Concat the connect command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.Disconnect,))


def concat_get_status_command() -> bytes:
    """
    Concat the get status command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.GetStatus,))


def concat_status_response(session_status: SessionStatus,
                           resource_protection_status: ProtectionStatus,
                           session_config_id: int,
                           endianess: str = "big") -> bytes:
    """
    Concat the response to get_status() command.

    :param session_status: The session status.
    :type session_status: SessionStatus
    :param resource_protection_status: The resource protection status.
    :type resource_protection_status: ProtectionStatus
    :param session_config_id: The session configuration id.
    :type session_config_id: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: The message as bytes.
    :rtype: bytes
    """
    ret = bytearray((session_status, resource_protection_status, 0))
    ret.extend(session_config_id.to_bytes(2, endianess))
    return ret


def concat_get_comm_mode_info() -> bytes:
    """
    Concat the get comm mode info command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.GetCommModeInfo,))


def concat_comm_mode_info_response(comm_mode_optional: ComModeOptional,
                                   max_bs: int,
                                   min_st: float,
                                   queue_size: int,
                                   xcp_driver_version: float,
                                   ) -> bytes:
    """
    Concat the response to get_com_mode_info() command.

    :param comm_mode_optional: Optional Com Mode Flags
    :type comm_mode_optional: ComModeOptional,
    :param max_bs: Max block size.
    :type max_bs: int
    :param min_st: Minimal separation time between packets in seconds(float). This is converted to 100us steps.
    :type min_st: float
    :param queue_size: Size of rx message queue in Server
    :type queue_size: int
    :param xcp_driver_version: The version number of xcp driver.
                               In Protocol this shows up as High Nibble = Major Version / Low Nibble = Minor Version
    :type xcp_driver_version: float
    :return: The message as bytes.
    :rtype: bytes
    """
    formatted_min_st = min_st * 10000  # 1ms = 10
    xcp_driver_version_major = int(xcp_driver_version)
    xcp_driver_version_minor = int((xcp_driver_version - xcp_driver_version_major) * 10)
    formatted_xcp_driver_version = ((xcp_driver_version_major << 4) | xcp_driver_version_minor)
    return bytes((0, comm_mode_optional, 0, max_bs, formatted_min_st, queue_size,
                  formatted_xcp_driver_version))


def concat_get_daq_list_mode_response(mode: DaqListMode, chan: int, prescaler: int,
                                      prio: int, endianess: str) -> bytearray:
    """
    Concat the response to get_daq_list_mode() command.

    :param mode: The daq list mode.
    :type mode: DaqListMode
    :param chan: The channel.
    :type chan: int
    :param prescaler: The prescaler.
    :type prescaler: int
    :param prio: The prio.
    :type prio: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :return: The message as bytes.
    :rtype: bytes
    """
    ret = bytearray((mode, 0, 0))
    ret.extend(chan.to_bytes(2, endianess))
    ret.append(prescaler)
    ret.append(prio)
    return ret


def concat_read_daq_response(bit_offset: int, size: int, ext: int, addr: int, endianess: str) -> bytearray:
    # TODO: to be refactored duplicate code with write daq
    ret = bytearray((bit_offset, size, ext))
    ret.extend(addr.to_bytes(4, endianess))
    return ret


def concat_sync() -> bytes:
    """
    Concat the sync command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.Sync,))


def concat_error_packet(error_code: ErrCode):
    return bytes((PacketIdFromServer.Error, error_code))


def concat_clear_daq_list(daq_list: int,
                          endianess: str) -> bytearray:
    ret = bytearray((StdCmd.ClearDaqList, 0))
    ret.extend(daq_list.to_bytes(2, endianess))
    return ret


def concat_set_daq_ptr(daq_list: int,
                       odt_list: int,
                       odt_elem: int,
                       endianess: str) -> bytearray:
    ret = bytearray((StdCmd.SetDaqPtr, 0))
    ret.extend(daq_list.to_bytes(2, endianess))
    ret.append(odt_list)
    ret.append(odt_elem)
    return ret


def concat_write_daq(bit_offset: int, size: int, ext: int, addr: int, endianess: str) -> bytearray:
    ret = bytearray((StdCmd.WriteDaq, bit_offset, size, ext))
    ret.extend(addr.to_bytes(4, endianess))
    return ret


def concat_set_daq_list_mode(mode: DaqListMode, daq_list: int, chan: int, prescaler: int,
                             prio: int, endianess: str) -> bytearray:
    ret = bytearray((StdCmd.SetDaqListMode, mode))
    ret.extend(daq_list.to_bytes(2, endianess))
    ret.extend(chan.to_bytes(2, endianess))
    ret.append(prescaler)
    ret.append(prio)
    return ret


def concat_get_daq_list_mode(daq_list: int, endianess: str) -> bytearray:
    ret = bytearray((StdCmd.GetDaqListMode, 0))
    ret.extend(daq_list.to_bytes(2, endianess))
    return ret


def concat_start_stop_daq_list(mode: DaqStartStopMode, daq_list: int, endianess: str) -> bytearray:
    ret = bytearray((StdCmd.StartStopDaqList, mode))
    ret.extend(daq_list.to_bytes(2, endianess))
    return ret


def concat_start_stop_daq_list_response(first_pid: int) -> bytes:
    return bytes((first_pid,))


def concat_start_stop_daq_sync(mode: DaqStartStopMode) -> bytes:
    """
    Concat the start stop daq sync command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.StartStopSync, mode))


def concat_get_daq_clock() -> bytes:
    """
    Concat the get daq clock command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.GetDaqClock,))


def concat_get_daq_clock_response(timestamp: int, endianess: str) -> bytearray:
    ret = bytearray(3)
    ret.extend(timestamp.to_bytes(4, endianess))
    return ret


def concat_read_daq() -> bytes:
    """
    Concat the read daq command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.ReadDaq,))


def concat_get_daq_processor_info() -> bytes:
    """
    Concat the get daq processor info command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.GetDaqProcessorInfo,))


def concat_get_daq_processor_info_response(daq_property: DaqProperty,
                                           max_daq: int,
                                           max_event_chan: int,
                                           min_daq: int,
                                           daq_key_byte_addr_ext: DaqKeyByteAddrExtention,
                                           daq_key_byte_id_type: DaqKeyByteIdentificaitonType,
                                           daq_key_byte_opt: DaqKeyByteOptimisation,
                                           endianess: str) -> bytearray:
    daq_key_byte = daq_key_byte_opt | (daq_key_byte_addr_ext << 4) | (daq_key_byte_id_type << 6)
    ret = bytearray((daq_property,))
    ret.extend(max_daq.to_bytes(2, endianess))
    ret.extend(max_event_chan.to_bytes(2, endianess))
    ret.append(min_daq)
    ret.append(daq_key_byte)
    return ret


def concat_get_daq_resolution_info() -> bytes:
    """
    Concat the get daq resolution command.

    :return: The message as bytes.
    :rtype: bytes
    """
    return bytes((StdCmd.GetDaqResolutionInfo,))


def concat_get_daq_resolution_info_response(daq_granularity: int,
                                            daq_max_elem_size: int,
                                            stim_granularity: int,
                                            stim_max_elem_size: int,
                                            timestamp_resolution: int,  # 1ns times 10 to the power of this number
                                            timestamp_size: int,
                                            timestamp_fixed: bool,
                                            timestamp_ticks: int,
                                            endianess: str) -> bytearray:
    ret = bytearray((daq_granularity, daq_max_elem_size, stim_granularity, stim_max_elem_size))
    timestamp_mode = (timestamp_size & 0x7) | (timestamp_fixed << 3) | (timestamp_resolution << 4)
    ret.append(timestamp_mode)
    ret.extend(timestamp_ticks.to_bytes(2, endianess))
    return ret


def concat_get_server_id(invert_echo: bool = False) -> bytearray:
    """
    Concat the get server id (CAN only) transport layer command

    Protocol calls it get slave id.
    :param invert_echo: A flag if the server should answer with inverted 'XCP' pattern
    :type invert_echo: bool
    :return: The message as bytes.
    :rtype: bytes
    """
    ret = bytearray((StdCmd.TransportLayerCmd, TransportLayerCmdCAN.GetSlaveId))
    ret.extend(b"XCP")
    ret.append(invert_echo)
    return ret


def concat_get_server_id_response(can_id: int,
                                  endianess: str,
                                  invert_echo: bool = False,
                                  ) -> bytearray:
    """
    Concat the get server id (CAN only) transport layer response

    Protocol calls it get slave id.
    :param can_id: The can id.
    :type can_id: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :param invert_echo: A flag if the server should answer with
    :type invert_echo: bool
    :return: The message as bytes.
    :rtype: bytes
    """
    if invert_echo:
        ret = bytearray.fromhex("A7 BC AF")
    else:
        ret = bytearray(b"XCP")
    ret.extend(can_id.to_bytes(4, endianess))
    return ret


def concat_get_daq_id(daq_list: int, endianess: str) -> bytearray:
    """
    Concat the get daq id (CAN only) transport layer command

    This requires knowledge of the endianess used, e.g. can only be used after connect.

    :param daq_list: The daq list.
    :type daq_list: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :return:
    """
    ret = bytearray((StdCmd.TransportLayerCmd, TransportLayerCmdCAN.GetDaqId))
    ret.extend(daq_list.to_bytes(2, endianess))
    return ret


def concat_get_daq_id_response(can_id: int,
                               endianess: str,
                               fixed: bool = False,
                               ) -> bytearray:
    """
    Concat the get daq id (CAN only) transport layer response

    :param can_id: The can id.
    :type can_id: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :param fixed: A flag if the daq id can be changed
    :type fixed: bool
    :return: The message as bytes.
    :rtype: bytes
    """
    ret = bytearray(3)
    ret[0] = fixed
    ret.extend(can_id.to_bytes(4, endianess))
    return ret


def concat_set_daq_id(daq_list: int, can_id: int, endianess: str) -> bytearray:
    """
    Concat the set daq id (CAN only) transport layer command

    This requires knowledge of the endianess used, e.g. can only be used after connect.

    :param can_id: The can id.
    :type can_id: int
    :param daq_list: The daq list.
    :type daq_list: int
    :param endianess: The endianess big or little.
    :type endianess: str
    :return:
    """
    ret = bytearray((StdCmd.TransportLayerCmd, TransportLayerCmdCAN.SetDaqId))
    ret.extend(daq_list.to_bytes(2, endianess))
    ret.extend(can_id.to_bytes(4, endianess))
    return ret


def raise_for_error(resp: dict) -> None:
    error_code_to_exception_mapping = {ErrCode.CmdSync: XcpErrorSyncCmd,
                                       ErrCode.OutOfRange: XcpErrorOutOfRange,
                                       }
    packet_id = resp.get("packet_id")
    if packet_id == PacketIdFromServer.Error:
        error_code = resp.get("error_code")
        error_code_class = error_code_to_exception_mapping.get(error_code)
        if error_code_class is not None:
            raise error_code_class
        else:
            raise XcpError("XcpErr: {error_code.name} {optional}".format_map(resp))


class XcpProtocolException(BaseException):
    pass


class XcpTimeout(XcpProtocolException):
    pass


class XcpTrueTimeout(XcpTimeout):
    """
    While Xcp does have a Timeout, this timeout is the true
    timeout after every timeout handling by protocol has happened.
    """
    pass


class XcpEvent(XcpProtocolException):
    pass


class XcpError(XcpProtocolException):
    pass


class XcpErrorSyncCmd(XcpError):
    pass


class XcpErrorOutOfRange(XcpError):
    pass
