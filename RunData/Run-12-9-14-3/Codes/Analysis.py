from pylab import *
import csv

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()

    # Here, we will just allow the default since it is an EMA
    a =  np.convolve(values, weights)[:len(values)]
    a[:window] = a[window]
    return a #again, as a numpy array.

def emaData(Data,window):
	EMA = zeros(shape(Data))
	EMA[:,0] = ExpMovingAverage(Data[:,0],window)
	EMA[:,1] = ExpMovingAverage(Data[:,1],window)
	EMA[:,2] = ExpMovingAverage(Data[:,2],window)
	return EMA

def volData(Data,Window):
	Vol = array([std(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])
	return Vol


def Extrema(Data):
	Arr1  = zeros(len(Data))
	Chg = zeros(len(Data))
	Last = 0
	Extr = []
	Min = []
	Max = []
	for i in range(2,len(Data) - 2):
		if Data[i] < Data[i-2] and Data[i+2] > Data[i] and std(Data[Last:i]) > 0.02*Data[i]:
			Arr1[i] = Data[i]
			Last = i
			Extr.append(Data[i])
			Min.append(Data[i])
		elif Data[i] > Data[i-2] and Data[i+2] < Data[i] and std(Data[Last:i]) > 0.02*Data[i]:
			Arr1[i] = Data[i]
			Last = i
			Extr.append(Data[i])
			Max.append(Data[i])
		if len(Extr) > 15 and abs((Extr[-1] - mean(array(Extr[-15:-1])))/std(array(Extr[-15:-1]))) > 2:
			Chg[i] = Data[i]
	return Arr1,Chg

File = file("test.csv","r")

Data = [[float(j) for j in i ] for i in csv.reader(File)]

Data = array(Data)

#plot(Data[:,2])

#plot(emaData(Data,15))

smData = emaData(Data,15)
smData = abs(smData)
msmData = mean(smData,1)
Arr1,Chg = Extrema(msmData)

plot(msmData)
plot(Arr1,'*')
plot(Chg,'*')

show()

Vol = volData(msmData,25)
oMicron = volData(Vol,25)
plot(Vol)
plot(oMicron)

Arr1,Chg = Extrema(Vol)

plot(Arr1,'*')
plot(Chg,'*')
show()

plot(where(Arr1[:-10] > 0, Arr1[10:]/Arr1[:-10]-1, 0))
show()



