from pylab import *
from Lib import Filters
import os
import matplotlib.backends.backend_pdf
import sys

Files = [i[:-4] for i in os.listdir(sys.argv[1]+"/"+sys.argv[2]) if i[-3:] == "csv"]

Filters.ClearPics("HP")

Type = "HP"

Window = int(sys.argv[3])

for File in Files:
	Data = Filters.LoadData(sys.argv[1],sys.argv[2],File)
	figure(num=None, figsize=(60,45))
	
	subplot(5,1,1)
	plot(Data[:,:3])
	title('Accelerometer ' + File)
	legend(['X','Y','Z'])

        subplot(5,1,2)
	Mag = Filters.Mag(Data[:,:3])
	HP = Filters.HPMA(Mag,Window)

        plot(HP)
        title('Accelerometer Magnitude ' + File)

	subplot(5,1,3)
	plot(Filters.RollStd(HP,Window))
	title('Accelerometer Rolling Standard Deviation')

	subplot(5,1,4)
	plot(Filters.RollMean(HP,Window))
	title('Accelerometer Rolling Sum')

	subplot(5,1,5)
	plot(Filters.MaxSearch(HP,Window)-Filters.MinSearch(HP,Window))
	title('Accelerometer Range')	

        savefig("RunPics/HP/"+File+"_Acc_"+Type+".png")
        close()

	if shape(Data)[1] == 6:
		figure(num=None, figsize=(60,45))

		subplot(5,1,1)
		plot(Data[:,3:])
		title('Gyroscope ' + File)
		legend(['X','Y','Z'])
		
		subplot(5,1,2)
		Mag = Filters.Mag(Data[:,3:])
		HP = Filters.HPMA(Mag,Window)
		
		plot(HP)
		title('Gyroscope Magnitude ' + File)
		
		subplot(5,1,3)
		plot(Filters.RollStd(HP,Window))
		title('Gyroscope Rolling Standard Deviation')
		
		subplot(5,1,4)
		plot(Filters.RollMean(HP,Window))
		title('Gyroscope Rolling Sum')
		
		subplot(5,1,5)
		plot(Filters.MaxSearch(HP,Window)-Filters.MinSearch(HP,Window))
		title('Gyrometer Range')
		
		savefig("RunPics/HP/"+File+"_Gyr_"+Type+".png")
		close()




