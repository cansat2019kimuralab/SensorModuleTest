# -*- coding: utf-8 -*-
import numpy as np
import time
import math

#https://qiita.com/r-fuji/items/99ca549b963cedc106ab

# Ellipsoid
ELLIPSOID_GRS80 = 1	# GRS80
ELLIPSOID_WGS84 = 2	# WGS84

# Long Axis Radius and Flat Rate
GEODETIC_DATUM = {
    ELLIPSOID_GRS80: [
        6378137.0,         # [GRS80] Long Axis Radius
        1 / 298.257222101, # [GRS80] Flat Rate
 	   ],
    ELLIPSOID_WGS84: [
        6378137.0,         # [WGS84] Long Axis Radius
        1 / 298.257223563, # [WGS84] Flat Rate
    ],
}

# Limited times of Itereation
ITERATION_LIMIT = 1000

'''
Vincenty法(逆解法)
2地点の座標(緯度経度)から、距離と方位角を計算する
:param lat1: 始点の緯度
:param lon1: 始点の経度
:param lat2: 終点の緯度
:param lon2: 終点の経度
:param ellipsoid: 楕円体
:return: 距離と方位角
'''
def vincenty_inverse(lat1, lon1, lat2, lon2, ellipsoid=None):
    if lat1 == lat2 and lon1 == lon2:
        return 0.0, 0.0
	
    # Calculate Short Axis Radius
    # if Ellipsoid is not specified, it uses GRS80
    a, f = GEODETIC_DATUM.get(ellipsoid, GEODETIC_DATUM.get(ELLIPSOID_GRS80))
    b = (1 - f) * a

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    # Corrected Latitude
    U1 = math.atan((1 - f) * math.tan(phi1))
    U2 = math.atan((1 - f) * math.tan(phi2))

    sinU1 = math.sin(U1)
    sinU2 = math.sin(U2)
    cosU1 = math.cos(U1)
    cosU2 = math.cos(U2)

    # Diffrence of Longtitude between 2 points
    L = lambda2 - lambda1

    # Reset lamb to L
    lamb = L

    # Calculate lambda untill it converges
    # if it doesn't converge, returns None
    for i in range(ITERATION_LIMIT):
        sinLambda = math.sin(lamb)
        cosLambda = math.cos(lamb)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cos2Alpha = 1 - sinAlpha ** 2
        cos2Sigmam = cosSigma - 2 * sinU1 * sinU2 / cos2Alpha
        C = f / 16 * cos2Alpha * (4 + f * (4 - 3 * cos2Alpha))
        lambdaʹ = lamb
        lamb = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2Sigmam + C * cosSigma * (-1 + 2 * cos2Sigmam ** 2)))

		#Deviation is udner 1e-12, break
        if abs(lamb - lambdaʹ) <= 1e-12:
            break
    else:
        return None

    # if it converges, calculates distance and angle
    u2 = cos2Alpha * (a	 ** 2 - b ** 2) / (b ** 2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    dSigma = B * sinSigma * (cos2Sigmam + B / 4 * (cosSigma * (-1 + 2 * cos2Sigmam ** 2) - B / 6 * cos2Sigmam * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2Sigmam ** 2)))

    s = b * A * (sigma - dSigma)															#Distance between 2 points
    alpha = -1 * math.atan2(cosU2 * sinLambda, cosU1 * sinU2 - sinU1 * cosU2 * cosLambda)	#Angle between 2 points

    # return s(distance), and alpha(angle)
    return s, math.degrees(alpha)


if __name__ == "__main__":
	lat_a, lon_a = 35.917281, 139.906248
	lat_b, lon_b = 35.917280, 139.906248
	lat_c, lon_c = 35.918295, 139.907818
	lat_d, lon_d = 35.918181, 139.907992
	lat_e, lon_e = 35.918257, 139.907706
	#dis, angle = GPS.Cal_RhoAng(lat_a, lon_a, lat_b, lon_b)
	a = vincenty_inverse(lat_c, lon_c, lat_d, lon_d)
	print(a)
	#print(dis, angle)
