from pylab import *
import csv

def corrData(Data,Window):
        Corr = array([corrcoef(Data[i-Window*2:i-Window],Data[i-Window:i])[0,1] if i > Window*2 else 0 for i in xrange(len(Data))])
        return Corr

def corr2Data(Data,Data2,Window):
	Corr = array([corrcoef(Data[i-Window:i],Data2[i-Window:i])[0,1] if i > Window else 0 for i in xrange(len(Data))])
	return Corr

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

smData = MovingAverage(Data[:,2],15)

sm2Data = smData - MovingAverage(smData,15)

smData = MovingAverage(Data[:,1],15)

sm1Data = smData - MovingAverage(smData,15)

smData = MovingAverage(Data[:,0],15)

sm0Data = smData - MovingAverage(smData,15)

corr02 = corr2Data(sm0Data,sm2Data,45)
corr01 = corr2Data(sm0Data,sm1Data,45)
corr12 = corr2Data(sm1Data,sm2Data,45)

#plot(corr02)
#plot(corr01)
plot(corr12)
show()



