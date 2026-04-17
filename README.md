# Matrix Generator

This project generates circuit-related matrices from a given netlist.

It currently supports:
- component parsing from a netlist
- Converter Adjacency Matrix (CAM) generation
- Modified Nodal Analysis (MNA) matrix generation

---

## Components

Main function: read components from netlist (`list`)

### Input
- `netlist` (`list`)

### Output
- `Netlist.components`

Each component object `comp` has the following attributes:

- `comp.name` (`str`): Name of the component
- `comp.type` (`str`): Type of the component  
  Supported types: `"V"`, `"I"`, `"L"`, `"C"`, `"R"`, `"D"`, `"S"`
- `comp.node1` (`int`): Node entering the component based on the reference current direction
- `comp.node2` (`int`): Node leaving the component based on the reference current direction
- `comp.value` (`float`): Component value  
  Unit depends on the component type:
  - `V`: Volt
  - `I`: Ampere
  - `L`: Henry
  - `C`: Farad
  - `R`: Ohm
  - `D`: Voltage drop
  - `S`: On-state resistance
- `comp.bidirection` (`bool`): Bidirectionality of the component

---

## Converter Adjacency Matrix (CAM)

Main functions:
- `fill_matrix()`
- `fill_matrix_str()`

### How to use

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

---

## Modified Nodal Analysis (MNA)

Main function: find `A_mat` and `b_vec`

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

---

## Notes

- `print_mat()` prints matrices and vectors in a formatted style for easier inspection.
- `*_str` variables store symbolic matrix expressions as strings.
- `substitute_numeric()` replaces symbolic terms with actual numeric values.
