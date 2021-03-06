#!/usr/bin/env python


#Copyright (c) 2016 Massimiliano Patacchiola
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## @package NAO
# Scree resolution 1920x1080
# It is necessary to have pyQt4 installed
# To generate python code from the .ui file: pyuic4 mainwindow.ui -o design.py

# Libraries for Qt
from PyQt4 import QtGui  # Import the PyQt4 module we'll need
from PyQt4.QtCore import QElapsedTimer
from PyQt4.QtCore import QThread
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore

import sys  
import os
import time
import math

#python -m pip install pyaudio
#sudo apt-get install python-pyaudio python3-pyaudio
import subprocess

#Importing my custom libraries
sys.path.insert(1, '../include')
sys.path.insert(1, "../include/pynaoqi-python2.7-2.1.3.3-linux64") #import this module for the nao.py module
import design
import pparser
import nao
import logbook

#Robot Paramaters
SPEED = 0.2

## Class WorkerThread
#  
# It is a QThread that send signals
# and receive signals from the GUI
#
class WorkerThread(QThread):
  def __init__(self):
    QThread.__init__(self)

    #Signal variables
    self.enable_components_gui_signal = SIGNAL("enable_components_gui_signal")
    self.disable_signal = SIGNAL("disable_signal")
    self.enable_signal = SIGNAL("enable_signal")
    self.no_robot_signal = SIGNAL("no_robot_signal")
    self.yes_robot_signal = SIGNAL("yes_robot_signal")
    self.bad_xml_signal = SIGNAL("bad_xml_signal")
    self.good_xml_signal = SIGNAL("good_xml_signal")
    self.update_gui_signal = SIGNAL("update_gui_signal")
    self.show_start_btn_signal = SIGNAL("show_start_btn_signal")

    #Misc variables
    self.timer = QElapsedTimer()
    self.myParser = pparser.Parser()    
    self.STATE_MACHINE = 0

    #Status variables
    self._robot_connected = False
    self._xml_uploaded = False
    self._start_pressed = False
    self._confirm_pressed = False
    self._session_info_given = False

    #Sub state of state 1
    self.SUB_STATE = 0

    #Logbook variables
    self._log_first_line = ""
    self._log_timer = 0
    self._log_trial = 0
    self._log_round = 10
    self._log_total = 0
    self._log_player_investment = 0
    self._log_person_investment = 0   
    self._log_robot_investment = 0
    self._log_multiplied_person_investment = 0

    self._log_pmult = 0
    self._log_rmult = 0
    self._log_gaze = False
    self._log_pointing = False
    self._log_mp3 = ""


  ## Main function of the Thread
  # 
  # It runs the State Machine
  #
  def run(self):
    #Init the State machine 
    #self.emit(self.enable_signal) #GUI enabled
    self.emit(self.enable_components_gui_signal, True,  False, False, False) #GUI components
    self.timer.start()
    self.STATE_MACHINE = 0

    while True:

        time.sleep(0.050) #50 msec sleep to evitate block

        #STATE-0 init
        if self.STATE_MACHINE == 0:
            if self._robot_connected==True and self._xml_uploaded==True and self._start_pressed==True and self._session_info_given==True:
                #When there are zero pretrial then jump to state 2
                #If there are more than zero pretrial go to state 1
                if self.myParser._pretrial_repeat == 0:
                    self.STATE_MACHINE = 2
                elif self.myParser._pretrial_repeat > 0:
                    self.STATE_MACHINE = 1 #switching to next state
                self.SUB_STATE = 0 #substate of state machine 1 set to zero
                #self.emit(self.disable_signal) #GUI disabled                
                self.logger = logbook.Logbook() #Logbook Init
                self.logger.AddTextLine(self._log_first_line)  #Add the first line to the logbook
                self.emit(self.show_start_btn_signal, False)
                self._start_pressed = False
            else:
                #self.emit(self.disable_signal) #GUI disabled
                current_time = time.strftime("%H:%M:%S", time.gmtime())
                status = "robot_coonnected = " + str(self._robot_connected) + "\n" 
                status += "xml_uploaded = " + str(self._xml_uploaded) + "\n" 
                status += "start_pressed = " + str(self._start_pressed) + "\n"
                status += "session_info_given = " + str(self._session_info_given) + "\n"
                print "[0] " + current_time + " Waiting... \n" + status
                time.sleep(3)

        #STATE-1 pretraining phase, subject play with researcher
        if self.STATE_MACHINE == 1:

            #SUB_STATE == 0
                #Init all the variables
                #self._pretrial_is_person_turn == True
            if self.SUB_STATE == 0:
                self._pretrial_counter = 0
                self._confirm_pressed = False
                self._start_pressed = False
                #self.emit(self.enable_signal) #GUI enabled
                print "[1][0] Enablig components"
                self.emit(self.enable_components_gui_signal, False,  True, True, False) #GUI components
                local_string = "It's your turn..."
                #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                self.emit(self.update_gui_signal, 0, 0, 10, 0, 15, 15, 30, local_string)
                self.SUB_STATE = 1    
          
            #SUB_STATE == 1
                #Waiting person answer CONFIRM
                #Print the result when person reply
            if self.SUB_STATE == 1:
                if self._confirm_pressed == True:
                    print "[1][1] Person Confirm Pressed"
                    self._confirm_pressed = False
                    self._log_round = float(self._log_round) - float(self._log_person_investment)
                    self._log_multiplied_person_investment = self._log_person_investment * 3.0
                    self._log_player_investment = self._log_multiplied_person_investment
                    self._log_robot_investment = 0
                    person_slider_value = self._log_person_investment
                    #total, player_investment, round_total, your_investment, robot_investment, robot_slider_value
                    local_string = ""
                    #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                    self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)
                    #GUI: start_btn, confirm_btn, person_slider, robot_slider
                    self.emit(self.enable_components_gui_signal, False,  False, False, True) #GUI components
                    print "[1][1] Waiting for researcher feedback..." 
                    self.SUB_STATE = 2

            #SUB_STATE == 2
                #Waiting researcher answer
                #Print result when researcher answer
                #Switch to SUBSTATE 3
            if self.SUB_STATE == 2:
                if self._confirm_pressed == True:
                    print "[1][2] Researcher Confirm Pressed"
                    self._confirm_pressed = False
                    #Updating the investment values
                    #self._log_multiplied_person_investment = self._log_person_investment * 3.0 #multiplied times 3         
                    robot_slider_value = self._log_robot_investment
                    energy_value = math.ceil(self._log_multiplied_person_investment / 2) #ceiling roundoff
                    energy_maximum = self._log_multiplied_person_investment
                    self._log_robot_investment = energy_value
                    self._log_total = self._log_total + self._log_round + self._log_robot_investment
                    local_string = "You invested: " + str(self._log_multiplied_person_investment / 3) 
                    local_string += "  Robot received: " + str(self._log_multiplied_person_investment) + "  Robot returned: " + str(self._log_robot_investment) + '\n'
                    local_string += "In this round you made: " + str(self._log_round + self._log_robot_investment) + '\n' 
                    local_string += "Total in your bank: " + str(self._log_total) + '\n\n'
                    local_string += "Please press START to begin a new round..."
                    #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                    self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round + self._log_robot_investment, self._log_robot_investment, robot_slider_value, energy_value, energy_maximum, local_string)
                    #self.emit(self.disable_signal) #GUI disabled
                    self.emit(self.enable_components_gui_signal, True,  False, False, False) #Start enabled
                    #time.sleep(10)
                    #self.emit(self.enable_components_gui_signal, False,  True, True, False) #GUI components
                    #self.emit(self.enable_signal) #GUI enabled                                                     
                    self.SUB_STATE = 3

            #SUB_STATE == 3
                #Waiting for the subject pressing START:
                #when subject press start goes to state 4
            if self.SUB_STATE == 3:
                if self._start_pressed == True: 
                    self._start_pressed = False
                    self.emit(self.enable_components_gui_signal, False,  True, True, False) #Start disabled
                    self.SUB_STATE = 4

            #SUB_STATE == 4
                #Check if pretrial is finished:
                #If pretrial is not finished jump to SUB_STATE 1
                #if Pretrial is finished show the START button and jump to SUB_STATE 4
            if self.SUB_STATE == 4:
                if int(self._pretrial_counter) == int(self.myParser._pretrial_repeat):
                    #Pretrial finished
                    print "[1][3] Pretrial finished, starting the game..."
                    self.emit(self.show_start_btn_signal, True) #show the button START
                    #self.emit(self.disable_signal) #GUI disabled
                    energy_value = self._log_robot_investment
                    energy_maximum = self._log_multiplied_person_investment
                    local_string = "The first part is finished." + '\n\n'
                    local_string += "Please press START to begin the game..."
                    #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                    self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)
                    self.emit(self.enable_components_gui_signal, True,  False, False, False) #Start enabled
                    self.SUB_STATE = 5
                else:
                    self._pretrial_counter = self._pretrial_counter + 1
                    #Updating the investment values (RESET)
                    self._log_round = 10
                    self._log_person_investment = 0
                    self._log_robot_investment = 0
                    self._log_player_investment = 0
                    local_string = "It's your turn..."
                    #total, player_investment, round_total, your_investment, robot_investment, robot_slider_value
                    self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)
                    print "[1][3] New Round: " + str(self._pretrial_counter) + " / " + str(self.myParser._pretrial_repeat)
                    self.SUB_STATE = 1


            #SUB_STATE == 5
                #When the START button is pressed go to STATE_MACHINE=2
                #but before it resets the robot arms and move the head to look down 
            if self.SUB_STATE == 5:
                if self._start_pressed == True: 
                    self._start_pressed = False
                    #Updating the investment values (RESET)
                    self._log_round = 10
                    self._log_person_investment = 0
                    self._log_robot_investment = 0
                    self._log_player_investment = 0
                    self._log_total = 0
                    #total, player_investment, round_total, your_investment, robot_investment, robot_slider_value
                    local_string = ""
                    #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                    self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)
                    #self.emit(self.show_start_btn_signal, False)
                    self.emit(self.enable_components_gui_signal, False,  False, False, False) #GUI components
                    self.STATE_MACHINE = 2
                    #Enabling the face tracking OR looking down
                    #Reset of the arms
                    #This has been done here because it starts
                    #before the 3 seconds pause
                    self.myPuppet.right_arm_pointing(False, SPEED)
                    self.myPuppet.left_arm_pointing(False, SPEED)
                    if self.myParser._gaze_list[self._log_trial] == "True":
                        print "[2] looking == True"
                        self._log_gaze = "True"
                        self.myPuppet.enable_face_tracking(True) #enables face tracking
                    elif self.myParser._gaze_list[self._log_trial] == "False":
                        print "[2] looking == False"
                        self._log_gaze = "False"
                        self.myPuppet.enable_face_tracking(False) #disable face tracking
                        self.myPuppet.look_to(1, SPEED) #angle(radians) + speed
                    #Pause then start...
                    time.sleep(3) #small pause before starting
            
 
        #STATE-2  Robot talk (look or not)
        if self.STATE_MACHINE == 2:
            #Updating the multiplication values
            self._log_pmult = float(self.myParser._pmf_list[self._log_trial])
            self._log_rmult = float(self.myParser._rmf_list[self._log_trial])
            #Updating the investment values (RESET)
            self._log_round = 10
            self._log_person_investment = 0
            self._log_robot_investment = 0
            self._log_player_investment = 0
            #total, player_investment, round_total, your_investment, robot_investment, robot_slider_value
            local_string = ""
            #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
            self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)     
            print "[2] Robot Talking + Looking/Non-Looking"            
            #self.myPuppet.look_to(1, SPEED)
            #time.sleep(2)
            if self.myParser._gaze_list[self._log_trial] == "True":
              print "[2] looking == True"
              self._log_gaze = "True"
              #self.myPuppet.look_to(0, SPEED) #angle(radians) + speed
              self.myPuppet.enable_face_tracking(True) #enables face tracking
            elif self.myParser._gaze_list[self._log_trial] == "False":
              print "[2] looking == False"
              self._log_gaze = "False"
              self.myPuppet.enable_face_tracking(False) #disable face tracking
              self.myPuppet.look_to(1, SPEED) #angle(radians) + speed

            print "[2] bla bla bla ..."
            self._log_mp3 = self.myParser._mp3_list[self._log_trial]
            mp3_path = "/home/nao/naoqi/mp3/" + self._log_mp3
            self.myPuppet.play_audio(mp3_path, 0.8) #play the audio file at that volume
            #mp3_path = "../share/mp3/" + self._log_mp3
            #self.myPuppet.say_something(mp3_path)
            #The sleep is not necessary here if the play_audio function is used
            #time.sleep(4) #sleep as long as the mp3 file
            #when mp3 file finish          
            self.STATE_MACHINE = 3 #next state
            #The robot look the screen
            #self.myPuppet.enable_face_tracking(False) #disable face tracking
            #self.myPuppet.look_to(1, SPEED) #angle(radians) + speed
            time.sleep(1)
            #Writing: "It is your turn"
            local_string = "It's your turn..."
            #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
            self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string) 
            #Reset the timer and switch to the next state
            self.timer.restart() #RESET here the timer
            print "[3] Waiting for the subject answer..." #going to state 3

        #STATE-3 waiting for the subject investment
        if self.STATE_MACHINE == 3:                      
            #self.emit(self.enable_signal) #GUI enbled
            self.emit(self.enable_components_gui_signal, False,  True, True, False)  #GUI components                    
            if self._confirm_pressed == True:   #when subject give the answer
                self._log_timer = self.timer.elapsed() #record the time
                print "[3] TIME: " + str(self._log_timer)
                print "[3] INVESTMENT: " + str(self._log_person_investment)
                self._confirm_pressed = False #reset the variable state
                #self.emit(self.disable_signal) #GUI disabled
                self.emit(self.enable_components_gui_signal, False,  False, False, True) #GUI components
                #Updating the investment values
                self._log_round = float(self._log_round) - float(self._log_person_investment)
                self._log_multiplied_person_investment = self._log_person_investment * float(self._log_pmult)
                self._log_player_investment = self._log_multiplied_person_investment
                self._log_robot_investment = 0
                #total, player_investment, round_total, your_investment, robot_investment
                local_string = ""
                #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
                self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string)
                #The person turn is finished, now switching to robot turn
                #The robot looks to the monitor (thinking what to do)
                self.myPuppet.enable_face_tracking(False) #disable face tracking
                self.myPuppet.look_to(1, SPEED) #angle(radians) + speed
                self.STATE_MACHINE = 4 #next state
                time.sleep(1) #Sleep to evitate fast movements of the robot just after the answer

        #STATE-4 Pointing or not and gives the reward
        if self.STATE_MACHINE == 4:
            print "[4] Pointing/Non-Pointing"                         
            #Updating the investment values
            #check if nasty or not and floor or ceil the number
            self._log_multiplied_person_investment = self._log_person_investment * float(self._log_pmult)          
            self._log_robot_investment = float(self._log_multiplied_person_investment) * float(self._log_rmult)
            if self.myParser._nasty_list[self._log_trial] == "True":
                 self._log_robot_investment = math.floor(self._log_robot_investment)
            elif self.myParser._nasty_list[self._log_trial] == "False":
                 self._log_robot_investment = math.ceil(self._log_robot_investment)
            self._log_total = self._log_total + self._log_round + self._log_robot_investment
            self._log_player_investment = self._log_multiplied_person_investment
            #self._log_player_investment = self._log_robot_investment

            time.sleep(1)

            #Computing the values to use for movements and GUI update
            robot_slider_value = self._log_robot_investment
            energy_value = self._log_robot_investment
            energy_maximum = self._log_multiplied_person_investment #always integer
            energy_half = (self._log_multiplied_person_investment / 2)

            #Pointing (or not) while looking to the screen
            if self.myParser._pointing_list[self._log_trial] == "True":
              print "[4] pointing == True"
              self._log_pointing = "True"
              #If robot returns ZERO no arm movement
              if (energy_value == 0):
                  self.myPuppet.right_arm_pointing(False, SPEED)
                  self.myPuppet.left_arm_pointing(False, SPEED) 
              #if value is less than 15                 
              elif (energy_value > 0 and energy_value < energy_half):
                  self.myPuppet.left_arm_pointing(True, SPEED)
              #If value is 15: move left if NASTY otherwise move right
              elif (energy_value == int(energy_half) ):
                  if self.myParser._nasty_list[self._log_trial] == "True":
                      self.myPuppet.left_arm_pointing(True, SPEED)
                  elif self.myParser._nasty_list[self._log_trial] == "False":
                      self.myPuppet.right_arm_pointing(True, SPEED)
              #If value is more than 15 then move the right arm
              elif (energy_value > energy_half):
                  self.myPuppet.right_arm_pointing(True, SPEED)
              time.sleep(0.2)
            #If the condition is pointing==FALSE then does not move the arm
            elif self.myParser._pointing_list[self._log_trial] == "False":
              print "[4] pointing == False"
              self._log_pointing = "False"
              self.myPuppet.right_arm_pointing(False, SPEED)
              self.myPuppet.left_arm_pointing(False, SPEED)
              time.sleep(2.0) #Sleep to slow down the flow in the non-movement condition

            #Updating the GUI
            local_string = "You invested: " + str(self._log_person_investment) 
            local_string += "  Robot received: " + str(self._log_multiplied_person_investment) + "  Robot returned: " + str(self._log_robot_investment) + '\n'
            local_string += "In this round you made: " + str(self._log_round + self._log_robot_investment) + '\n' 
            local_string += "Total in your bank: " + str(self._log_total) + '\n\n'
            local_string += "Please press START to begin a new round..."
            #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
            self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round+ self._log_robot_investment, self._log_robot_investment, robot_slider_value, energy_value, energy_maximum, local_string)

            #Reset the arms
            time.sleep(0.5)
            self.myPuppet.right_arm_pointing(False, SPEED)
            self.myPuppet.left_arm_pointing(False, SPEED)

            #Looking (or not) the subject
            if self.myParser._gaze_list[self._log_trial] == "True":
              print "[2] looking == True"
              self._log_gaze = "True"
              self.myPuppet.look_to(0, SPEED) #angle(radians) + speed
              time.sleep(0.2)
              self.myPuppet.enable_face_tracking(True) #enables face tracking
            elif self.myParser._gaze_list[self._log_trial] == "False":
              print "[2] looking == False"
              self._log_gaze = "False"
              self.myPuppet.enable_face_tracking(False) #disable face tracking
              self.myPuppet.look_to(1, SPEED) #angle(radians) + speed

            #Change state
            time.sleep(0.5)
            self.STATE_MACHINE = 5 #next state        

        #STATE-5 Saving in the logbook
        if self.STATE_MACHINE == 5:
            print "[5] Saving the trial in the logbook"
            self.logger.AddLine(self._log_trial+1, self._log_person_investment, self._log_robot_investment, self._log_pmult, self._log_rmult, self._log_total, self._log_gaze, self._log_pointing, self._log_timer, self._log_mp3)
            print "[5] " + str(self._log_trial+1) + "," + str(self._log_person_investment) + "," + str(self._log_robot_investment) + "," + str(self._log_pmult) + "," + str(self._log_rmult) + "," + str(self._log_total) + "," + str(self._log_gaze) + "," + str(self._log_pointing) + "," + str(self._log_timer)+ "," + str(self._log_mp3)

            if self._log_trial+1 != self.myParser._size:
                self.STATE_MACHINE = 6 #cycling to state 6
                self.emit(self.enable_components_gui_signal, True,  False, False, False) #Enable the Start Button
                self._log_trial = self._log_trial + 1
            elif self._log_trial+1 == self.myParser._size:
                self.STATE_MACHINE = 7 #experiment finished               

        #STATE-6 Waiting for the subject pressing START
        if self.STATE_MACHINE == 6:
            if self._start_pressed == True: 
                self._start_pressed = False
                print "[6] Start pressed..."
                self.emit(self.enable_components_gui_signal, False,  False, False, False)
                self.STATE_MACHINE = 2 #cycling to state 2
                time.sleep(1)

        #STATE-7 Final state is called to shutdown the robot
        if self.STATE_MACHINE == 7:
            print "[7] The game is finished"
            self._xml_uploaded = False #reset status variable
            self._start_pressed = False
            self._log_trial = 0
            self.STATE_MACHINE = 0 #cycling to state 0
            #Updating the investment values (RESET)
            self._log_round = 10
            self._log_person_investment = 0
            self._log_robot_investment = 0
            self._log_player_investment = 0
            #total, player_investment, round_total, your_investment, robot_investment, robot_slider_value
            local_string = "The game is finished." + '\n\n' + "Thank you..."
            #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
            self.emit(self.update_gui_signal, self._log_total, self._log_player_investment, self._log_round, self._log_robot_investment, 15, 15, 30, local_string) 
            self.emit(self.enable_components_gui_signal, False,  False, False, False) #GUI components
            time.sleep(5)


  def start_experiment(self):
    self._start_pressed = True

  def confirm(self, person_investment, robot_investment):
    self._confirm_pressed = True
    self._log_person_investment = float(person_investment)
    self._log_robot_investment = float(robot_investment)

  def ip(self, ip_string, port_string):
    print "IP: " + str(ip_string) 

    try:
        self.myPuppet = nao.Puppet(ip_string, port_string, True)
        self.emit(self.yes_robot_signal)
        self._robot_connected=True
    except Exception,e:
        print "\nERROR: Impossible to find the robot!\n"
        print "Error was: ", e
        self.emit(self.no_robot_signal)
        self._robot_connected=False

  def xml(self, path):
    print("Looking for external files... ")
    if not os.path.isfile(str(path)):
            print("\n# ERROR: I cannot find the XML file. The programm will be stopped!\n")
            self._xml_uploaded = False
            return
    print("Initializing XML Parser... ")
    try:
        self.myParser.LoadFile(str(path))
        self.myParser.parse_experiment_list()
        self.myParser.parse_pretrial_list()
        file_existance = self.myParser.check_file_existence("../share/mp3/")
        if file_existance == True:
            self.emit(self.good_xml_signal)
            self._xml_uploaded = True
        elif file_existance == False:
            self.emit(self.bad_xml_signal)
            print("\n # ERROR: Some audio files do not exist. \n")
            self._xml_uploaded = False 
    except:
        self.emit(self.bad_xml_signal)
        print("\n # ERROR: Impossible to read the XML file! \n")
        self._xml_uploaded = False


  def wake(self, state):
        if state == True:
             self.myPuppet.wake_up()
        else:     
             self.myPuppet.rest()

  def face_tracking(self, state):
        self.myPuppet.enable_face_tracking(state)


  def session_info_update(self, info1, info2, info3):
      my_string = str(info1) + "," + str(info2) + "," + str(info3)
      print("SESSION INFO: ", info1, info2, info3)
      self._log_first_line = my_string
      self._session_info_given = True
        

  def stop(self):
    self.stopped = 1

  def __del__(self):
    self.wait()


## Class ExampleApp
#  
# It is a GUI class created in pyQT
# and receive signals from the GUI
#
class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.btnBrowse.clicked.connect(self.browse_folder)  # When the button is pressed execute browse_folder function
        #self.btnStartExperiment.clicked.connect(lambda: self.start_experiment(1))
        self.btnStartExperiment.clicked.connect(self.start_experiment)
        self.btnConfirm.clicked.connect(self.confirm_pressed)
        self.btnConnectToNao.clicked.connect(self.connect_pressed)
        self.btnWakeUp.clicked.connect(self.wake_up_pressed)
        self.btnRest.clicked.connect(self.rest_pressed)
        self.btnFaceTrackingEnable.clicked.connect(lambda:  self.face_tracking_pressed(True))
        self.btnFaceTrackingDisable.clicked.connect(lambda:  self.face_tracking_pressed(False))
        self.btnSessionInfoConfirm.clicked.connect(self.session_info_pressed)

        #Buttons investment
        self.pushButton_0.clicked.connect(lambda: self.confirm_pressed(0))
        self.pushButton_1.clicked.connect(lambda: self.confirm_pressed(1))
        self.pushButton_2.clicked.connect(lambda: self.confirm_pressed(2))
        self.pushButton_3.clicked.connect(lambda: self.confirm_pressed(3))
        self.pushButton_4.clicked.connect(lambda: self.confirm_pressed(4))
        self.pushButton_5.clicked.connect(lambda: self.confirm_pressed(5))
        self.pushButton_6.clicked.connect(lambda: self.confirm_pressed(6))
        self.pushButton_7.clicked.connect(lambda: self.confirm_pressed(7))
        self.pushButton_8.clicked.connect(lambda: self.confirm_pressed(8))
        self.pushButton_9.clicked.connect(lambda: self.confirm_pressed(9))
        self.pushButton_10.clicked.connect(lambda: self.confirm_pressed(10))


        #Signal to be sent to Thread
        self.start_signal = SIGNAL("start_signal")
        self.confirm_signal = SIGNAL("confirm_signal")
        self.xml_path_signal = SIGNAL("xml_path_signal")
        self.ip_signal = SIGNAL("ip_signal")
        self.wake_up_signal = SIGNAL("wake_up_signal")
        self.face_tracking_signal = SIGNAL("face_tracking_signal")
        self.session_info_signal = SIGNAL("session_info_signal")

        self.showMaximized()

    def start_experiment(self):
        self.emit(self.start_signal)
        #self.btnStartExperiment.hide() #hiding the start button

    def confirm_pressed(self, person_investment):
        #self.emit(self.confirm_signal, self.horizontalSlider.sliderPosition(), self.horizontalSliderRobot.sliderPosition())
        self.emit(self.confirm_signal, person_investment, self.horizontalSliderRobot.sliderPosition())
        print "CONFIRM: " + str(person_investment)

    def connect_pressed(self):
        ip_string = str(self.lineEditNaoIP.text())
        port_string = str(self.lineEditNaoPort.text())
        #print "IP: " + ip_string
        self.emit(self.ip_signal, ip_string, port_string)

    def face_tracking_pressed(self, state):
        self.emit(self.face_tracking_signal, state)

    def wake_up_pressed(self):
        self.emit(self.wake_up_signal, True)

    def rest_pressed(self):
        self.emit(self.wake_up_signal, False)

    def session_info_pressed(self):
        info1 = str(self.textEditSubjectNumber.toPlainText())
        info2 = str(self.textEditSessionNumber.toPlainText())
        info3 = str(self.textEditOther.toPlainText())
        self.emit(self.session_info_signal, info1, info2, info3)

    def show_start_btn(self, is_visible):
        if is_visible == True:
            self.btnStartExperiment.show()
        elif is_visible == False:        
            self.btnStartExperiment.hide()

    #start_btn, confirm_btn, person_slider, robot_slider, show_slider
    def enable_components_gui(self, start_btn, confirm_btn, person_slider, robot_slider, show_slider=False):
        if  start_btn == True:
            self.btnStartExperiment.show()
        elif  start_btn == False:        
            self.btnStartExperiment.hide()
        self.btnConfirm.setEnabled(robot_slider)
        #self.horizontalSlider.setEnabled(person_slider)
        self.horizontalSliderRobot.setEnabled(robot_slider)
        #Enabling the confirm buttons
        self.pushButton_0.setEnabled(confirm_btn)
        self.pushButton_1.setEnabled(confirm_btn)
        self.pushButton_2.setEnabled(confirm_btn)
        self.pushButton_3.setEnabled(confirm_btn)
        self.pushButton_4.setEnabled(confirm_btn)
        self.pushButton_5.setEnabled(confirm_btn)
        self.pushButton_6.setEnabled(confirm_btn)
        self.pushButton_7.setEnabled(confirm_btn)
        self.pushButton_8.setEnabled(confirm_btn)
        self.pushButton_9.setEnabled(confirm_btn)
        self.pushButton_10.setEnabled(confirm_btn)
        #Showing or not the slider
        if (show_slider == False):
            self.horizontalSliderRobot.hide()
        else:
            self.horizontalSliderRobot.show()

        if confirm_btn == True:
            #self.pushButton_0.setStyleSheet("background-color: green")
            self.pushButton_0.setStyleSheet("border-style: solid")
            self.pushButton_0.setStyleSheet("border-color: green")
        elif confirm_btn == False:
            #self.pushButton_0.setStyleSheet("background-color: red")
            self.pushButton_0.setStyleSheet("border-style: solid")
            self.pushButton_0.setStyleSheet("border-color: red")

    #total, pinv, round_tot, rinv, rslider, energy_value, max_energy, text
    def update_gui(self, total, player_investment, round_total,  robot_investment, robot_slider_value, energy_value, maximum_energy, text_label=""):
        self.lcdNumberTotal.display(float(total))
        self.lcdNumberPlayerInvestment.display(float(player_investment))
        self.lcdNumberRound.display(float(round_total))
        self.lcdNumberRobotInvestment.display(float(robot_investment))
        self.horizontalSliderRobot.setValue(robot_slider_value)
        #Setting the energy bar
        if(maximum_energy == 0):
            maximum_energy = 100
            energy_value = 0
        if(energy_value > maximum_energy):
            energy_value = maximum_energy        
        self.progressBar.setMaximum(maximum_energy) #First set the maximum, then set the value
        self.progressBar.setValue(energy_value)
        #Update the textEdit label
        self.textEdit.clear() #clear the textedit            
        self.textEdit.append(QtCore.QString(text_label))      


    def browse_folder(self):
        selected_file = QtGui.QFileDialog.getOpenFileName(self, "Select a configuration file", "../etc/xml","XML files(*.xml)")

        if selected_file: # if user didn't pick a directory don't continue
            self.textEditXML.setText(selected_file) # self.listWidget.addItem(selected_file)  # add file to the listWidget
            self.emit(self.xml_path_signal, selected_file)
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setWindowTitle("No file selected")
            msgBox.setText("ATTENTION: You did not select any XML file.");
            msgBox.exec_();

    def no_robot_error(self):
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setWindowTitle("Ops... Connection Error")
            msgBox.setText("ERROR: It was not possible to find the robot. \nFollow these tips and try to connect again. \n \n1- Check if the robot is running correctly. \n2- Check if the wifi router is running properly. \n3- Press the button on the robot chest to verify if the IP address is correct. \n4- Check if another software or GUI is connected to the robot. \n");
            msgBox.exec_();
            self.btnWakeUp.setEnabled(False)
            self.btnRest.setEnabled(False)
            self.btnFaceTrackingEnable.setEnabled(False)
            self.btnFaceTrackingDisable.setEnabled(False)

    def yes_robot_confirmation(self):
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Information)
            msgBox.setWindowTitle("Well Done!")
            msgBox.setText("I found the robot, the connection was successfully established!")
            msgBox.exec_();
            self.btnWakeUp.setEnabled(True)
            self.btnRest.setEnabled(True)
            self.btnFaceTrackingEnable.setEnabled(True)
            self.btnFaceTrackingDisable.setEnabled(True)

    def bad_xml_error(self):
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setWindowTitle("Ops... malformed XML file")
            msgBox.setText("ERROR: It was not possible to read the XML file. \nFollow these tips and try to select again. \n \n1- Verify if you can open correctly the file with a text editor (es. notepad). \n2- Once opened the file, check if for each open bracket <trial> there is a closed bracket </trial>. \n3- Check if the name of the audio files is correct.\n");
            msgBox.exec_();

    def good_xml_confirmation(self):
            msgBox = QtGui.QMessageBox()
            msgBox.setIcon(QtGui.QMessageBox.Information)
            msgBox.setWindowTitle("Very Good!")
            msgBox.setText("I opened the XML file correctly. Be carefull, this does not mean that what you write inside the file is correct...")
            msgBox.exec_();

def main():

    #New instance of QApplication
    app = QtGui.QApplication(sys.argv)  
    form = ExampleApp()

    #Creating the main thread
    thread = WorkerThread()

    #Connecting: form > thread
    thread.connect(form, form.start_signal, thread.start_experiment)
    thread.connect(form, form.xml_path_signal, thread.xml) #sending XML path
    thread.connect(form, form.confirm_signal, thread.confirm)
    thread.connect(form, form.ip_signal, thread.ip)
    thread.connect(form, form.wake_up_signal, thread.wake)
    thread.connect(form, form.face_tracking_signal, thread.face_tracking)
    thread.connect(form, form.session_info_signal, thread.session_info_update)

    #Connecting: thread > form
    form.connect(thread, thread.enable_components_gui_signal, form.enable_components_gui)
    #form.connect(thread, thread.disable_signal, form.disable_gui)
    #form.connect(thread, thread.enable_signal, form.enable_gui)
    form.connect(thread, thread.no_robot_signal, form.no_robot_error)
    form.connect(thread, thread.yes_robot_signal, form.yes_robot_confirmation)
    form.connect(thread, thread.bad_xml_signal, form.bad_xml_error)
    form.connect(thread, thread.good_xml_signal, form.good_xml_confirmation)
    form.connect(thread, thread.update_gui_signal, form.update_gui)
    form.connect(thread, thread.show_start_btn_signal, form.show_start_btn)

    #Starting thread
    thread.start()

    #Show the form and execute the app
    form.show()  
    app.exec_()  



if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function





