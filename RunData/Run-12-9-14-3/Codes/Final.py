from pylab import *

import csv

def MovingAverage(values, window):

    # Here, we will just allow the default since it is an EMA
    a =  np.convolve(values, ones([window,])/window)[:len(values)]
    a[:window] = a[window]
    return a #again, as a numpy array.

def ParabolicSmooth(values, rad):
	g = lambda x:1-x**2
	weights = array([g(i) for i in [-0.66,-0.33,1,0.33,0.66]])
	a = np.convolve(values,weights/sum(weights))
	a[:5] = a[5]
	return a

def Extrema(Data):
        Arr1  = zeros(len(Data))
        Chg = zeros(len(Data))
        Last = 0
        Extr = []
        Min = []
        Max = []
	Rad = 5
	Type = 0
        for i in range(Rad,len(Data) - Rad):
                if Data[i] < Data[i-Rad] and Data[i+Rad] > Data[i] and Data[i] < 0.5*(Data[i-1] + Data[i+1]) and Type <> 1 and sign(Data[i+1]-Data[i]) + sign(Data[i] - Data[i-1]) == 0:
                        Arr1[i] = Data[i]
                        Last = i
                        Extr.append(Data[i])
                        Min.append(Data[i])
			Type = 1
                elif Data[i] > Data[i-Rad] and Data[i+Rad] < Data[i] and Data[i]> 0.5*(Data[i-1] + Data[i+1]) and Type <> 2  and sign(Data[i+1]-Data[i]) + sign(Data[i] - Data[i-1]) == 0:
                        Arr1[i] = Data[i]
                        Last = i
                        Extr.append(Data[i])
                        Max.append(Data[i])
			Type = 2

        return Arr1

File = file("test.csv","r")

Data = [[float(j) for j in i ] for i in csv.reader(File)]

Data = array(Data)

smData = MovingAverage(Data[:,2],15)

smData = ParabolicSmooth(smData,5)

sm2Data = smData - MovingAverage(smData,15)

#sm2Data = sm2Data - MovingAverage(sm2Data,15)

Arr1 = Extrema(sm2Data)

plot(sm2Data)
plot(Arr1,'*')

show()





