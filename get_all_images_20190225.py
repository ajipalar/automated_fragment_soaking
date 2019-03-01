# python3.7.0
#Project/dropk#/well/profileID/name_ef.jpg
#run this command above the echo project directory

import glob
import sys
import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.util import pad
from skimage import io
import os
from classes_only import Well_well_well as well
from classes_only import Plate

# argument is plateID_****
if len(sys.argv) != 2:
	print('Provide path to plateID_####')
	print('Aborting script')
	sys.exit()

current_directory = os.getcwd()
plate_dir = sys.argv[1]
#Function Definitions
#Params
	#r1 lower radius bound
	#r2 upper radius bound
	#search step size between radii
	#edge: a binary image which is the output of canny edge detection
	#peak_num the # of circles searched for in hough space

#Output:
	#accums 
	#cx : circle center x
	#cy : circle center y
	#radii circle radii
def circular_hough_transform(r1,r2,step,edge, peak_num):
    hough_radii = np.arange(r1,r2,step)
    hough_res = hough_circle(edge,hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res,hough_radii,total_num_peaks=peak_num)
    return accums, cx, cy, radii
def single_radii_circular_hough_transform(r1,edge):
    hough_res = hough_circle(edge,r1)
    accums, cx, cy, radii = hough_circle_peaks(hough_res,r1,total_num_peaks=1)
    return accums, cx, cy, radii
#Params
	#This functions draws a circle of radius r centered on x,y on an image. It draws the center of the circle
	#image: input greyscale numpy 2darray
	#cx: int center x
	#cy: int center y
	#color: single 8-bit channel int. i.e 0-255
def draw_circles_on_image(image,cx,cy,radii,colour,dotsize):
    for center_y, center_x, radius in zip(cy,cx,radii):
        circy, circx = circle_perimeter(center_y,center_x,radius)
        image[circy,circx] = colour
        image[cy[0]-dotsize:cy[0]+dotsize,cx[0]-dotsize:cx[0]+dotsize] = colour
def draw_circles_on_image_center(image,cx,cy,radii,colour,dotsize):
    for center_y, center_x, radius in zip(cy,cx,radii):
        circy, circx = circle_perimeter(center_y,center_x,radius)
        image[circy,circx] = colour
        image[cy[0]-dotsize:cy[0]+dotsize,cx[0]-dotsize:cx[0]+dotsize] = colour
def save_canny_save_fit(path,sig,low,high): #sig=3,low = 0, high = 30
	zstack = io.imread(path)
	image = img_as_ubyte(zstack[:,:,0])
	
	
	mask = image > 20
	
	fprefix = os.path.basename(path).strip('.jpg')
	bn = fprefix + '_CANNY.jpg'
	current_dir = os.getcwd()

	cannysavepath = current_dir + '/' + plate_dir.strip('/') + '_canny/' + bn

	edges = canny(image,sigma=sig,low_threshold=low,high_threshold=high)
	#plt.imsave(fname=str(p + fprefix + '_ubyte.jpg'), arr=image)
	#plt.imsave(fname=str(p + fprefix + '_bounded.jpg'), arr=mask)
	bn = fprefix + '_dropfinder2.jpg'
	fitsavepath = current_dir + '/' + plate_dir.strip('/') + '_fit/' + bn
	try:
		plt.imsave(fname=cannysavepath, arr=edges)
		plt.close()
	except FileNotFoundError:
		print('FileNotFoundError: making ' + plate_dir.strip('/') + '_canny')
		os.mkdir(current_dir + '/' + plate_dir.strip('/') + '_canny/')
		print('writing ' + cannysavepath)
		plt.imsave(fname=cannysavepath, arr=edges)
		plt.close()
	print(cannysavepath)
	accum_d, cx_d, cy_d, radii_d = circular_hough_transform(135,145,2,edges,1) #edge detection on drop
	accum_w, cx_w, cy_w, radii_w = circular_hough_transform(479,495,1,edges,1) #edge detection on well
	
	try:
		im = image
		padsize = np.array([(0,100),(0,100)])
		pad_im = pad(image,padsize,mode='constant')
		fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(20,8))
		draw_circles_on_image(pad_im,cx_d,cy_d,radii_d,255,2)
		draw_circles_on_image(pad_im,cx_w,cy_w,radii_w,255,2)

		### Code to draw the inner circle

		r_inner = 0.73701*radii_w
		r_inner = r_inner.astype(int)
		draw_circles_on_image(pad_im,cx_w,cy_w,r_inner,255,2)

		
		cx=641
		cy=553
		rad=487
		c, r = circle_perimeter(cx, cy,rad)
		#pad_im[r,c] = 255
		#pad_im[cx-2:cx+2,cy-2:cy+2]=255

		try:
			plt.imsave(fname=fitsavepath, arr=pad_im,cmap='Greys_r')
			plt.close()
		except FileNotFoundError:
			print('making ' + plate_dir.strip('/') + '_fit/')
			os.mkdir(current_dir + '/' + plate_dir.strip('/') + '_fit/')
			print('writing' + bn)
			plt.imsave(fname=fitsavepath, arr=pad_im,cmap='Greys_r')
			plt.close()
		print(fitsavepath)
	except IndexError:
		print('IndexError' + ' ' + fitsavepath)
	#plt.imshow(pad_im)
	
	return cx_d,cy_d,radii_d, cx_w, cy_w, radii_w

def find_image_paths():
	my_paths = glob.glob('plateID_9552/*/wellNum_*/profileID*')
	my_paths.sort(key=lambda x: (int(x.split('wellNum_')[1].split('/')[0])))
	return my_paths

my_paths = find_image_paths() #The path string object

image_list = [] #empty holder list
# test#,well#,d#
#Save format t1w1d1,t2w1d1
#gets only the images
for path in my_paths: #
	print(str(path))
	images = glob.glob(path + '/*ef*')
	images.sort(key=lambda x: int(x.split('_r')[1].split('_ef')[0]))
	image = images[1]
	image_list.append(image)


print(current_directory + '/' + plate_dir.strip('/') + '_offsets.csv')
#f = open(current_directory + '/' + plate_dir.strip('/') + '_offsets.csv','wa')
#f.write('offset_x,offset_y,radii_d,radii_w,cx_d,cy_d,cx_w,cy_w\n')

wellnames = Plate.well_names
plate_to_pickle = Plate(Plate.plate_dict)
	#code to w
n=0
for im_path in image_list:
	cx_d,cy_d,radii_d, cx_w, cy_w, radii_w = save_canny_save_fit(im_path,3,0,50) #calling this function also saves
	offset_x = cx_d - cx_w
	offset_y = cy_w - cy_d

	name = wellnames[n]
	print(name)
	plate_to_pickle.plate_dict[name] = well(cx_w,cy_w,radii_w,cx_d,cy_d,radii_d,cx_w,cy_w,radii_d,name,im_path)
	print(plate_to_pickle.plate_dict[name])
	n+=1
	if n == 12:
		break
f = open(current_directory + '/' + 'fitsforgui.pkl', 'wb')
pkl.dump(plate_to_pickle,f)
print('dumped')
	#code to write to .csv
	#f.write('%s,%s,%s,%s,%s,%s,%s,%s\n' %(offset_x,offset_y,radii_d,radii_w,cx_d,cy_d,cx_w,cy_w))


	#code to save file 
#f.close()