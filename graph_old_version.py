from copy import deepcopy
import datetime
import string
import sys
import time
graph_path = 'grafos/'

class Edge:
    def __init__(self, u, v, c, f, status='network') -> None:
        self.node_from = u
        self.node_to = v
        self.capacity = c
        self.flow = f
        self.status = status

    def update_flow(self, f):
        if f <= self.capacity:
            self.flow = f
    
    def __str__(self) -> str:
        return '{}->{}, c={}, f={}, {}'.format(self.node_from, self.node_to,self.capacity,self.flow, self.status)

class Vertex:
    def __init__(self, n, e, h, edges=[], status='file') -> None:
        self.node = n
        self.excess = e
        self.height = h
        self.edges = edges
        self.status = status

    def add_edge(self, e):
        self.edges.append(e)

    def __str__(self) -> str:
        adj_list = '\n[\n'
        for e in self.edges:
            adj_list += str(e) + ';\n'
        adj_list += ']'
        return 'n={}, e={}, h={}, {}'.format(self.node, self.excess, self.height, self.status) + adj_list


class Graph:
    def __init__(self):
        self.problem_type = None
        self.num_vertex = -1
        self.num_vertex_from_file = -1
        self.num_intermediary_vertex = -1
        self.num_edges = -1
        self.source = -1
        self.sink = -1
        self.network = []
        self.residual_network = []
        self.num_pushes = -1
        self.num_relabels = -1
        self.file_name = ''

    # OK
    def read_file(self):
        excess = 0
        flow = 0
        height = 0
        self.network = []
        self.num_vertex = -1
        self.num_intermediary_vertex = 0
        # get problem
        splited_line = get_line('p')
        self.problem_type, self.num_vertex_from_file, self.num_edges = splited_line[1], int(splited_line[2]), int(splited_line[3])
        self.num_vertex = deepcopy(self.num_vertex_from_file)
        self.get_source_and_sink()
        self.file_name = self.problem_type + 'flow_{}_{}'.format(self.source, self.sink)
        # get graph
        self.network = [None for node in range(self.num_vertex)]
        for e in range(self.num_edges):
            splited_line = get_line('a')
            u, v, c = int(splited_line[1]), int(splited_line[2]), int(splited_line[3])
            edge = Edge(u, v, c, flow)
            if self.network[u-1] == None:
                vertex_u = Vertex(u, excess, height, [edge])
                self.add_network_vertex(vertex_u)
            else:
                self.update_network_vertex(u, edge)
            if self.network[v-1] == None:
                vertex_v = Vertex(v, excess, height, [])
                self.add_network_vertex(vertex_v)

        # create vertex for not initialized positions
        for i in range(len(self.network)):
            if self.network[i] == None:    
                vertex = Vertex(i+1, excess, height)
                self.add_network_vertex(vertex)
        # adjust reversed edges, such that: if uv, vu are in G, then remove vu, create w, create vw, create wu. Now, we only have foward arcs.
        for u in self.network:
            for uv in self.get_network_neighbors(u.node):
                found = False
                i = 0
                capacity = -1
                for vu in self.get_network_neighbors(uv.node_to):
                    if vu.node_to == u.node:
                        capacity = vu.capacity
                        del self.network[uv.node_to - 1].edges[i]
    
                        found = True
                        break
                    i += 1
                if found:
                    self.num_intermediary_vertex += 1
                    self.num_vertex += 1
                    w = Vertex(self.num_vertex, excess, height, [], 'intermediary')
                    vw = Edge(uv.node_to, w.node, capacity, flow)
                    wu = Edge(w.node, uv.node_from, capacity, flow)
                    self.network[uv.node_to - 1].add_edge(vw)
                    w.add_edge(wu)
                    self.network.append(w)

        # create residual network
        self.residual_network = []
        for i in range(self.num_vertex):
            vertex = Vertex(i+1, excess, height, [], 'residual')
            self.residual_network.append(vertex)
        for u in self.network:
            for uv in self.get_network_neighbors(u.node):
                residual_uv = Edge(uv.node_from, uv.node_to, uv.capacity, flow, 'residual-foward')
                residual_vu = Edge(uv.node_to, uv.node_from, uv.flow, flow, 'residual-backward')
                self.residual_network[residual_uv.node_from - 1].add_edge(residual_uv)
                self.residual_network[residual_vu.node_from - 1].add_edge(residual_vu)

    # OK
    def update_network_vertex(self, node, edge):
        self.network[node - 1].add_edge(edge)

    # OK
    def add_network_vertex(self, vertex:Vertex):    
        self.network[vertex.node - 1] = vertex

    # OK
    def get_network_neighbors(self, node:int):
        return self.network[node-1].edges

    # OK
    def get_residual_neighbors(self, node:int):
        return self.residual_network[node-1].edges 

    # OK
    def print(self):
        print('source: ' + str(self.source))
        print('sink: ' + str(self.sink))
        print('network:')
        for v in self.network:
            print(str(v))
        print('residual network:')
        for v in self.residual_network:
            print(str(v))

    # OK
    def get_source_and_sink(self):
        for i in range(2):
            splited_line = get_line('n')
            if splited_line[2] == 's':
                self.source = int(splited_line[1])
            else:
                self.sink = int(splited_line[1])
    
    # OK
    def change_vertex_height(self, vertex: Vertex, new_height: int):
        self.residual_network[vertex.node - 1].height = new_height

    def find_backward_edge(self, residual_u: Vertex, residual_v_position):
        # recover v
        residual_v = self.residual_network[self.residual_network[residual_u.node-1].edges[residual_v_position].node_to -1]
        residual_u_position = 0
        found = False
        for vu in self.residual_network[residual_v.node - 1].edges:
            if vu.node_to == residual_u.node:
                found = True
                break
            else:
                residual_u_position += 1
        if not found:
            residual_u_position = -1
        return residual_u_position

    # OK
    def move_flow(self, residual_u: Vertex, residual_v_position: int, flow: int):
        # foward arc: cf = c - f    <-- how can I improve the current flow
        self.residual_network[residual_u.node-1].edges[residual_v_position].flow = flow
        # backward arc: cf = f      <-- how can I change the current flow
        residual_u_position = self.find_backward_edge(residual_u, residual_v_position)
        if residual_u_position >= 0:
            self.residual_network[self.residual_network[residual_u.node-1].edges[residual_v_position].node_to-1].edges[residual_u_position].capacity = flow
        else:
            quit()
    
    def get_residual_capacity(self, residual_u: Vertex, residual_v_position:int):
        return self.residual_network[residual_u.node - 1].edges[residual_v_position].capacity - self.residual_network[residual_u.node - 1].edges[residual_v_position].flow

    # OK
    def change_vertex_excess(self, vertex: Vertex, excess: int):
        self.residual_network[vertex.node - 1].excess = excess

    # OK
    def initialize_preflow(self):
        source = self.network[self.source-1]
        self.change_vertex_height(source, self.num_vertex)
        sum_capacities = 0
        for i in range(len(self.get_network_neighbors(self.source))):
            capacity = self.network[self.source-1].edges[i].capacity
            self.move_flow(source, i, capacity)
            neighbor = self.network[source.edges[i].node_to - 1]
            self.change_vertex_excess(neighbor, capacity)
            sum_capacities -= capacity
        self.change_vertex_excess(source, sum_capacities)


    def push(self, residual_u:Vertex, residual_v_position: int):
        uv = self.residual_network[residual_u.node-1].edges[residual_v_position]
        pushed = False
        residual_v = self.residual_network[uv.node_to - 1]
        if residual_u.excess > 0 and residual_u.height == residual_v.height + 1:
            self.num_pushes += 1
            delta = min(residual_u.excess, self.residual_network[residual_u.node-1].edges[residual_v_position].capacity)
            if uv.status == 'residual-foward':
                self.move_flow(residual_u, residual_v_position, self.residual_network[residual_u.node -1].edges[residual_v_position].flow + delta)
            else:
                residual_u_position = self.find_backward_edge(residual_u, residual_v_position)
                if residual_u_position >= 0:
                    self.move_flow(residual_v, residual_u_position, self.residual_network[residual_v.node - 1].edges[residual_u_position].flow - delta)
                else:
                    quit()
            self.change_vertex_excess(residual_u, self.residual_network[residual_u.node -1].excess - delta)
            self.change_vertex_excess(residual_v, self.residual_network[residual_v.node -1].excess + delta)
            pushed = True
        return pushed

    def relabel(self, residual_u:Vertex):
        if residual_u.excess > 0:
            self.num_relabels += 1
            min_height = float('inf')
            i = 0
            for uv in self.get_residual_neighbors(residual_u.node):
                if self.get_residual_capacity(residual_u, i) > 0:
                    v = self.residual_network[uv.node_to - 1]
                    if v.height < min_height:
                        min_height = v.height
                i += 1 
            self.residual_network[residual_u.node -1].height = 1 + min_height

    def push_and_relabel(self):
        start_t = time.time()
        self.num_pushes = 0
        self.num_relabels = 0
        self.initialize_preflow()
        activated_vertex = [vertex for vertex in self.residual_network if vertex.excess > 0]
        activated_vertex.sort(key= lambda vertex: (vertex.height, vertex.excess))
        while activated_vertex:
            u = activated_vertex[-1]
            while self.residual_network[u.node - 1].excess > 0:
                pushed = False
                for i in range(len(self.get_residual_neighbors(u.node))):
                    if self.get_residual_capacity(u, i) > 0:
                        pushed = self.push(u, i)
                    if self.residual_network[u.node - 1].excess <= 0:
                        break
                if not pushed:
                    self.relabel(u)
            activated_vertex = [vertex for vertex in self.residual_network if vertex.excess > 0 and not vertex.node == self.source and not vertex.node == self.sink]
            activated_vertex.sort(key= lambda vertex: (vertex.height, vertex.excess))
        delta_t = time.time() - start_t 
        maxflow = self.residual_network[self.sink-1].excess
        return maxflow, delta_t, self.num_pushes, self.num_relabels

def get_line(char):
    found = False
    while not found:
        line = input()
        splited_line = line.split(' ')
        if splited_line[0] == char:
            found = True
    return splited_line