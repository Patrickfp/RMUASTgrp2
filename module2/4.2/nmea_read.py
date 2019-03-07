#!/usr/bin/python
#/****************************************************************************
# nmea read function
# Copyright (c) 2018, Kjeld Jensen <kj@kjen.dk>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************/
'''
2018-03-13 Kjeld First version, that reads in CSV data
'''

#from utm import utmconv
import matplotlib as mpl
from exportkml import kmlclass
import matplotlib.path as mpath
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class nmea_class:
  def __init__(self):
    self.data = []

  def import_file(self, file_name):
    file_ok = True
    try:
      # read all lines from the file and strip \n
      lines = [line.rstrip() for line in open(file_name)]
    except:
      file_ok = False
    if file_ok == True:
      pt_num = 0
      for i in range(len(lines)): # for all lines
        if len(lines[i]) > 0 and lines[i][0] != '#': # if not a comment or empty line
          csv = lines[i].split (',') # split into comma separated list
          self.data.append(csv)

  def print_data(self):
    for i in range(len(self.data)):
      print self.data[i]


if __name__ == "__main__":
    #read_file = 'nmea_trimble_gnss_eduquad_flight.txt'
    read_file = 'nmea_ublox_neo_24h_static.txt'


    print 'Importing file'
    nmea = nmea_class()
    nmea.import_file (read_file)

    MSL = []
    NrOfSatellites = []
    GNSSAccuracy = []
    timeSplitted = []
    longitude = []
    lattitude = []
    timeSplitted = []
    time_in_seconds = []
    start_time = 0.0
    temp_time = 0.0
    splitedcord = []
    tempcord = 0

    kml = kmlclass()
    kml.begin('DroneTrack.kml','Drone track','Creating of the track of the drone', 0.1)
    kml.trksegbegin('','','red','absolute')


    for i in range(len(nmea.data)-1):   #len(nmea.data)-1
        if(nmea.data[i][0] != '$GPGGA'):
            continue
        if(len(nmea.data[i][1]) < 1 or len(nmea.data[i][2]) < 1):
            continue

        for t in str(nmea.data[i][1]):
            if t != ".":
                timeSplitted.append(float(t))
        temp_time = ((timeSplitted[0]*10) + (timeSplitted[1])) * 3600
        temp_time += ((timeSplitted[2]*10) + (timeSplitted[3])) * 60
        temp_time += timeSplitted[4]*10
        temp_time += timeSplitted[5]
        temp_time += timeSplitted[6]*0.1
        temp_time += timeSplitted[7]*0.01
        timeSplitted[:] = []
        if(i == 0):
            start_time = temp_time

        time_in_seconds.append((temp_time - start_time))

        for elem1 in str(nmea.data[i][2]):
            if elem1 != ".":
                splitedcord.append(float(elem1))
        tempcord = splitedcord[0]*10.0 + splitedcord[1]
        tempcord += (splitedcord[2]*10.0 + splitedcord[3])/60.0
        tempcord += (splitedcord[4]*0.10 + splitedcord[5]*0.01)/60.0
        tempcord += (splitedcord[6]*0.001 + splitedcord[7]*0.0001)/60.0
        #tempcord += (splitedcord[8]*0.00001 + splitedcord[9]*0.000001)/60.0
        lattitude.append(tempcord)
        splitedcord[:] = []

        for elem2 in str(nmea.data[i][4]):
            if elem2 != ".":
                splitedcord.append(float(elem2))
        tempcord2 = splitedcord[1]*10.0 + splitedcord[2]
        tempcord2 += (splitedcord[3]*10.0 + splitedcord[4])/60.0
        tempcord2 += (splitedcord[5]*0.10 + splitedcord[6]*0.01)/60.0
        tempcord2 += (splitedcord[7]*0.001 + splitedcord[8]*0.0001)/60.0
        #tempcord += (splitedcord[9]*0.00001 + splitedcord[10]*0.000001)/60.0
        longitude.append(tempcord2)
        splitedcord[:] = []

        NrOfSatellites.append(float(nmea.data[i][7]))
        GNSSAccuracy.append(float(nmea.data[i][8]))
        MSL.append(float(nmea.data[i][9]))

        kml.trkpt(tempcord, tempcord2, float(nmea.data[i][9]))

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(17, 10))

    axes[0].set_title("Altitude")
    axes[0].plot(time_in_seconds, MSL, color='C0')
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Amplitude")

    axes[1].set_title("Satellites ")
    axes[1].plot(time_in_seconds, NrOfSatellites, color='C1')
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Satellites in use")

    fig.tight_layout()
    #plt.show()
    plt.savefig("att-MLS-fig")
    plt.close()

    kml.trksegend()
    kml.end()






















#end
