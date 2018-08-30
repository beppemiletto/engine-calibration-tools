from DriveSerial.thGenerator import *
from DriveSerial.constants import *

if __name__ == '__main__':
    """ Only for testing functions"""

    th_vector_load = thGenerator()
    th = th_vector_load.gen_SteadySeq(mode=LOADTH, load=[10, 100, 5], speed=None, steadytime=60, direction=DOWNWARDS, transtime = 20)
    print('Vector load th=',th_vector_load.th)

    th_vector_speed = thGenerator()
    th = th_vector_speed.gen_SteadySeq(mode=SPEEDTH, load=[10, 100, 5], speed=[600, 2100, 100], steadytime=30, direction=UPWARDS, transtime = 10)
    print('Vector speed th=',th_vector_speed.th)

    th_vector_speedload = thGenerator()
    th = th_vector_speedload.gen_SteadyTable(mode=SPEEDLOADTH, load=[10, 100, 10], speed=[600, 2000, 200], steadytime=30, direction=UPWARDS, transtime = 0.5)
    print('Vector speed th=',th_vector_speedload.th)