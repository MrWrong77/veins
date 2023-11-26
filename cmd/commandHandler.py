
class CommandHandler:
 def __init__(self):
     self.command_id_to_callback = {}

 def register_callback(self, command):
     command_id = command.get_command_id()
     callback = command.get_callback()
     if command_id in self.command_id_to_callback:
         raise ValueError(f"Command ID {command_id} already has a registered callback")
     self.command_id_to_callback[command_id] = callback

 def handle_command(self, command_id, data):
     if command_id not in self.command_id_to_callback:
         raise ValueError(f"Command ID {command_id} does not have a registered callback")
     callback = self.command_id_to_callback[command_id]
     return callback(data)

# 示例用法
def example_callback(command_id):
  print(f"Received command ID: {command_id}")

def Hello():
  print("Hello")

def InitCommandSet():
    handler = CommandHandler()

    return handler