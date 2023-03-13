from math import floor
import sys
import networkx as nx

def opm_to_flow():
    args = input().split(' ')
    width = int(args[0])
    height = int(args[1])
    filename = 'w' + args[0] + '_h' + args[1] 
    costs = []
    max_cost = 1
    # linhas
    for row in range(height):
        c = input().split(' ')
        if '' in c: 
            c.remove('')
        # colunas
        for column in range(width):
            c[column] = int(c[column])
            max_cost += abs(c[column])
        costs.append(c)
    source, sink = (width*height)+1, (width*height)+2
    g = nx.DiGraph()

    for row in range(height):
        for column in range(width):
            if costs[row][column] >= 0:
                u, v, c = source, (width * row) + column + 1, costs[row][column]
            else:
                u, v, c = (width * row) + column + 1, sink , -costs[row][column]
            g.add_edge(str(u), str(v), capacity=c)
    for row in range(height):
        if row > 0:
            for column in range(width):
                g.add_edge(str((width * row) + column + 1), str((width * (row-1)) + column + 1), capacity= max_cost)
                if column >= 1:
                    g.add_edge(str((width * row) + column + 1), str((width * (row-1)) + (column-1) + 1), capacity= max_cost)
                if column + 1 < width :
                    g.add_edge(str((width * row) + column + 1), str((width * (row-1)) + (column+1) + 1), capacity= max_cost)
    cut_value, partition = nx.minimum_cut(g, str(source), str(sink))
    reachable, non_reachable = partition
    selected = []
    for row in range(height):
        line = []
        for column in range(width):
            v = (row*width) + column + 1
            if not v == source and not v == sink and str(v) in reachable:
                line.append(1)
            else:
                line.append(0)
        selected.append(line)
    solutions_file = 'opm/solutions/' + filename + '.pbm'
    with open(solutions_file, 'w') as f:
        f.write('P1\n# '+filename+'\n')
        f.write(str(width) + ' ' + str(height) + '\n')
        for row in range(height):
            line = ''
            for column in range(width):
                line += str(selected[row][column]) + ' '
            line = line[:-1]
            line += '\n'
            f.write(line)
opm_to_flow()