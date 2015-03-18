function [projectionMatrix, est_A,est_R,est_T] = estimateCamera(Model3D, fidu_XY)
% Used for estimating face pose pose. This is part of the distribution for
% face image frontalization ("frontalization" software), described in [1].
%
% If you find this code useful and use it in your own work, please add
% reference to [1] and [2,3] for the calib function.
%
% Please see project page for more details:
%   http://www.openu.ac.il/home/hassner/projects/frontalize
%
% Please see demo.m for example usage.
%
% Input: 
%   Model3D: Detector struct with 2D-3D reference correspondences. 
%       This distribution comes with pre-prepared structs for two facial
%       feature detectors. Others can be produced with the function
%       makeNew3DModel.m
%   fidu_XY: Matrix of n x 2 facial feature coordinates obtained with the
%       same detector represented by the Model3D struct.
% Output:
%   projectionMatrix, est_A, est_R, est_T: Estimated projection matrix, 
%       intrinsic matric (est_A), camera rotation matrix (est_R) and
%       translation vector (est_T). 
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
    % remove bad points (point outside the 3d models
    fidu_XY(Model3D.indbad,:) = [];
    
    % compute pose using refrence 3D points + query 2D points
    [est_A,est_R,est_T]=doCalib(Model3D.sizeU(1),...
        Model3D.sizeU(2), fidu_XY,Model3D.threedee,...
        Model3D.outA,[],[]);

    % calculate projection matrix from camera rotation
    RT = [est_R est_T'];
    projectionMatrix = est_A * RT;
    
end
