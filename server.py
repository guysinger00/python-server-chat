import socket
import select

from PIL import ImageGrab, Image
import PIL
import msvcrt

server_socket=socket.socket()
server_socket.bind(('0.0.0.0',8080))
server_socket.listen(5)
client_sockets = []
messages_to_send = []
users_online=[]
print("starting server..")



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


def who_is_online():
    #enter-none
    #exit-the online users
    client_socket.send(str(users_online).encode())


def notify_all(msg, non_receptors):
    #enter-messge to send to all the client and the sockets list that show as the non receptors of the messge
    #exit-send the messge to all the clients exept the client who send the massge
    for client in client_sockets:
        if client not in non_receptors:
            try:
                client.send(str(msg).encode())
            except Exception as e:
                print(e)


while True:
    rlist,wlist,xlist = select.select([server_socket]+client_sockets, client_sockets,[])
    for client_socket in rlist:
        if client_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            print(address[0], "connected…")
            try:
                name=new_socket.recv(1024).decode()
            except Exception as e:
                print(e)
            else:
                notify_all(name+" join to the chat", [server_socket, client_sockets])
                users_online.append(name)
                client_sockets.append(new_socket)
        else:
            try:
                data=client_socket.recv(1024).decode()
            except Exception as e:
                print(e)
                client_socket.close()
            else:
                try:
                    (name,msg)=get_msg(data)
                    notify_all(name+">>>>>"+msg+"            online users-"+str(users_online), [server_socket,client_socket])
                except Exception as e:
                    print(e)
                    client_socket.close()





