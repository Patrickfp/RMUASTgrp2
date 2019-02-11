#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2018 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

##### Insert initialize code below ###################

## Uncomment the file to read ##
#fileName = '../../rmuast_s19_materials_week_6/exercise_imu/imu_razor_data_static.txt'
fileName = '../../rmuast_s19_materials_week_6/exercise_imu/imu_razor_data_pitch_55deg.txt'
#fileName = '../../rmuast_s19_materials_week_6/exercise_imu/imu_razor_data_roll_65deg.txt'
#fileName = '../../rmuast_s19_materials_week_6/exercise_imu/imu_razor_data_yaw_90deg.txt'

## IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

## Variables for plotting ##
showPlot = True
plotData = []

## Initialize your variables here ##
count = 0
delta_time = 0
g_roll = 0
g_pitch = 0
g_yaw = 0
pitch = 0
roll = 0
prev_roll = 0
prev_pitch = 0
pp_pitch = 0
pp_roll = 0


######################################################

# import libraries
from math import pi, sqrt, atan2, atan
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

# open the imu data file
f = open (fileName, "r")

# initialize variables
count = 0


def butter_lowpass(cutoff, fs, order=5):
	nyq = 0.5 * fs
	normal_cutoff = cutoff / nyq
	b, a = butter(order, normal_cutoff, btype='low', analog=False)
	return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
	b, a = butter_lowpass(cutoff, fs, order=order)
	y = lfilter(b, a, data)
	return y

# looping through file

for line in f:
	count += 1

	# split the line into CSV formatted data
	line = line.replace ('*',',') # make the checkum another csv value
	csv = line.split(',')

	# keep track of the timestamps 
	ts_recv = float(csv[0])
	if count == 1: 
		ts_now = ts_recv # only the first time
	ts_prev = ts_now
	ts_now = ts_recv

	if imuType == 'sparkfun_razor':
		# import data from a SparkFun Razor IMU (SDU firmware)
		acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
		acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
		acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
		gyro_x = int(csv[5]) * 1/14.375 * pi/180.0;
		gyro_y = int(csv[6]) * 1/14.375 * pi/180.0;
		gyro_z = int(csv[7]) * 1/14.375 * pi/180.0;

	elif imuType == 'vectornav_vn100':
		# import data from a VectorNav VN-100 configured to output $VNQMR
		acc_x = float(csv[9])
		acc_y = float(csv[10])
		acc_z = float(csv[11])
		gyro_x = float(csv[12])
		gyro_y = float(csv[13])
		gyro_z = float(csv[14])
	 		
	##### Insert loop code below #########################

	# Variables available
	# ----------------------------------------------------
	# count		Current number of updates		
	# ts_prev	Time stamp at the previous update
	# ts_now	Time stamp at this update
	# acc_x		Acceleration measured along the x axis
	# acc_y		Acceleration measured along the y axis
	# acc_z		Acceleration measured along the z axis
	# gyro_x	Angular velocity measured about the x axis
	# gyro_y	Angular velocity measured about the y axis
	# gyro_z	Angular velocity measured about the z axis

	## Insert your code here ##
	## Insert your code here ##
	#GYRO:
	delta_time = ts_now - ts_prev
	g_roll = g_roll + gyro_y * delta_time
	g_pitch = g_pitch + gyro_x * delta_time
	g_yaw = g_yaw + gyro_z * delta_time

	#ACC:
	pp_pitch = prev_pitch
	pp_roll = prev_roll

	prev_pitch = pitch
	prev_roll = roll

	pitch = math.atan((acc_y)/math.sqrt(math.pow(acc_x,2)+math.pow(acc_z,2)))
	roll = math.atan((-(acc_x))/(acc_z))

	pitch = (pp_pitch + prev_pitch + pitch)/3
	roll = (pp_roll + prev_roll + roll)/3

	
	
	myValue = pitch # relevant for the first exercise, then change this.

	# in order to show a plot use this function to append your value to a list:
	plotData.append (myValue*180.0/pi)

	######################################################

# closing the file	
f.close()


# show the plot
if showPlot == True:
	plt.plot(butter_lowpass_filter(plotData,3,100,3))
	#plt.plot(plotData)
	#plt.savefig('imu_exercise_plot.png')
	plt.show()


