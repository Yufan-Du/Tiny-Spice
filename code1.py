import numpy as np
MAX_LIST=1000
MAX_NODES=1000
# The set of components
class COM_SET:
    def __init__(self, dic):
        self.dict=dic
    def get_item(self, key):
        return self.dict[key]
# A class for matrix of circuits
class NA_MATRIX:
    def __init__(self,_A,_RHS):
        self.current_nodes=0
        self.A=_A
        self.RHS=_RHS
    def __init__(self,nodes):
        self.current_nodes=0
        self.A=[[0 for i in range(nodes)] for i in range(nodes)]
        self.RHS=[0 for i in range(nodes)]
    def convert_to_float(self,value): # change the NUM[k/m/...] to float
        unit = value[-1]
        if unit == "K" or unit == "k":
            multiplier = 1000.0
        elif unit == "M" or unit == "Meg":
            multiplier = 1000000.0
        elif unit == "G":
            multiplier = 1000000000.0
        elif unit == "T":
            multiplier = 1000000000000.0
        elif unit == "P":
            multiplier = 1000000000000000.0
        elif unit == 'p':
            multiplier = 0.000000000001
        elif unit == "n":
            multiplier = 0.000000001
        elif unit == "u":
            multiplier = 0.000001
        elif unit == "m":
            multiplier = 0.001
        else:
            return float(value)
        number = float(value[:-1])
        return number * multiplier
    def update_nodes_num(self, node):
        if node>self.current_nodes:
            self.current_nodes = node

    def add_I(self,_from,_to,_value):
        node_from=int(_from)
        node_to=int(_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        node_value=self.convert_to_float(_value)
        self.RHS[node_from]-=node_value
        self.RHS[node_to]+=node_value

    def add_R(self,_from,_to,_value):
        node_from=int(_from)
        node_to=int(_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        node_value=self.convert_to_float(_value)
        g=(float)(1/node_value)
        self.A[node_from][node_from]+=g
        self.A[node_from][node_to]-=g
        self.A[node_to][node_to]+=g
        self.A[node_to][node_from]-=g

    def add_G(self,_source_from,_source_to,_from,_to,_value):
        node_from=int(_from)
        node_to=int(_to)
        source_from=int(_source_from)
        source_to=int(_source_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        self.update_nodes_num(source_from)
        self.update_nodes_num(source_to)
        node_value=self.convert_to_float(_value)
        g=(float)(1/node_value)
        self.A[node_from][source_from]+=g
        self.A[node_from][source_to]-=g
        self.A[node_to][source_from]-=g
        self.A[node_to][source_to]+=g

    def print_matrix(self):
        print("MatrixA and the RHS:(zeor row and column ignored)")
        for i in range(self.current_nodes):
            for j in range(self.current_nodes):
                print(f"{self.A[i+1][j+1]:.8f} ",end="")
            print(f" {self.RHS[i+1]:.8f}")
    def solve_matrix(self):
        A_np=np.array([self.A[i+1][1:self.current_nodes+1:1] for i in range(self.current_nodes)],dtype=np.float64)
        RHS_np=np.array(self.RHS[1:self.current_nodes+1:1],dtype=np.float64)
        A_inv = np.linalg.inv(A_np)
        X=A_inv @ RHS_np
        print("the voltage of a node:")
        print(X)
def parse_netlist():
    number_total=0
    number_to_element={}
    netlist=[0 for i in range(MAX_LIST)]
    print("Input the netlist, enter q to stop.")
    while True:
        line=input()
        if line == "q":
            break
        elements=line.split(" ")
        number_this=int(elements[0][1:]) # get the number of certain branch
        elements[0]=elements[0][0]
        number_to_element[number_this]=elements
        number_total+=1
    return COM_SET(number_to_element)

def form_matrix(netlist):
    node_matrix=NA_MATRIX(MAX_NODES)
    for node_num in netlist.dict:
        element=netlist.get_item(node_num)
        com_type=element[0]
        if com_type == 'R':
            node_matrix.add_R(element[1],element[2],element[3])
        elif com_type == 'I':
            node_matrix.add_I(element[1],element[2],element[3])
        elif com_type == 'G':
            node_matrix.add_G(element[1],element[2],element[3],element[4],element[5])
    return node_matrix
        

def main():
    msg=parse_netlist()
    node_matrix=form_matrix(msg)
    node_matrix.print_matrix()
    node_matrix.solve_matrix()
if __name__ == "__main__":
    main()

