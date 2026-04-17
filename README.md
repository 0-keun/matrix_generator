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
```python
from lib.CAM import CAM
from lib.utils.display import print_mat

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
```

## Modified Nodal Analysis (MNA)
Main function: Find A_mat and b_vec
### How to use
```python
from lib.MNA import MNA
from lib.MMC import MMC_netlist
from lib.utils.display import print_mat

netlist = MMC_netlist(sm_num=6,
                      Vin=200,
                      Coss=25e-9,
                      Csm=15e-3,
                      Larm=8e-3,
                      R=20)
                      
print(f'netlist: {netlist}')

if __name__ == "__main__":
    mna = MNA(netlist)

    print('A mat is:')
    print_mat(mna.A_mat_str)
    print_mat(mna.substitute_numeric(mna.A_mat_str))

    print('\n')
    
    print('b vec is:')
    print_mat(mna.b_vec_str)
```
