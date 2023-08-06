import warnings

from .consts import ETH_ANSWER_NOQUEUE

from .utils import checksum


class SerialError(Exception):
    """Exception raised when there's a problem with serial."""


class SerialErrCheckSum(SerialError):
    """Exception raised when there'a problem with checksum."""


class SerialErrPckgLen(SerialError):
    """Exception raised when there'a problem with package length."""


class SerialForbidden(SerialError):
    """Exception raised when a given operation is not permitted by the UDC"""


class SerialInvalidCmd(SerialError):
    """Exception raised when the supplied command is invalid"""


SERIAL_ERROR = [
    "Ok",
    "Power supply in local mode",
    "Power supply in PC host mode",
    "Power supply interlocked",
    "UDC stuck",
    "DSP timeout",
    "DSP busy",
    "Resource is busy",
    "Invalid command",
]


def validate(func):
    def wrapper(*args, **kwargs):
        reply = func(*args, **kwargs)
        if len(reply) == 1 and reply[0] == ETH_ANSWER_NOQUEUE:
            warnings.warn(
                "Server declared that no data was available in the read queue. If this is a write-only operation, use _transfer_write",
                RuntimeWarning,
            )
            return b""

        reply = reply[1:] if len(reply) - 1 == args[2] else reply

        if reply[1] == 0x53:
            if reply[-2] == 4:
                raise SerialForbidden
            if reply[-2] == 8:
                raise SerialInvalidCmd

        if len(reply) != args[2]:
            raise SerialErrPckgLen(
                "Expected {} bytes, received {} bytes".format(args[2], len(reply))
            )

        if reply != checksum(reply[:-1]):
            raise SerialErrCheckSum

        return reply

    return wrapper
