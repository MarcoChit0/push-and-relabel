for size in 10 20 30 40 50 60 70 80 90 100
do
    echo instance $size
    python gen_ins.py $size $size > opm/instances/$size.ins

done