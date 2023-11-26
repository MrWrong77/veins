import socket
import os
import sys

sys.path.append("/home/veins/src/veins/cmd/python_out")
sys.path.append("/home/veins/src/sumo/tools")
import traci
import time

from const import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("set SUMO_HOME")


from sim import SimStart

# 创建一个 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 定义veins地址和端口
host = '127.0.0.1'
port = 8888

# 连接veins服务器
s.connect((host, port))

# guarantee python-client be the second client connected to sumo-traci-server
time.sleep(1)
traci.init(9999, host=host)
# traci.connect(9999,label="default")
# traci.setOrder(1)
# traci.simulationStep(1)

# start sim
SimStart(s)
traci.close()
s.close()
