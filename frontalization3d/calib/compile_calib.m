function compile_calib(LIB_PATH,USE_CV_TWO_ONE)
cmd='mex calib.cpp POSIT.cpp util/util.cpp -Iutil/ ';
if USE_CV_TWO_ONE
    cmd=[cmd '-lcv -lcxcore'];
else
    cmd=[cmd '-lopencv_calib3d -lopencv_core '];
end
if exist('LIB_PATH','var') && ~isempty(LIB_PATH)
    libpath=fullfile(LIB_PATH,'lib');
    incpath=fullfile(LIB_PATH,'include');
    cmd=[cmd sprintf(' -L%s/ -I%s',libpath,incpath)];
end
fprintf('Executing %s\n',cmd);
eval(cmd);