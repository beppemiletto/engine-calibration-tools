#!/usr/bin/python

import serial, time, struct
import numpy as np
import matplotlib.pyplot as plt


# initialization and open the port

# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
# ser.port = "/dev/ttyUSB0"
# ser.port = "/dev/ttyS0"
ser.port = "/dev/pts/1"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser.parity = serial.PARITY_NONE  # set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
# ser.timeout = None          #block read
ser.timeout = 0.15  # non-block read
# ser.timeout = 2              #timeout block read
ser.xonxoff = False  # disable software flow control
ser.rtscts = False  # disable hardware (RTS/CTS) flow control
ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2  # timeout for write

try:
    ser_open=False
    ser.open()
    ser_open = True
    numbers_str =[bytes('','ascii'),bytes('','ascii'),bytes('','ascii')]
    number_str =bytes('','ascii')
    data_idx = 0
    time_old = time.time()
    t0=time_old
    elapsed_time=0
    idle_time=0
    duty = False
    el_times = []
    t = []

except Exception as e:
    print("error open serial port: " + str(e))
    exit()
while ser.isOpen():
    if ser.isOpen():

        try:
            response = ser.read()
            if len(response):

                if response == b'\x00':
                    numbers_str[data_idx]=number_str
                    if data_idx < 2:
                        data_idx += 1
                    number_str = bytes('','ascii')

                elif response == b'\n':
                    if duty :
                        elapsed_time = time.time()-time_old
                    else:
                        elapsed_time = time.time()-time_old-idle_time
                    t.append(time.time()-t0)
                    el_times.append(elapsed_time)
                    duty = True
                    idle_time=0
                    time_old = time.time()
                    print("data: {} elapsed {} idle {}".format(numbers_str, elapsed_time, idle_time))
                    data_idx = 0
                    numbers_str = [bytes('', 'ascii'), bytes('', 'ascii'), bytes('', 'ascii')]
                elif response == b'\t':
                    fig = plt.figure(num=1,figsize=(10,4),dpi=200,facecolor='blue',edgecolor='yellow',frameon=True)
                    ax1=plt.subplot(1,1,1)
                    ax1.plot(t,el_times)
                    ax1.set_ylim(0,0.5)
                    ax1.grid(b=None,which='both',axis='both')
                    fig.show()

                    plt.savefig('plot.png')
                    el_times = []
                    t = []
                    t0=time_old
                    exit(0)

                else:
                    number_str += response
                response = ''
            else:
                idle_time = time.time()-time_old
                duty = False
        except Exception as e1 :
            print ("error communicating...: " + str(e1))
            ser.close()


    else:
        print ("cannot open serial port ")

