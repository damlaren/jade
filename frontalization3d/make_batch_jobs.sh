#!/bin/bash
# http://www.mathworks.com/help/matlab/ref/matlablinux.html

n_files=20489

echo "#!/bin/bash" > matlab_jobs.sh
echo "" >> matlab_jobs.sh

for start_index in `seq 1 25 20489`; do
    end_index=`expr $start_index + 24`
    cmd="matlab -r \"frontalize_pic5(${start_index}, ${end_index}); exit;\""
    echo $cmd >> matlab_jobs.sh
    cmd="echo \"${start_index} - ${end_index} done\""
    echo $cmd >> matlab_jobs.sh
done
