function inside = calcInside(A, R, T, width, height,objPoints)
frustum = ExtractFrustum(A, R, T, width, height);
inside=0;
for i=1:size(objPoints,1)
    if (PointInFrustum(objPoints(i,1),objPoints(i,2),objPoints(i,3),frustum)>0)
        inside=inside+1;
    end
end
% fprintf('inside %d of %d\n',inside,size(objPoints,1));
end