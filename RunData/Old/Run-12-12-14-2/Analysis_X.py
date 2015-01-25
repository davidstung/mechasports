from pylab import *
import sys
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
        Extr = []
        Min = []
        Max = []
	Time = []
	Rad = 5
	Type = 0
	Class = []
	Last = len(Extr)
        for i in range(Rad,len(Data) - Rad):
                if Data[i] < Data[i-Rad] and Data[i+Rad] > Data[i] and Data[i] < 0.5*(Data[i-1] + Data[i+1]) and Type <> 1 and sign(Data[i+1]-Data[i]) + sign(Data[i] - Data[i-1]) == 0:
                        Arr1[i] = Data[i]
                        Extr.append(Data[i])
			Time.append(i)
			Type = 1
			Class.append(1)
                elif Data[i] > Data[i-Rad] and Data[i+Rad] < Data[i] and Data[i]> 0.5*(Data[i-1] + Data[i+1]) and Type <> 2  and sign(Data[i+1]-Data[i]) + sign(Data[i] - Data[i-1]) == 0:
                        Arr1[i] = Data[i]
                        Extr.append(Data[i])
			Time.append(i)
			Type = 2
			Class.append(2)
		if len(Extr) > Last and len(Extr) >= 5:
			if CheckJump(Extr[-5:],Time[-5:],Class[-5:]) == True:
				print "jumped at " + str(i)
				print Extr[-5:]
				print array(Time[-4:]) - array(Time[-5:-1])
				Extr = Extr[-1:]
				Time = Time[-1:]
				Class = Class[-1:]
				Arr1[i] = 20000
		if len(Extr) > Last and len(Extr) >= 4:
			if CheckWalk(Extr[-4:],Time[-4:],Class[-4:]) == True:
				print "walked at " + str(i)
				print Extr[-4:]
				print array(Time[-3:]) - array(Time[-4:-1])
				Extr = Extr[-1:]
				Time = Time[-1:]
				Class = Class[-1:]
				Arr1[i] = 10000
		if len(Extr) > Last and len(Extr) >= 3:
			if CheckRun(Extr[-3:],Time[-3:],Class[-3:]) == True:
				print "ran at " + str(i)
				print Extr[-4:]
				print array(Time[-3:])
				Extr = Extr[-1:]
				Time = Time[-1:]
				Class = Class[-1:]
				Arr1[i] = 15000
			elif CheckBike(Extr[-3:],Time[-3:],Class[-3:]) == True:
                                print "biked at " + str(i)
                                print Extr[-4:]
                                print array(Time[-3:])
                                Extr = Extr[-1:]
                                Time = Time[-1:]
                                Class = Class[-1:]
                                Arr1[i] = 25000				
		Last = len(Extr)
        return Arr1,Extr,Time,Class

def CheckWalk(Extr,Time,Class):
	Bool = 0
	# check slopes sign
	if sign(Extr[3]-Extr[2]) > 0 and sign(Extr[1]-Extr[0]) > 0 and sign(Extr[2]-Extr[1]) < 0:
		Bool = Bool + 1

	# check magnitudes
	if abs(Extr[2]-Extr[1]) > abs(Extr[1]-Extr[0]):
		Bool = Bool + 1
	if (Extr[3]-Extr[2])/(Extr[1]-Extr[0]) > 1.5 and (Extr[3]-Extr[2])/abs(Extr[2]-Extr[1]) > 1.5:
		Bool = Bool + 1

	# check ampl
	if max(Extr) - min (Extr) < 15000:
		Bool = Bool + 1
	
	# check if walk
	if Bool == 4:
		return True
	else:
		return False

def CheckRun(Extr,Time,Class):
	Bool = 0
	#check slopes sign
	if sign(Extr[2]-Extr[1]) + sign(Extr[1]-Extr[0]) == 0:
		Bool = Bool + 1
	# check difference
	if abs(abs(Extr[2]-Extr[1])/abs(Extr[1]-Extr[0]) - 1) <= 0.25:
		Bool = Bool + 1
	#check mag
	if max(Extr) - min(Extr) > 15000 and max(Extr) - min(Extr) < 20000:
		Bool = Bool + 1
	#check time
	if abs(abs(Time[2]-Time[1])/abs(Time[1]-Time[0]) - 1) <= 0.5:
		Bool = Bool + 1	
	#check if run
	if Bool == 4:
		return True
	else:
		return False

def CheckBike(Extr,Time,Class):
        Bool = 0
        #check slopes sign
        if sign(Extr[2]-Extr[1]) + sign(Extr[1]-Extr[0]) == 0:
                Bool = Bool + 1
        # check difference
        if abs(abs(Extr[2]-Extr[1])/abs(Extr[1]-Extr[0]) - 1) <= 0.25:
                Bool = Bool + 1
        #check mag
        if max(Extr) - min(Extr) < 15000 and max(Extr) - min(Extr) > 5000:
                Bool = Bool + 1
        #check time
        if abs(abs(Time[2]-Time[1])/abs(Time[1]-Time[0]) - 1) >= 0.5:
                Bool = Bool + 1
        #check if bike
        if Bool == 4:
                return True
        else:
                return False

def CheckJump(Extr,Time,Class):
	Bool = 0
	#check slope sign and magnitude
	if sign(Extr[4]-Extr[3]) + sign(Extr[1]-Extr[0]) == 0 and abs(abs(Extr[4]-Extr[3])/abs(Extr[1]-Extr[0]) - 1) < 0.6:
		Bool = Bool  + 1	
	if sign(Extr[3]-Extr[2]) + sign(Extr[2]-Extr[1]) == 0 and sqrt(abs(Extr[3]-Extr[2])*abs(Extr[2]-Extr[1])) >= 20000:
		Bool = Bool + 1
	if abs(Extr[4]-Extr[3]) * 1.5 <= abs(Extr[3]-Extr[2]):
		Bool = Bool + 1
	if abs(Extr[2]-Extr[1]) >= abs(Extr[1]-Extr[0]) * 1.5:
		Bool = Bool + 1
	
	if Bool == 4:
		return True
	else:
		return False

File = file("test.csv","r")

Data = [[float(j) for j in i ] for i in csv.reader(File)]

Data = array(Data)

Axis = int(sys.argv[1])
axL = sys.argv[2]
smData = MovingAverage(Data[:,Axis],15)

smData = ParabolicSmooth(smData,5)

sm2Data = smData - MovingAverage(smData,15)

#sm2Data = sm2Data - MovingAverage(sm2Data,15)

Arr1,Extr,Time,Class = Extrema(sm2Data)

plot(Data[:,Axis])
plot(sm2Data,linewidth=2.0)
plot(Arr1,'*')

title('Filtered Accelerometer Data')

xlabel('Time Step')
ylabel('Magnitude of Acceleration in ' + axL + '-Axis')

legend(['Raw','Filtered','Local Min/Max'])

show()

Arr1 = array(Arr1)
Extr = array(Extr)
Time = array(Time)
Class = array(Class)



