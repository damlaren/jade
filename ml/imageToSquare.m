clear; close all;

% Which folder {train, test}
FOLDER = 'train/';
TARGET_DIR = 'train64/';
RESIZE = 64;

% Get the list of images
fnames = dir([FOLDER '*.jpg']);
num_images = length(fnames);
image_names = cell(1, num_images);
for i = 1:num_images
   image_names{i} = [fnames(i).name]; 
end

% Loop through every image and do things
maxHeight = 0;
maxWidth = 0;
maxHeightIdx = 0;
maxHeightName = '';
maxWidthName = '';
maxWidthIdx = 0;
tic
for i = 1:num_images
    img = imread([FOLDER image_names{i}], 'jpeg');
    [H, W] = size(img);
    M = max(H,W);
    
    square = uint8(255*ones(M, M));
    % Place the (smaller) original image centered in the square image
    % Center it horizontally
    if W < M
        %fprintf('%i: center x\n',i);
        diff = M - W;
        if mod(diff, 2) == 0
            left = diff/2;
            right = diff/2;
        else
            % If the difference is odd
            left = uint32(diff/2);
            right = M - left - W;
        end
        square(:,left:end-right-1) = img;
    elseif H < M
        % Center it vertically
        %fprintf('%i: center y\n',i);
        diff = M - H;
        if mod(diff, 2) == 0
            top = diff/2;
            bot = diff/2;
        else
            % If the difference is odd
            top = uint32(diff/2);
            bot = M - top - H;
        end
        %fprintf('top: %i, H: %i, bot: %i, size: %i, W: %i\n',top,H,bot,M,W);
        square(top:end-bot-1,:) = img;
    else
        % Image is already a square
        square = img;
    end
    % Write the square image to file
    % Standardizing image sizes is done by someone else
    resized = imresize(square, [RESIZE RESIZE], 'bicubic', 'Antialiasing', true);
    imwrite(resized, [TARGET_DIR image_names{i}]);
    if mod(i, 1000) == 0
        fprintf('Finished %i, Elapsed: %d\n', i, toc);
    end
end