function [A,R,T]=doCalib(width,height,imPoints,objPoints,A,RGuess,TGuess)
if isempty(RGuess) || isempty(TGuess)
    [A,R,T]=calib(width,height,imPoints,objPoints,A,0,1); %extrinsic only
else
    [A,R,T]=calib(width,height,imPoints,objPoints,A,0,2,RGuess,TGuess); %extrinsic only + use guess
end

inside = calcInside(A, R, T, width, height,objPoints);
if (inside==0)
    T=-T;
    t=pi;
	RRz180=[cos(t) -sin(t) 0;sin(t) cos(t) 0;0 0 1];
	R=RRz180*R;
end
end