#!/usr/bin/env sh
# Compute the mean image from the imagenet training leveldb
# N.B. this is available in data/ilsvrc12

/home/albert/caffe/build/tools/compute_image_mean /home/albert/caffe/examples/imagenet/ilsvrc12_train_lmdb \
  /home/albert/caffe/data/ilsvrc12/imagenet_mean.binaryproto

echo "Done."
