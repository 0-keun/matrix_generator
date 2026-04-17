from lib.CAM import CAM
from lib.MNA import MNA
from lib.MMC import MMC_netlist
from lib.utils.display import print_mat

# Components types in this version: V(DC), I(DC), L, C, R, D, S
# All component's node1 and 2 is defined based on current direction.

'''
# Netlist of Buck converter
netlist = [['Vs', 0, 1, 48],
           ['S1', 1, 2, 4.8e-3],
           ['D2', 0, 2, 0.7],
           ['L1', 2, 3, 7.7e-6],
           ['C1', 3, 0, 150e-6],
           ['R1', 3, 0, 0.165]]
'''

'''
# Netlist of MMC
netlist = [['V1',  0,  1, 200],
           ['V2', 11,  0, 200],
           ['S1',  1,  2, 25e-9],
           ['S2',  3,  1, 25e-9],
           ['S3',  3,  4, 25e-9],
           ['S4',  5,  3, 25e-9],
           ['S5',  7,  8, 25e-9],
           ['S6',  9,  7, 25e-9],
           ['S7',  9, 10, 25e-9],
           ['S8', 11,  9, 25e-9],
           ['C1',  2,  3, 15e-3],
           ['C2',  4,  5, 15e-3],
           ['C3',  8,  9, 15e-3],
           ['C4', 10, 11, 15e-3],
           ['L1',  5,  6, 8e-3],
           ['L2',  6,  7, 8e-3],
           ['R1',  6,  0, 20]]
'''

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