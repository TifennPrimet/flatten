#from distutils import extension
import numpy as np
import cv2 as cv
import glob
import doctest

def findCorners( path, extention, row, columns, criteria, val):
    """"
    Function that calculates the distortions parameters 
    Parameters
    ----------
    path : string
        path where the images are strored
    extention : string
        .png, .jpg the extension of you images
    row : int
        number of rows of the chessboard
    columns : int 
        number of columns of the chessboard
    criteria : TermCriteria 
        Criteria for termination of the iterative process of corner refinement.
        That is, the process of corner position refinement stops either after criteria.
        maxCount iterations or when the corner position moves by less than criteria.epsilon on some iteration. 
    val : int 
    	Various operation flags that can be zero or a combination of the following values:
            CALIB_CB_ADAPTIVE_THRESH Use adaptive thresholding to convert the image to black and white, rather than a fixed threshold level (computed from the average image brightness).
            CALIB_CB_NORMALIZE_IMAGE Normalize the image gamma with equalizeHist before applying fixed or adaptive thresholding.
            CALIB_CB_FILTER_QUADS Use additional criteria (like contour area, perimeter, square-like shape) to filter out false quads extracted at the contour retrieval stage.
            CALIB_CB_FAST_CHECK Run a fast check on the image that looks for chessboard corners, and shortcut the call if none is found. This can drastically speed up the call in the degenerate condition when no chessboard is observed.

    Returns
    -------
    objpoints : <class 'list'>
        3d point in real world space
    imgpoints : <class 'list'>
        2d points in image plane.
    images : <class 'list'>
        list of the path to all the images
    mtx : <class 'numpy.ndarray'>
        3x3 floating-point camera intrinsic matrix
    dist : <class 'numpy.ndarray'>
        vector of distortion coefficients
    rvecs : <class 'tuple'>
        Output vector of rotation vectors
    tvecs : <class 'tuple'>
        vector of translation 
    """

    objp = np.zeros((row*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:columns,0:row].T.reshape(-1,2)                                 
    # Arrays to store object points and image points from all the images.
    objpoints = []                                                                  # 3d point in real world space sous la former de liste de  [6. 0. 0.]
    imgpoints = []                                                                  # 2d points in image plane. sous la forme de liste de liste  [[294.44348   54.95562 ]]
    images = glob.glob(path+'\*'+ extention , recursive = True)                              #donne tout les .jpg à l'addresse mensionnée
    print(images)
    nb_images = len(images)
    i = 0
    for fname in images:
        i+=1
        print(fname[len(path):],"image", i, "sur", nb_images)
        img = cv.imread(fname)      
        print(fname)                                                #ouvre l'image
        if "MS1" in fname or "MS2" in fname: 
            print('yep')
            img = img *2**4 

        r ,c, s =img.shape
        img = cv.resize(img,(int(c//2),int(r//2)))                                    #pour plus de rapidité de traitement on de dimmensionne l'image
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)                                    # on passe en niveaux de gris pour ne plus avoir des liste des listes
        if "MS1" in fname or "MS2" in fname: 
            print('yep')
            
            graytr = cv.threshold(gray, 0.01*gray.max(), 255,0)
        cv.imshow('im', img)
        cv.waitKey(100)
        cv.imshow('imgray', gray)
        cv.waitKey(100)
        print(gray)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (row,columns), criteria)        #val à la place de none           
        print(ret)                                                                   # True if chessboard found

        # If found, add object points, image points (after refining them)
        if ret:
                
            objpoints.append(objp) # on ajoute les coordonnées des points a la liste   
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)#affine la recherche des points du damier
            imgpoints.append(corners2)                                               # ajout des coornonées des points
            # Draw and display the corners
            cv.drawChessboardCorners(img, (row,columns), corners2, ret)                     #dessine les coins du damier sur l'image
            cv.imshow( fname[len(path) : -4], img)
            cv.waitKey(100)                                           # renvoie la liste des points en 3D ( chiffres ronds dans un refferentiel fixe), celles en 2D( coordonnées approx), et l'image en niveaux de gris et l'image en couleur
    print("fin des images")
    cv.destroyAllWindows()
   
    if ret : 
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        return objpoints, imgpoints, images, mtx, dist, rvecs, tvecs
    else : 
        return None





# path = 'D:\STAGE\MS\RGB'
# extention = '.jpg'
# row = 19
# columns = 12
# val = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FILTER_QUADS
# criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.00001)      
# findCorners( path, extention, row, columns, criteria, val)
# doctest.testmod()