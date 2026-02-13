import struct
from enum import IntEnum

MAX_PAYLOAD_SIZE = 255

# -------------------------
# Enums (uint32_t)
# -------------------------

class MsgType(IntEnum):
    COMMAND = 0
    CONTROL = 1
    TELEMETRY = 2


class TelemetryCommand(IntEnum):
    SYNC = 0
    ACK = 1
    NACK = 2
    SYNC_ACK = 3
    OTHER = 4


# -------------------------
# teleCommand struct
# uint32_t commandId;
# uint32_t defaultCommandType;
# uint32_t command;
# -------------------------

class TeleCommand:
    FORMAT = "<III"  # little-endian, 3 unsigned int (uint32_t)
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, commandId, defaultCommandType, command):
        self.commandId = commandId
        self.defaultCommandType = defaultCommandType
        self.command = command

    def pack(self):
        return struct.pack(self.FORMAT,
                           self.commandId,
                           self.defaultCommandType,
                           self.command)

    @classmethod
    def unpack(cls, data):
        fields = struct.unpack(cls.FORMAT, data[:cls.SIZE])
        return cls(*fields)


# -------------------------
# teleSegment struct
# uint32_t msgType;
# uint8_t data[255];
# -------------------------

class TeleSegment:
    FORMAT = "<I255s"  # uint32 + 255 bytes
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, msgType, data):
        self.msgType = msgType
        self.data = data.ljust(MAX_PAYLOAD_SIZE, b'\x00')[:MAX_PAYLOAD_SIZE]

    def pack(self):
        return struct.pack(self.FORMAT,
                           self.msgType,
                           self.data)

    @classmethod
    def unpack(cls, data):
        msgType, payload = struct.unpack(cls.FORMAT, data[:cls.SIZE])
        return cls(msgType, payload)


# -------------------------
# Callback type equivalent
# typedef void (*callBack)(uint8_t *);
# -------------------------

# In Python this is simply:
# def callback(data: bytes): ...
