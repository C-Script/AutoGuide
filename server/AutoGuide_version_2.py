import cv2
import numpy as np 
from glob import glob 
import argparse
from helpers import *
import time
import sys
from matplotlib import pyplot as plt 


class BOV:
    def __init__(self, no_clusters,modelName='pharos.pkl'):
        self.no_clusters = no_clusters
        self.modelName=modelName
        self.train_path = None
        self.test_path = None
        self.im_helper = ImageHelpers()
        self.bov_helper = BOVHelpers(no_clusters)
        self.file_helper = FileHelpers()
        self.images = None
        self.trainImageCount = 0
        self.train_labels = np.array([])
        self.name_dict = {}
        self.descriptor_list = []

    def trainModel(self):
        """
        This method contains the entire module 
        required for training the bag of visual words model

        Use of helper functions will be extensive.

        """

        # read file. prepare file lists.
        self.images, self.trainImageCount = self.file_helper.getFiles(self.train_path)
        # extract SIFT Features from each image
        label_count = 0 
        for word, imlist in self.images.items():
            self.name_dict[str(label_count)] = word
            print( "Computing Features for ", word)
            for im in imlist:
                # print(im)
                # cv2.imshow("im", im)
                # cv2.waitKey(0)
                self.train_labels = np.append(self.train_labels, label_count)
                try:
                    kp, des = self.im_helper.features(im)
                except:
                    continue
                self.descriptor_list.append(des)

            label_count += 1


        # perform clustering
        # print(self.descriptor_list)
        bov_descriptor_stack = self.bov_helper.formatND(self.descriptor_list)
        self.bov_helper.cluster()
        self.bov_helper.developVocabulary(n_images = self.trainImageCount, descriptor_list=self.descriptor_list)

        # show vocabulary trained
        # self.bov_helper.plotHist()
 

        self.bov_helper.standardize()
        self.bov_helper.train(self.train_labels)

    def trainMLP(self):
        """
        This method contains the entire module 
        required for training the bag of visual words model

        Use of helper functions will be extensive.

        """

        # read file. prepare file lists.
        self.images, self.trainImageCount = self.file_helper.getFiles(self.train_path)
        # extract SIFT Features from each image
        label_count = 0 
        for word, imlist in self.images.items():
            self.name_dict[str(label_count)] = word
            print( "Computing Features for ", word)
            for im in imlist:
                # print(im)
                # cv2.imshow("im", im)
                # cv2.waitKey(0)
                self.train_labels = np.append(self.train_labels, label_count)
                # try:
                kp, des = self.im_helper.features(im)
                # except:
                    # continue
                self.descriptor_list.append(des)

            label_count += 1

        # print(self.descriptor_list)
        # perform clustering
        # print(self.descriptor_list)
        bov_descriptor_stack = self.bov_helper.formatND(self.descriptor_list)
        self.bov_helper.cluster()
        self.bov_helper.developVocabulary(n_images = self.trainImageCount, descriptor_list=self.descriptor_list)

        # show vocabulary trained
        # self.bov_helper.plotHist()
 

        self.bov_helper.standardize()
        self.bov_helper.trainMLP(self.train_labels)

    def recognize(self,test_img,classifier,test_image_path=None):

        """ 
        This method recognizes a single image 
        It can be utilized individually as well.


        """

        kp, des = self.im_helper.features(test_img)
        # print kp
        print( des.shape)

        # generate vocab for test image
        vocab = np.array( [[ 0 for i in range(self.no_clusters)]])
        # locate nearest clusters for each of 
        # the visual word (feature) present in the image
        
        # test_ret =<> return of kmeans nearest clusters for N features
        test_ret = self.bov_helper.kmeans_obj.predict(des)
        # print test_ret

        # print vocab
        for each in test_ret:
            vocab[0][each] += 1

        print( vocab)
        # Scale the features
        vocab = self.bov_helper.scale.transform(vocab)

        # predict the class of the image
        if(classifier=='svm'):
            lb = self.bov_helper.clf.predict(vocab)
            return lb
        else:
            lb = self.bov_helper.MLP.predict(vocab)
            return lb
        # print "Image belongs to class : ", self.name_dict[str(int(lb[0]))]
        



    def testModel(self,classifier):
        """ 
        This method is to test the trained classifier

        read all images from testing path 
        use BOVHelpers.predict() function to obtain classes of each image

        """

        self.testImages, self.testImageCount = self.file_helper.getFiles(self.test_path)

        predictions = []

        for word, imlist in self.testImages.items():
            print( "processing " ,word)
            for im in imlist:
                # print imlist[0].shape, imlist[1].shape
                print( im.shape)
                cl = self.recognize(im,classifier)
                print( cl)
                predictions.append({
                    'image':im,
                    'class':cl,
                    'object_name':self.name_dict[str(int(cl[0]))]
                    })

        print(predictions)
        # for each in predictions:
        #     # cv2.imshow(each['object_name'], each['image'])
        #     # cv2.waitKey()
        #     # cv2.destroyWindow(each['object_name'])
        #     # 
        #     plt.imshow(cv2.cvtColor(each['image'], cv2.COLOR_GRAY2RGB))
        #     plt.title(each['object_name'])
        #     plt.show()
        return predictions

    def print_vars(self):
        pass
    def saveModel(self):
        self.bov_helper.ModelSave(self.modelName)
        joblib.dump(self.name_dict,'NameDict'+self.modelName)
    def loadModel(self):
        self.bov_helper.ModelLoad(self.modelName)
        self.name_dict=joblib.load('NameDict'+self.modelName)
    def SaveKmeansScaleAndDic(self):
        self.bov_helper.SaveKmeansScale(self.modelName)
        joblib.dump(self.name_dict, 'NameDict'+self.modelName)
    def LoadKmeansScaleAndDic(self):    
        self.bov_helper.LoadKmeansScale(self.modelName)
        self.name_dict = joblib.load('NameDict'+self.modelName)
    def SaveMLP(self):
        self.bov_helper.SaveMLP(self.modelName)
    def LoadMLP(self):
        self.bov_helper.LoadMLP(self.modelName)

def testingMain(n_clusters, Testpath,classifier='mlp'):
    bov = BOV(no_clusters=n_clusters)
    bov.test_path=Testpath
    # loading the svm classifier
    if(classifier.lower()=='svm'):
        bov.loadModel()
        predic=bov.testModel(classifier)
        return predic[0]['object_name']
    # loading the mlp classifer
    else:
        bov.LoadMLP()
        bov.LoadKmeansScaleAndDic()
        predic=bov.testModel(classifier)
        return predic[0]['object_name']
