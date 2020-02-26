from DriveSerial.constants import *
import sys
import pickle
from DriveSerial.thGenerator import *


def GenLoadTh(name: object, load: object, steadytime: object, direction: object, transtime: object, repetition: object) -> object:
    th_vector = thGenerator()
    th = th_vector.gen_SteadySeq(mode=LOADTH ,
                                        load=load ,
                                        speed=None,
                                        steadytime=steadytime,
                                        direction=direction,
                                        transtime=transtime,
                                        repetition=repetition,
                                        name=name )

    return (th)

def GenSpeedTh(name: object, speed: object,load: object, steadytime: object, direction: object, transtime: object, repetition: object) -> object:
    th_vector = thGenerator()
    th = th_vector.gen_SteadySeq( mode = SPEEDTH,
                                       load=None,
                                       speed=speed,
                                       steadytime=steadytime,
                                       direction=direction,
                                       transtime=transtime,
                                       repetition=repetition,
                                       name=name)

    return(th)

def SaveThGeneratorSetup():
    try:
        if len(self.th) > 1:
            print('save the time history {}.ext'.format(self.gen_seq_name))
            try:
                filename= self.gen_seq_name+'.pickle'
                with open(filename, 'wb') as handle:
                    pickle.dump(self.th, handle, protocol=pickle.HIGHEST_PROTOCOL)
            except:
                print("file recording problems!!")

    except:
        print("nothing to save")



def file_save(filename,th):
    from os.path import isfile
    if isfile(filename):
        print(f"File {filename} already exists.")
        filename=filename.split('.')[0]+'_1.'+filename.split('.')[-1]
        file = open(filename, 'w')
        assert isinstance(th, object)
        file.writelines(th)
        file.close()
    else:
        file = open(filename, 'w')
        assert isinstance(th, object)
        file.writelines(th)
        file.close()







if __name__ == '__main__':
    """ Only for testing functions"""
    name: str = 'LoadTimeHistory_sample'
    th = GenLoadTh(name,load=[10, 100, 15], steadytime=30, direction=DOWNWARDS,transtime=10, repetition = True)
    print("Time history total time = {} seconds.".format(len(th)*TRN_D_TIME))
    filename: str = THFILE_PATH + name + ".csv"
    file_save(filename,th)


    name: str = 'SpeedTimeHistory_sample'
    th = GenSpeedTh(name,speed=[600,2000,200],load=None, steadytime=30, direction=UPWARDS,transtime=10, repetition = True)
    print("Time history total time = {} seconds.".format(len(th)*TRN_D_TIME))
    filename: str = THFILE_PATH + name + ".csv"
    file_save(filename,th)

    #
    # th_vector_speed = thGenerator()
    # th = th_vector_speed.gen_SteadySeq(mode=SPEEDTH, load=[10, 100, 5], speed=[600, 2100, 100], steadytime=30,
    #                                    direction=UPWARDS, transtime=10)
    # print('Vector speed th=', th_vector_speed.th)
    #
    # th_vector_speedload = thGenerator()
    # th = th_vector_speedload.gen_SteadyTable(mode=SPEEDLOADTH, load=[10, 100, 10], speed=[600, 2000, 200],
    #                                          steadytime=30, direction=UPWARDS, transtime=0.5)
    # print('Vector speed th=', th_vector_speedload.th)

    exit(0)
