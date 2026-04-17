'''
Module Name : MNA
Description : Modified Nodal Analysis
Version     : 1.0.0
Author      : Youngkeun Kim
Created     : 2026-04-16
Updated     : 2026-04-16
Notes       : Initial version
'''

import numpy as np
from lib.components import Netlist

class MNA():
    '''
    comp.name(str): Name of the component
    comp.type(str): Type of the component ("V", "I", "L", "C", "R", "D", "S")
    comp.node1(int): Node getting into the component based on standard current
    comp.node2(int): Node getting out from the component based on standard current
    comp.value(float): Value of component (unit: V, A, H, F, Ohm, V(Voltage drop), Ohm)
    comp.bidirection(bool): Bidirectionality of the component
    '''
    def __init__(self, _netlist):
        self.netlist = Netlist(netlist=_netlist, comp_check=False)
        self.components = self.netlist.components
        self.mat_size = self.maximum_node() + self.maximum_source() # including node 0 (GND)
        self.src_idx = self.set_src_idx()
        self.Ts = 1e-7

        ## RUN Functions
        self.get_A_mat_str()
        self.get_b_vec_str()

    ###################################
    ##        Basic functions        ##
    ###################################

    def set_src_idx(self):
        src_idx = {}
        idx = 0
        for comp in self.components:
            if comp.type in self.netlist.source_type:
                src_idx[comp.name] = self.maximum_node() + idx
                idx += 1
        return src_idx

    def maximum_node(self):
        max_node = 0
        for comp in self.components:
            max_node = comp.node1 if comp.node1 > max_node else max_node
            max_node = comp.node2 if comp.node2 > max_node else max_node
        return max_node+1

    def maximum_source(self):
        max_source = 0
        for comp in self.components:
            max_source += 1 if comp.type in self.netlist.source_type else 0
        return max_source

    def fill_zero2empty_str(self, mat):
        # 1D vector -> column vector
        if mat.ndim == 1:
            mat = mat.reshape(-1, 1)
        # 2D
        if mat.ndim != 2:
            raise ValueError("print_mat only supports 1D or 2D arrays.")

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == '':
                    mat[i][j] += '0' 
                if len(mat[i][j]) >= 30:
                    print(f'Warning! Matrix[{i}][{j}] is too long. You should check it contains everything you need.')

    ####################################
    ##          A Matrix Gen          ##
    ####################################

    def get_A_mat_str(self):
        self.A_mat_str = np.full((self.mat_size, self.mat_size), '', dtype='<U30')
        for comp in self.components:
            self.add_source_to_mat(comp) if comp.type in self.netlist.source_type else self.add_G_to_mat(comp)
        
        self.A_mat_str = self.A_mat_str[1:,1:]
        self.fill_zero2empty_str(self.A_mat_str)

    def add_str_to_mat(self, row, col, value):    
        if self.A_mat_str[row][col] == '':
            self.A_mat_str[row][col] += value
        else:
            self.A_mat_str[row][col] += value if value[0]=='-' else '+'+value

    def add_G_to_mat(self, comp):
        self.add_str_to_mat(row=comp.node1,col=comp.node1,value=f'G_{comp.name}')
        self.add_str_to_mat(row=comp.node1,col=comp.node2, value=f'-G_{comp.name}')
        self.add_str_to_mat(row=comp.node2,col=comp.node1, value=f'-G_{comp.name}')
        self.add_str_to_mat(row=comp.node2,col=comp.node2,value=f'G_{comp.name}')

    def add_source_to_mat(self, comp):
        if comp.type == 'V':
            self.add_str_to_mat(row=comp.node1,col=self.src_idx[comp.name],value='-1')
            self.add_str_to_mat(row=comp.node2,col=self.src_idx[comp.name],value='1')
            self.add_str_to_mat(row=self.src_idx[comp.name],col=comp.node1,value='-1')
            self.add_str_to_mat(row=self.src_idx[comp.name],col=comp.node2,value='1')
        elif comp.type == 'I':
            self.add_str_to_mat(row=comp.node1,col=self.src_idx[comp.name],value='-1')
            self.add_str_to_mat(row=comp.node2,col=self.src_idx[comp.name],value='1')
            self.add_str_to_mat(row=self.src_idx[comp.name],col=self.src_idx[comp.name],value='-1')
        else:
            print(f'Warning! {comp.name} is undefined source. Take a look <add_source_to_mat> method in <MNA> class')

    ####################################
    ##          b vector Gen          ##
    ####################################

    def get_b_vec_str(self):
        self.b_vec_str = np.full((self.mat_size), '', dtype='<U30')
        for comp in self.components:
            if comp.type in self.netlist.jterm_type:
                self.add_j_to_vec(comp)
            elif comp.type in self.netlist.source_type:
                self.add_source_to_vec(comp)

        self.b_vec_str = self.b_vec_str[1:]
        self.fill_zero2empty_str(self.b_vec_str)

    def add_str_to_vec(self, idx, value):    
        if self.b_vec_str[idx] == '':
            self.b_vec_str[idx] += value
        else:
            self.b_vec_str[idx] += value if value[0]=='-' else '+'+value

    def add_source_to_vec(self, comp):
        if comp.type == 'V':
            self.add_str_to_vec(idx=self.src_idx[comp.name],value=f'{comp.name}')
        elif comp.type == 'I':
            self.add_str_to_vec(idx=self.src_idx[comp.name],value=f'{comp.name}')
        else:
            print(f'Warning! {comp.name} is undefined source. Take a look <add_source_to_vec> method in <MNA> class') 

    def add_j_to_vec(self, comp):
        self.add_str_to_vec(idx=comp.node1,value=f'j_{comp.name}')
        self.add_str_to_vec(idx=comp.node2, value=f'-j_{comp.name}')

    ####################################
    ##       substitute_numeric       ##
    ####################################
    def get_value_dict(self):
        value_dict = {}
        for comp in self.components:
            if comp.type in self.netlist.source_type:
                value_dict[f'{comp.name}'] = comp.value
            else:
                value_dict[f'G_{comp.name}'] = self.set_G_value(comp)
        return value_dict        

    def set_G_value(self, comp):
        if comp.type == 'S':
            return comp.value/self.Ts
        elif comp.type == 'D':
            return comp.value/self.Ts
        elif comp.type == 'C':
            return comp.value/self.Ts
        elif comp.type == 'L':
            return self.Ts/comp.value
        elif comp.type == 'R':
            return 1/comp.value
        else:
            print(f'Warning! {comp.name} is undefined component type!')

    def eval_string_expr(self, expr, values):
        expr = expr.strip()
        if expr == '0':
            return 0.0
        return eval(expr, {"__builtins__": None}, values)

    def substitute_numeric(self, mat_str):
        values = self.get_value_dict()
        n_row = len(mat_str)
        n_col = len(mat_str[0])
        out = np.zeros((n_row, n_col), dtype=float)

        for i in range(n_row):
            for j in range(n_col):
                out[i, j] = self.eval_string_expr(mat_str[i][j], values)

        return out