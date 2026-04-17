# matrix generator
## components
Main function: read components from netlist (type: list)
input netlist (type: list)
output: Netlist.components -> 
comp:

comp.name(str): Name of the component
comp.type(str): Type of the component ("V", "I", "L", "C", "R", "D", "S")
comp.node1(int): Node getting into the component based on standard current
comp.node2(int): Node getting out from the component based on standard current
comp.value(float): Value of component (unit: V, A, H, F, Ohm, V(Voltage drop), Ohm)
comp.bidirection(bool): Bidirectionality of the component


## Converter Adjacency Matrix (CAM)
Main function: fill_matrix, fill_matrix_str
### How to use (at the main.py)
'''python
from lib.CAM import CAM

netlist = [['Vs', 0, 1, 48],
           ['S1', 1, 2, 4.8e-3],
           ['D2', 0, 2, 0.7],
           ['L1', 2, 3, 7.7e-6],
           ['C1', 3, 0, 150e-6],
           ['R1', 3, 0, 0.165]]

if __name__ == "__main__":
    cam = CAM(netlist)
    cam.fill_matrix_str()
    print_mat(cam.mat)
    cam.fill_matrix()
    print_mat(cam.mat)
'''
