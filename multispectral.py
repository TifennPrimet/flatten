from concurrent.futures.process import _ExceptionWithTraceback
from re import I
import cv2 as cv
import numpy as np
from enlarge import*
# Files that read the information of 3 wavelength images and combine them in a false color image
# By default OpenCV use the BGR format ( red is the less important information)

path = "D:\STAGE\calibre\Bank"      # path to all the images 

Blue = cv.imread( path +  '\imgChannel_3.tiff')   # this will be the blue channel
Green = cv.imread( path +  '\imgChannel_6.tiff')  # the green one
Red = cv.imread( path +  '\imgChannel_0.tiff')     # the red one

NewMatrix = np.zeros(Blue.shape) # The new image null by default
# We enter all the values of the images one by one in the new image
for i in range(Blue.shape[0]):
    for j in range(Blue.shape[1]):
        # write the value of the BGR in NewMatrix
        NewMatrix[i,j][0] = Blue[i,j][0]        #Blue[i,j][0] to get the fisrt value of the blue matrix  [[[3. 3. 3.] , [1. 1. 1.]] , [[3. 3. 3.] , [2. 2. 2.]] , ... , [[0. 0. 0.] , [0. 0. 0.]]]
        NewMatrix[i,j][1] = Green[i,j][0]
        NewMatrix[i,j][2] = Red[i,j][0]

NewMatrix =  255 * ( NewMatrix / (np.max(NewMatrix))) # we scale the matrix to have information btwn [0,255] and not [0,3]

cv.imwrite(path+"\_3channel.bmp",NewMatrix) # create a new file


# To control what we've done we read the file we made


carre = 10
essai = NewMatrix[-carre:,-carre:]
# cv.imshow("essaie", essai)
# print(NewMatrix[:21,:21])
# essai = np.array([[[0.,0.,0.],[0.,0.,255.],[0.,255.,0.]],[[0.,255.,255.],[255.,0.,0.],[255.,0.,255.]],[[255.,255.,0],[255.,255.,255.],[0.,0.,0.]]])
#essai2 = essai[:2,:2]
cv.imwrite(path+"\essai_petit.png",essai)

          

c = 20
res1 = enlarge(essai, c)
cv.imwrite(path+"\extrait_image.png",res1)
cv.imshow("image agrandi", res1)

ImageConcat = cv.imread( path +  "\_3channel.bmp")
#bla =enlarge(essai,50)
cv.rectangle(NewMatrix, (NewMatrix.shape[1]-carre,NewMatrix.shape[0]-carre),(NewMatrix.shape[1],NewMatrix.shape[0]), (255,255,0),5)
cv.imshow("The three infos combined together",NewMatrix)

cv.waitKey(0)
