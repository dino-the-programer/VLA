import asyncio
import dtype
import socket
import threading
import queue
from enum import IntEnum
import typing
import time

commandQueue = queue.Queue()
telemetryQueue = queue.Queue()
controlQueue = queue.Queue()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Client:
    class CLIENTSTATE(IntEnum):
        NEW = 0
        CONNECTED = 1
        DISCONNECTED = 2
    
    class COMMANDSTATE(IntEnum):
        READY = 0
        WAITING = 1

    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.clientstate = self.CLIENTSTATE.NEW
        self.commandstate = self.COMMANDSTATE.WAITING
    
    @property
    def addr(self):
        return (self.ip,self.port)
    
    @property
    def connected(self):
        return self.clientstate == self.CLIENTSTATE.CONNECTED

    @connected.setter
    def connected(self,val):
        if val:
            self.clientstate = self.CLIENTSTATE.CONNECTED
            self.commandstate = self.COMMANDSTATE.READY
        else:
            self.clientstate = self.CLIENTSTATE.NEW
    
    @property
    def ready(self):
        return self.commandstate == self.COMMANDSTATE.READY
    
    @ready.setter
    def ready(self,val):
        if val:
            self.commandstate = self.COMMANDSTATE.READY
        else:
            self.commandstate = self.COMMANDSTATE.WAITING

clientPool:dict[str,Client] = {}

def handleCommands():
    while True:
        cmd = commandQueue.get()
        command = dtype.TeleCommand.unpack(cmd[0])
        match (command.defaultCommandType):
            case dtype.TelemetryCommand.SYNC:
                tempClient = Client(cmd[1][0],9999)
                clientPool.update({cmd[1][0]:tempClient})
                syncCommand = dtype.TeleCommand(0,dtype.TelemetryCommand.SYNC_ACK,0)
                message = dtype.TeleSegment(dtype.MsgType.COMMAND,syncCommand.pack())
                client_socket.sendto(message.pack(), tempClient.addr)
            
            case dtype.TelemetryCommand.ACK:
                client = clientPool.get(cmd[1][0])
                if not client:
                    continue
                client.connected = True
                print(f"{client.addr} connected")

def handleTelemetry():
    while True:
        msgbyte = telemetryQueue.get()[0]
        print(msgbyte[:17])

def sendControl():
    time.sleep(10)
    val = 0
    l = 0
    u = 255
    inc = 1
    while True:
        if val <= l:
            inc = 1
        elif val >= u:
            inc = -1
        val+=inc
        # print(val)
        message = dtype.TeleSegment(dtype.MsgType.CONTROL,chr(val).encode())
        client_socket.sendto(message.pack(), list(clientPool.values())[0].addr)
        time.sleep(0.01)

class EchoServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        print("new con")
        self.transport = transport

    def datagram_received(self, data, addr):
        decoded = dtype.TeleSegment.unpack(data)
        match (decoded.msgType):
            case dtype.MsgType.COMMAND:
                commandQueue.put((decoded.data,addr))
                # print(decoded.data)
            
            case dtype.MsgType.TELEMETRY:
                telemetryQueue.put((decoded.data,addr))

    def connection_lost(self, exc):
        print("Connection lost")

async def main():
    loop = asyncio.get_running_loop()
    commandhandler = threading.Thread(target=handleCommands)
    ping = threading.Thread(target=sendControl)
    telemetry = threading.Thread(target=handleTelemetry)
    commandhandler.start()
    ping.start()
    telemetry.start()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('0.0.0.0', 9999))
    try:
        await asyncio.Event().wait() # Keep the server running indefinitely
    finally:
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())
