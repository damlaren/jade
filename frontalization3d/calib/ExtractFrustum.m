function frustum = ExtractFrustum(A, R, T, width, height)
[mv,proj] = getOpenGLMatrices(A, R, T, width, height);
clip=proj*mv;
frustum=zeros(6,4);
%/* Extract the numbers for the RIGHT plane */
frustum(1,1) = clip(4) - clip(1);
frustum(1,2) = clip(8) - clip(5);
frustum(1,3) = clip(12) - clip(9);
frustum(1,4) = clip(16) - clip(13);

% 	/* Normalize the result */
v=frustum(1,1:3);
t = sqrt(sum(v.*v));
frustum(1,:) =frustum(1,:)/t;

%	/* Extract the numbers for the LEFT plane */
frustum(2,1) = clip(4) + clip(1);
frustum(2,2) = clip(8) + clip(5);
frustum(2,3) = clip(12) + clip(9);
frustum(2,4) = clip(16) + clip(13);

% 	/* Normalize the result */
v=frustum(2,1:3);
t = sqrt(sum(v.*v));
frustum(2,:) =frustum(2,:)/t;

% 	/* Extract the BOTTOM plane */
frustum(3,1) = clip(4) + clip(2);
frustum(3,2) = clip(8) + clip(6);
frustum(3,3) = clip(12) + clip(10);
frustum(3,4) = clip(16) + clip(14);

% 	/* Normalize the result */
v=frustum(3,1:3);
t = sqrt(sum(v.*v));
frustum(3,:) =frustum(3,:)/t;


% 	/* Extract the TOP plane */
frustum(4,1) = clip(4) - clip(2);
frustum(4,2) = clip(8) - clip(6);
frustum(4,3) = clip(12) - clip(10);
frustum(4,4) = clip(16) - clip(14);

% 	/* Normalize the result */
v=frustum(4,1:3);
t = sqrt(sum(v.*v));
frustum(4,:) =frustum(4,:)/t;

% 	/* Extract the FAR plane */
frustum(5,1) = clip(4) - clip(3);
frustum(5,2) = clip(8) - clip(7);
frustum(5,3) = clip(12) - clip(11);
frustum(5,4) = clip(16) - clip(15);

% 	/* Normalize the result */
v=frustum(5,1:3);
t = sqrt(sum(v.*v));
frustum(5,:) =frustum(5,:)/t;

% 	/* Extract the NEAR plane */
frustum(6,1) = clip(4) + clip(3);
frustum(6,2) = clip(8) + clip(7);
frustum(6,3) = clip(12) + clip(11);
frustum(6,4) = clip(16) + clip(15);

% 	/* Normalize the result */
v=frustum(6,1:3);
t = sqrt(sum(v.*v));
frustum(6,:) =frustum(6,:)/t;
end