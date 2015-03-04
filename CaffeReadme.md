# Getting Started with Caffe

Modified by Albert (March 4, 2015), Documentation originally from the official Caffe repo.

## Contents

1. Installing Caffe
2. Data Preparation
3. Hyperparameters

## 1. Installing Caffe

Installing Caffe section is from: https://github.com/BVLC/caffe/wiki/Ubuntu-14.04-VirtualBox-VM

This is a guide to setting up Caffe in a 14.04 virtual machine with CUDA 6.5 and the system Python for getting started with examples and PyCaffe.

* Download newest Ubuntu release. I used KUbuntu from http://cdimage.ubuntu.com/kubuntu/releases/trusty/release/kubuntu-14.04.1-desktop-amd64.iso
* Start VirtualBox, create a new virtual machine (Linux/Ubuntu/64bit/DynamicHD/8GbRAM/…). Then start the VM from the downloaded .iso (do this from inside VirtualBox). Installation of Kubuntu will begin.
* Install system updates (3.13.0-32 -> 3.13.0-36)
* Install build essentials:
  * `sudo apt-get install build-essential`
* Install latest version of kernel headers:
  * ``sudo apt-get install linux-headers-`uname -r` ``
* Install curl (for the CUDA download):
  * `sudo apt-get install curl`
* Download CUDA.
  * `cd ~/Downloads/`
  * `curl -O "http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run"`
* Make the downloaded installer file runnable:
  * `chmod +x cuda_6.5.14_linux_64.run`
* Run the CUDA installer:
  * ``sudo ./cuda_6.5.14_linux_64.run --kernel-source-path=/usr/src/linux-headers-`uname -r`/ ``
    * Accept the EULA
    * Do **NOT** install the graphics card drivers (since we are in a virtual machine)
    * Install the toolkit (leave path at default)
    * Install symbolic link
    * Install samples (leave path at default)
* Update the library path
  * `echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/lib' >> ~/.bashrc`
  * `source ~/.bashrc`
* Install dependencies:
  * `sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libatlas-base-dev git python-dev python-pip libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml`
  * `sudo easy_install pillow`
* Download Caffe:
  * `cd ~`
  * `git clone https://github.com/BVLC/caffe.git`
* Install python dependencies for Caffe:
  * `cd caffe`
  * `cat python/requirements.txt | xargs -L 1 sudo pip install`
* Add a couple of symbolic links for some reason:
  * `sudo ln -s /usr/include/python2.7/ /usr/local/include/python2.7`
  * `sudo ln -s /usr/local/lib/python2.7/dist-packages/numpy/core/include/numpy/ /usr/local/include/python2.7/numpy`
* Create a `Makefile.config` from the example:
  * `cp Makefile.config.example Makefile.config`
  * `nano Makefile.config`
    * Uncomment the line `# CPU_ONLY := 1`  (In a virtual machine we do not have access to the the GPU)
    * Under `PYTHON_INCLUDE`, replace `/usr/lib/python2.7/dist-packages/numpy/core/include` with `/usr/local/lib/python2.7/dist-packages/numpy/core/include` (i.e. add `/local`)
* Compile Caffe:
  * `make pycaffe`
  * `make all`
  * `make test`
* Download the ImageNet Caffe model and labels:
  * `./scripts/download_model_binary.py models/bvlc_reference_caffenet`
  * `./data/ilsvrc12/get_ilsvrc_aux.sh`
* Modify `python/classify.py` to add the `--print_results` option
  * Compare `https://github.com/jetpacapp/caffe/blob/master/python/classify.py` (version from 2014-07-18) to the current version of `classify.py` in the official Caffe distribution `https://github.com/BVLC/caffe/blob/master/python/classify.py` 
* Test your installation by running the ImageNet model on an image of a kitten:
  * `cd ~/caffe` (or whatever you called your Caffe directory)
  * `python python/classify.py --print_results examples/images/cat.jpg foo`
  * Expected result: `[('tabby', '0.27933'), ('tiger cat', '0.21915'), ('Egyptian cat', '0.16064'), ('lynx', '0.12844'), ('kit fox', '0.05155')]`
* Test your installation by training a net on the MNIST dataset of handwritten digits:
  * `cd ~/caffe` (or whatever you called your Caffe directory)
  * `./data/mnist/get_mnist.sh`
  * `./examples/mnist/create_mnist.sh`
  * `./examples/mnist/train_lenet.sh`
  * See http://caffe.berkeleyvision.org/gathered/examples/mnist.html for more information...

## 2. Data Preparation

See: http://caffe.berkeleyvision.org/gathered/examples/imagenet.html

### Lightning Memory-Mapped Database (LMDB) Creation

1. Navigate to `caffe/examples/imagenet/create_imagenet.sh` and modify the first 5 variables. It is best to use absolute paths. EXAMPLE, DATA, and TOOLS refer to Caffe folders while TRAIN_DATA_ROOT and VAL_DATA_ROOT refer to your own dataset paths.
2. If your images are not 256x256, change the RESIZE flag to true on line 14.
3. Copy your train.txt and val.txt labels into $DATA/ (see line 44 and 54)
4. Now run `caffe/examples/imagenet/create_imagenet.sh`. This may take several minutes depending on the size of your training data.

If you get the "Check failed: mkdir(db_path, 0744)" error, that means the lmdb folders have already been created. You need to delete them first.

### Compute the Mean Image

1. Navigate to `caffe/examples/imagenet/make_imagenet_mean.sh` and modify the three paths on lines 5 and 6 to use absolute paths.
2. Change `ilsvrc12_train_leveldb` to `ilsvrc12_train_lmdb`
3. Run `caffe/examples/imagenet/make_imagenet_mean.sh`. This should be faster than the LMDB creation.

### Select the Model

1. In `caffe/models/bvlc_reference_caffenet/train_val.prototxt` modify the paths again to use absolute paths. You can also modify parameters for each layer here.
2. In `caffe/models/bvlc_reference_caffenet/solver.prototxt` modify the paths to use absolute paths as well. Here you can modify the hyperparameters. Make sure to change GPU to CPU on the last line.
3. Make sure to modify the number of outputs in the last FC layer to match the number of classes

### Train the Model

To start training, run: `./build/tools/caffe train --solver=models/bvlc_reference_caffenet/solver.prototxt`

## 3. Hyperparameters
Note these files are located in: `CAFFE_HOME/models/model_name_here/`

* On the machine you will use (only need to do once on farmshare, will work for any machine), download and build Caffe. Follow the notes above for building. Note: the readme above (at least the part from Berkeley for building Caffe) is for building Caffe on a VM with a CPU only. Sometimes a step won't apply so use common sense to skip it or not.
* Test it to make sure everything is working with the pic5 gender classification. Follow the Data Preparation guide above.
* Only change settings to/from GPU/CPU if that’s actually what you want to use.

#### solver.prototxt
Example:
```
net: "/home/albert/caffe/models/faces_gender_net/train_val.prototxt"
test_iter: 58
test_interval: 416
base_lr: 0.001
lr_policy: "step"
gamma: 0.1
stepsize: 20000
display: 416
max_iter: 450000
momentum: 0.9
weight_decay: 0.0005
snapshot: 20000
snapshot_prefix: "/home/albert/caffe/models/faces_gender_net/gender_train"
solver_mode: GPU
```
##### Solver Explanation
* net: "/home/albert/caffe/models/faces_gender_net/train_val.prototxt"
    * Location of the ConvNet architecture file
* test_iter: 58
    * When we start the validation run, how many iterations should we do. This should be equal to VALIDATION_SIZE / BATCH_SIZE
* test_interval: 416
    * After this many training iterations, we will run the validation/test run
* base_lr: 0.001
    *  Starting learning rate
* lr_policy: "step"
    * This means we will decrease the learning rate after “stepsize” below
* gamma: 0.1
    * I think how much to decrease the learning rate (on a log scale?). Don't touch this
* stepsize: 20000
    * How often to decrease the learning rate
* display: 416
     * How often to display results to the screen. Should be NUM_TRAINING / BATCH_SIZE 
* max_iter: 450000
    * When to terminate
* momentum: 0.9
    * This is an advanced stochastic gradient descent modification, ignore for now
* weight_decay: 0.0005
    * Ignore this
* snapshot: 20000
    * How frequently to snapshot the network and write the weights to a file. This should be once every couple of hours. Do the math depending on how long one epoch takes. Here, 416 iterations is 1 epoch and this takes 3 minutes, so a snapshot will be saved once every 2.1 hours)
* snapshot_prefix: "/home/albert/caffe/models/faces_gender_net/gender_train"
    * The prefix of the snapshot file. it will be written as gender_train_00, gender_train01,...)
* solver_mode: GPU
    * GPUs all day every day!


#### train_val.prototxt

```
  data_param {
    source: "/home/albert/caffe/examples/imagenet/ilsvrc12_train_lmdb" 
    batch_size: 48 
    backend: LMDB
  }
```

* Near the top of the file you’ll see two “Data” layers, one for train and one for test. Make sure to update the paths to absolute references.
* The only value of interest here is the batch_size. This should be the same for the test and training layer (this is the same batch sized used in solver.prototxt).
* Set this to somewhere between 32 and 128 (if you can go this high). I say “if you can go this high” because the batch size dictates how much GPU memory is required. If you set it too high, you’ll run into a Caffe error when you try to run the file. If you set it too small (like 8 or 16) then the network will require more iterations to train. Play with it until you get to a nice number.
* My desktop’s GPU has 2 GB memory and batch size of 48 works fine. 64 gives me an error.

#### Classification
At the bottom of `train_val.prototxt`, we need to change the output layer to match the number of classes we have. Find the ``fc8`` layer and where it says:
```
  inner_product_param {
    num_output: 2
    ...
  }
```
The `num_output` here should be equal to the number of output classes you have. (Usually) at the very bottom of `train_val.prototxt`, you will see a layer titled `loss`. For classification this should be `type: "SoftmaxWithLoss"`.

#### Regression
For the `loss` layer we will use `EuclideanLoss` and have one output node from the fully connected `fc8` layer. This requires a different Data Preparation step which will be updated here soon. (Need to use HD5 format instead of LMDB)