g++ graph_gen.cpp -o graph_gen

for p in 0.2 0.3 0.4 0.5 0.6
do  
    cd graphs
    mkdir $p
    cd ..
    for n in {10..300}
    do
        echo instance $n $p
        ./graph_gen $n $p > graphs/$p/inst$n.gr
    done
done