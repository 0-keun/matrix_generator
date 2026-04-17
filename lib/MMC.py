'''
Module Name : MMC
Description : Get netlist according to the number of sub-modules
Version     : 1.0.0
Author      : Youngkeun Kim
Created     : 2026-04-16
Updated     : 2026-04-16
Notes       : Initial version
'''

def add_source(sm_num,Vin):
    return [['V1',0,1,Vin],['V2',2*sm_num+3,0,Vin]]

def comp_in_sm(sm_num,Coss,Csm):
    sm_netlist = []
    for sm_idx in range(1, sm_num + 1):
        axis = 1 if sm_idx > sm_num/2 else 0
        sm_netlist.append([f'S{2*sm_idx-1}',2*sm_idx-1+2*axis,2*sm_idx+2*axis,Coss])
        sm_netlist.append([f'S{2*sm_idx}',2*sm_idx+1+2*axis,2*sm_idx-1+2*axis,Coss])
        sm_netlist.append([f'C{sm_idx}',2*sm_idx+2*axis,2*sm_idx+1+2*axis,Csm])

    return sm_netlist

def add_L(N_half,Larm):
    return [['L1',2*N_half+1,2*N_half+2,Larm],['L2',2*N_half+2,2*N_half+3,Larm]]

def add_R(N_half,R):
    return [['R1',2*N_half+2,0,20]]

def MMC_netlist(sm_num,Vin,Coss,Csm,Larm,R):
    N_half = sm_num/2
    mmc_netlist = []
    mmc_netlist.append(add_source(sm_num,Vin))
    mmc_netlist.append(comp_in_sm(sm_num,Coss,Csm))
    mmc_netlist.append(add_L(sm_num,Larm))
    mmc_netlist.append(add_R(sm_num,R))

    return [item for sublist in mmc_netlist for item in sublist]
