from copy import deepcopy
import datetime
import string
import sys
import time
graph_path = 'grafos/'

class Vertex:
    def __init__(self, n, e=0, h=0) -> None:
        self.node = n
        self.excess = e
        self.height = h

    def __str__(self) -> str:
        return 'n={}, e={}, h={}'.format(self.node, self.excess, self.height)

class Edge:
    def __init__(self, node_from:Vertex, node_to:Vertex, capacity:int, residual= None) -> None:
        self.node_from = node_from
        self.node_to = node_to
        self.capacity = capacity
        self.residual = residual
        self.max_capacity = deepcopy(capacity)

    def push(self, flow:int):
        self.capacity -= flow
        self.residual.capacity += flow

    def max_push(self):
        if self.capacity >= 0:
            self.residual.capacity = deepcopy(self.capacity)
            self.capacity = 0
    
    def __str__(self) -> str:
        return '[ {} ] -> [ {} ], c={}, mc={}'.format(self.node_from, self.node_to,self.capacity, self.max_capacity)

class AdjList:
    def __init__(self, num_vertex) -> None:
        self.adj_list = [[] for v in range(num_vertex)]
    
    def add_edge(self, node_from: Vertex, node_to:Vertex, new_edge: Edge):
        found = False
        for old_edge in self.adj_list[node_to.node - 1]:
            if old_edge.node_to.node == node_from.node:
                # delete old edge's residual edge
                edge_to_be_deleted = deepcopy(old_edge.residual)
                i = 0
                for edge in self.adj_list[edge_to_be_deleted.node_from.node-1]:
                    if edge.node_from.node == edge_to_be_deleted.node_from.node and edge.node_to.node == edge_to_be_deleted.node_to.node:
                        break
                    i += 1

                del self.adj_list[edge_to_be_deleted.node_from.node-1][i] 
                old_edge.residual = new_edge
                new_edge.residual = old_edge
                self.adj_list[node_from.node-1].append(new_edge)
                found = True
                break
        if not found:
            residual = Edge(node_to, node_from, 0, new_edge)
            new_edge.residual = residual
            self.adj_list[node_from.node-1].append(new_edge)
            self.adj_list[node_to.node-1].append(residual)

    def print(self):
        for uv_list in self.adj_list:
            for uv in uv_list:
                print(uv)


class Graph:
    def __init__(self):
        self.problem_type = None
        self.num_vertex = -1
        self.num_edges = -1
        self.source = -1
        self.sink = -1
        self.network = None
        self.num_pushes = -1
        self.num_relabels = -1
        self.file_name = ''
        self.vertex = []
        self.queue = []

    # OK
    def from_input(self):
        # get problem
        splited_line = get_line('p')
        self.problem_type, self.num_vertex, self.num_edges = splited_line[1], int(splited_line[2]), int(splited_line[3])
        self.get_source_and_sink()
        self.file_name = self.problem_type + 'flow_{}_{}'.format(self.source, self.sink)
        # get graph
        self.network = AdjList(self.num_vertex)
        self.vertex = [Vertex(i+1) for i in range(self.num_vertex)]
        for e in range(self.num_edges):
            splited_line = get_line('a')
            u, v, c = int(splited_line[1]), int(splited_line[2]), int(splited_line[3])
            edge = Edge(self.vertex[u-1], self.vertex[v-1], c)
            self.network.add_edge(self.vertex[u-1],self.vertex[v-1],edge)
    
    def read_file(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                splited_line = line.split(' ')
                if line[0] == 'p':
                    self.problem_type, self.num_vertex, self.num_edges = splited_line[1], int(splited_line[2]), int(splited_line[3])
                    self.network = AdjList(self.num_vertex)
                    self.vertex = [Vertex(i+1) for i in range(self.num_vertex)]
                elif line[0] == 'n':
                    if splited_line[2] == 's':
                        self.source = int(splited_line[1])
                    else:
                        self.sink = int(splited_line[1])
                elif line[0] == 'a':
                    u, v, c = int(splited_line[1]), int(splited_line[2]), int(splited_line[3])
                    edge = Edge(self.vertex[u-1], self.vertex[v-1], c)
                    self.network.add_edge(self.vertex[u-1],self.vertex[v-1],edge)


    def get_source_and_sink(self):
        for i in range(2):
            splited_line = get_line('n')
            if splited_line[2] == 's':
                self.source = int(splited_line[1])
            else:
                self.sink = int(splited_line[1])

    # OK
    def initialize_preflow(self):
        self.vertex[self.source-1].height = self.num_vertex
        sum_capacities = 0
        for sv in self.network.adj_list[self.source-1]:
            capacity = deepcopy(sv.capacity)
            sv.max_push()
            sv.node_to.excess = capacity
            sum_capacities -= capacity
        self.vertex[self.source-1].excess = sum_capacities


    def push(self, edge:Edge):
        pushed = False
        u = self.vertex[edge.node_from.node-1]
        v = self.vertex[edge.node_to.node-1]
        if  u.height == v.height + 1:
            pushed = True
            self.num_pushes += 1
            delta = min(u.excess, edge.capacity)
            edge.push(delta)
            u.excess -= delta
            v.excess += delta
            if v.excess > 0 and not v.node == self.source and not v.node == self.sink and not v in self.queue:
                self.queue.append(v)
        return pushed

    def relabel(self, vertex:Vertex):
        if vertex.excess > 0:
            self.num_relabels += 1
            min_height = float('inf')
            i = 0
            for uv in self.network.adj_list[vertex.node-1]:
                if uv.capacity > 0:
                    if uv.node_to.height < min_height:
                        min_height = deepcopy(uv.node_to.height)
                i += 1 
            vertex.height = 1 + min_height

    def push_and_relabel(self):
        start_t = time.time()
        self.num_pushes = 0
        self.num_relabels = 0
        self.initialize_preflow()
        self.queue = [v for v in self.vertex if v.excess > 0]
        self.queue.sort(key= lambda vertex: (vertex.height, vertex.excess))
        while self.queue:
            overflowing_vertex = self.queue[-1]
            while overflowing_vertex.excess > 0:
                pushed = False
                for uv in self.network.adj_list[overflowing_vertex.node-1]:
                    if uv.capacity > 0:
                        pushed = self.push(uv)
                    if overflowing_vertex.excess <= 0:
                        break
                if not pushed:
                    self.relabel(overflowing_vertex)
            self.queue = sorted([vertex for vertex in self.queue if vertex.excess > 0 and not vertex.node == self.source and not vertex.node == self.sink], key= lambda vertex: (vertex.height, vertex.excess))
        maxflow = self.vertex[self.sink-1].excess
        delta_t = time.time() - start_t
        return '{},{},{},{},{},{}'.format(self.num_vertex,self.num_edges,maxflow,delta_t,self.num_pushes,self.num_relabels)

def get_line(char):
    found = False
    while not found:
        line = input()
        splited_line = line.split(' ')
        if splited_line[0] == char:
            found = True
    return splited_line