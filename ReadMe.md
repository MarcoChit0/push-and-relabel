Para gerar grafos: 
./run_graph_gen.sh


Para rodar o algoritmo de push and relabel em todos os gráficos: 
./run_main.sh


Para gerar os plots dos dados:
python plot.py


Para gerar as tabelas dos dados:
python tables.py


Para rodar apenas o algoritmo de push and relabel:
python main.py < 'path_to_graph.gr'


Para rodar a redução do problema de Open Pit Mining para o problema do Fluxo Máximo:
python opm.py 'filename' < 'path_to_instance.ins'

opm.py salvará o arquivo 'filename'.pbm contendo a solução da instância do problema na pasta solutions. O algoritmo não converte a imagem da solução para .png