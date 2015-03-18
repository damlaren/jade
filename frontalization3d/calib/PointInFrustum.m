function bool = PointInFrustum(x, y, z,frustum)
%for p = 1:6
%changed to p=1:4 (ignore near,far) as OSG computes and changes these
%automatically (they are not constants)
for p = 1:4
    if (frustum(p,1) * x + frustum(p,2) * y + frustum(p,3) * z + frustum(p,4) <= 0)
        bool=0;
        return;
    end
end
bool=1;
end
