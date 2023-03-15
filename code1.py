import numpy as np
MAX_LIST=1000
MAX_NODES=1000
MAX_BAD_BRANCH=100
# The set of components
class COM_SET:
    def __init__(self, dic):
        self.dict=dic
    def get_item(self, key):
        return self.dict[key]
# A class for matrix of circuits
class NA_MATRIX:
    def __init__(self,_A,_RHS,_bad_current,_bad_g,_bad_z,_bad_dict,_RHS_bad):
        self.current_nodes=0
        self.current_bad_branch=0
        self.A=_A
        self.bad_current=_bad_current
        self.bad_g=_bad_g
        self.bad_z=_bad_z
        self.bad_dict=_bad_dict
        self.RHS=_RHS
        self.RHS_bad=_RHS_bad
    def __init__(self,nodes,bad_branch):
        self.current_nodes=0
        self.current_bad_branch=0
        self.A=[[0 for i in range(nodes)] for i in range(nodes)]
        self.RHS=[0 for i in range(nodes)]
        self.bad_z=[[0 for i in range(bad_branch)]for i in range(bad_branch)]
        self.bad_g=[[0 for i in range(nodes)] for i in range(bad_branch)]
        self.bad_current=[[0 for i in range(bad_branch)] for i in range(nodes)]
        self.RHS_bad=[0 for i in range(bad_branch)]
        self.bad_dict={i:["undefined",0,0,0] for i in range(bad_branch)}
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
        if node_value:
            g=(float)(1/node_value)
            self.A[node_from][node_from]+=g
            self.A[node_from][node_to]-=g
            self.A[node_to][node_to]+=g
            self.A[node_to][node_from]-=g
        else:
            self.bad_dict[self.current_bad_branch]=["Resistor-0Ω",node_from,node_to,0]
            self.bad_current[node_from][self.current_bad_branch]+=1
            self.bad_current[node_to][self.current_bad_branch]-=1
            self.bad_g[self.current_bad_branch][node_from]+=1
            self.bad_g[self.current_bad_branch][node_to]-=1
            self.current_bad_branch+=1

    # input the g not r for a resistor
    def add_R_G(self,_from,_to,_value):
        node_from=int(_from)
        node_to=int(_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        node_value=self.convert_to_float(_value)
        g=(float)(node_value)
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
        if node_value:
            g=(float)(1/node_value)
            self.A[node_from][source_from]+=g
            self.A[node_from][source_to]-=g
            self.A[node_to][source_from]-=g
            self.A[node_to][source_to]+=g
        else:
            print("wrong G choice of the VCCS")
            quit()
    
    def add_F(self,_source_from,_source_to,_from,_to,_value,_name):
        node_from=int(_from)
        node_to=int(_to)
        source_from=int(_source_from)
        source_to=int(_source_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        self.update_nodes_num(source_from)
        self.update_nodes_num(source_to)
        node_value=self.convert_to_float(_value)
        # control&source port together
        self.bad_dict[self.current_bad_branch]=[f"{_name}-source&control",source_from,source_to,0]
        self.bad_current[source_from][self.current_bad_branch]+=1
        self.bad_current[source_to][self.current_bad_branch]-=1
        self.bad_current[node_from][self.current_bad_branch]+=node_value
        self.bad_current[node_to][self.current_bad_branch]-=node_value
        self.bad_g[self.current_bad_branch][source_from]+=1
        self.bad_g[self.current_bad_branch][source_to]-=1
        self.current_bad_branch+=1
    
    def add_H(self,_source_from,_source_to,_from,_to,_value,_name):
        node_from=int(_from)
        node_to=int(_to)
        source_from=int(_source_from)
        source_to=int(_source_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        self.update_nodes_num(source_from)
        self.update_nodes_num(source_to)
        node_value=self.convert_to_float(_value)
        # control port
        self.bad_dict[self.current_bad_branch]=[f"{_name}-source",source_from,source_to,0]
        self.bad_current[source_from][self.current_bad_branch]+=1
        self.bad_current[source_to][self.current_bad_branch]-=1
        self.bad_g[self.current_bad_branch][source_from]+=1
        self.bad_g[self.current_bad_branch][source_to]-=1
        self.current_bad_branch+=1
        # control port
        self.bad_dict[self.current_bad_branch]=[f"{_name}-control",node_from,node_to,node_value]
        self.bad_current[node_from][self.current_bad_branch]+=1
        self.bad_current[node_to][self.current_bad_branch]-=1
        self.bad_g[self.current_bad_branch][node_from]+=1
        self.bad_g[self.current_bad_branch][node_to]-=1
        self.bad_z[self.current_bad_branch][self.current_bad_branch-1]-=node_value
        self.current_bad_branch+=1

    def add_E(self,_source_from,_source_to,_from,_to,_value,_name):
        node_from=int(_from)
        node_to=int(_to)
        source_from=int(_source_from)
        source_to=int(_source_to)
        self.update_nodes_num(node_from)
        self.update_nodes_num(node_to)
        self.update_nodes_num(source_from)
        self.update_nodes_num(source_to)
        node_value=self.convert_to_float(_value)
        # control port / source port together
        self.bad_dict[self.current_bad_branch]=[f"{_name}-source&control",source_from,source_to,node_value]
        self.bad_current[node_from][self.current_bad_branch]+=1
        self.bad_current[node_to][self.current_bad_branch]-=1
        self.bad_g[self.current_bad_branch][source_from]-=node_value
        self.bad_g[self.current_bad_branch][source_to]+=node_value
        self.bad_g[self.current_bad_branch][node_from]+=1
        self.bad_g[self.current_bad_branch][node_to]-=1
        self.current_bad_branch+=1

    def add_V(self,_from,_to,__value,_name):
        _from=int(_from)
        _to=int(_to)
        _value=(float)(self.convert_to_float(__value))
        self.update_nodes_num(_from)
        self.update_nodes_num(_to)
        self.bad_dict[self.current_bad_branch]=[_name,_from,_to,_value]
        self.bad_current[_from][self.current_bad_branch]+=1
        self.bad_current[_to][self.current_bad_branch]-=1
        self.bad_g[self.current_bad_branch][_from]+=1
        self.bad_g[self.current_bad_branch][_to]-=1
        self.RHS_bad[self.current_bad_branch]=_value
        self.current_bad_branch+=1


    def print_matrix(self):
        print(f"current nodes:{self.current_nodes}, current bad branches{self.current_bad_branch}")
        print("MatrixA and the RHS:(zeor row and column ignored)")
        for i in range(self.current_nodes):
            for j in range(self.current_nodes):
                print(f"{self.A[i+1][j+1]:.6f} ",end="")
            for j in range(self.current_bad_branch):
                print(f"{self.bad_current[i+1][j]:.6f} ",end="")
            print(f" {self.RHS[i+1]:.6f}")
        for i in range(self.current_bad_branch):
            for j in range(self.current_nodes):
                print(f"{self.bad_g[i][j+1]:.6f} ",end="")
            for j in range(self.current_bad_branch):
                print(f"{self.bad_z[i][j+1]:.6f} ",end="")
            print(f"{self.RHS_bad[i]:.6f}")
    def solve_matrix(self):
        A_np=np.array([self.A[i+1][1:self.current_nodes+1:1] for i in range(self.current_nodes)],dtype=np.float64)
        bad_current_np=np.array([self.bad_current[i+1][0:self.current_bad_branch] for i in range(self.current_nodes)],dtype=np.float64)
        bad_g_np=np.array([self.bad_g[i][1:self.current_nodes+1:1] for i in range(self.current_bad_branch)],dtype=np.float64)
        bad_z_np=np.array([self.bad_z[i][0:self.current_bad_branch:1] for i in range(self.current_bad_branch)],dtype=np.float64)
        RHS_bad_np=np.array(self.RHS_bad[0:self.current_bad_branch:1],dtype=np.float64).reshape((self.current_bad_branch,1))
        RHS_np=np.array(self.RHS[1:self.current_nodes+1:1],dtype=np.float64).reshape((self.current_nodes,1))
        if self.current_bad_branch:
            upper_half=np.hstack((A_np,bad_current_np))
            lower_half=np.hstack((bad_g_np,bad_z_np))
            all_left=np.vstack((upper_half,lower_half))
            inv = np.linalg.inv(all_left)
            all_right=np.vstack((RHS_np,RHS_bad_np))
            X=inv @ all_right
        else:
            inv = np.linalg.inv(A_np)
            X=inv @ RHS_np
        print(f"the node 1 to {self.current_nodes} voltage:")
        for i in range(self.current_nodes):
            print("node",i+1,":", f"{X[i,0]:.8f}V")
        print(f"current {self.current_nodes+1} to {self.current_bad_branch+self.current_nodes} of bad branches")
        for i in range(self.current_bad_branch):
            print(f"Bad{i}{self.bad_dict[i]}. Current = {X[self.current_nodes+i,0]:.8f}A")
def parse_netlist():
    number_total=0
    number_to_element={}
    print("Input the netlist, enter q to stop.")
    while True:
        line=input()
        if line == "q":
            break
        elements=line.split(" ")
        number_this=int(elements[0][1:]) # get the number of certain branch
        # elements[0]=elements[0][0]
        number_to_element[number_this]=elements
        number_total+=1
    return COM_SET(number_to_element)

def form_matrix(netlist):
    node_matrix=NA_MATRIX(MAX_NODES,MAX_BAD_BRANCH)
    for node_num in netlist.dict:
        element=netlist.get_item(node_num)
        com_type=element[0][0]
        if com_type == 'R':
            node_matrix.add_R(element[1],element[2],element[3])
        elif com_type == 'I':
            node_matrix.add_I(element[1],element[2],element[3])
        elif com_type == 'G':
            node_matrix.add_G(element[3],element[4],element[1],element[2],element[5])
        elif com_type == 'V':
            node_matrix.add_V(element[1],element[2],element[3],element[0])
        elif com_type == 'F':
            node_matrix.add_F(element[3],element[4],element[1],element[2],element[5],element[0])
        elif com_type == 'E':
            node_matrix.add_E(element[3],element[4],element[1],element[2],element[5],element[0])
        elif com_type == 'H':
            node_matrix.add_H(element[3],element[4],element[1],element[2],element[5],element[0])
        elif com_type == 'g':
            node_matrix.add_R_G(element[1],element[2],element[3])
    return node_matrix
        

def main():
    msg=parse_netlist()
    node_matrix=form_matrix(msg)
    node_matrix.print_matrix()
    node_matrix.solve_matrix()
if __name__ == "__main__":
    main()

