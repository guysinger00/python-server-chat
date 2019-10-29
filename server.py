import socket
import select



server_socket=socket.socket()
server_socket.bind(('0.0.0.0',8080))
server_socket.listen(5)
client_sockets = []
messages_to_send = []
users_online=[]
print("starting server..")


def get_encrypted_msg(msg):
    index=0
    new_msg = ""
    for letter in msg:
        ch = (ord(letter)+index) / 2
        new_msg = new_msg + str(chr(int(ch)))
        index=index+1
    return new_msg



def send_encrypted_msg(msg):
    new_msg = ""
    index=0
    for letter in msg:
        ch = chr(ord(letter) * 2-index)
        new_msg = new_msg + ch
        index=index+1
    return new_msg








def get_msg(msg):
    #enter-get message with the length of the one who send her,his name and the message
    #exit-  retun the name of the sender and the messge
    try:
        len=int(msg[0])*10+int(msg[1])
        name = msg[2:len+2]
        msg=msg[len+2:]
    except Exception:
        len = int(msg[0])
        name = msg[1:len+1]
        msg = msg[len+1:]
    return name,msg


def notify_all(msg, non_receptors):
    #enter-messge to send to all the client and the sockets list that show as the non receptors of the messge
    #exit-send the messge to all the clients exept the client who send the massge
    for client in client_sockets:
        if client not in non_receptors:
            try:
                client.send(send_encrypted_msg(str(msg)).encode())
            except Exception as e:
                print(e)


while True:
    rlist,wlist,xlist = select.select([server_socket]+client_sockets, client_sockets,[])
    for client_socket in rlist:
        if client_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            print(address[0], "connected…")
            try:
                name=get_encrypted_msg(new_socket.recv(1024).decode())
            except Exception as e:
                print(e)
            else:
                notify_all(name+" joined the chat", [server_socket, client_sockets])
                users_online.append(name)
                client_sockets.append(new_socket)
        else:
            try:
                data=get_encrypted_msg(client_socket.recv(1024).decode())
            except Exception as e:
                print(e)
                client_socket.close()
            else:
                try:
                    (name,msg)=get_msg(data)
                    notify_all(name+">>>>>"+msg+"           online users-"+str(users_online), [server_socket,client_socket])
                except Exception as e:
                    print(e)
                    client_socket.close()




