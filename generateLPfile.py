import subprocess
import time

#generate the nodes of source, transfer, destination
X = 7 
Y = int(input('The amount of transfer nodes:'))
Z = 7

print('Source nodes : {}\nTransfer nodes : {}\nDestination node : {}'.format(X, Y, Z))
print('---------------------')


def DV_contraint():
    '''return the demand volume constraint: 
    Xikj = hij
    which Xikj means the sum of load between source i to destination j'''
    DV = []
    demand_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            dv = []
            for k in range(1, Y + 1):
                dv.append("x{}{}{}".format(i, k, j))
            DV = ' + '.join(dv) + ' = {}'.format(i + j)
            demand_equation.append(DV)
    demand_constraint = '\n'.join(demand_equation)
    return demand_constraint


def BV_constriant():
    '''return the binary variables constraint: 
    Uikj = Nk 
    which Uikj means the sum of used paths and Nk = 3 in this problem'''
    BV = []
    binary_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            bv = []
            for k in range(1, Y + 1):
                bv.append("u{}{}{}".format(i, k, j))
            BV = ' + '.join(bv) + ' = {}'.format(3)
            binary_equation.append(BV)
    binary_constraint = '\n'.join(binary_equation)
    return binary_constraint
 
 
def DF_constraint():
    '''return the demand flow constraint:
    Nk * Xikj = hij * Uikj'''
    DF = []
    flow_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            for k in range(1, Y + 1):
                DF = '3 x{}{}{} - {} u{}{}{} = 0'.format(i, k, j, i + j, i, k, j)
                flow_equation.append(DF)
    demand_flow_constraint = '\n'.join(flow_equation)
    return demand_flow_constraint


def ST_capp_constraint():
    '''return the cappacity constraint from source to transit node'''
    ST, ST_r = [], []
    capp1_equation, capp1_equation_r = [], []
    for i in range (1, X + 1):
        for k in range (1, Y +1):
            st = []
            for j in range(1, Z+1):
                st.append('x{}{}{}'.format(i, k, j))
            ST = ' + '.join(st) + ' - c{}{} <= 0'.format(i, k)
            ST_r = ' + '.join(st) + ' - c{}{} r <= 0'.format(i, k)
            capp1_equation.append(ST)
            capp1_equation_r.append(ST_r)
    capp1_constraint = '\n'.join(capp1_equation)
    capp1_constraint_r = '\n'.join(capp1_equation_r)  
    return capp1_constraint, capp1_constraint_r


def TD_capp_constraint():
    '''return the cappacity constraint from transit node to dest node'''
    TD, TD_r = [], []
    capp2_equation, capp2_equation_r = [], []
    for k in range(1, Y+1):
        for j in range(1, Z+1):
            td = []
            for i in range(1, X+1):
                td.append('x{}{}{}'.format(i, k, j))
            TD = ' + '.join(td) + ' - d{}{} <= 0'.format(k, j)     
            TD_r = ' + '.join(td) + ' - d{}{} r <= 0'.format(k, j)
            capp2_equation.append(TD)
            capp2_equation_r.append(TD_r)
    capp2_constraint = '\n'.join(capp2_equation)
    capp2_constraint_r = '\n'.join(capp2_equation_r)
    return capp2_constraint, capp2_constraint_r
 
                
def Bounds_variable():
    '''return the bounds of demand variable : Xikj of this problem'''
    bound_x = []
    bound_unequation_x = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            for k in range(1, Y + 1):
                bound_x = '0 <= x{}{}{}'.format(i, k, j)
                bound_unequation_x.append(bound_x)
    Bounds_x = '\n'.join(bound_unequation_x)
    return Bounds_x

def Bounds_capacity():
    '''return the bounds of capacity cik and dkj'''
    bound_c, bound_d = [], []
    bound_unequation_c, bound_unequation_d = [], []
    for i in range(1, X + 1):
        for k in range (1, Y + 1):
            bound_c = '0 <= c{}{}'.format(i, k)
            bound_unequation_c.append(bound_c)
    Bounds_c = '\n'.join(bound_unequation_c)
    
    for j in range(1, Z + 1):
        for k in range(1, Y + 1):
            bound_d = '0 <= d{}{}'.format(k, j)
            bound_unequation_d.append(bound_d)
    Bounds_d = '\n'.join(bound_unequation_d)
    
    return Bounds_c, Bounds_d


def binary_constraint():
    '''return binary constraints'''
    bc = ''
    for i in range(1, X+1):
        for k in range(1, Y+1):
            for j in range(1, Z+1):
                bc += 'u{}{}{}\n'.format(i,k,j)
    return bc


def createLP():
    '''create a LP file for this problem'''
    f = open(filename, 'w')
    content = \
    '''Minimize
        r
Subject to
demand volume: \n{}
binary variables: \n{}
demand flow: \n{}
srouce to tranfer node capp1: \n{}\n{}
transfer to destination node capp2: \n{}\n{}
Bounds
0 <= r
{}
{}
{}
Binaries
{}
End'''.format(demand_volume, binary_variables, demand_flow, ST_capacity, ST_capacity_r,
              TD_capacity, TD_capacity_r, bounds_x, bounds_c, bounds_d, binaries)
    f.write(content)
    f.close


def set_filename():
    '''return the filename : XYZ.lp which Y belongs to {3, 4, 5, 6, 7}'''
    filename = 'X{}Z.lp'.format(Y)
    return filename


demand_volume = DV_contraint()
binary_variables = BV_constriant()
demand_flow = DF_constraint()
ST_capacity, ST_capacity_r = ST_capp_constraint()
TD_capacity, TD_capacity_r = TD_capp_constraint()
bounds_x = Bounds_variable()
bounds_c, bounds_d = Bounds_capacity()
binaries = binary_constraint()
filename = set_filename()

createLP()
