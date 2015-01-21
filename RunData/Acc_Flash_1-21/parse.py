from pylab import *
from csv import reader

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

subplot(2,2,1) 
plot(mag1)

subplot(2,2,2) 
plot(mag2)

subplot(2,2,3) 
plot(mag3)

subplot(2,2,4) 
plot(mag4)

show()

lp1 = array([mean(mag1[i-50:i]) for i in range(50,len(mag1))])
lp2 = array([mean(mag2[i-50:i]) for i in range(50,len(mag2))])
lp3 = array([mean(mag3[i-50:i]) for i in range(50,len(mag3))])
lp4 = array([mean(mag4[i-50:i]) for i in range(50,len(mag4))])

subplot(2,2,1)
plot(lp1)

subplot(2,2,2)
plot(lp2)

subplot(2,2,3)
plot(lp3)

subplot(2,2,4)
plot(lp4)

show()

hp1 = array([mean(mag1[i-50:i]) for i in range(50,len(mag1))])
hp2 = array([mean(mag2[i-50:i]) for i in range(50,len(mag2))])
hp3 = array([mean(mag3[i-50:i]) for i in range(50,len(mag3))])
hp4 = array([mean(mag4[i-50:i]) for i in range(50,len(mag4))])

subplot(2,2,1)
plot(hp1)

subplot(2,2,2)
plot(hp2)

subplot(2,2,3)
plot(hp3)

subplot(2,2,4)
plot(hp4)

show()








