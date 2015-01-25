from pylab import *
import csv

def MovingAverage(values, window):

    # Here, we will just allow the default since it is an EMA
    a =  np.convolve(values, ones([window,])/window)[:len(values)]
    a[:window] = a[window]
    return a #again, as a numpy array.

def volData(Data,Window):
	Vol = array([std(Data[i-Window:i]) if i > Window else 0 for i in xrange(len(Data))])
	return Vol

File = file("test.csv","r")

Data = [[float(j) for j in i ] for i in csv.reader(File)]

Data = array(Data)

#plot(Data[:,2])

#plot(emaData(Data,15))

smData = MovingAverage(mean(abs(Data),1),15)
vData = volData(mean(abs(Data),1),15)
ratio = where(smData > 0, vData / smData, 0)

#plot(mean(abs(Data),1) - smData)

plot(smData - MovingAverage(smData,15))

show()



