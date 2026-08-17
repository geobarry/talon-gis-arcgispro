from talon import actions, Module
import socket
import json

def send_to_arcpy(cmd: dict):
    HOST = "127.0.0.1"
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(cmd).encode("utf-8"))
        data = s.recv(4096)
        return json.loads(data.decode("utf-8"))

mod=Module()

@mod.action_class
class UserArcpyActions:
    def set_outline_color(hex_color: str):
        """Modifies the currently selected layers outline color"""
        result = send_to_arcpy({
            "action": "set_outline_color",
            "color": hex_color
        })
        print("ArcPy result:", result)

