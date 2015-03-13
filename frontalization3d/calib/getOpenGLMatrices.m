function [mv,projectionMatrix] = getOpenGLMatrices(A, R, T, width, height)
    projectionMatrix=zeros(4,4);

	nearPlane = 0.0001;
	farPlane = 10000;
TRIPLET=3;

	fx = A(1,1);
	fy = A(2,2);
	px = A(1,3);
	py = A(2,3);
	projectionMatrix(1) = 2.0 * fx / width;
	projectionMatrix(2) = 0.0;
	projectionMatrix(3) = 0.0;
	projectionMatrix(4) = 0.0;

	projectionMatrix(5) = 0.0;
	projectionMatrix(6) = 2.0 * fy / height;
	projectionMatrix(7) = 0.0;
	projectionMatrix(8) = 0.0;

	projectionMatrix(9) = 2.0 * (px / width) - 1.0;
	projectionMatrix(10) = 2.0 * (py / height) - 1.0;
	projectionMatrix(11) = -(farPlane + nearPlane) / (farPlane - nearPlane);
	projectionMatrix(12) = -1.0;

	projectionMatrix(13) = 0.0;
	projectionMatrix(14) = 0.0;
	projectionMatrix(15) = -2.0 * farPlane * nearPlane / (farPlane - nearPlane);
	projectionMatrix(16) = 0.0;


% 	//OpenGL's Y and Z axis are opposite to the camera model (OpenCV)
% 	//same as RRz(180)*RRy(180)*R:
% 	//  1.0000    0.0000    0.0000
% 	//  0.0000   -1.0000    0.0000		*		R
% 	//  0.0000         0   -1.0000
deg=180;
t=deg*pi/180.;

RRz=[cos(t) -sin(t) 0;sin(t) cos(t) 0;0 0 1];
RRy=[cos(t) 0 sin(t);0 1 0;-sin(t) 0 cos(t)];
R=RRz*RRy*R;

    mv=zeros(4,4);
    mv(1:3,1:3)=R;
	mv(4) = 0.0;
	mv(8) = 0.0;
	mv(12) = 0.0;
	mv(13) = T(1);
% 	// also invert Y and Z of translation
	mv(14) = -T(2);
	mv(15) = -T(3);
	mv(16) = 1.0;
end
