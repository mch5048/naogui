#!/usr/bin/env python

import os
import time

class Logbook(object):

    def __init__(self):
        """
        Class initialization
        """
        self._id = time.strftime("%d%m%Y_%H%M%S", time.gmtime()) #id of the log, it's the timestamp
        self._trial = 0
        self._pinv = 0.0
        self._rinv = 0.0
        self._pmult = 0.0
        self._rmult = 0.0
        self._gaze = False
        self._pointing = False
        self._timer = 0
        self._mp3 = ""

        #create the file
        open(self._id + ".csv", 'a').close()

        #Write the header as first line
        try:
           path_to_file = self._id + ".csv"
           with open(path_to_file, "a") as f:
               f.write( "trial, person_investment_first, robot_investment_first, person_investment_second, log_robot_investment_second, player_b_investment, pmf, bmf, person_total, gaze, pointing, timer_first, timer_second" + '\n')
               f.close()
        except:
           # log exception
           print("* LOGBOOK: execpion creating the header.")

    def AddTextLine(self, stringToAdd):
        try:
            path_to_file = self._id + ".csv"
            with open(path_to_file, "a") as f:
                f.write( stringToAdd + '\n')
                f.close()
        except:
            # log exception
            print("* LOGBOOK: execpion adding a text line to the file.")


    def AddLine(self, trial, pinv_first, rinv_first, pbinv, pmult, bmult, total, gaze, pointing, timer_first):
        '''Add a line in the log file

        trial, person_investment_first, robot_investment_first,
        player_b_investment, person mult factor, player b mult factor, total, gaze, pointing, timer_first
        '''
        try:
            path_to_file = self._id + ".csv"
            with open(path_to_file, "a") as f:
                f.write( str(trial) + "," + str(pinv_first) + "," +  str(rinv_first) + "," + str(pbinv) 
                         + "," + str(pmult) + "," + str(bmult) + "," + str(total) + "," + str(gaze) + "," + str(pointing) + "," + str(timer_first) + '\n')
                f.close()
        except:
            # log exception
            print("* LOGBOOK: execpion adding a line to the file.")
               
          
    def SaveFile(self, filePath):
        print(filePath)
        if os.path.isfile(filePath):
            self._path = filePath
            self._doc = minidom.parse(filePath)
            print("PARSER: the XML file was correctly loaded.")
            return True
        else:
            print("PARSER: Error the XML file does not exist, please check if the path is correct.")
            return False

