from pylab import *
import csv

File = file("test.csv","r")

Data = [[float(j) for j in i ] for i in csv.reader(File)]

Data = array(Data)

plot(Data[:,2])

show()



