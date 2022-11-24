# -*- coding: UTF-8 -*-
import cv2
import math
import requests
import sys
import json
import datetime
from time import strftime, localtime
import urllib.request

def imageProcessing():
	img = cv2.imread(sys.argv[1])
	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
	ret, thresh = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	hole1 = contours[0]
	hole2 = contours[1]
	hole3 = contours[2]
	hole1_green = getAverageRGB(img, hole1)[1]
	hole2_green = getAverageRGB(img, hole2)[1]
	hole3_green = getAverageRGB(img, hole3)[1]
	hole = [hole1_green,hole2_green,hole3_green]
	hole1_green = min(hole)
	hole2_green = max(hole)
	hole.remove(hole1_green)
	hole.remove(hole2_green)
	hole3_green = hole[0]
	print('Detection area of hole1 average Green value : {}'.format(hole1_green)) 
	print('Detection area of hole2 average Green value : {}'.format(hole2_green)) 
	print('Detection area of hole3 average Green value : {}'.format(hole3_green)) 
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	if abs(hole3_green - hole1_green) < 10:
		print('The sample to be tested is negative !')
	return hole1_green,hole2_green,hole3_green

def getAverageRGB(image, contour):
	inside = 0
	r = 0
	g = 0
	b = 0
	for x in range(image.shape[0]):
		for y in range(image.shape[1]):
			if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
				inside += 1
				px = image[y, x]
				b += px[0]
				g += px[1]
				r += px[2]
	return (r / inside, g / inside, b / inside)

def getRelativeRGB(hole1_green,hole2_green,hole3_green):
	rel_hole2_green = hole2_green / hole1_green 
	rel_hole3_green = hole3_green / hole1_green
	return rel_hole2_green , rel_hole3_green 



def getWeather(city):
	# r = requests.get('http://www.weather.com.cn/data/sk/101190101.html')
	# r.encoding = 'utf-8'
	# temp = float(r.json()['weatherinfo']['temp'])
	# print(r.json()['weatherinfo']['city'] + " temperature : " + r.json()['weatherinfo']['temp'])
	# return temp
	url = 'http://wthrcdn.etouch.cn/weather_mini?city='+city
	resq = requests.get(url)
	data = json.loads(resq.text)
	temp = float(data['data']['wendu'])
	print('Nanjing {} temperature : {}'.format(strftime('%Y-%m-%d %H:%M:%S', localtime()),str(temp)))
	return temp


def calculate(temp, RGB_2, RGB_3):   #RBG_2 is hole2 G value, RGB is hole3 G value
	x = 0
	if temp >= 4 and temp < 8:
		PH = 2.806 * RGB_2 - 0.236
		if PH >= 5.8 and PH < 6.2:
			x = 322.78 * RGB_3 - 327.93
		if PH >= 6.2 and PH < 6.6:
			x = 280.16 * RGB_3 - 286.77
		if PH >= 6.6 and PH < 7.0:
			x = 250.84 * RGB_3 - 254.67
		if PH >= 7.0 and PH < 7.4:
			x = 221.05 * RGB_3 - 223.55
		if PH >= 7.4 and PH < 7.8:
			x = 198.00 * RGB_3 - 200.80
		if PH >= 7.8 and PH < 8.2:
			x = 277.92 * RGB_3 - 280.61

	if temp >= 8 and temp < 12:
		PH = 2.921 * RGB_2 - 0.359
		if PH >= 5.8 and PH < 6.2:
			x = 298.66 * RGB_3 - 304.04
		if PH >= 6.2 and PH < 6.6:
			x = 276.19 * RGB_3 - 284.3
		if PH >= 6.6 and PH < 7.0:
			x = 261.45 * RGB_3 - 255.57
		if PH >= 7.0 and PH < 7.4:
			x = 217.56 * RGB_3 - 219.23
		if PH >= 7.4 and PH < 7.8:
			x = 185.38 * RGB_3 - 188.68
		if PH >= 7.8 and PH < 8.2:
			x = 279.07 * RGB_3 - 275.58

	if temp >= 12 and temp < 16:
		PH = 2.912 * RGB_2 - 0.228
		if PH >= 5.8 and PH < 6.2:
			x = 202.73 * RGB_3 - 207.64
		if PH >= 6.2 and PH < 6.6:
			x = 157.38 * RGB_3 - 159.84
		if PH >= 6.6 and PH < 7.0:
			x = 139.41 * RGB_3 - 140.53
		if PH >= 7.0 and PH < 7.4:
			x = 108.43 * RGB_3 - 105.65
		if PH >= 7.4 and PH < 7.8:
			x = 102.71 * RGB_3 - 106.42
		if PH >= 7.8 and PH < 8.2:
			x = 150.00 * RGB_3 - 157.50

	if temp >= 16 and temp < 20:
		PH = 3.060 * RGB_2 - 0.595
		if PH >= 5.8 and PH < 6.2:
			x = 148.54 * RGB_3 - 152.08
		if PH >= 6.2 and PH < 6.6:
			x = 142.12 * RGB_3 - 144.23
		if PH >= 6.6 and PH < 7.0:
			x = 126.64 * RGB_3 - 134.42
		if PH >= 7.0 and PH < 7.4:
			x = 99.16 * RGB_3 - 101.84
		if PH >= 7.4 and PH < 7.8:
			x = 101.64 * RGB_3 - 103.52
		if PH >= 7.8 and PH < 8.2:
			x = 162.12 * RGB_3 - 157.04

	if temp >= 20 and temp < 24:
		PH = 2.905 * RGB_2 - 0.140
		if PH >= 5.8 and PH < 6.2:
			x = 145.81 * RGB_3 - 149.57
		if PH >= 6.2 and PH < 6.6:
			x = 127.35 * RGB_3 - 131.59
		if PH >= 6.6 and PH < 7.0:
			x = 121.50 * RGB_3 - 126.68
		if PH >= 7.0 and PH < 7.4:
			x = 117.11 * RGB_3 - 124.69
		if PH >= 7.4 and PH < 7.8:
			x = 82.66 * RGB_3 - 89.83
		if PH >= 7.8 and PH < 8.2:
			x = 118.15 * RGB_3 - 122.30

	if temp >= 24 and temp < 28:
		PH = 3.078 * RGB_2 - 0.501
		if PH >= 5.8 and PH < 6.2:
			x = 144.97 * RGB_3 - 148.43
		if PH >= 6.2 and PH < 6.6:
			x = 136.78 * RGB_3 - 141.77
		if PH >= 6.6 and PH < 7.0:
			x = 115.80 * RGB_3 - 116.71
		if PH >= 7.0 and PH < 7.4:
			x = 105.69 * RGB_3 - 110.51
		if PH >= 7.4 and PH < 7.8:
			x = 87.493 * RGB_3 - 88.166
		if PH >= 7.8 and PH < 8.2:
			x = 120.20 * RGB_3 - 123.04

	if temp >= 28 and temp < 32:
		PH =  3.005 * RGB_2 - 0.516
		if PH >= 5.8 and PH < 6.2:
			x = 120.43 * RGB_3 - 124.98
		if PH >= 6.2 and PH < 6.6:
			x = 130.70 * RGB_3 - 135.98
		if PH >= 6.6 and PH < 7.0:
			x = 114.49 * RGB_3 - 115.78
		if PH >= 7.0 and PH < 7.4:
			x = 101.80 * RGB_3 - 106.52
		if PH >= 7.4 and PH < 7.8:
			x = 87.57 * RGB_3 - 88.296
		if PH >= 7.8 and PH < 8.2:
			x = 121.94 * RGB_3 - 127.07

	if temp >= 32 and temp < 36:
		PH = 2.932 * RGB_2 - 0.036
		if PH >= 5.8 and PH < 6.2:
			x = 101.41 * RGB_3 - 109.3
		if PH >= 6.2 and PH < 6.6:
			x = 95.49 * RGB_3 - 98.21
		if PH >= 6.6 and PH < 7.0:
			x = 92.55 * RGB_3 - 90.38
		if PH >= 7.0 and PH < 7.4:
			x = 87.11 * RGB_3 - 89.19
		if PH >= 7.4 and PH < 7.8:
			x = 77.588 * RGB_3 - 78.505
		if PH >= 7.8 and PH < 8.2:
			x = 116.11 * RGB_3 - 117.88

	if temp >= 36 and temp < 40:
		PH = 3.102 * RGB_2 - 0.402
		if PH >= 5.8 and PH < 6.2:
			x = 127.49 * RGB_3 - 132.47
		if PH >= 6.2 and PH < 6.6:
			x = 122.64 * RGB_3 -127.32
		if PH >= 6.6 and PH < 7.0:
			x = 111.98 * RGB_3 - 114.91
		if PH >= 7.0 and PH < 7.4:
			x = 75.99 * RGB_3 - 81.99
		if PH >= 7.4 and PH < 7.8:
			x = 62.41 * RGB_3 - 65.98
		if PH >= 7.8 and PH < 8.2:
			x = 98.86 * RGB_3 -107.77

	if temp >= 40 and temp < 44:
		PH = 3.162 * RGB_2 - 0.491
		if PH >= 5.8 and PH < 6.2:
			x = 145.21 * RGB_3 - 139.23
		if PH >= 6.2 and PH < 6.6:
			x = 128.74 * RGB_3 - 136.98
		if PH >= 6.6 and PH < 7.0:
			x = 120.49 * RGB_3 - 122.56
		if PH >= 7.0 and PH < 7.4:
			x = 99.84 * RGB_3 - 101.23
		if PH >= 7.4 and PH < 7.8:
			x = 85.62 * RGB_3 - 90.33
		if PH >= 7.8 and PH < 8.2:
			x = 118.23 * RGB_3 - 119.31

	if temp >= 44 and temp < 48:
		PH = 3.263 * ln_temp + 0.576
		if PH >= 5.8 and PH < 6.2:
			x = 140.54 * RGB_3 - 141.67
		if PH >= 6.2 and PH < 6.6:
			x = 139.18 * RGB_3 - 134.66
		if PH >= 6.6 and PH < 7.0:
			x = 121.89 * RGB_3 - 140.11
		if PH >= 7.0 and PH < 7.4:
			x = 99.86 * RGB_3 - 115.89
		if PH >= 7.4 and PH < 7.8:
			x = 108.34 * RGB_3 - 100.31
		if PH >= 7.8 and PH < 8.2:
			x = 142.12 * RGB_3 - 158.11
	print("PH : {}".format(PH))
	if PH >= 8.2 or PH < 5.8:
		print("Test limit exceeded !")
		print("Task ending !")
		sys.exit()
	return x

if __name__ == '__main__':
	print("Task beginning ......")
	hole1_green,hole2_green,hole3_green = imageProcessing()
	rel_hole2_green,rel_hole3_green = getRelativeRGB(hole1_green,hole2_green,hole3_green)
	# temp = getWeather('南京')
	print("The current laboratory temperature is 26 degrees !")
	enzyme_concentration = calculate(26, rel_hole2_green, rel_hole3_green)
	print("Hole3 enzyme concentration is {:.2f}".format(enzyme_concentration))
	print("Task ending !")
