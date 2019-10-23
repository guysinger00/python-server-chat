# client code:
import socket
from select import select
import msvcrt

client_socket = socket.socket()


def send_msg(msg):
    # enter- messge
    # exit-return string with the length of the user name,te use name,the mmessge
    msg = str(len(my_name)) + my_name + msg
    return msg


my_name = input("pls enter your name you name-")
while my_name[0] in "1234567890":
    my_name = input("Can't start with a number pls try again-")
try:
    client_socket.connect(("127.0.0.1", 8080))
    client_socket.send(my_name.encode())
except Exception as e:
    print(e)
    client_socket.close()
else:
    while True:
        try:
            rlist,_,_ = select([client_socket], [client_socket], [], 1)
        except:
            print("Connection has been lost")
            break
        if rlist:
            try:
                data = client_socket.recv(1024).decode()
            except Exception as e:
                print(e)
                client_socket.close()
            else:
                print(data)
        elif msvcrt.kbhit():
            data = input()
            try:
                client_socket.send(send_msg(data).encode())
            except Exception as e:
                print(e)
                client_socket.close()