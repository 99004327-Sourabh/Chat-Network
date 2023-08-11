import os
import socket
import re
import threading
import time




def write(s_name, port_no):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.bind((s_name, port_no))
        soc.listen(1)
        conn, addr = soc.accept()

        while True:
            try:
        
                message = conn.recv(1024).decode()
                if message == "exit":
                    conn.close()
                    soc.close()
                    return
                
                
                elif message == "file_transfer":
                    f1 = conn.recv(256).decode()     
                  
                    x = re.findall("<.+>$", f1)
                    print(f"filename: {x[0][1:-1]}")
                    if not x:
                        print("Error:  did not match the pattern")
                        break
                
                    file_tup2 = os.path.splitext(x[0][1:-1])
                    name = "recv_"+str(file_tup2[0])+f'{username}to{username1}'+str(file_tup2[1])
                    with open(name, "wb") as download_file:
                        file_writer = b""
                        while True:
                            rec = conn.recv(1024)
                            if rec[-3:] == b'DRD':
                                file_writer += rec[:-3]
                                break
                            file_writer += rec
                        download_file.write(file_writer)
                        print("Received File")
                        conn.send("recv".encode())
                else:
                    print(message)

            except Exception as e:
                print(f"An error occurred: {str(e)}")

        conn.close()
        soc.close()



def read(s_name, username, port_no):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((s_name, port_no))
    print(f"connected to {username1} at {port_no}\n")
    while True:
        message = input()
        if message == "exit":
            conn.send(message.encode())
            conn.close()

            break
        elif message.startswith("transfer "):

                x = re.findall("<.+>$", message)
               
                if not os.path.exists(x[-1][1:-1]):
                    print("File not found")
                    conn.send(message.encode())
                    continue
                conn.send("file_transfer".encode())
                time.sleep(1)
                conn.send(message.encode())
                upload = open(x[-1][1:-1], "rb")
                data0 = upload.read(1024)
                time.sleep(2)
                while data0:
                    conn.send(data0)
                    data0 = upload.read(1024)
                conn.send(b'DRD')
                upload.close()
                conn.recv(32).decode()
                print("File successfully sent")
        else:
            conn.send(message.encode())


if __name__ == '__main__':
    username = input("Enter username: ")
    port_no = int(input("Enter port number: "))
    s_name = socket.gethostname()
    connection = threading.Thread(target=write, args=(s_name, port_no), daemon=True)
    connection.start()
    ip = input("Enter the user and their port number to be connected (separated by commas): ")
    ipn = ip.split(",")
    username1 = ipn[0]
    port_n = int(ipn[1])
    time.sleep(3)
    read(s_name, username1, port_n)
