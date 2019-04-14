import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def exists(image, template,method,thresh):

    digit_res = cv.matchTemplate(image, template,method)
    loc = np.where(digit_res >= thresh)

    if len(loc[-1]) == 0:
        return False,digit_res

    for pt in zip(*loc[::-1]):
        if digit_res[pt[1]][pt[0]] == 1:
            return False,digit_res

    return True ,digit_res


img = cv.imread('nf_image1.jpg',0)
img2 = img.copy()
template = cv.imread('nf_template_e.jpg',0)
w, h = template.shape[::-1]
threshold=0.95
title=''
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    flag,res = exists(img,template,method,threshold)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    if not flag :
        title='Wrong Detection'
    else:
        title='Detected point'
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title(title), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()