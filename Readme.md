# Windows python Backdoor exe
Server and client to explore backdoor files
Exemple with local and virtual machines

#### Server
- Execute on your computer with python
- Server ip need to be the same on Client code

#### Client
Locate on a Windows computer. Execute and store on registry to load on windows start.
- Server ip need to be the same on Server code

#### Commands
- cd               -> list commands
- upload '$file'   -> Upload files
- download '$file' -> Download files
- screenshot       -> Screenshots
- get '$url'       -> Download files from internet on client
- start            -> Exec Commands
- check            -> Check user privileges

#### Requirements
- pip install requests
- pip install mss
- pip install pyinstaller
- pip install --upgrade setuptools

#### Execute python conversion to .exe
- $ cd client
- $ pyinstaller client.py --onefile --noconsole -i "../resources/microsoft.ico" --specpath ../executable/spec --distpath ../executable/dist --workpath ../executable/build 
- ONLY need dist folder content
- Share your exe file with infected computer
- $ python -m http.server
- Check your browser http://192.168.xxx.xxx:8000 

#### Execute on infected computer
- Execute client.exe on infected computer
- Enjoy your tests

#### Utilities
- https://readme.so/
- https://www.iconfinder.com/search?q=windows
- https://www.freeconvert.com/png-to-ico
- https://www.virtualbox.org/
- ipconfig
- netstat