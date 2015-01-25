from pylab import *
from csv import reader
from scipy import stats

def PeakFind(Data):
	Peaks = [i for i in xrange(len(Data) - 5) if Data[i] > Data[i-5] and Data[i] > Data[i-4] and Data[i] > Data[i-3] and Data[i] > Data[i-2] and Data[i] > Data[i-1] and Data[i] > Data[i+5] and Data[i] > Data[i+4] and Data[i] > Data[i+3] and Data[i] > Data[i+2] and Data[i] > Data[i+1] ]
	Peaks = array(Peaks)
	if len(Peaks) > 1:
		return mean(Peaks[1:]-Peaks[:-1])
	else:
		return NaN

def TrufFind(Data):
        Trufs = [i for i in xrange(len(Data) - 5) if Data[i] < Data[i-5] and Data[i] < Data[i-4] and Data[i] < Data[i-3] and Data[i] < Data[i-2] and Data[i] < Data[i-1] and Data[i] < Data[i+5] and Data[i] < Data[i+4] and Data[i] < Data[i+3] and Data[i] < Data[i+2] and Data[i] < Data[i+1] ]
        Trufs = array(Trufs)
        if len(Trufs) > 1:
                return mean(Trufs[1:]-Trufs[:-1])
        else:
                return NaN

data1 = array([[float(j) for j in i] for i in reader(file("run1.csv","r"))])
data2 = array([[float(j) for j in i] for i in reader(file("run2.csv","r"))])
data3 = array([[float(j) for j in i] for i in reader(file("run3.csv","r"))])
data4 = array([[float(j) for j in i] for i in reader(file("run4.csv","r"))])

data1 = data1[:,:3]
data2 = data2[:,:3]
data3 = data3[:,:3]
data4 = data4[:,:3]

mag1 = sqrt(data1[:,0]**2+data1[:,1]**2+data1[:,2]**2)
mag2 = sqrt(data2[:,0]**2+data2[:,1]**2+data2[:,2]**2)
mag3 = sqrt(data3[:,0]**2+data3[:,1]**2+data3[:,2]**2)
mag4 = sqrt(data4[:,0]**2+data4[:,1]**2+data4[:,2]**2)

lp1 = array([mean(mag1[i-50:i]) for i in range(50,len(mag1))])
lp2 = array([mean(mag2[i-50:i]) for i in range(50,len(mag2))])
lp3 = array([mean(mag3[i-50:i]) for i in range(50,len(mag3))])
lp4 = array([mean(mag4[i-50:i]) for i in range(50,len(mag4))])

hp1 = array([mag1[i]-mean(mag1[i-50:i]) for i in range(50,len(mag1))])
hp2 = array([mag2[i]-mean(mag2[i-50:i]) for i in range(50,len(mag2))])
hp3 = array([mag3[i]-mean(mag3[i-50:i]) for i in range(50,len(mag3))])
hp4 = array([mag4[i]-mean(mag4[i-50:i]) for i in range(50,len(mag4))])

hm1 = array([mean(hp1[i-50:i]) for i in range(50,len(hp1))])
hm2 = array([mean(hp2[i-50:i]) for i in range(50,len(hp2))])
hm3 = array([mean(hp3[i-50:i]) for i in range(50,len(hp3))])
hm4 = array([mean(hp4[i-50:i]) for i in range(50,len(hp4))])

hm1 = array([mean(hp1[i-50:i]) for i in range(50,len(hp1))])
hm2 = array([mean(hp2[i-50:i]) for i in range(50,len(hp2))])
hm3 = array([mean(hp3[i-50:i]) for i in range(50,len(hp3))])
hm4 = array([mean(hp4[i-50:i]) for i in range(50,len(hp4))])

hs1 = array([std(hp1[i-50:i]) for i in range(50,len(hp1))])
hs2 = array([std(hp2[i-50:i]) for i in range(50,len(hp2))])
hs3 = array([std(hp3[i-50:i]) for i in range(50,len(hp3))])
hs4 = array([std(hp4[i-50:i]) for i in range(50,len(hp4))])

m1 = array([max(mag1[i-50:i]) for i in range(50,len(mag1))])
m2 = array([max(mag2[i-50:i]) for i in range(50,len(mag2))])
m3 = array([max(mag3[i-50:i]) for i in range(50,len(mag3))])
m4 = array([max(mag4[i-50:i]) for i in range(50,len(mag4))])

hpm1 = array([max(hp1[i-50:i]) for i in range(50,len(hp1))])
hpm2 = array([max(hp2[i-50:i]) for i in range(50,len(hp2))])
hpm3 = array([max(hp3[i-50:i]) for i in range(50,len(hp3))])
hpm4 = array([max(hp4[i-50:i]) for i in range(50,len(hp4))])

hpn1 = array([min(hp1[i-50:i]) for i in range(50,len(hp1))])
hpn2 = array([min(hp2[i-50:i]) for i in range(50,len(hp2))])
hpn3 = array([min(hp3[i-50:i]) for i in range(50,len(hp3))])
hpn4 = array([min(hp4[i-50:i]) for i in range(50,len(hp4))])

hms1 = array([std(hm1[i-50:i]) for i in range(50,len(hm1))])
hms2 = array([std(hm2[i-50:i]) for i in range(50,len(hm2))])
hms3 = array([std(hm3[i-50:i]) for i in range(50,len(hm3))])
hms4 = array([std(hm4[i-50:i]) for i in range(50,len(hm4))])

hmk1 = array([stats.kurtosis(hm1[i-50:i]) for i in range(50,len(hm1))])
hmk2 = array([stats.kurtosis(hm2[i-50:i]) for i in range(50,len(hm1))])
hmk3 = array([stats.kurtosis(hm3[i-50:i]) for i in range(50,len(hm1))])
hmk4 = array([stats.kurtosis(hm4[i-50:i]) for i in range(50,len(hm1))])

hpp1 = array([PeakFind(hp1[i-50:i]) for i in range(50,len(hp1))])
hpp2 = array([PeakFind(hp2[i-50:i]) for i in range(50,len(hp2))])
hpp3 = array([PeakFind(hp3[i-50:i]) for i in range(50,len(hp3))])
hpp4 = array([PeakFind(hp4[i-50:i]) for i in range(50,len(hp4))])

hpt1 = array([TrufFind(hp1[i-50:i]) for i in range(50,len(hp1))])
hpt2 = array([TrufFind(hp2[i-50:i]) for i in range(50,len(hp2))])
hpt3 = array([TrufFind(hp3[i-50:i]) for i in range(50,len(hp3))])
hpt4 = array([TrufFind(hp4[i-50:i]) for i in range(50,len(hp4))])


subplot(2,2,1)
plot(hp1[50:])
plot(hpt1[50:])

subplot(2,2,2)
plot(hp2)
plot(hpt2[50:])

subplot(2,2,3)
plot(hp3)
plot(hpt3[50:])

subplot(2,2,4)
plot(hp4)
plot(hpt4[50:])

show()



