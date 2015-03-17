% Frontalize images in pic5 data set.
% Adapted from provided file demo.m.

clear all;

add_to_search_path; % set up paths

input_path = '../../pic5/train/';
%input_path = '../../pic5/val/'; %TODO dont forget to switch output path

% load some data
load eyemask eyemask % mask to exclude eyes from symmetry
load DataAlign2LFWa REFSZ REFTFORM % similarity transf. from rendered view to LFW-a coordinates

% Detect facial features with prefered facial feature detector 
% detector = 'SDM'; % alternatively 'ZhuRamanan'
detector = 'ZhuRamanan';
load model3DZhuRamanan Model3D % reference 3D points corresponding to Zhu & Ramanan detections

%%% Load some constant data for Zhu-Ramanan detector
        addpath(genpath('face-release1.0-basic'))
        load('face-release1.0-basic/face_p146_small.mat','model');
        model.interval = 5;
        model.thresh = min(-0.65, model.thresh);
        if length(model.components)==13 
            posemap = 90:-15:-90;
        elseif length(model.components)==18
            posemap = [90:-15:15 0 0 0 0 0 0 -15:-15:-90];
        else
            error('Can not recognize this model');
        end
%%% End load

addpath calib

error_file = fopen('errors.txt', 'w');

dir_files = dir(input_path);
n_files = length(dir_files);

for file_index = 1 : n_files
  query_image_fn = [input_path, dir_files(file_index).name];
  if mod(file_index, 100) == 0
    file_index
  end

try
  [pathname, filename, ext] = fileparts(query_image_fn);
  if strcmp(ext, '.jpg') ~= 1
    continue
  end
  I_Q = imread(query_image_fn);

  % Note that the results in the paper were produced using SDM. We have found
  % other detectors to produce inferior frontalization results. 
  % (Bummer. The SDM code is not publicly available anymore.)
  fidu_XY = [];

  %%% Detect facial features (pasted in part of facial_feature_detection.m)
  % Zhu and Ramanan detector
        
  % detect facial features on query
        
  I_Q_bs = detect(I_Q, model, model.thresh);
  if isempty(I_Q_bs)
    return
  end

  I_Q_bs = clipboxes(I_Q, I_Q_bs);
  I_Q_bs = nms_face(I_Q_bs,0.3);

  if (isempty(I_Q_bs))
    return;
  end
  x1 = I_Q_bs(1).xy(:,1);
  y1 = I_Q_bs(1).xy(:,2);
  x2 = I_Q_bs(1).xy(:,3);
  y2 = I_Q_bs(1).xy(:,4);
  fidu_XY = [(x1+x2)/2,(y1+y2)/2];
  %%% End facial feature detection

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
    
  % Save results
  output_dir = '../../pic5_frontal/train/';
  [pathname, filename, ext] = fileparts(query_image_fn);
  imwrite(I_Q, [output_dir, filename, ext]);
  imwrite(frontal_raw, [output_dir, filename, '_front_nosym', ext]);
  imwrite(frontal_sym, [output_dir, filename, '_front_softsym', ext]);

catch ME
  disp(['Failed to frontalize image: ', query_image_fn]);
  fprintf(error_file, ['Failed to frontalize image: ', query_image_fn, '\n']);
  continue;
end

end

disp(['all done?']);

fclose(error_file);
