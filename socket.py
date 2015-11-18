#Создать процесс с двумя дочерними, процесс с двумя потоками.
#Организовать передачу данных между ними.

import multiprocessing
import time
import threading
import socket

#suprocess 1
def fun1():
    print('Child Process 1 started')
    #client
    sock=socket.socket()
    sock.connect(('localhost',64444))
    sdata='Subprocess 1 send message to Main Process'
    sock.send(sdata.encode("utf-8"))
    data=sock.recv(1024)
    print(data.decode("utf-8"))
    sock.close()

#subprocess 2
def fun2():
    print('Child Process 2 started')
    #client
    sock=socket.socket()
    sock.connect(('localhost',64444))
    sdata='Subprocess 2 send message to Main Process'
    sock.send(sdata.encode("utf-8"))
    sock.close()


#main process 2
def fun3():
    print('Process 2 started')
    t1=threading.Thread(target=fun4)
    t2=threading.Thread(target=fun4)
    t1.start()
    t2.start()

#Threads    
def fun4():
    print('Thread started')
    #client
    sock=socket.socket()
    sock.connect(('localhost',64444))
    sdata='Thread send message to Main Process'
    sock.send(sdata.encode("utf-8"))
       
    sock.close()
   
#main process 1/server 
if __name__ =='__main__':
    print('Process 1 started')
    p1=multiprocessing.Process(target=fun1)
    p2=multiprocessing.Process(target=fun2)
    p1.start()
    p2.start()

    p3=multiprocessing.Process(target=fun3)
    p3.start()

    #server
    sockserv=socket.socket()
    sockserv.bind(('',64444))
    sockserv.listen(5)
    try:
        while True:
            conn, addr=sockserv.accept()
            print ("New connection from " + addr[0])
            data=conn.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"))
            sdata=("accept")
            conn.send(sdata.encode("utf-8"))
    except:
        print("Error")
    finally:
        conn.close()
        sockserv.close()
  
    p1.join()
    p2.join()
    p3.join()
    time.sleep(10)
