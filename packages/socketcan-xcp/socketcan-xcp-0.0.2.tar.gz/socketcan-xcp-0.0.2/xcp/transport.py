""" module:: xcp.transport
    :platform: Any
    :synopsis: XCP Transport Layer
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3

    Note: XCP distinguishes between protocol and transport. This implementation is meant for CAN only but should
          be easy to adapt for another transport layer.
"""

from abc import ABC, abstractmethod

from socketcan import CanRawSocket, CanFilter, CanFrame, CanFdFrame

XCP_TRANSPORT_LAYER_VERSION = 0x10


class XcpTransport(ABC):

    @property
    def transport_layer_version(self):
        return XCP_TRANSPORT_LAYER_VERSION

    @abstractmethod
    def send(self, data: bytes) -> None:
        """
        Send a Xcp Message on a transport layer

        :param data: The message.
        :type data: bytes
        :return: Nothing
        :rtype: None
        """

    @abstractmethod
    def recv(self) -> bytes:
        """
        Receive a Xcp Message on a transport layer
        :return: The message.
        :rtype: bytes
        """


class XcpOnCan(XcpTransport):

    def __init__(self,
                 interface: str,
                 tx_can_id: int,
                 rx_can_id: int,
                 use_can_fd: bool = True,
                 ):
        """
        Constructor

        Constructs a XcpOnCan Object.

        :param interface: The CAN Interface name.
        :type interface: str
        :param tx_can_id: A CAN ID (only one for now)
        :type tx_can_id: int
        :param rx_can_id: A CAN ID (only one for now)
        :type rx_can_id: int
        """
        super().__init__()
        self._use_can_fd = use_can_fd
        self.tx_can_id = tx_can_id
        self.rx_can_id = rx_can_id

        can_mask = 0x1FFFFFFF
        if self.rx_can_id < 0x800:
            can_mask = 0x7FF
        filters = [CanFilter(can_id=self.rx_can_id, can_mask=can_mask), ]
        self.socket = CanRawSocket(interface=interface,
                                   can_filters=filters)

    def send(self, data: bytes) -> int:
        """
        Send a Xcp Message on a transport layer

        :param data: The message.
        :type data: bytes
        :return: The number of bytes written.
        :rtype: int
        """
        if self._use_can_fd or (64 >= len(data) > 8):
            frame = CanFdFrame(can_id=self.tx_can_id,
                               data=data)
        else:
            frame = CanFrame(can_id=self.tx_can_id,
                             data=data)
        return self.socket.send(frame=frame)

    def recv(self) -> bytes:
        """
        Receive a Xcp Message on a transport layer
        :return: The message.
        :rtype: bytes
        """
        frame = self.socket.recv()
        return frame.data

    def __del__(self):
        if hasattr(self, "socket"):
            del self.socket


class TransportError(BaseException):
    pass


class TransportTimeout(TransportError):
    pass
