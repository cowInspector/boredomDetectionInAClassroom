#!/usr/bin/python

#Boredom Detection using openCV and SimpleCV, hopefully I'll use the GUI modules soon.

#Usage: python facedetect.py

import sys
import os
import cv
import Image
import ImageDraw
import time
import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import pylab
import SimpleCV
import random

def saveFaces(ImagePath, coords, outName, fillColorLevel):
  """
  ImagePath: Path to the Image
  coords: coordinates of all the faces in the image. format: [(x1, y1), (x2, y2)]
  outName: output file name
  fillColorLevel: the fill color of the rectange
  returns: nothing. It just saves the image.
  """
  img = Image.open(ImagePath)
  draw = ImageDraw.Draw(img)

  for i in coords:	#iterate through all the faces and fill the coordinates with the color specified
   draw.rectangle(i,fill = fillColorLevel)
   
  img.save(outName)

def findCoords(ImagePath, classifierPath):
  """
  ImagePath: Path to the Image
  ClassifierPath: Path to the classifier that will be used to detect faces
  """
  image = cv.LoadImage(ImagePath);
  grayscale = cv.CreateImage(cv.GetSize(image), 8, 1) 	#create a grayscale image of same size and bit-depth 8
  cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY) 	#convert the input image to grayscale
  
  cv.EqualizeHist(grayscale, grayscale) #equalize histograms
  cascade = cv.Load(classifierPath)	#load the specified classifier
  faces = cv.HaarDetectObjects(grayscale, cascade, cv.CreateMemStorage(0), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50,50))	#detect faces - I have absolutely no clue as to how it works. Drop me a mail at mv.vijesh@gmail.com if you get to know how.
  
  coords = []	#extracting the coordinates and saving it in the required format. format: [(x1, y1), (x2, y2)]
  if faces:
    for f in faces:
      coords.append( [(f[0][0], f[0][1]), (f[0][0]+f[0][2], f[0][1]+f[0][3])] )
      
  return coords
  
def dist(point1, point2): #returns the euclidean distance between the two given points
  return math.sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )
  
'''
class faceOld:
  'Each face is implemented as a class'
  coords = False
  centers = False
  
  size = False #size must be calculated after getting to know that there is no False face
  
  average = False
  dist_from_avrg = False
  std_dev = False
  disturbance_factor = False #calcuate using the size info also!!!
  validFace = False
  
  def __init__(self, coord):
    self.coords = {}
    self.coords[0] = coord
    #self.size = (coord[0][0] - coord[1][0]) * (coord[0][1] - coord[1][1])
    
    self.centers = {}
    self.centers[0] = ((coord[0][0] + coord[1][0]) / 2.0, (coord[0][1] + coord[1][1]) / 2.0)
    
    self.updateParams()
    
  def updateParams(self):
    self.setAvrg()
    self.setDistFromAvrg()
    self.setStdDev()
  
  def setAvrg(self):
    self.average = (numpy.average([x for x,y in self.centers.values()]), numpy.average([y for x,y in self.centers.values()]))
    
  def setDistFromAvrg(self):
    self.dist_from_avrg = [dist(self.average, point) for point in self.centers.values()]
    
  def setStdDev(self):
    self.std_dev = numpy.std(self.dist_from_avrg)
    
  def addCoord(self, coord, frameNumber):
    self.coords[frameNumber] = coord
    self.centers[frameNumber] = ((coord[0][0] + coord[1][0]) / 2.0, (coord[0][1] + coord[1][1]) / 2.0)
    #print self.centers[frameNumber]
    self.updateParams()
    
  def printDetails(self):
    print ""
    print "coords: ", self.coords
    print "centers: ", self.centers
    print "size: ", self.size
    print "average: ", self.average
    print "dist_from_avrg: ", self.dist_from_avrg
    print "std_dev: ", self.std_dev
'''

class faceNew:
  'Each face is implemented as a class. Refer to the documentation for more details.'
  coord = None			#coordinates of the face that was detected in the initial frame.
  size = None			#size is the number of pixels that the face occupies
  BaseMatrices = None		#the cropped matrix obtained directly from the image - This will be a dictionary with frameNumber as the key and the cropped image as value
  differenceMatrices = None	#the numpy matrix of differences between the pixel values of a frame and its previous frame - its implemented as a dictionary with key as (frameNumber-1, frameNumber) and value as the numpy matrix of differences
  avrgOfDiff = None		#the average of each difference Matrix - implemented as a dictionary with key as (frameNumber-1, frameNumber) and value as the average of the corresponding numpy matrix
  averageSum = None		#the average of all the average differences - this is a floating point member
  dist_from_avrg = None		#the deviation of avrgDifference from averageSum - implemented as a dictionary with key as (frameNumber-1, frameNumber) and value as the deviation from averageSum
  averageDeviation = None	#the average of all the deviations
  std_dev = None		#the standard deviation of all the deviations
  disturbed_bool = None		#the indicator that indicates whether a person was bored at that frame - implemented as a dictionary with key as frameNumber and value as {0,1}
  
  def __init__(self, coord, image):	#constructor for faceNew. For some dabba reason, I cant give the name of the class as 'face'
    self.coord = coord			#set the initial coordinates. This is unique for a given object
    self.size = (coord[0][0] - coord[1][0]) * (coord[0][1] - coord[1][1])	#set the size of the face coordinate
    self.BaseMatrices = {}
    self.BaseMatrices[1] = image.crop( (coord[0][0], coord[0][1], coord[1][0], coord[1][1]) ) #frame numbering starts from 1. The first base image set in the constructor and serves as a reference to the second
    self.differenceMatrices = {}	#initialize all other required dictionaries
    self.avrgOfDiff = {}
    self.dist_from_avrg = {}
    self.disturbed_bool = {}
        
  def updateParams(self, frameNumber): #updates the parameters averageSum, dist_from_avrg, averageDeviation, std_dev, disturbed_bool
    self.setAvrgSum()
    self.setDistFromAvrg(frameNumber)
    self.setAvrgDeviation()
    self.setStdDev()
    self.setDisturbedBool(frameNumber)
  
  def setAvrgSum(self):
    self.averageSum = numpy.average(self.avrgOfDiff.values()) #calculates the average of averageDifference values
    
  def setDistFromAvrg(self, frameNumber):
    self.dist_from_avrg = dict( [ (frameIter, numpy.abs(self.averageSum - self.avrgOfDiff[(frameIter - 1, frameIter)]) ) for frameIter in range(2, frameNumber + 1) ] ) #create a list of tuples. format of the tuple: (frameNumber, deviation of this frame value from the average)
    #update the dictionary with key as the first value in the tuple and value as the second pair.
    
  def setStdDev(self):
    self.std_dev = numpy.std(self.avrgOfDiff.values()) #standard deviation of all the deviations
  
  def setAvrgDeviation(self):
    self.averageDeviation = numpy.average(self.dist_from_avrg.values()) #average of deviation from average, from all the frames
  
  def setDisturbedBool(self, frameNumber):
    if( numpy.abs( self.averageSum - self.avrgOfDiff[(frameNumber - 1, frameNumber)]) > self.averageDeviation ): #if the deviation for the current frame is greater than the average deviation so far, then the person is disturbed. Hence, set the boolean factor to 1.
      self.disturbed_bool[frameNumber] = 1
    else:
      self.disturbed_bool[frameNumber] = 0
      
  #At any given timeFrame, to find out the boredom of the entire class, just see the fraction of people whose value for the given timeFrame is 1.
    
  def addFrame(self, frameNumber, frame):
    self.BaseMatrices[frameNumber] = frame.crop( (self.coord[0][0], self.coord[0][1], self.coord[1][0], self.coord[1][1]) )
    #self.BaseMatrices[frameNumber].show()
    self.differenceMatrices[(frameNumber - 1, frameNumber)] = numpy.abs( numpy.asarray(self.BaseMatrices[frameNumber-1].convert(mode="L"), dtype = numpy.int) - numpy.asarray( self.BaseMatrices[frameNumber].convert(mode="L"), dtype = numpy.int ) )
    
    #print numpy.asarray(self.BaseMatrices[frameNumber].convert(mode="L"), dtype = numpy.int)
    #print numpy.asarray( self.BaseMatrices[frameNumber].convert(mode="L"), dtype = numpy.int )
    #print self.differenceMatrices[(frameNumber - 1, frameNumber)]
    
    self.avrgOfDiff[(frameNumber - 1, frameNumber)] = numpy.sum(self.differenceMatrices[(frameNumber - 1, frameNumber)]) / float(numpy.size(self.differenceMatrices[(frameNumber - 1, frameNumber)]))
    self.updateParams(frameNumber)
    
  def printDetails(self):
    print ""
    print "coords: ", self.coord
    print "size: ", self.size
    print "average: ", self.averageSum
    print "dist_from_avrg: ", self.dist_from_avrg
    print "std_dev: ", self.std_dev
    
def plotData(frameNumber, x, faceObjs, xWidth, fig, ax, lines):
  #x = range(xWidth)
  #y = random.sample(range(100), xWidth)
  
  #fig.clear()
  #fig.canvas.draw()
  
  #y = [ [face.avrgOfDiff[(frameNumber - 1, frameNumber)] for frameNumber in range(2,frameNumber+1)] for face in faceObjs]
  y = [ [face.disturbed_bool[frameIter] for frameIter in range(2,frameNumber+1)] for face in faceObjs] #last one is the all-channel
  netEffect = [ sum([ y[j][i] for j in range(len(y))]) for i in range(frameNumber - 1)]
  y.append(netEffect)
  
  for i in range(len(y)):
    faceVariation = y[i]
    if(len(faceVariation) < xWidth):
      ax.set_xbound(lower=0, upper=xWidth)
      ax.set_ybound(lower=0, upper=max(faceVariation))
      lines[i].set_xdata(range(len(faceVariation)))
      lines[i].set_ydata(faceVariation)
    else:
      ax.set_xbound(lower=len(faceVariation) - xWidth, upper=len(faceVariation))
      ax.set_ybound(lower=0, upper=max(faceVariation[-xWidth:]))
      lines[i].set_xdata(range(len(faceVariation) - xWidth, len(faceVariation)))
      lines[i].set_ydata(faceVariation[-xWidth:])
    
  fig.canvas.draw()
  
def getImage(cam, ImgName):
  img = cam.getImage()
  img.save(ImgName)
  

def main():
  cam = SimpleCV.Camera()
  frameLimit = {'low':5, 'high': 100}
  sleepDur = 0.01
  ImgDefaultName = "shots.png"
  xWidth = 50
  
  classifierPath = '../haarcascades/haarcascade_frontalface_default.xml'
  
  outName = "output.png"
  fillColorLevel = 128
  
  getImage(cam, ImgDefaultName)
  ImagePath=ImgDefaultName
  #ImagePath = "../1/avrg001.png"
  #ImagePath = "../4/extraheavy001.png"
  
  coords = findCoords(ImagePath, "../haarcascades/haarcascade_frontalface_alt.xml")
  #print coords
  saveFaces(ImagePath, coords, outName, fillColorLevel)
  
  if(not coords):
    print "No face detected."
  else:
    matplotlib.use('TkAgg')
    pylab.ion()
  
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    lines = []
    
    image = Image.open(ImagePath)
    
    faceObjs = []
    for faceCoord in coords:
      faceObjs.append( faceNew(faceCoord, image) )
      
      line, = ax.plot(range(10), [0]*10)
      lines.append(line)
    
    line, = ax.plot(range(10), [0]*10)
    lines.append(line)
    
  
    x = []
    for frameNumber in range(2, frameLimit['high'] + 1):
      #print ""
      getImage(cam, ImgDefaultName)
      ImagePath = ImgDefaultName
      #print ""
      
      #ImagePath = "../1/avrg" + str(frameNumber).zfill(3) + ".png"
      #ImagePath = "../4/extraheavy" + str(frameNumber).zfill(3) + ".png"
      
      image = Image.open(ImagePath);
      #print ImagePath, 
  
      for face in faceObjs:
	face.addFrame(frameNumber, image)
      
      x.append(frameNumber)
      plotData(frameNumber, x, faceObjs, xWidth, fig, ax, lines)
      
      time.sleep(sleepDur)
      #raw_input("")
    pylab.ioff()
  
#if __name__ == "__main__":
#face("jyg", " gh")

main()

print "Press return to Exit"
raw_input("")