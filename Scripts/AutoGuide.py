import numpy as np
import sys
from matplotlib import pyplot as plt
import cv2 
import csv
import glob
im=cv2.imread('ak1.jpg')
# print(im)*//
# cv.xfeatures2d.SIFT_create()
foldersPaths=[r'D:\Auto Guide\AutoGuide\Data\train\Characters\Akhenaten',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\Cleopatra vii',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\hatshepsut',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\khufu',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\Nefrtiti',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\rahotep',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\rahotep and his wife',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\sesostris i',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\sesostris iii',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\sheik el balad',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\the dwarf seneb and his family',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\The seated scribe',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\Thutmose III',
r'D:\Auto Guide\AutoGuide\Data\train\Characters\Tutankhamoun',
r'D:\Auto Guide\AutoGuide\Data\train\Objects\apis',
r'D:\Auto Guide\AutoGuide\Data\train\Objects\ceremonial chair of tutankhamoun',
r'D:\Auto Guide\AutoGuide\Data\train\Objects\The bed of tutankhamoun',
r'D:\Auto Guide\AutoGuide\Data\train\Objects\The chair of tut',
r'D:\Auto Guide\AutoGuide\Data\train\Objects\The dagger of tut'
]
filename='extractedFeatures.csv'

def writeTofile(row,label,fileName):
    # table=dgv.get_items()[3:]
    with open(fileName, mode='w', newline='') as f:
        file_writer = csv.writer(f,delimiter=',',dialect="excel", lineterminator="\n")
        for r in row:
            addlabel=np.append(r,label)
            file_writer.writerow(addlabel)

        # file_writer.writerow([label])
def appendToFile(row,label,fileName):
    # table=dgv.get_items()[3:]
    with open(fileName, mode='a', newline='') as f:
        file_writer = csv.writer(f,delimiter=',',dialect="excel", lineterminator="\n")
        # print(row)
        for r in row:
            addlabel = np.append(r, label)
            file_writer.writerow(addlabel)
        # file_writer.writerow([label])
def getFromFile(fileName):
    contents=[]
    with open(fileName, mode='r', newline='') as f:
        file_reader = csv.reader(f,delimiter=';',dialect="excel", lineterminator="\n")
        for row in file_reader:
            contents.append(row)
        # print(contents)
        # sys.exit()
        return (contents)



def exists(image, template,method,thresh):

    digit_res = cv2.matchTemplate(image, template,method)
    loc = np.where(digit_res >= thresh)

    if len(loc[-1]) == 0:
        return False,digit_res

    for pt in zip(*loc[::-1]):
        if digit_res[pt[1]][pt[0]] == 1:
            return False,digit_res

    return True ,digit_res

def split2d(img, cell_size, flatten=True):
    h, w = img.shape[:2]
    sx, sy = cell_size
    cells = [np.hsplit(row, w//sx) for row in np.vsplit(img, h//sy)]
    cells = np.array(cells)
    if flatten:
        cells = cells.reshape(-1, sy, sx)
    return cells
def gen_sift_features(gray_img):
    sift = cv2.xfeatures2d.SIFT_create()
    # kp is the keypoints
    #
    # desc is the SIFT descriptors, they're 128-dimensional vectors
    # that we can use for our final features
    kp, desc = sift.detectAndCompute(gray_img, None)
    return kp, desc
def show_sift_features(gray_img, color_img, kp):
    return plt.imshow(cv2.drawKeypoints(gray_img, kp, color_img.copy()))

def to_gray(color_img):
    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    return gray
def getFolderImages(folderPath,ext='jpg'):
    images = [cv2.imread(f) for f in glob.glob(folderPath+'\*.'+ext)]
    return images
def saveExtractedFeatures():
        descriptors=np.zeros((0,128))
        print(descriptors)
        # sys.exit()
        for i,folder in enumerate(foldersPaths):
                images=getFolderImages(folder)
                for j,image in enumerate(images):
                        grayimage=to_gray(image)
                        # print(grayimage.shape)
                        kp,desc=gen_sift_features(grayimage)
                        # descriptors=descriptors.reshape(desc.shape)
                        print('F#{} IMG#{}'.format(i,j),desc.shape)
                        # print(desc,len(desc[0])) #for testing
                        # print('one desc / ') #// for testing
                        # for r in desc:
                        #     descriptors=np.append(descriptors,[r],axis=0)
                        # print(descriptors.shape)

                        # continue #//for testing
                        # desc.append(i)
                        if(i==0):
                                writeTofile(desc,i,filename)
                                # sys.exit()
                        else:
                                appendToFile(desc,i,filename)

                # res = np.array(descriptors)
                # print(res)
                # print(len(descriptors))
                # sys.exit()

# digits_img = cv2.imread('ak1.jpg', cv2.IMREAD_GRAYSCALE)
# digits = split2d(digits_img, (20, 20))
# cv2.imshow(digits)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# arr=np.loadtxt(filename,delimiter=',')
# print(arr.shape)
# sys.exit()
saveExtractedFeatures()
# grayimg=to_gray(im)
# kp1,desc2=gen_sift_features(grayimg)
# print(desc2)
# show_sift_features(grayimg,im,kp1)
# plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()