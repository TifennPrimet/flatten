import glob
from findCorners import *
from reforme_images import *
from error import *
from read_XML import *
import doctest

path = "D:\STAGE\MS\RGB"
path_xml = "D:\STAGE\XML"
extention =".jpg"
name = "\MatriceMS1"
row = 19
columns = 12
val = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FILTER_QUADS
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.00001)                                             #forme le critère de recherche #modification du dernier critère

#objpoints, imgpoints, images , mtx, dist, rvecs, tvecs =findCorners(path, extention, row, columns, criteria, val)     
images = glob.glob(path+'\*'+ extention,recursive = True)            
mtx, dist = read_XML(path_xml, name)
print(images)
for fname in images:
    reforme_images(fname, path, extention, mtx, dist)
print('flattenned')
doctest.testmod()
