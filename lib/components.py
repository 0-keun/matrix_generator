'''
Module Name : components
Description : Read components in netlist using class
Version     : 1.0.1
Author      : Youngkeun Kim
Created     : 2026-04-16
Updated     : 2026-04-16
Notes       : print_data_comp is added.
'''

import numpy as np

class Component:
    def __init__(self, comp_data):
        self.component_no1 = ("V", "I", "L", "C", "R", "D", "S")
        self.bidirectional_type  = ("L", "C", "R", "S")
        self.unidirectional_type = ("V", "I", "D")

        self.name = comp_data[0]
        self.type = self.name[0]

        self.get_values_from_data(comp_data)
        self.define_bidirectionality(comp_data)
    
    def define_bidirectionality(self, comp_data):
        if self.type in self.bidirectional_type:
            self.bidirection = True
        elif self.type in self.unidirectional_type:
            self.bidirection = False
        else:
            print("Warning! This component is not defned in this program.")

    def get_values_from_data(self, comp_data):
        if self.type in self.component_no1:
            self.node1 = comp_data[1]
            self.node2 = comp_data[2]
            self.value = comp_data[3]
        else:
            print("Warning! This component is not defned in this program.")

    def print_data_comp(self):
        if self.type in self.component_no1:
            print(f'name: {self.name}, type: {self.type}, node1(in): {self.node1}, node2(out): {self.node2}, value: {self.value}, bidirect: {self.bidirection}')
        else:
            print("Warning! This component is not defned in this program.")

class Netlist:
    '''
    comp.name(str): Name of the component
    comp.type(str): Type of the component ("V", "I", "L", "C", "R", "D", "S")
    comp.node1(int): Node getting into the component based on standard current
    comp.node2(int): Node getting out from the component based on standard current
    comp.value(float): Value of component (unit: V, A, H, F, Ohm, V(Voltage drop), Ohm)
    comp.bidirection(bool): Bidirectionality of the component
    '''
    def __init__(self, netlist, comp_check = True):
        self.components = self.read_netlist(netlist)
        self.source_type = ("V", "I")
        self.jterm_type = ("L", "C", "D", "S")
        if comp_check:
            self.check_comps_from_netlist()
    
    def read_netlist(self, netlist):
        components = []
        for comp in netlist:
            components.append(self.read_comp(comp))
        return components

    def read_comp(self, comp):
        return Component(comp)

    def check_comps_from_netlist(self):
        for comp in self.components:
            comp.print_data_comp()


        
    

