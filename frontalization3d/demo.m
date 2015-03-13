% DEMO script for frontalizing faces, based on the method described in [1]
% This demo produces a frontalized face for the image test.jpg
%
% If you find this code useful and use it in your own work, please add
% reference to [1] and, if appropriate, any of the other papers mentioned below.
%
% Dependencies: 
%   The demo uses the following dependencies. You MUST have these installed and
%   available on the MATLAB path:
%   1. calib function available from [2,3], required for estimating the query
%       camera projection matrix, C_Q. Calib functions are assumed to be
%       under folder <frontalization>/calib
%   2. Facial feature detection functions. The demo provides examples
%       showing frontalization results obtained using the SDM method [4] (default) 
%       and the facial feature detector of Zhu and Ramanan [5]. Please see
%       the script facial_feature_detection.m on how to use these (as well as 
%       edit paths to the detector used in practice, in case these differ from 
%       the ones in the script). See the function makeNew3DModel.m in case
%       a different facial feature detector is used.
%   3. OpenCV required by calib for calibration routines and some of the
%       detectors for cascase classifiers (e.g., SDM)
%
%  References:
%   [1] Tal Hassner, Shai Harel, Eran Paz, Roee Enbar, "Effective Face
%   Frontalization in Unconstrained Images," forthcoming. 
%   See project page for more details: 
%   http://www.openu.ac.il/home/hassner/projects/frontalize
%
%   [2] T. Hassner, L. Assif, and L. Wolf, "When Standard RANSAC is Not Enough: Cross-Media 
%   Visual Matching with Hypothesis Relevancy," Machine Vision and Applications (MVAP), 
%   Volume 25, Issue 4, Page 971-983, 2014 
%   Available: http://www.openu.ac.il/home/hassner/projects/poses/
%
%   [3] T. Hassner, "Viewing Real-World Faces in 3D," International Conference on Computer Vision (ICCV), 
%   Sydney, Austraila, Dec. 2013
%   Available: http://www.openu.ac.il/home/hassner/projects/poses/
%
%   [4] X. Xiong and F. De la Torre, "Supervised Descent Method and its Application to Face
%   Alignment," IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2013
%   Available: http://www.humansensing.cs.cmu.edu/intraface
%
%   [5] X. Zhu, D. Ramanan. "Face detection, pose estimation and landmark localization in the wild," 
%   Computer Vision and Pattern Recognition (CVPR) Providence, Rhode Island, June 2012. 
%   Available: http://www.ics.uci.edu/~xzhu/face/
%
%   Copyright 2014, Tal Hassner
%   http://www.openu.ac.il/home/hassner/projects/frontalize
%
%
%   The SOFTWARE ("frontalization" and all included files) is provided "as is", without any
%   guarantee made as to its suitability or fitness for any particular use.
%   It may contain bugs, so use of this tool is at your own risk.
%   We take no responsibility for any damage that may unintentionally be caused
%   through its use.
%
%   ver 1.1, 14-Nov-2014
%
% clear;
% close all;
addpath calib

% Load query image
I_Q = imread('test.jpg');

% load some data
load eyemask eyemask % mask to exclude eyes from symmetry
load DataAlign2LFWa REFSZ REFTFORM % similarity transf. from rendered view to LFW-a coordinates

% Detect facial features with prefered facial feature detector 
% detector = 'SDM'; % alternatively 'ZhuRamanan'
detector = 'ZhuRamanan';

% Note that the results in the paper were produced using SDM. We have found
% other detectors to produce inferior frontalization results. 
fidu_XY = [];
facial_feature_detection;
if isempty(fidu_XY)
    error('Failed to detect facial features / find face in image.');
end

% Estimate projection matrix C_Q
[C_Q, ~,~,~] = estimateCamera(Model3D, fidu_XY);

% Render frontal view
[frontal_sym, frontal_raw] = Frontalize(C_Q, I_Q, Model3D.refU, eyemask);


% Apply similarity transform to LFW-a coordinate system, for compatability
% with existing methods and results
frontal_sym = imtransform(frontal_sym,REFTFORM,'XData',[1 REFSZ(2)], 'YData',[1 REFSZ(1)]);
frontal_raw = imtransform(frontal_raw,REFTFORM,'XData',[1 REFSZ(2)], 'YData',[1 REFSZ(1)]);
    

% Display results
figure; imshow(I_Q); title('Query photo');
figure; imshow(I_Q); hold on; plot(fidu_XY(:,1),fidu_XY(:,2),'.'); hold off; title('Query photo with detections overlaid');
figure; imshow(frontal_raw); title('Frontalilzed no symmetry');
figure; imshow(frontal_sym); title('Frontalilzed with soft symmetry');



