import sys
sys.path.append("/home/veins/src/sumo/tools")
sys.path.append("/home/veins/src/veins/cmd/python_out")
import traci

from const import *

from vehicle_pb2 import PV_GetVehicle
from vehicle_pb2 import VP_GetVehicle
from vehicle_pb2 import PV_GetNeigbours
from vehicle_pb2 import VP_GetNeigbours

from net import Send
from net import Recv

from command import *
from commandHandler import InitCommandSet
commandHandler = InitCommandSet()


def SimStart(socket):
    while True  :
        cmd,data = Recv(socket)
        if cmd == CMD_NEW_STEP:
            END = SimStep(socket,commandHandler)
            if END == False:
                print("Simulation End")
                return

def SimStep(socket,hander):
    print(traci.vehicle.getIDList())

    Send(socket, CmdGetVehicle("flow0.0"))
    cmd,data = Recv(socket)
    commandHandler.handle_command(cmd,data)

    Send(socket, CmdGetNeibours("flow0.0"))
    cmd,data = Recv(socket)
    commandHandler.handle_command(cmd,data)

    # Send(socket, CmdGetSimTime)
    # cmd,data = Recv(socket)
    # commandHandler.handle_command(cmd,data)

    StepFinish(socket)
    return True

def StepFinish(socket):
    print("[python] step finish")
    Send(socket, CmdSimNext())

class CmdNewStep:
    def get_command_id(self):
        return CMD_NEW_STEP
    
    def get_data_send(self):
        return b''

    def get_callback(self):
        def cmdHandler(data):
            print("New sim step")
            return True
        return cmdHandler
 
class CmdGetVehicle:
    def __init__(self,v):
        self.vehicle=v

    def get_command_id(self):
        return CMD_GET_VEHICLE
    
    def get_data_send(self):
        req = PV_GetVehicle()
        # req.id = "flow0.0"
        req.id = self.vehicle
        data = req.SerializeToString()
        return data
    
    def get_callback(self):
        def cmdHandler(data):
            v = VP_GetVehicle()
            v.ParseFromString(data)
            print("get vehicle data success:",v)
            return True
        return cmdHandler
 
class CmdGetNeibours:
    def __init__(self,v):
        self.vehicle=v

    def get_command_id(self):
        return CMD_GET_NEIGBOURS
    
    def get_data_send(self):
        req = PV_GetNeigbours()
        req.id = self.vehicle
        data = req.SerializeToString()
        return data
    
    def get_callback(self):
        def cmdHandler(data):
            v = VP_GetNeigbours()
            v.ParseFromString(data)
            print("get neigbour data success:",v)
            return True
        return cmdHandler
 
class CmdGetSimTime:
    def get_command_id(self):
        return CMD_GET_SIM_TIME
    
    def get_data_send(self):
        return b''
    
    def get_callback(self):
        def cmdHandler(data):
            print("get simtime data success")
            return True
        return cmdHandler
    
class CmdSimEnd:
    def get_command_id(self):
        return CMD_SIM_END
    
    def get_data_send(self):
        return b''
    
    def get_callback(self):
        def cmdHandler(data):
            print("sim end")
            return False
        return cmdHandler

class CmdSimNext:
    def get_command_id(self):
        return CMD_SIM_NEXT
    
    def get_data_send(self):
        return b''
    
    def get_callback(self):
        def cmdHandler(data):
            print("no need callback")
            return False
        return cmdHandler

class CmdInvalid:
    def get_command_id(self):
        return CMD_INVALID
    
    def get_data_send(self):
        return b''
    
    def get_callback(self):
        def cmdHandler(data):
            print("invalid cmd:"+data.decode("utf-8"))
            return False
        return cmdHandler
    
commandHandler.register_callback(CmdNewStep())
commandHandler.register_callback(CmdGetVehicle(""))
commandHandler.register_callback(CmdGetNeibours(""))
commandHandler.register_callback(CmdGetSimTime())
commandHandler.register_callback(CmdSimEnd())
commandHandler.register_callback(CmdInvalid())