# Tiny-Spice
A simple but fully functional spice is continuously updated. 
Now support all the basic elements in the circuit for steady-state analysis, elements such as resistor, voltage source, current source,VCVS,VCCS,CCCS,CCVS are supported.
To input resistance according to the value of conductance, the g[key] NP NM VALUE is also OK.
The total number of nodes will be counted automatically.

Input is almost the same as spice netlist.
KEY NP NM (NCP NCM) VALUE
such as

R1 6 1 4
R2 1 2 4
G3 1 0 5 0 2
E4 2 3 3 0 2
R5 3 0 4
F6 3 0 6 7 2
V7 8 0 5
R8 3 4 2
H9 4 5 7 8 2
R10 5 0 4
I11 5 0 3

and finish with a q in single line

The output is the whole matrix, the RHS vector, every node voltage, and simultaneously the current and information of the bad branch.

It is planned to add these functions in the future:

1.Inductance and capacitance will be introduced, complex frequency domain analysis will be adopted.
2.Transient analysis will be added.
