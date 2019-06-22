# how to install
# python receiver.py install
# python receiver.py start

import asyncio
import websockets
import keyboard

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import win32api
import time
import win32con

debug = False

current_desktop_name = "DEFAULT"

def SetDesktop(deskname):
    hWinSta0 = win32service.OpenWindowStation("WinSta0", False, win32con.MAXIMUM_ALLOWED)
    hWinSta0.SetProcessWindowStation()
    hdesk = win32service.OpenDesktop(deskname, 0, False, win32con.MAXIMUM_ALLOWED)
    hdesk.SetThreadDesktop()

def SetInputDesktop():
    global current_desktop_name

    hWinSta0 = win32service.OpenWindowStation("WinSta0", False, win32con.MAXIMUM_ALLOWED)
    hWinSta0.SetProcessWindowStation()
    hdesk = win32service.OpenInputDesktop(0, False, win32con.MAXIMUM_ALLOWED)
    hdesk_name = GetDesktopName(hdesk).upper()

    print("current desktop : " + hdesk_name)
    if(current_desktop_name == hdesk_name):
        return

    hdesk.SetThreadDesktop()
    print("changed desktop to : " + hdesk_name)
    current_desktop_name = hdesk_name

def GetDesktopName(hdesk):
    name = win32service.GetUserObjectInformation(hdesk, win32con.UOI_NAME)
    return name

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "SomeService1"
    _svc_display_name_ = "SomeService1"

    def __init__(self,args):
        if not debug:
            win32serviceutil.ServiceFramework.__init__(self,args)
            self.hWaitStop = win32event.CreateEvent(None,0,0,None)
            socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    async def main2(self):
        print("connecting...")

        # SetDesktop("winlogon")
        # SetDesktop("default")

        async with websockets.connect('ws://192.168.4.148:8766') as websocket:
            await websocket.send("CONNECT_RECEIVER")

            while(True):
                print("waiting for server...")
                server = await websocket.recv()

                SetInputDesktop() # make sure we use the current desktop

                keyboard.write(server)
                print("writing : " + server)

    def main(self):
        asyncio.get_event_loop().run_until_complete(self.main2())
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__': 
    if debug:
        lol = AppServerSvc(None)
        lol.main()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)

# reference 
# # https://stackoverflow.com/questions/16010659/how-to-switch-a-process-between-default-desktop-and-winlogon-desktop
