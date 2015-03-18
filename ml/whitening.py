
#https://theclevermachine.wordpress.com/2013/03/30/the-statistical-whitening-transform/
inputdir = "/home/albert/Desktop/pic5_dataset/singles/"
outputdir = "/home/albert/Desktop/pic5_dataset/whitened/"

# https://gist.github.com/duschendestroyer/5170087
import numpy as np
from scipy import linalg
from scipy import misc
from sklearn.utils import array2d, as_float_array
from sklearn.base import TransformerMixin, BaseEstimator
import matplotlib.pyplot as plt
import os

# filename = '00026eb27c4918da6470f236536be805_face_0.jpg'
allfiles = os.listdir(inputdir)
imagefiles = [f for f in allfiles if f[-4:] == '.jpg']
#chunksize = len(imagefiles)
chunksize = 10
RESIZED = 64

X = np.zeros((chunksize, RESIZED*RESIZED*3))

for i in xrange(chunksize):
    img = misc.imresize(misc.imread(inputdir + imagefiles[i]), (RESIZED,RESIZED,3))
    # print np.reshape(img, (1, 256*256*3))
    X[i,:] = np.reshape(img, (1, RESIZED*RESIZED*3))
    # X = misc.imresize(img, (256,256,3))[:,:,i]
    # plt.imshow(X)
    # plt.figure()

# the actual whitening: ########
X -= np.mean(X, axis=0) # zero-center the data (important)
cov = np.dot(X.T, X) / X.shape[0] # get the data covariance matrix


U,S,V = np.linalg.svd(cov)

Xrot = np.dot(X, U) # decorrelate the data

Xrot_reduced = np.dot(X, U[:,:]) # Xrot_reduced becomes [N x 100]

# whiten the data:
# divide by the eigenvalues (which are square roots of the singular values)
Xwhite = Xrot / np.sqrt(S + 1e-5)

#####################

for i in xrange(chunksize):
    newimg = Xwhite[i,:].reshape((RESIZED,RESIZED,3))
    misc.imsave(outputdir + imagefiles[i], newimg)

# plt.imshow(newimg)
# plt.show()

'''

class ZCA(BaseEstimator, TransformerMixin):
 
    def __init__(self, regularization=10**-5, copy=False):
        self.regularization = regularization
        self.copy = copy
 
    def fit(self, X, y=None):
        X = array2d(X)
        X = as_float_array(X, copy = self.copy)
        self.mean_ = np.mean(X, axis=0)
        X -= self.mean_
        sigma = np.dot(X.T,X) / X.shape[1]
        U, S, V = linalg.svd(sigma)
        tmp = np.dot(U, np.diag(1/np.sqrt(S+self.regularization)))
        self.components_ = np.dot(tmp, U.T)
        return self
 
    def transform(self, X):
        X = array2d(X)
        X_transformed = X - self.mean_
        X_transformed = np.dot(X_transformed, self.components_.T)
        return X_transformed
'''




'''
def whiten(X,fudge=1E-18):
   # the matrix X should be observations-by-components

   # get the covariance matrix
   Xcov = np.dot(X.T,X)

   # eigenvalue decomposition of the covariance matrix
   d, V = np.linalg.eigh(Xcov)

   # a fudge factor can be used so that eigenvectors associated with
   # small eigenvalues do not get overamplified.
   D = np.diag(1. / np.sqrt(d+fudge))

   # whitening matrix
   W = np.dot(np.dot(V, D), V.T)

   # multiply by the whitening matrix
   X_white = np.dot(X, W)

   return X_white, W
'''