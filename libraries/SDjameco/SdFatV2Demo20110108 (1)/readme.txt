SdFat V2 Demo

Warning this is a demo for comments, not even a beta.

Please send comments to fat16lib@sbcglobal.net.

Do not use this library for applications.  It is unfinished and not well tested.

Much of the html needs to be updated. The class and file documentation is
from the source and is more up to date than the intro.

SdFat V2 has many new features.

Path names and a current working directory have been added.

The new class, SdFat, simplifies initialization and implements the
current working directory.

SdFat implements many C++ iostream features.  New classes include:

ofstream: Stream class to write to files.
ifstream: Stream class to read from files.
fstream: Stream class to both read and write from/to files.
ibufstream: Stream class to parse char strings.
obufstream: Stream class to format char strings.
ArduinoOutStream: Steam to write to Serial and other "Print" devices.
ArduinoInStream: Stream to read from Serial and other "Stream" devices.

You must remove SdFat V1 to run this demo.

Place SdFat in your libraries directory.

SdFatConfig.h has configuration options.


Try the following examples from the SdFat/examples folder:

HelloWorld.pde - Simple version of the classic program for Serial.

eventlog.pde - Append a line to a file - demo of pathnames and streams.

readlog.pde - Read logfile - demo of pathnames and current working directory.

formatting.pde - Print a table with various formatting options and prints dates.

average.pde - Calculate the sum and average of a list of floating point numbers.

getline.pde - Example of getline from section 27.7.1.3 of the C++ standard.

bufstream.pde - Use ibufstream to parse a line and obufstream to format a line.

AnalogLogger.pde - A simple data logger for the Arduino analog pins.

SdInfo.pde - This sketch attempts to initialize the SD card and
             analyze its structure.
             
SdFormatter.pde - This sketch will format an SD or SDHC card.

append.pde - Test that appends 10,000 lines to a file in groups of 100.

bench.pde - This sketch is a simple binary write/read benchmark.

cin_cout.pde - Demo of ArduinoInStream and ArduinoOutStream.

SD_Size.pde - Sketch to compare size of Arduino SD library with SdFat V2.

SdFatSize.pde - Sketch to compare size of SdFat V2 with Arduino SD library.
