# bot to manage palworld on discord
 ## English [日本語](./ja-README.md) ##


 ### This program is currently in beta, so there may be some features that do not work. Also, since I do not speak English, I am using machine translation, so there will be a lot of strange English.
 ### Debugging was done on Ubuntu

![banner](./image/banner.png)
 ### ToDolist (Hopefully one day it will end)

- [x] In-game display of join and leave
- [x] Game join and leave display on discord
- [ ] automatic restart
- [x] Only the bot administrator, server administrator, or role holder can execute commands.
- [x] Server startup and shutdown indication
- [x] Implementation with slash command
- [ ] Implement the help command
- [ ] Fixed garbled characters in non-English (waiting for official fix)
- [ ] Show steam name when logging in (waiting for official fix)
- [ ] update using steamcmd
- [ ] Support for Windows version  
- [ ] Edit INI
- [ ] web page   
### update
------------------------
2024 2/6 v0.1　Only the base is implemented.
### ⚠️Currently this discordbot does not work on Windows ⚠️
## How to Install
```
pip install -r ./code/requirements.txt
```
<details>
<summary> <big> How to create a dscord bot </big></summary>
</details>

### Setup items
#### English
```en_example.env```
#### 日本語
```ja_example.env```
#### Please edit the following
```
#Server Address
server_address=
#Server's MCrcon port
server_pass = 
#server port
port =
#Administrator's discord id
discord_id =
#Discord bot token
token=
#Location of the folder with palworld
#Example: folder_pach="~/Steam/steamapps/common/PalServer"
folder_pach=
```
### Activation Method
#### Linux
```
./start.sh
```
#### Windows
```
./start.bat
```
## discord setup items
### Creating Administrative Roles
![image](./image/role_command.png)
![image](./image/role.png)
### Active Channel Settings
![image](./image/channel_command.png)



## discord command
#### under construction
```
/help
```
### Send command and bot chat to
```
/channel
```
#### Create an administrative role If not created, only the server administrator or bot owner can execute commands.
```
/createroll
```
#### Start server
```
/start
```
#### Stop server
```
/stop
```
#### Restart server
```
/restart
```
#### Sends a command to the server
```
/command command:
```
#### Still not working.
```
/update
```
## Main Features
### Entering and exiting servers
![image](./image/login.png)
![image](./image/server_login.png)
### Secure command submission
![image](./image/command.png)
### Start server !
![image](./image/start_command%20%20.png)