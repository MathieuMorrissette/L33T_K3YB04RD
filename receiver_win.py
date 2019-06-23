# how to install
# python receiver.py install
# python receiver.py start

import asyncio
import websockets
import keyboard
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import win32api
import time
import win32con
import win32ts
import win32security
import win32process
import subprocess
import pyscreenshot
import base64
import win32profile
import win32pipe
import win32file
import psutil

from io import BytesIO

def get_pid(proc_name):
    for proc in psutil.process_iter():
        if proc.name() == proc_name:
            return proc.pid
    return 0

def getusertoken():
    # to escape session 0 isolation when running as a service
    print("Getting winlogon pid...")
    winlogon_pid = get_pid('winlogon.exe')
    print("PID:" + str(winlogon_pid))

    p = win32api.OpenProcess(1024, 0, get_pid('winlogon.exe'))
    t = win32security.OpenProcessToken(p, win32security.TOKEN_DUPLICATE)
    
    primaryToken = win32security.DuplicateTokenEx(t,
                                win32security.SecurityImpersonation,
                                win32security.TOKEN_ALL_ACCESS,
                                win32security.TokenPrimary)
    return primaryToken

def StartAgent():
    #pythonw (run in background)
    my_app_path = r'C:\Users\Mathieu\AppData\Local\Programs\Python\Python37-32\pythonw.exe'
    #my_app_path = r'C:\Windows\System32\cmd.exe'
    startup = win32process.STARTUPINFO()
    priority = win32con.NORMAL_PRIORITY_CLASS
    console_user_token = getusertoken()

    environment = win32profile.CreateEnvironmentBlock(console_user_token, False)
    handle, thread_id ,pid, tid = win32process.CreateProcessAsUser(console_user_token, my_app_path, r' C:\git\L33T_K3YB04RD\injector.py', None, None, True, priority, environment, None, startup)

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "SomeService3"
    _svc_display_name_ = "SomeService3"

    def __init__(self,args):
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

    def main(self):
        StartAgent()

        time.sleep(20)

if __name__ == '__main__': 
    win32serviceutil.HandleCommandLine(AppServerSvc)
    #StartAgent()

# reference 
# # https://stackoverflow.com/questions/16010659/how-to-switch-a-process-between-default-desktop-and-winlogon-desktop
#1. WTSGetActiveConsoleSessionId(); 
#2. WTSQueryUserToken() for winlogon.exe winlogon pid
#3. DuplicateTokenEx ()
#4. AdjustTokenPrivileges ()
#5. CreateProcessAsUser () lpDesktop to Winsta0\Winlogon 
# https://stackoverflow.com/questions/2426594/starting-a-uac-elevated-process-from-a-non-interactive-service-win32-net-power
