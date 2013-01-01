from face_client import face_client
keys = face_client.FaceClient('7cdb6b372b654db15b7e8f864f5b81f2','6b240a54151159aab5658893a098bbb7')
centers_multiple = []
centers_average = []
#assuming this set loops 'frame_number' times, over the whole video
#-----------------------------------------------------------------------------------------------
info = keys.faces_detect(urls=None, file='/home/vijesh/Desktop/IMG_3772.JPG',aggressive = False)
face_number = len(info[u'photos'][0][u'tags'])
centers_single = []
for i in range(0,face_number):
	centers_single.append( [ (info[u'photos'][0][u'tags'][i][u'center'][u'x'],info[u'photos'][0][u'tags'][i][u'center'][u'y']) ] )
centers_average = centers_single
centers_multiple = centers_single
frame_number = 1
#-----------------------------------------------------------------------------------------------

#function called when a new frame is added: newframe()
#-----------------------------------------------------------------------------------------------
#info = keys.faces_detect(urls=None, file=path,aggressive = False)
for i in range(0, face_number):
	centers_multiple[i].append( (info[u'photos'][0][u'tags'][i][u'center'][u'x'],info[u'photos'][0][u'tags'][i][u'center'][u'y']) )
#-----------------------------------------------------------------------------------------------

#function to find average
#-----------------------------------------------------------------------------------------------
for i in range(0, face_number):
	avgx = 0
	avgy = 0
	for j in range(0, len( centers_multiple[i]) ) ):
		avgx += centers_multiple[i][j][0]
		avgy += centers_multiple[i][j][1]
	avgx /= len( centers_multiple[i]
	avgy /= len( centers_multiple[i]
	centers_average[i][0] = (avgx,avgy)
#-----------------------------------------------------------------------------------------------


#To eliminate the extreme case and compute the new average centre for all the faces
#-----------------------------------------------------------------------------------------------
#threshold_dev = ________
for i in range(0,face_number):
	for j in range(0,len(centers_multiple[i])):
		dev = sqrt ( abs ( (centers_multiple[i][j][0] - centers_average[i][0][0])**2 +  (centers_multiple[i][j][1] - centers_average[i][0][1])**2 ) )
		if dev > threshold_dev:
			del centers_multiple[i][j]

#To update the avrg information
for i in range(0, face_number):
	avgx = 0
	avgy = 0
	for j in range(0, len( centers_multiple[i]) ) )
		avgx += centers_multiple[i][j][0]
		avgy += centers_multiple[i][j][1]
	avgx /= len( centers_multiple[i]
	avgy /= len( centers_multiple[i]
	centers_average[i][0] = (avgx,avgy)

#-----------------------------------------------------------------------------------------------

#file = open('detectdata.txt','w')
#file.write(info)
#file.close()
