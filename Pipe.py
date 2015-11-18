#Создать процесс с двумя дочерними, процесс с двумя потоками.
#Организовать передачу данных между ними.

import multiprocessing
import time
import threading

(pout11,pin11)=multiprocessing.Pipe() #Main process 1 - subprocess 1
(pout12,pin12)=multiprocessing.Pipe() #Main process 1 - subropcess 2
(pout22,pin22)=multiprocessing.Pipe() #Main process 1 - Main process 2
(pout23,pin23)=multiprocessing.Pipe() #Main process 2 - threads
#suprocess 1
def fun1(pin11, pout11):
    print('Subprocess 1 started')
    time.sleep(1)
    while 1:
        print(pout11.recv())  
        pin11.send('Subprocess 1 send message to Main process 1')
        time.sleep(0.5)
    
#subprocess 2
def fun2(pin12, pout12):
    print('Subprocess 2 started')
    time.sleep(1)
    while 1:
        print(pout12.recv())
        pin12.send('Child Process 2 send message to Child Process 1')
        time.sleep(0.6)

#main process 2
def fun3(pin22, pout22):
    print('Main process 2 started')
    time.sleep(1)
    t1=threading.Thread(target=fun4, args=(pin23, pout23))
    t2=threading.Thread(target=fun4, args=(pin23, pout23))
    t1.start()
    t2.start()
    while 1:
        print(pout22.recv())  
        pin22.send('Main process 2 send message to Main process 1')
        time.sleep(0.7)

#Threads    
def fun4(pin23,pout23):
    pin23.send('Thread active')
    time.sleep(1)
   
#main process 1 
if __name__ =='__main__':
    print('Main process 1 started')
    time.sleep(1)
    p1=multiprocessing.Process(target=fun1, args=(pin11, pout11 ))
    p2=multiprocessing.Process(target=fun2, args=(pin12, pout12 ))
    p1.start()
    p2.start()
    pin11.send('Main process 1 send message to Subprocess 1')
    pin12.send('Main process 1 send message to Subprocess 2')

    p3=multiprocessing.Process(target=fun3, args=(pin22, pout22))
    p3.start()

    while 1:
        print(pout22.recv())
    
    p1.join()
    p2.join()
    p3.join()
    time.sleep(10)
