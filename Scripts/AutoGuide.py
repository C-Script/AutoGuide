import numpy as np
import os
from matplotlib import pyplot as plt
import cv2 
import csv
import glob
import time
im=cv2.imread('ak1.jpg',cv2.IMREAD_GRAYSCALE)
# print(im)*//
# cv.xfeatures2d.SIFT_create()
foldersPaths=[r'..\Data\train\Characters\Akhenaten',
r'..\Data\train\Characters\Cleopatra vii',
r'..\Data\train\Characters\hatshepsut',
r'..\Data\train\Characters\khufu',
r'..\Data\train\Characters\Nefrtiti',
r'..\Data\train\Characters\rahotep',
r'..\Data\train\Characters\rahotep and his wife',
r'..\Data\train\Characters\sesostris i',
r'..\Data\train\Characters\sesostris iii',
r'..\Data\train\Characters\sheik el balad',
r'..\Data\train\Characters\the dwarf seneb and his family',
r'..\Data\train\Characters\The seated scribe',
r'..\Data\train\Characters\Thutmose III',
r'..\Data\train\Characters\Tutankhamoun',
r'..\Data\train\Objects\apis',
r'..\Data\train\Objects\ceremonial chair of tutankhamoun',
r'..\Data\train\Objects\The bed of tutankhamoun',
r'..\Data\train\Objects\The chair of tut',
r'..\Data\train\Objects\The dagger of tut'
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
        # print(descriptors)
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

        return True
def modelInitAndTrain(featurs,labels,gamma=0.5,C=1):
    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_RBF)
    svm.setGamma(gamma)
    svm.setC(C)
    # svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
    svm.train(np.float32(featurs), cv2.ml.ROW_SAMPLE, np.int32(labels))
    return svm
def getDataset(filepath):
    arr = np.loadtxt(filepath, delimiter=',')
    x, Y = arr[:, :-1], arr[:, -1]
    return x,Y
if __name__ == '__main__':
    if( not (os.path.exists('pharos.xml'))):
        print('oops, can\'t find any saved models,please be patient :)')
        if(not (os.path.exists(filename))):
            print('sounds like it\'s the first time you run the great Model,please be patient extracting features...')
            if(saveExtractedFeatures()):
                print('congrats , we have successfully extracted the features ,and it\'s ready to be feed to the classifier...')
                x,Y=getDataset(filename)
                print('training the model , you need to be patient :)')
                start =time.time()
                svm=modelInitAndTrain(x,Y,C=2.67, gamma=5.383)
                end=time.time()
                print('training time = ',(end-start),' S')
                print('congrats, saving the model...')
                svm.save('pharos.xml')
        else:
            print('great!, we found the features file ,that will save you some time')
            x, Y = getDataset(filename)
            print('training the model , you need to be patient :)')
            start=time.time()
            svm = modelInitAndTrain(x, Y,C=2.67, gamma=5.383)
            end=time.time()
            print('training time = ', (end - start),' S')
            print('congrats, saving the model...')
            svm.save('pharos.xml')
            while(1):
                testImage = input('model ready to be tested ,please enter the full path of an image to be tested:\n')
                sampleImage = cv2.imread(testImage, cv2.IMREAD_GRAYSCALE)
                k, imgDesc = gen_sift_features(sampleImage)
                response, arr = svm.predict((imgDesc))
                # print(response)
                print('this image belongs to class :#',response)
                y=input('do you want to try another image ? y/n: ')
                if (not (y.lower()) == 'y'):
                    print('thanks! ')
                    break
    else:
        print('loading the model...')
        svm=cv2.ml.SVM_load('pharos.xml')
        while(1):
            testImage=input('model ready to be tested ,please enter the full path of an image to be tested:\n')
            sampleImage=cv2.imread(testImage,cv2.IMREAD_GRAYSCALE)
            k,imgDesc=gen_sift_features(sampleImage)
            # print((imgDesc))
            # sampleImage=np.reshape(sampleImage,(1,128))
            # sampleImage=sampleImage.reshpe(1,128)
            response,arr = svm.predict((imgDesc))
            # print(arr)
            print('this image belongs to class :#',response)
            y=input('do you want to try another image ? y/n: ')
            if(not(y.lower())=='y'):
                print('thanks! ')
                break









#testing stuff

# grayimg=to_gray(im)
# print(seated_img.shape)
# kp1,desc1=gen_sift_features(seated_img)
# print(desc1)
# show_sift_features(grayimg,im,kp1)
# plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()