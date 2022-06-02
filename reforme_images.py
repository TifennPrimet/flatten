import cv2 as cv
import os 
def reforme_images(fname, path, extention, mtx, dist):
    """"
    Function that calibrates the images  according to the distortion matrix you gave it
    Parameters
    ----------
    path : string
        path where the images are strored
    extention : string
        .png, .jpg the extension of you images
    mtx : <class 'numpy.ndarray'>
        3x3 floating-point camera intrinsic matrix
    dist : <class 'numpy.ndarray'>
        vector of distortion coefficients
    """
    img = cv.imread(fname)
    r ,c, s =img.shape
    #img = cv.resize(img,(int(c),int(r)))                                    #l'image que l'on reforme doit avoir la même taille que les sample de travail
    h,w = img.shape[:2]
    # chemin = path + "\calibree" +(fname[len(path):]).strip(extention)
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    #remap
    # mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    # dst_remap = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)


    if roi !=(0,0,0,0):
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.waitKey(50)

    if not os.path.exists(path + '_flat'):
                os.makedirs(path + '_flat')

    cv.imwrite(path + '_flat' + fname[len(path):-4]+".png", dst)
    #cv.imwrite(chemin+ "_remap.png", dst_remap)
        
    cv.imshow('dst', dst)
    # cv.imshow('dst remap', dst_remap)
    cv.waitKey(50)
