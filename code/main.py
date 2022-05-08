# -*- coding:utf-8 -*-

import time
import l76x
import time
import math

'''
uart_print = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
#uart_print = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
StandBy = Pin(17,Pin.OUT)
StandBy.value(0)
ForceOn = Pin(14,Pin.OUT)
ForceOn.value(0)
rxData = bytes()

while True:
    while uart_print.any() > 0:
        rxData += uart_print.read(1)
    print(rxData.decode('utf-8'))
'''

x=l76x.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_400MS);

#Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT);

time.sleep(2)
x.L76X_Exit_BackupMode();
x.L76X_Send_Command(x.SET_SYNC_PPS_NMEA_ON)

#x.L76X_Send_Command(x.SET_STANDBY_MODE)
#time.sleep(10)
#x.L76X_Send_Command(x.SET_NORMAL_MODE)
#x.config.StandBy.value(1)h

# File for storing GPS coordinates
f = open('GPSData.csv','w')
f.write("GPShr,GPSmin,GPSsec,latitude,longitude\n")

try:
    while(1):
        x.L76X_Gat_GNRMC()
        print ('Time %d: %d : %d'%(x.Time_H,x.Time_M,x.Time_S))

        if(x.Status == 1):
            print ('Already positioned hi')

            print ('Lon = %f  Lat = %f'%(x.Lon,x.Lat))
            x.L76X_Baidu_Coordinates(x.Lat, x.Lon)
            print ('Baidu coordinate %f ,%f'%(x.Lat_Baidu,x.Lon_Baidu))
            x.L76X_Google_Coordinates(x.Lat,x.Lon)
            print ('Google coordinate %f ,%f'%(x.Lon_Google,x.Lat_Google))

            # Write GPS data to file
            GPShr =  str(x.Time_H)
            GPSmin = str(x.Time_M)
            GPSsec = str(x.Time_S)
            lat = str(x.Lat_Google)
            lon = str(x.Lon_Google)
            f.write(GPShr + ',' + GPSmin + ',' + GPSsec + ',' + lat + ',' + lon + '\n')

        else:
            print ('No positioning')
            # Write GPS data to file
            GPShr =  str(x.Time_H)
            GPSmin = str(x.Time_M)
            GPSsec = str(x.Time_S)
            lat = str(x.Lat_Google)
            lon = str(x.Lon_Google)
            f.write(GPShr + ',' + GPSmin + ',' + GPSsec + ',' + lat + ',' + lon + '\n')

        time.sleep(5)

except (KeyboardInterrupt, SystemExit): #when press ctrl+c
    print("Done.\nExiting.")
    f.close()
