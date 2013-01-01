import Image

def func(pixel):
	return(pixel%avg)

img = Image.open('vijay.JPG')
imggray = img.convert("L")

sum = 0;
for i in range(1,img.size[0]):
	for j in range(1,img.size[1]):
		sum += imggray.getpixel((i,j))
avg = int(sum / (img.size[0]*img.size[1]))
print "Avrage is " + str(avg)

imggray.point(func).show()
