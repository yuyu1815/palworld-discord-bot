from mcrcon import MCRcon

server_address = "192.168.3.5"
server_pass = "adminkokoa"
server_port=32235

try:
    with MCRcon(server_address, server_pass, server_port) as mcr:
        cm = input("起動したいコマンドを入力してね！")
        log = mcr.command(cm)
        print(log)
        if not log.find('Unknown command'):
            print("True")
        else:  
            print("False")
except Exception as e:
    print("False")
