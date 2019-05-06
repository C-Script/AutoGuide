import cv2
import numpy as np 
from glob import glob
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from matplotlib import pyplot as plt

class ImageHelpers:
	def __init__(self):
		self.sift_object = cv2.xfeatures2d.SIFT_create()

	def gray(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		return gray

	def features(self, image):
		keypoints, descriptors = self.sift_object.detectAndCompute(image, None)
		return [keypoints, descriptors]


class BOVHelpers:
	def __init__(self, n_clusters = 20):
		self.n_clusters = n_clusters
		self.kmeans_obj = KMeans(n_clusters = n_clusters,verbose=True)
		self.kmeans_ret = None
		self.descriptor_vstack = None
		self.mega_histogram = None
		self.clf  = SVC(verbose=True,max_iter=1000,kernel='linear',decision_function_shape='ovo')
		self.MLP=MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=500, alpha=0.1,solver='adam', verbose=True,  random_state=21,tol=0.000000001)	

	def cluster(self):
		"""	
		cluster using KMeans algorithm, 

		"""
		self.kmeans_ret = self.kmeans_obj.fit_predict(self.descriptor_vstack)

	def developVocabulary(self,n_images, descriptor_list, kmeans_ret = None):
		
		"""
		Each cluster denotes a particular visual word 
		Every image can be represeted as a combination of multiple 
		visual words. The best method is to generate a sparse histogram
		that contains the frequency of occurence of each visual word 

		Thus the vocabulary comprises of a set of histograms of encompassing
		all descriptions for all images

		"""

		self.mega_histogram = np.array([np.zeros(self.n_clusters) for i in range(n_images)])
		old_count = 0
		for i in range(n_images):
			l = len(descriptor_list[i])
			for j in range(l):
				if kmeans_ret is None:
					idx = self.kmeans_ret[old_count+j]
				else:
					idx = kmeans_ret[old_count+j]
				self.mega_histogram[i][idx] += 1
			old_count += l
		print("Vocabulary Histogram Generated")

	def standardize(self, std=None):
		"""
		
		standardize is required to normalize the distribution
		wrt sample size and features. If not normalized, the classifier may become
		biased due to steep variances.

		"""
		if std is None:
			self.scale = StandardScaler().fit(self.mega_histogram)
			self.mega_histogram = self.scale.transform(self.mega_histogram)
		else:
			print("STD not none. External STD supplied")
			self.mega_histogram = std.transform(self.mega_histogram)

	def formatND(self, l):
		"""	
		restructures list into vstack array of shape
		M samples x N features for sklearn

		"""
		vStack = np.array(l[0])
		for remaining in l[1:]:
			vStack = np.vstack((vStack, remaining))
		self.descriptor_vstack = vStack.copy()
		return vStack

	def train(self, train_labels):
		"""
		uses sklearn.svm.SVC classifier (SVM) 


		"""
		print( "Training SVM")
		print( self.clf)
		print( "Train labels", train_labels)
		self.clf.fit(self.mega_histogram, train_labels)
		print( "Training completed")

	def trainMLP(self,train_labels):
		self.MLP.fit(self.mega_histogram,train_labels)

	def predict(self, iplist):
		predictions = self.clf.predict(iplist)
		return predictions
	def predictMLP(self,iplist):
		predictions=self.MLP.predict(iplist)
		return predictions
	def plotHist(self, vocabulary = None):
		print( "Plotting histogram")
		if vocabulary is None:
			vocabulary = self.mega_histogram

		x_scalar = np.arange(self.n_clusters)
		y_scalar = np.array([abs(np.sum(vocabulary[:,h], dtype=np.int32)) for h in range(self.n_clusters)])

		print( y_scalar)

		plt.bar(x_scalar, y_scalar)
		plt.xlabel("Visual Word Index")
		plt.ylabel("Frequency")
		plt.title("Complete Vocabulary Generated")
		plt.xticks(x_scalar + 0.4, x_scalar)
		plt.show()
	def ModelSave(self,name):
		joblib.dump(self.clf,name)
		joblib.dump(self.scale,'Scale'+name)
		joblib.dump(self.kmeans_obj,'Kmeans'+name)
	def ModelLoad(self,name):
		self.kmeans_obj=joblib.load('Kmeans'+name)
		self.scale=joblib.load('Scale'+name)
		print(self.kmeans_obj)
		self.clf=joblib.load(name)
	def SaveKmeansScale(self,name):
		joblib.dump(self.kmeans_obj, 'MLPKmeans'+name)
		joblib.dump(self.scale, 'MLPScale'+name)
		joblib.dump(self.kmeans_ret,'Kmeans_ret'+name)
	def LoadKmeansScale(self,name):
		self.scale = joblib.load('Scale'+name)
		self.kmeans_obj = joblib.load('Kmeans'+name)
		self.kmeans_ret=joblib.load('Kmeans_ret'+name)
	def LoadMLP(self,name):
		self.MLP = joblib.load('MLP'+name)
	def SaveMLP(self,name):
		joblib.dump(self.MLP,'MLP'+name)
class FileHelpers:

	def __init__(self):
		pass

	def getFiles(self, path):
		"""
		- returns  a dictionary of all files 
		having key => value as  objectname => image path

		- returns total number of files.

		"""
		imlist = {}
		count = 0
		for each in glob(path + "/*"):
			print(each)
			word = each.split("/")[-1]
			print(word)
			print( " #### Reading image category ", word, " ##### ")
			imlist[word] = []
			for imagefile in glob(path+'/'+word+"/*.jpg"):
				print(imagefile)
				print( "Reading file ", imagefile)
				try:
					im = cv2.imread(imagefile, 0)
				except:
					print('image {}  error '.format(imagefile))
					continue
				imlist[word].append(im)
				count +=1

		return imlist, count