for size in 10 20 30 40 50 60 70 80 90 100
do
    echo instance $size
    pypy3 opm.py $size -opt=3 < opm/instances/$size.ins >> opm/data/$size.csv

done 