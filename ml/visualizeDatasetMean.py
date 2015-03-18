import caffe
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import ndimage

if len(sys.argv) != 2:
	print "Usage: python visualizeDatasetMean.py path_to_mean.binaryproto"
	sys.exit()

blob = caffe.proto.caffe_pb2.BlobProto()
data = open( sys.argv[1] , 'rb' ).read()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
out = arr[0]

data2 = np.rollaxis(out[0], 0, 2) 
data_rotated =  ndimage.rotate(data2, -90)

plt.imshow(data_rotated)
plt.show()