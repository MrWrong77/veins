import struct

def Send(socket, command):
    cmd=command.get_command_id()
    data = command.get_data_send()
    send_package_len = 0x5+len(data)  # 数据包长度, 4+1
    packed_data = struct.pack('>I', send_package_len)
    packed_data += struct.pack('>B', cmd)
    packed_data += data
    socket.send(packed_data)


def Recv(socket):
    PACKAGE_LENGTH_IN_HEAD = 4
    data = b''
    length = 0
    while True:
        tmp = socket.recv(1024)
        if not tmp:
            return 0, data[:0]
        data += tmp
        if len(data) >= PACKAGE_LENGTH_IN_HEAD:
            length = struct.unpack('>I', data[:PACKAGE_LENGTH_IN_HEAD])[0]
            if len(data) >= length:
                break
    # package-len[4] + cmd[1] +  data
    cmd = struct.unpack(
        '>B', data[PACKAGE_LENGTH_IN_HEAD:PACKAGE_LENGTH_IN_HEAD+1])[0]  # CMD
    return cmd, data[PACKAGE_LENGTH_IN_HEAD+1:]