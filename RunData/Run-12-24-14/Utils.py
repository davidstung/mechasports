import csv
from pylab import *

def LoadFile(fileName):
	File = file(fileName,"r")
	Reader = csv.reader(File)
	Date = []
	Time = []
	Latitude = []
	NS = []
	Longitude = []
	EW = []
	Altitude = []
	Speed = []
	[[Date.append(int(i[0])),Time.append(float(i[1])),Latitude.append(float(i[2])),NS.append(i[3]),Longitude.append(float(i[4])),EW.append(i[5]),Altitude.append(float(i[6])),Speed.append(float(i[7])*0.51444444444)] for i in Reader if len(i) == 8]
	Dict = {'date':array(Date),'time':array(Time),'lat':array(Latitude),'ns':NS,'lon':array(Longitude),'ew':EW,'alt':array(Altitude),'sp':array(Speed)}
	return Dict
	File.close()

def PlotVel(Dict):
	plot(Dict['sp'])
	show()

def MA(Data,Window):
	return array([mean(Data[i-Window:i]) if i > Window else Data[i] for i in xrange(len(Data))])

def SmoothVel(Dict):
	return MA(Dict['sp'],5)

def GetIntervals(Dict):
	Interval = zeros(shape(Dict['time']))
	Interval[1:] = mod(Dict['time'][1:]-Dict['time'][:-1],1)
	return Interval

def CalcDistance(Interval,Speed):
	return sum(Interval*Speed)

def GetSpeedStats(Speed):
	return [min(Speed),mean(Speed),max(Speed)]

def ClassifySpeeds(Speed,Interval):
	Range = zeros(80,)
	[ClassifySpeedHelper(Speed[i],Interval[i],Range) for i in xrange(len(Interval))]
	return Range

def ClassifySpeedHelper(Speed,Time,Range):
	Range[int(Speed/0.25)] = Range[int(Speed/0.25)] + Time


def ClassifyTransitions
