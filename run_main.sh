for p in 0.2 0.3 0.4 0.5 0.6
do  
    echo num_vertex,num_edges,maxflow,delta_t,num_pushes,num_relabels > data/$p.csv
    for n in {10..300}
    do
        for i in {1..30}
        do
            echo instance $n $p run $i
            python main.py < graphs/$p/inst$n.gr >> data/$p.csv
        done
    done
done