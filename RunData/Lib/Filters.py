from pylab import *
from csv import reader
import os

def LoadData(Dir1,Directory,File):
	Path = "/Users/samirpatel/Documents/Fitbit/mechasports/RunData/"+Dir1+"/"+Directory+"/"+File+".csv"
	File = file(Path,"r")
	Data = array([[float(j) for j in i] for i in reader(File)])
	File.close()
	return Data	

def ClearPics(Folder):
	Path = "/Users/samirpatel/Documents/Fitbit/mechasports/RunData/RunPics/"+Folder+"/"
	Files = os.listdir(Path)
	for File in Files:
		if "csv" in File:
			os.remove(Path+File)

def MA(Data,Window):
	return array([mean(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])

def nMA(Data,Window):
	return array([mean(Data[i-Window:i,:],0) if i > Window else 0 for i in xrange(len(Data))])

def eMA(Data,Window):
	Values = []
	Strength = 2.0/(1+Window)
	[Values.append(Values[-1]*(1-Strength)+Data[i]*Strength) if i > Window else Values.append(mean(Data[:i])) for i in xrange(len(Data))]
	return array(Values)

def HPMA(Data,Window):
	LP = MA(Data,Window)
	return Data-LP

def HPnMA(Data,Window):
	LP = nMA(Data,Window)
	return Data-LP

def HPeMA(Data,Window):
        LP = MA(Data,Window)
        return Data-LP


def Mag(Data):
	Cols = shape(Data)[1]
	Result = zeros(shape(Data[:,0]))
	for i in xrange(Cols):
		Result = Result + Data[:,i]**2
	return sqrt(Result)

def Integrate(Data,dt,Window):
	return array([(sum(Data[i-Window:i-1])+sum(Data[i-Window+1:i]))*0.5*dt if i > Window else 0 for i in xrange(len(Data))])

def RollStdMean(Data,Window):
	return array([mean(Data[i-Window:i])/std(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])

def RollMean(Data,Window):
        return array([mean(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])

def RollStd(Data,Window):
        return array([std(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])

def PeakFind(Data):
        Peaks = [Data[i] for i in xrange(len(Data) - 5) if Data[i] >= Data[i-5] and Data[i] >= Data[i-4] and Data[i] >= Data[i-3] and Data[i] >= Data[i-2] and Data[i] >= Data[i-1] and Data[i] >= Data[i+5] and Data[i] >= Data[i+4] and Data[i] >= Data[i+3] and Data[i] >= Data[i+2] and Data[i] >= Data[i+1] ]
        Peaks = array(Peaks)
        if len(Peaks) > 0:
                return mean(Peaks)
        else:
                return Data[-1]

def TrufFind(Data):
        Trufs = [Data[i] for i in xrange(len(Data) - 5) if Data[i] <= Data[i-5] and Data[i] <= Data[i-4] and Data[i] <= Data[i-3] and Data[i] <= Data[i-2] and Data[i] <= Data[i-1] and Data[i] <= Data[i+5] and Data[i] <= Data[i+4] and Data[i] <= Data[i+3] and Data[i] <= Data[i+2] and Data[i] <= Data[i+1] ]
        Trufs = array(Trufs)
        if len(Trufs) > 0:
                return mean(Trufs)
        else:
                return Data[-1]

def MaxSearch(Data,Window):
	return array([PeakFind(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])

def MinSearch(Data,Window):
	return array([TrufFind(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])



 
