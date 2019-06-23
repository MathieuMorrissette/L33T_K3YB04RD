import errno
import os
import sys
import base64
from io import BytesIO
import keyboard
import win32service, win32con
import websockets
import pyscreenshot
import subprocess
import asyncio

current_desktop_name = "DEFAULT"

def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str

def GetDesktopName(hdesk):
    name = win32service.GetUserObjectInformation(hdesk, win32con.UOI_NAME)
    return name


def SetDesktop(deskname):
    hWinSta0 = win32service.OpenWindowStation("WinSta0", False, win32con.MAXIMUM_ALLOWED)
    hWinSta0.SetProcessWindowStation()
    hdesk = win32service.OpenDesktop(deskname, 0, False, win32con.MAXIMUM_ALLOWED)
    hdesk.SetThreadDesktop()

def SetInputDesktop():
    global current_desktop_name

    hWinSta0 = win32service.OpenWindowStation("WinSta0", True, win32con.MAXIMUM_ALLOWED)
    hWinSta0.SetProcessWindowStation()
    hdesk = win32service.OpenInputDesktop(0, True, win32con.MAXIMUM_ALLOWED)
    
    hdesk_name = GetDesktopName(hdesk).upper()

    print("current desktop : " + hdesk_name)
    if(current_desktop_name == hdesk_name):
        return

    hdesk.SetThreadDesktop()
    
    print("changed desktop to : " + hdesk_name)
    current_desktop_name = hdesk_name


async def main():
    async with websockets.connect('ws://192.168.4.148:8766') as websocket:
        await websocket.send("CONNECT_RECEIVER")

        while(True):
            print("waiting for server...")
            server = await websocket.recv()
            
            SetInputDesktop() # make sure we use the current desktop

            if(server.startswith("KEY|")):
                keyboard.write(server[4:])
        
            if(server.startswith("CMD|")):
                output = subprocess.getoutput(server[4:])
                await websocket.send("RECEIVER_OUTPUT|" + output)

            if(server.startswith("SCREEN|")):
                im = pyscreenshot.grab()
                im.show()
                await websocket.send("RECEIVER_OUTPUT|" + im_2_b64(im).decode("utf-8"))



asyncio.get_event_loop().run_until_complete(main())