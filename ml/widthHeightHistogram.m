clear; close all;

% Which folder {train, test}
FOLDER = 'train_square/';

% Get the list of images
fnames = dir([FOLDER '*.jpg']);
num_images = length(fnames);
image_names = cell(1, num_images);
for i = 1:num_images
   image_names{i} = [fnames(i).name]; 
end

heights = zeros(1, num_images);
tic
for i = 1:num_images
    img = imread([FOLDER image_names{i}], 'jpeg');
    [H, W] = size(img);
    heights(i) = H;
    
    if mod(i, 1000) == 0
        fprintf('Finished %i, Elapsed: %d\n', i, toc);
    end
end