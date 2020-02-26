# -*- coding: utf-8 -*-
"""thGenerator.py

This module provides class with methods for building a time history developped as series
of command  values.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from typing import List, Any

from DriveSerial.constants import *
import time


class thGenerator():
    row_template: str
    th: List[Any]

    def __init__(self):
        self.th =[]
        self.mode = None
        self.row_template="{};{};{}\n"


     ## Steady vector time history geneators , load and speed methods
    # self.th = th_vector_load.gen_SteadySeq(mode=LOADTH,
    #                                        load=[self.load_min, self.load_max, self.load_step],
    #                                        speed=None,
    #                                        steadytime=self.steady_time,
    #                                        direction=DOWNWARDS,
    #                                        transtime=self.move_time,
    #                                        repetition=self.load_repetition,
    #                                        name=self.gen_seq_name)

    def gen_SteadySeq(self, mode: object = None, load: object = [None, None, None], speed: object = [None, None, None], steadytime: object = None,
                      direction: object = None,
                      transtime: object = None,
                      repetition: object = None,
                      name: object = None) -> object:
        if mode :
            if mode == LOADTH:
                self.mode = LOADTH
                if len(load)<3:
                    self.warning = 'WARNING: missing parameters for time history generator'
                    return 1, self.warning
                elif len(load)>=3 :
                    self.load_min = load[0]
                    self.load_max = load[1]
                    self.load_stp = load[2]

                    try:
                        self.steadytime = steadytime
                    except:
                        self.steadytime = DEFAULTSTEADYTIME

                    if self.load_min >= self.load_max:
                        self.warning = 'WARNING: minimum ({}) bigger then maximum ({}) in parameters for time history generator'.format(self.load_min, self.load_max)
                        return 2, self.warning
                    if STEADYMAXTIME < self.steadytime :
                        self.warning = 'WARNING: steady time ({}) exceeding the maximum ({}) allowed'.format(self.steadytime, STEADYMAXTIME)
                        return 3, self.warning
                    if STEADYMINTIME > self.steadytime :
                        self.warning = 'WARNING: steady time ({}) lower than the minimum ({}) allowed'.format(self.steadytime, STEADYMINTIME)
                        return 4, self.warning
                    if self.load_stp > (self.load_max - self.load_min):
                        self.warning = 'WARNING: step time ({}) bigger than total range ({}) '.format(self.load_stp, (self.load_max - self.load_min))
                        return 5, self.warning

                try:
                    self.direction = direction
                    if UPWARDS < self.direction < DOWNWARDS:
                        self.warning = 'WARNING: direction specification not correct. Assuming default.'
                        self.direction= DEFAULTDIR
                except:
                    self.warning = 'WARNING: direction specification missing. Assuming default.'
                    self.direction= DEFAULTDIR

                ## generate the time history
                steps_nr= int((self.load_max-self.load_min)/self.load_stp)+1
                steps: List[float]=[]
                idx: int
                for idx in range(steps_nr):
                    if self.direction == UPWARDS:
                        steps.append(float(self.load_min+idx*self.load_stp))
                    else:
                        steps.append(float(self.load_max-idx*self.load_stp))

                if transtime :
                    self.transtime = transtime
                else:
                    self.transtime = DEFAULTTRNTIME

                # initialize time of time history
                load_old = STARTMINLOAD
                # write the title of column in csv like table
                csv_row: str = self.row_template.format('Brake [RPM]','Torque [%]','ExternalControl')
                self.th.append(csv_row)
                for idx, target in enumerate(steps):
                    # transition to next
                    trn_steps = int(self.transtime / TRN_D_TIME )+1
                    trn_x_step: float = float((target - load_old)/ trn_steps)

                    if idx < steps_nr:
                        for jdx in range(trn_steps):
                            csv_row = self.row_template.format(0,load_old + jdx * trn_x_step,1)
                            self.th.append(csv_row)

                    steady_steps = int(steadytime/TRN_D_TIME)
                    for jdx in range(steady_steps):
                        csv_row = self.row_template.format(0,int(target),1)
                        self.th.append(csv_row)
                    load_old=target

                if repetition:
                    buffer_th = self.th.copy()
                    buffer_th.reverse()
                    for csv_row in buffer_th:
                        self.th.append(csv_row)


                    


            if mode == SPEEDTH:
                self.mode = SPEEDTH
                if len(speed) < 3:
                    self.warning = 'WARNING: missing parameters for time history generator'
                    return 1, self.warning
                elif len(speed) >= 3:
                    self.speed_min = speed[0]
                    self.speed_max = speed[1]
                    self.speed_stp = speed[2]

                    try:
                        self.steadytime = steadytime
                    except:
                        self.steadytime = DEFAULTSTEADYTIME

                    if self.speed_min >= self.speed_max:
                        self.warning = 'WARNING: minimum ({}) bigger then maximum ({}) in parameters for time history generator'.format(
                            self.speed_min, self.speed_max)
                        return 2, self.warning
                    if STEADYMAXTIME < self.steadytime:
                        self.warning = 'WARNING: steady time ({}) exceeding the maximum ({}) allowed'.format(
                            self.steadytime, STEADYMAXTIME)
                        return 3, self.warning
                    if STEADYMINTIME > self.steadytime:
                        self.warning = 'WARNING: steady time ({}) lower than the minimum ({}) allowed'.format(
                            self.steadytime, STEADYMINTIME)
                        return 4, self.warning
                    if self.speed_stp > (self.speed_max - self.speed_min):
                        self.warning = 'WARNING: step time ({}) bigger than total range ({}) '.format(self.speed_stp, (
                                    self.speed_max - self.speed_min))
                        return 5, self.warning

                try:
                    self.direction = direction
                    if UPWARDS < self.direction < DOWNWARDS:
                        self.warning = 'WARNING: direction specification not correct. Assuming default.'
                        self.direction = DEFAULTDIR
                except:
                    self.warning = 'WARNING: direction specification missing. Assuming default.'
                    self.direction = DEFAULTDIR

                # generate the time history
                steps_nr= int((self.speed_max-self.speed_min)/self.speed_stp)+1
                steps: List[float]=[]
                idx: int
                for idx in range(steps_nr):
                    if self.direction == UPWARDS:
                        steps.append(float(self.speed_min+idx*self.speed_stp))
                    else:
                        steps.append(float(self.speed_max-idx*self.speed_stp))

                if transtime :
                    self.transtime = transtime
                else:
                    self.transtime = DEFAULTTRNTIME

                # initialize time of time history
                speed_old = STARTMINSPEED
                # write the title of column in csv like table
                csv_row: str = self.row_template.format('Brake [RPM]','Torque [%]','ExternalControl')
                self.th.append(csv_row)
                for idx, target in enumerate(steps):
                    # transition to next
                    trn_steps = int(self.transtime / TRN_D_TIME )+1
                    trn_x_step: float = float((target - speed_old)/ trn_steps)

                    if idx < steps_nr:
                        for jdx in range(trn_steps):
                            csv_row = self.row_template.format(speed_old + jdx * trn_x_step, 0, 1)
                            self.th.append(csv_row)

                    steady_steps = int(steadytime/TRN_D_TIME)
                    for jdx in range(steady_steps):
                        csv_row = self.row_template.format(int(target),0,1)
                        self.th.append(csv_row)
                    speed_old=target

                if repetition:
                    buffer_th = self.th.copy()
                    buffer_th.reverse()
                    for csv_row in buffer_th:
                        self.th.append(csv_row)

            return self.th

    ## Steady tables time history geneators , speed x load and load x speed methods

    def gen_SteadyTable(self, mode=None, load=[None, None, None], speed=[None, None, None], steadytime=None,
                      direction=None, transtime=None):
        if mode:

            if mode == SPEEDLOADTH or mode == LOADSPEEDTH:
                self.mode = mode
                if len(speed) < 3:
                    self.warning = 'WARNING: missing parameters for time history generator'
                    return 1, self.warning
                elif len(speed) >= 3:
                    self.speed_min = speed[0]
                    self.speed_max = speed[1]
                    self.speed_stp = speed[2]

                    try:
                        self.steadytime = steadytime
                    except:
                        self.steadytime = DEFAULTSTEADYTIME

                    if self.speed_min >= self.speed_max:
                        self.warning = 'WARNING: minimum ({}) bigger then maximum ({}) in parameters for time history generator'.format(
                            self.speed_min, self.speed_max)
                        return 2, self.warning
                    if STEADYMAXTIME < self.steadytime:
                        self.warning = 'WARNING: steady time ({}) exceeding the maximum ({}) allowed'.format(
                            self.steadytime, STEADYMAXTIME)
                        return 3, self.warning
                    if STEADYMINTIME > self.steadytime:
                        self.warning = 'WARNING: steady time ({}) lower than the minimum ({}) allowed'.format(
                            self.steadytime, STEADYMINTIME)
                        return 4, self.warning
                    if self.speed_stp > (self.speed_max - self.speed_min):
                        self.warning = 'WARNING: step time ({}) bigger than total range ({}) '.format(self.speed_stp, (
                                self.speed_max - self.speed_min))
                        return 5, self.warning

                try:
                    self.direction = direction
                    if UPWARDS < self.direction < DOWNWARDS:
                        self.warning = 'WARNING: direction specification not correct. Assuming default.'
                        self.direction = DEFAULTDIR
                except:
                    self.warning = 'WARNING: direction specification missing. Assuming default.'
                    self.direction = DEFAULTDIR

                if len(load) < 3:
                    self.warning = 'WARNING: missing parameters for time history generator'
                    return 1, self.warning
                elif len(load) >= 3:
                    self.load_min = load[0]
                    self.load_max = load[1]
                    self.load_stp = load[2]

                if self.load_min >= self.load_max:
                    self.warning = 'WARNING: minimum ({}) bigger then maximum ({}) in parameters for time history generator'.format(
                        self.load_min, self.load_max)
                    return 2, self.warning
                if self.load_stp > (self.load_max - self.load_min):
                    self.warning = 'WARNING: step time ({}) bigger than total range ({}) '.format(
                        self.load_stp, (
                                self.load_max - self.load_min))
                    return 5, self.warning

                ## generate the time history, calculate the steps

                speed_steps_nr = int((self.speed_max - self.speed_min) / self.speed_stp) + 1
                steps_speed = []
                for idx_speed in range(speed_steps_nr):
                    if self.direction == UPWARDS:
                        steps_speed.append(float(self.speed_min + idx_speed * self.speed_stp))
                    else:
                        steps_speed.append(float(self.speed_max - idx_speed * self.speed_stp))

                load_steps_nr = int((self.load_max - self.load_min) / self.load_stp) + 1
                steps_load = []
                for idx_load in range(load_steps_nr):
                    if self.direction == UPWARDS:
                        steps_load.append(float(self.load_min + idx_load * self.load_stp))
                    else:
                        steps_load.append(float(self.load_max - idx_load * self.load_stp))

                if transtime:
                    self.transtime = transtime
                else:
                    self.transtime = DEFAULTTRNTIME

                # initialize time of time history
                if self.mode == SPEEDLOADTH:
                    for idx_speed, target_speed in enumerate(steps_speed):
                        ## generate the time history
                        for idx_load, target_load in enumerate(steps_load):
                            csv_row = "{},{},{},{}".format(self.mode, self.steadytime, target_speed, target_load)
                            self.th.append(csv_row)
                            # transition to next load
                            if idx_load < load_steps_nr - 1:
                                trn_steps = int(self.transtime / TRN_D_TIME) + 1
                                load_step = float((steps_load[idx_load + 1] - target_load) / float(trn_steps))
                                for iidx in range(trn_steps):
                                    load_new = target_load + load_step * iidx
                                    csv_row = "{},{},{},{}".format(self.mode, TRN_D_TIME, target_speed, load_new)
                                    self.th.append(csv_row)

                        # transition to next speed
                        if idx_speed < speed_steps_nr - 1:
                            trn_steps = int(self.transtime / TRN_D_TIME) + 1
                            speed_step = float((steps_speed[idx_speed + 1] - target_speed) / float(trn_steps))
                            for iidx in range(trn_steps):
                                speed_new = target_speed + speed_step * iidx
                                csv_row = "{},{},{},{}".format(self.mode, TRN_D_TIME, speed_new, steps_load[0])
                                self.th.append(csv_row)

            return self.th


    def segment_load_gen(self, mode: object = None, load: object = [None, None, None],
                         speed: object = [None, None, None],
                         steadytime: object = None,
                         direction: object = None,
                         transtime: object = None,
                         repetition: object = None,
                         name: object = None) -> object:
        ## generate the time history
        steps_nr = int((self.load_max - self.load_min) / self.load_stp) + 1
        steps: List[float] = []
        idx: int
        for idx in range(steps_nr):
            if self.direction == UPWARDS:
                steps.append(float(self.load_min + idx * self.load_stp))
            else:
                steps.append(float(self.load_max - idx * self.load_stp))

        if transtime:
            self.transtime = transtime
        else:
            self.transtime = DEFAULTTRNTIME

        # initialize time of time history
        load_old = STARTMINLOAD
        # write the title of column in csv like table
        csv_row: str = self.row_template.format('Brake [RPM]', 'Torque [%]', 'ExternalControl')
        self.th.append(csv_row)
        for idx, target in enumerate(steps):
            # transition to next
            trn_steps = int(self.transtime / TRN_D_TIME) + 1
            trn_x_step: float = float((target - load_old) / trn_steps)

            if idx < steps_nr:
                for jdx in range(trn_steps):
                    csv_row = self.row_template.format(0, load_old + jdx * trn_x_step, 1)
                    self.th.append(csv_row)

            steady_steps = int(steadytime / TRN_D_TIME)
            for jdx in range(steady_steps):
                csv_row = self.row_template.format(0, int(target), 1)
                self.th.append(csv_row)
            load_old = target

        if repetition:
            buffer_th = self.th.copy()
            buffer_th.reverse()
            for csv_row in buffer_th:
                self.th.append(csv_row)






