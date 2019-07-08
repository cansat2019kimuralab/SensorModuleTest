
import cv2
import numpy as np
import math


'''
引数	画像(cv::Mat)
戻り値	[距離,角度]

'''



def ParaDetection(img):
	#cv2.imshow('Input Image',img)
	hig, wid, col = img.shape

	#mask生成

	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)

	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]

	mask = np.zeros(h.shape, dtype=np.uint8)
	mask[((h < 10) | (h > 200)) & (s > 120)] = 255

	#cv2.imshow('Red Zone', mask)

	#輪郭処理
	mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


	#最大面積
	max_area = 0
	max_area_contour = -1

	for j in range(0,len(contours)):
		area = cv2.contourArea(contours[j])
		if max_area < area:
			max_area = area
			max_area_contour = j

	cnt = contours[max_area_contour]

	#print('Max area is',max_area)

	#goal未検出時
	if max_area <= 100:
		print( "There is not the Parachute" )
		return 0

	#goal判定

	else:
		print( "There is the Parachute" )
		return 1

if __name__ == "__main__":
	im = cv2.imread('photo/photo1.jpg')
	ParaDetection(im)
