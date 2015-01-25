from pylab import *
from Lib import Filters
import os

Files = [i[:-4] for i in os.listdir("Arrilaga_1-22") if i[-3:] == "csv"]

Filters.ClearPics("Mag")

for File in Files:
	Data = Filters.LoadData("Arrilaga_1-22",File)
	figure(num=None, figsize=(48,36))
	
	subplot(4,1,1)
	plot(Data[:,:3])
	title('Accelerometer ' + File)
	legend(['X','Y','Z'])

        subplot(4,1,2)
	Mag = Filters.Mag(Data[:,:3])
        plot(Mag)
        title('Accelerometer Magnitude ' + File)

	subplot(4,1,3)
	plot(Filters.RollStd(Mag,50))
	title('Accelerometer Rolling Standard Deviation')

	subplot(4,1,4)
	plot(Filters.RollMean(Mag,50))
	title('Accelerometer Rolling Sum')


        savefig("RunPics/Mag/"+File+"_Acc.png")
        close()

	figure(num=None, figsize=(48,36))

	subplot(4,1,1)
	plot(Data[:,3:])
	title('Gyroscope ' + File)
	legend(['X','Y','Z'])
	
        subplot(4,1,2)
        Mag = Filters.Mag(Data[:,3:])
        plot(Mag)
	title('Gyroscope Magnitude ' + File)
	
	subplot(4,1,3)
	plot(Filters.RollStd(Mag,50))
	title('Gyroscope Rolling Standard Deviation')

	subplot(4,1,4)
	plot(Filters.RollMean(Mag,50))
	title('Gyroscope Rolling Sum')

	savefig("RunPics/Mag/"+File+"_Gyr.png")
	close()




