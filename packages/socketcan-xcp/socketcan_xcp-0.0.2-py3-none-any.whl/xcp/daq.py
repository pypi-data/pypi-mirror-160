""" module:: xcp.daq
    :platform: Any
    :synopsis: Data Aquisition (DAQ) objects, e.g. the DAQ list.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from typing import Optional

from xcp.protocol import DaqListMode, DaqProperty, DaqKeyByteAddrExtention, DaqKeyByteIdentificaitonType, \
    DaqKeyByteOptimisation


class OdtElem:
    """
    ODT Element, called ODT Entry by spec

    Using an object is more convenient than a dictionary.
    """

    def __init__(self,
                 addr: int = 0,
                 size: int = 0,
                 ext: int = 0,
                 bit_offset: int = 0
                 ):
        """
        Constructor

        :param addr: Address
        :type addr: int
        :param size: Size
        :type size: int
        :param ext: Address Extention
        :type ext: int
        :param bit_offset: Bit Offset
        :type bit_offset: int
        """
        self.addr = addr
        self.size = size
        self.ext = ext
        self.bit_offset = bit_offset


class OdtList:
    """
    ODT list - A list of ODT elements.

    It provides the interface to read and write elements directly.
    """

    def __init__(self, odt_list_length: int):
        self.elems = []
        for idx in range(odt_list_length):
            self.elems.append(OdtElem())
        self.current_elem = self.elems[0]
        self._idx = 0

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value) -> None:
        """
        The index setter.

        :param value:
        :return: Nothing
        :raises: IndexError
        """
        self.current_elem = self.elems[value]
        self._idx = value

    @property
    def current_elem(self):
        return self._current_elem

    @current_elem.setter
    def current_elem(self, value):
        self._current_elem = value

    def read(self) -> OdtElem:
        """
        Indexed read operation

        :return: The Element.
        """
        ret = self._current_elem
        if (self.idx < len(self) - 1):
            self.idx += 1
        return ret

    def write(self, value: OdtElem) -> None:
        """
        Indexed write operation

        :param value: The value
        :return: Nothing.
        """
        self.elems[self.idx] = value
        if (self.idx < len(self) - 1):
            self.idx += 1

    def __len__(self):
        return len(self.elems)


class DaqList:
    """
    DAQ list -  A list of ODT lists.

    It also has properties for the transmission parameters of the list.

    It provides an interface to set the daq pointer to the specific ODT element
    and to read/write that element from this level.
    """

    def __init__(self,
                 daq_list_length: int,
                 odt_list_length: int = 10,
                 mode: Optional[DaqListMode] = None,
                 prescaler: Optional[int] = None,
                 prio: Optional[int] = None,
                 chan: Optional[int] = None,
                 first_pid: Optional[int] = None,
                 can_id: Optional[int] = None):

        self.elems = []
        for idx in range(daq_list_length):
            self.elems.append(OdtList(odt_list_length=odt_list_length))
        self.current_elem = self.elems[0]
        self._idx = 0

        self.mode = DaqListMode(0)
        if mode is not None:
            self.mode = mode

        self.prescaler = 1
        if prescaler is not None:
            self.prescaler = prescaler

        self.prio = 0xFF
        if prio is not None:
            self.prio = prio

        self.chan = 0
        if chan is not None:
            self.chan = chan

        self.first_pid = 0
        if first_pid is not None:
            self.first_pid = first_pid

        self.can_id = 0
        if can_id is not None:
            self.can_id = can_id

    def set_ptr(self, odt_list_idx, odt_elem_idx):
        self.idx = odt_list_idx
        self._current_elem.idx = odt_elem_idx

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value) -> None:
        """
        The index setter.

        :param value:
        :return: Nothing
        :raises: IndexError
        """
        self.current_elem = self.elems[value]
        self._idx = value

    @property
    def current_elem(self):
        return self._current_elem

    @current_elem.setter
    def current_elem(self, value):
        self._current_elem = value

    def read(self) -> OdtElem:
        """
        Read ODT element from the selected odt list.

        :return: The ODT element.
        :rtype: OdtElem
        """
        return self.current_elem.read()

    def write(self, value: OdtElem) -> None:
        """
        Write ODT element to the selected odt list.

        :param value: The ODT element.
        :type value: OdtElem
        :return: Nothing
        """
        return self.current_elem.write(value)

    def __len__(self):
        return len(self.elems)


class DaqTable:
    """
    DAQ Table -  A list of Daq lists.

    The top level class for interacting with DAQ
    It is essentially another level of indexed list on top of DaqList
    """

    def __init__(self,
                 daq_table_length: int,
                 daq_list_length: int,
                 odt_list_length: int):
        self.elems = []
        for idx in range(daq_table_length):
            self.elems.append(DaqList(daq_list_length=daq_list_length,
                                      odt_list_length=odt_list_length,
                                      ))
        self.current_elem = self.elems[0]
        self._idx = 0

    def set_ptr(self, daq_list_idx, odt_list_idx, odt_elem_idx):
        self.idx = daq_list_idx
        self.current_elem.set_ptr(odt_list_idx=odt_list_idx,
                                  odt_elem_idx=odt_elem_idx)

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value) -> None:
        """
        The index setter.

        :param value:
        :return: Nothing
        :raises: IndexError
        """
        self.current_elem = self.elems[value]
        self._idx = value

    @property
    def current_elem(self):
        return self._current_elem

    @current_elem.setter
    def current_elem(self, value):
        self._current_elem = value

    def read(self) -> OdtElem:
        """
        Read ODT element from the selected odt list.

        :return: The ODT element.
        :rtype: OdtElem
        """
        return self.current_elem.read()

    def write(self, value: OdtElem) -> None:
        """
        Write ODT element to the selected odt list.

        :param value: The ODT element.
        :type value: OdtElem
        :return: Nothing
        """
        return self.current_elem.write(value)

    def __len__(self):
        return len(self.elems)


class DaqProcessor:

    def __init__(self, daq_table: DaqTable):
        self._daq_table = daq_table
        self._daq_properties = DaqProperty(0)
        self._max_daq = 10
        self._max_event_chan = 1
        self._min_daq = 0
        self._daq_key_byte_addr_ext = DaqKeyByteAddrExtention(0)
        self._daq_key_byte_id_type = DaqKeyByteIdentificaitonType(0)
        self._daq_key_byte_opt = DaqKeyByteOptimisation(0)
        self._daq_granularity = 4
        self._daq_max_elem_size = 4
        self._stim_granularity = 4
        self._stim_max_elem_size = 4
        self._timestamp_resolution = 9
        self._timestamp_size = 4
        self._timestamp_fixed = False
        self._timestamp_ticks = 0x42
        self._daq_can_id = 0x12345678

    @property
    def daq_table(self):
        return self._daq_table

    @property
    def daq_properties(self):
        return self._daq_properties

    @property
    def daq_key_byte_addr_ext(self):
        return self._daq_key_byte_addr_ext

    @property
    def daq_key_byte_id_type(self):
        return self._daq_key_byte_id_type

    @property
    def daq_key_byte_opt(self):
        return self._daq_key_byte_opt

    @property
    def max_daq(self):
        return self._max_daq

    @property
    def min_daq(self):
        return self._min_daq

    @property
    def max_event_chan(self):
        return self._max_event_chan

    @property
    def daq_granularity(self):
        return self._daq_granularity

    @property
    def daq_max_elem_size(self):
        return self._daq_max_elem_size

    @property
    def stim_granularity(self):
        return self._stim_granularity

    @property
    def stim_max_elem_size(self):
        return self._stim_max_elem_size

    @property
    def timestamp_resolution(self):
        return self._timestamp_resolution

    @property
    def timestamp_size(self):
        return self._timestamp_size

    @property
    def timestamp_fixed(self):
        return self._timestamp_fixed

    @property
    def timestamp_ticks(self):
        return self._timestamp_ticks

    def get_can_id_for_daq_list(self, daq_list: int):
        return self.daq_table.elems[daq_list].can_id

    def set_can_id_for_daq_list(self, daq_list: int, can_id: int):
        self._daq_table.elems[daq_list].can_id = can_id
