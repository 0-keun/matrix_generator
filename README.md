# Matrix Generator

This project generates circuit matrices from a given netlist.
It currently supports:
- component parsing from a netlist
- Converter Adjacency Matrix (CAM) generation
- Modified Nodal Analysis (MNA) matrix generation

---

## Components

The component parser reads a netlist and converts each entry into a component object.

### Main Function
Read components from a netlist.

### Input
- `netlist` (`list`)

### Output
- `Netlist.components`

Each component object `comp` has the following attributes:

- `comp.name` (`str`): Name of the component
- `comp.type` (`str`): Type of the component  
  Supported types: `"V"`, `"I"`, `"L"`, `"C"`, `"R"`, `"D"`, `"S"`
- `comp.node1` (`int`): Starting node of the component based on the reference current direction
- `comp.node2` (`int`): Ending node of the component based on the reference current direction
- `comp.value` (`float`): Component value  
  Unit depends on component type:
  - `V`: Volt
  - `I`: Ampere
  - `L`: Henry
  - `C`: Farad
  - `R`: Ohm
  - `D`: Voltage drop
  - `S`: On-state resistance
- `comp.bidirection` (`bool`): Whether the component is bidirectional

---

## Converter Adjacency Matrix (CAM)

The CAM module generates the converter adjacency matrix from the given netlist.

### Main Functions
- `fill_matrix()`
- `fill_matrix_str()`

### Example
```python
from lib.CAM import CAM
from lib.utils.display import print_mat

netlist = [
    ['Vs', 0, 1, 48],
    ['S1', 1, 2, 4.8e-3],
    ['D2', 0, 2, 0.7],
    ['L1', 2, 3, 7.7e-6],
    ['C1', 3, 0, 150e-6],
    ['R1', 3, 0, 0.165]
]

if __name__ == "__main__":
    cam = CAM(netlist)

    cam.fill_matrix_str()
    print_mat(cam.mat)

    cam.fill_matrix()
    print_mat(cam.mat)
