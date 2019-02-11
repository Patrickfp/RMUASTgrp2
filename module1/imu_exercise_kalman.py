#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2017 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

# import libraries
import math
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
from pylab import ion
#from imu_box3d import imu_visualize

# name of the file to read ##
fileName = '../../rmuast_s19_materials_week_6/exercise_imu/imu_razor_data_pitch_55deg.txt'

## IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

# other parameters
showPlot = True
show3DLiveView = False
show3DLiveViewInterval = 3

##### Insert initialize code below ###################

# approx. bias values determined by averaging over static measurements
bias_gyro_x = 0.0 # [rad/measurement]
bias_gyro_y = 0.0 # [rad/measurement]
bias_gyro_z = 0.0 # [rad/measurement]

# variances
gyroVar_x = 0
gyroVar_y = 0
gyroVar_z = 0
pitchVar = 0

# Kalman filter start guess
estAngle_x = -pi/4.0
estAngle_y = -pi/4.0
estAngle_z = -pi/4.0
estVar_x = pi
estVar_y = pi
estVar_z = pi

# Kalman filter housekeeping variables
gyroVarAcc_x = 0
gyroVarAcc_y = 0
gyroVarAcc_z = 0

######################################################

## Variables for plotting ##
plotDataGyro = []
plotDataAcc = []
plotDataKalman = []

## Initialize your variables here ##
gyro_x_rel = 0.0
gyro_y_rel = 0.0
gyro_z_rel = 0.0

# open the imu data file
f = open (fileName, "r")

# initialize variables
count = 0
delta_time = 0
gyro_x = 0
gyro_y = 0
gyro_z = 0
pitch = 0
roll = 0
acc_x = 0
acc_y = 0
acc_z = 0
pred_angle_x = 0
pred_angle_y = 0
pred_angle_z = 0
pred_var_x = 0
pred_var_y = 0
pred_var_z = 0
kx = 0
ky = 0
kz = 0
corrVar_x = 0
corrVar_y = 0
corrVar_z = 0
corrAngle_x = 0
corrAngle_y = 0
corrAngle_z = 0

# initialize 3D liveview
if show3DLiveView == True:
	imuview = imu_visualize()
	imuview.set_axis (0, 0, 0)
	imuview.update()

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
		# outputs ENU reference system
		acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
		acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
		acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
		gyro_x = int(csv[5]) * 1/14.375 * pi/180.0;
		gyro_y = int(csv[6]) * 1/14.375 * pi/180.0;
		gyro_z = int(csv[7]) * 1/14.375 * pi/180.0;

	elif imuType == 'vectornav_vn100':
		# import data from a VectorNav VN-100 configured to output $VNQMR
		# outputs NED reference system (therefore converted to ENU)
		acc_y = float(csv[9])
		acc_x = float(csv[10])
		acc_z = -float(csv[11])
		gyro_y = float(csv[12])
		gyro_x = float(csv[13])
		gyro_z = -float(csv[14])

	# subtract defined static bias for each gyro
	gyro_x -= bias_gyro_x
	gyro_y -= bias_gyro_y
	gyro_z -= bias_gyro_z

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

	# calculate pitch (x-axis) and roll (y-axis) angles
	pitch = math.atan((acc_y)/math.sqrt(math.pow(acc_x,2)+math.pow(acc_z,2)))
	roll = math.atan((-(acc_x))/(acc_z))

	# integrate gyro velocities to releative angles
	delta_time = ts_now - ts_prev

	gyro_x_rel += gyro_x * delta_time
	#gyro_y_rel += gyro_y * delta_time
	#gyro_z_rel += gyro_z * delta_time

	# Kalman prediction step (we have new data in each iteration)

	pred_angle_x = estAngle_x + gyro_x_rel
	#pred_angle_y = estAngle_y + gyro_y_rel
	#pred_angle_z = estAngle_z + gyro_z_rel

	gyroVarAcc_x += gyroVar_x
	#gyroVarAcc_y += gyroVar_y
	#gyroVarAcc_z += gyroVar_z

	pred_var_x = estVar_x + gyroVarAcc_x * delta_time
	#pred_var_y = estVar_y + gyroVarAcc_y * delta_time
	#pred_var_z = estVar_z + gyroVarAcc_z * delta_time

	estAngle_x = pred_angle_x
	#estAngle_y = pred_angle_y
	#estAngle_z = pred_angle_z

	estVar_x = pred_var_x
	#estVar_y = pred_var_y
	#estVar_z = pred_var_z



	# Kalman correction step (we have new data in each iteration)

	kx = (pred_var_x)/((pred_var_x)+(acc_x))
	#ky = (pred_var_y)/((pred_var_y)+(acc_y))
	#kz = (pred_var_z)/((pred_var_z)+(acc_z))

	corrAngle_x = pred_angle_x + kx * ((acc_x)-(pred_angle_x))
	#corrAngle_y = pred_angle_y + ky * ((acc_y)-(pred_angle_y))
	#corrAngle_z = pred_angle_z + kz * ((acc_z)-(pred_angle_z))

	corrVar_x = pred_var_x * (1-kx)
	#corrVar_y = pred_var_y * (1-ky)
	#corrVar_z = pred_var_z * (1-kz)

	estAngle_x = corrAngle_x
	#estAngle_y = corrAngle_y
	#estAngle_z = corrAngle_z

	estVar_x = corrVar_x
	#estVar_y = corrVar_y
	#estVar_z = corrVar_z

	gyroVarAcc_x = 0
	gyroVarAcc_y = 0
	gyroVarAcc_z = 0

	# define which value to plot as the Kalman filter estimate
	kalman_estimate = estAngle_x

	# define which value to plot as the absolute value (pitch/roll)
	pitch_roll_plot = pitch

	# define which value to plot as the relative gyro value
	gyro_rel_plot = gyro_x_rel

	######################################################

	# if 3D liveview is enabled
#	if show3DLiveView == True and count % show3DLiveViewInterval == 0:
#
#		# determine what variables to liveview
#		roll_view = 0.0
#		yaw_view = 0.0
#		pitch_view = kalman_estimate
#
#		imuview.set_axis (-pitch_view, -yaw_view, roll_view)
#		imuview.update()

	# if plotting is enabled
#	if showPlot == True:
#		plotDataGyro.append(gyro_rel_plot*180.0/pi)
#		plotDataAcc.append(pitch_roll_plot*180.0/pi)
#		plotDataKalman.append(kalman_estimate*180.0/pi)

# closing the file
f.close()

# show the plot
if showPlot == True:
	ion()
	plt.figure(1)
	plt.title('Gyro integrated (relative) angle')
	plt.plot(plotDataGyro)
	plt.savefig('imu_exercise_gyro.png')

	plt.figure(2)
	plt.title('Accelerometer (blue) & Kalman estimation (red) angles')
	plt.plot(plotDataAcc,'blue')
	plt.plot(plotDataKalman,'red')
	plt.savefig('imu_exercise_acc_kalman.png')
	plt.draw()
	print ('Press enter to quit')
	#raw_input()

