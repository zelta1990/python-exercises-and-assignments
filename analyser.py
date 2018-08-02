import subprocess
import sys

def CPLEX(filename):
    '''run CPLEX to solve the problem of given lp file'''
    args1 = ['/Users/mac/Desktop/cplex', '-c', 'read /Users/mac/Desktop/' + filename, 'optimize',
            'display solution variable -']
    
    time1 = time.time()
    process1 = subprocess.Popen(args1, stdout = subprocess.PIPE)
    time2 = time.time()
    execution_time = time2 - time1
   
    output, error = process1.communicate()
    return output
    


def main():
    for n in range(3, 8):
        filename = 'x{}z.lp'.format(n)
    result = CPLEX(filename)