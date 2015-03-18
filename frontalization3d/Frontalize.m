function [frontal_sym, frontal_raw] = Frontalize(C_Q, I_Q, refU, eyemask)                                         
% Actual frontalization function. This is part of the distribution for
% face image frontalization ("frontalization" software), described in [1].
%
% If you find this code useful and use it in your own work, please add
% reference to [1].
%
% Please see project page for more details:
%   http://www.openu.ac.il/home/hassner/projects/frontalize
%
% Please see demo.m for example usage.
%
% Input: 
%   C_Q: Estimated camera projection matrix used to produce the query photo. 
%       Computed by estimateCamera.m
%   I_Q: Query photo
%   refU: NxMx3 matrix assigning each pixel in the reference (frontalized
%       coordinate system, the 3D coordinates of the surface of the face
%       projected onto that pixel. Available from Model3D.refU
%   eyemask: NxMx3 matrix with alpha weights for the eyes, in order to
%       exclude them from the symmetry.
%
% Output:
%   frontal_sym: Synthesized frontal view using soft symmetry.
%   frontal_raw: Synthesized frontal view without (before) soft symmetry.
%
%  References:
%   [1] Tal Hassner, Shai Harel, Eran Paz, Roee Enbar, "Effective Face
%   Frontalization in Unconstrained Images," forthcoming. 
%   See project page for more details: 
%   http://www.openu.ac.il/home/hassner/projects/frontalize
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
    ACC_CONST = 800; 
    I_Q = double(I_Q);

    bgind = sum(abs(refU),3)==0;

    % count the number of times each pixel in the query is accessed
    threedee = reshape(refU,[],3)';
    tmp_proj = C_Q * [threedee;ones(1,size(threedee,2))];
    tmp_proj2 = tmp_proj(1:2,:)./ repmat(tmp_proj(3,:),2,1);
    

    bad = min(tmp_proj2)<1 | tmp_proj2(2,:)>size(I_Q,1) | tmp_proj2(1,:)>size(I_Q,2) | bgind(:)';
    tmp_proj2(:,bad) = [];

    ind = sub2ind([size(I_Q,1),size(I_Q,2)], round(tmp_proj2(2,:)),round(tmp_proj2(1,:)));

    synth_frontal_acc = zeros(size(refU,1),size(refU,2));
    
    ind_frontal = 1:(size(refU,1)*size(refU,2));
    ind_frontal(bad) = [];
        
    [c,~,ic] = unique(ind);
    count = hist(ind,c);
    synth_frontal_acc(ind_frontal) = count(ic);

    synth_frontal_acc(bgind) = 0;
    synth_frontal_acc = imfilter(synth_frontal_acc,fspecial('gaussian', 16, 30),'same','replicate');
    
    % create synthetic view, without symmetry
    c1 = I_Q(:,:,1); f1 = zeros(size(synth_frontal_acc));
    c2 = I_Q(:,:,2); f2 = zeros(size(synth_frontal_acc));
    c3 = I_Q(:,:,3); f3 = zeros(size(synth_frontal_acc));
    
    f1(ind_frontal) = interp2(c1, tmp_proj2(1,:), tmp_proj2(2,:), 'cubic'); 
    f2(ind_frontal) = interp2(c2, tmp_proj2(1,:), tmp_proj2(2,:), 'cubic'); 
    f3(ind_frontal) = interp2(c3, tmp_proj2(1,:), tmp_proj2(2,:), 'cubic'); 
    frontal_raw = cat(3,f1,f2,f3);
    
    % which side has more occlusions?
    midcolumn = round(size(refU,2)/2);
    sumaccs = sum(synth_frontal_acc);
    sum_left = sum(sumaccs(1:midcolumn));
    sum_right = sum(sumaccs(midcolumn+1:end));
    sum_diff = sum_left - sum_right;
    
    if abs(sum_diff)>ACC_CONST % one side is occluded
        if sum_diff > ACC_CONST % left side of face has more occlusions
            weights = [zeros(size(refU,1),midcolumn), ones(size(refU,1),midcolumn)];
        else % right side of face has occlusions
            weights = [ones(size(refU,1),midcolumn), zeros(size(refU,1),midcolumn)];
        end
        weights = imfilter(weights, fspecial('gaussian', 33, 60.5),'same','replicate');
       
        % apply soft symmetry to use whatever parts are visible in ocluded
        % side
        synth_frontal_acc = synth_frontal_acc./max(synth_frontal_acc(:));
        weight_take_from_org = 1./exp(0.5+synth_frontal_acc);%
        weight_take_from_sym = 1-weight_take_from_org;
        
        weight_take_from_org = weight_take_from_org.*fliplr(weights);
        weight_take_from_sym = weight_take_from_sym.*fliplr(weights);
        
        weight_take_from_org = repmat(weight_take_from_org,[1,1,3]);
        weight_take_from_sym = repmat(weight_take_from_sym,[1,1,3]);
        weights = repmat(weights,[1,1,3]);
        
        denominator = weights + weight_take_from_org + weight_take_from_sym;
        frontal_sym = (frontal_raw.*weights + frontal_raw.*weight_take_from_org + flipdim(frontal_raw,2).*weight_take_from_sym)./denominator;
        
        % Exclude eyes from symmetry        
        frontal_sym = frontal_sym.*(1-eyemask) + frontal_raw.*eyemask;
        

    else %% both sides are occluded pretty much to the same extent -- do not use symmetry
        frontal_sym = uint8(frontal_raw);
    end
    frontal_raw = uint8(frontal_raw);
    frontal_sym = uint8(frontal_sym);
  
end