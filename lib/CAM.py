'''
Module Name : CAM
Description : Converter adjacency matrix generation for Graph Theory
Version     : 1.0.0
Author      : Youngkeun Kim
Created     : 2026-04-16
Updated     : 2026-04-16
Notes       : Initial version
'''

from lib.components import *

class CAM():
    def __init__(self, _netlist):
        self.netlist = Netlist(_netlist)
        self.components = self.netlist.components
        self.mat_size = self.maximum_node()+1 # including node 0 (GND)
        self.fill_matrix_str()
                
    def maximum_node(self):
        max_node = 0
        for comp in self.components:
            max_node = comp.node1 if comp.node1 > max_node else max_node
            max_node = comp.node2 if comp.node2 > max_node else max_node
        # print(f'max_node: {max_node}')
        return max_node

    def fill_matrix(self):
        self.mat = np.zeros((self.mat_size, self.mat_size))
        self.mat += np.eye(self.mat_size)
        for comp in self.components:
            self.mat[comp.node1][comp.node2] += comp.value
            self.mat[comp.node2][comp.node1] += comp.value if comp.bidirection else 0

    def fill_matrix_str(self):
        self.mat = np.full((self.mat_size, self.mat_size), '', dtype='<U20')

        for _ in range(self.mat_size):
            self.mat[_][_] += '1'

        for comp in self.components:            
            if self.mat[comp.node1][comp.node2] == '':
                self.mat[comp.node1][comp.node2] += comp.name
            else:
                self.mat[comp.node1][comp.node2] += '+'+comp.name

            if self.mat[comp.node2][comp.node1] == '':
                self.mat[comp.node2][comp.node1] += comp.name if comp.bidirection else ''
            else:
                self.mat[comp.node2][comp.node1] += '+'+comp.name if comp.bidirection else ''
        
        self.fill_zero2empty()

    def fill_zero2empty(self):
        for i in range(self.mat_size):
            for j in range(self.mat_size):
                if self.mat[i][j] == '':
                    self.mat[i][j] += '0' 
                if len(self.mat[i][j]) >= 20:
                    print(f'Warning! Matrix[{i}][{j}] is too long. You should check it contains everything you need.')