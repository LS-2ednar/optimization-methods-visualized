"""
Downhil Simplex: Nelder Mead

The algorithm uses four possible operations: reflection, expansion, contraction,
and shrink, each being associated with a scalar parameter: alpha (reflection), 
beta (expansion), gamma (contraction), and delta (shrink).

The example is explained with the Himmelblau function which has local minima 
which are identical and show a value of 0.
"""
#Used libraries
import numpy as np
import matplotlib.pyplot as plt


"""
------------------------------------------------------------------------------
The Problem
------------------------------------------------------------------------------
"""
#define the problem function himmelblau function
def OptiFun(x,y):
    a = x*x+y-11
    b = y*y+x-7
    return a*a +b*b

"""
------------------------------------------------------------------------------
The Optimization Algorithm
------------------------------------------------------------------------------
"""
def DownhillSimplexNelderMead(triangle):
    """
    triangle is an array of 3 points
    """
    alpha = 1.00 
    beta  = 2.00
    gamma = 0.5
    delta = 0.5
    
    #gernerate variables
    x = np.arange(-6,6,0.01)
    y = np.arange(-6,6,0.01)
    x, y = np.meshgrid(x, y)
    z = OptiFun(x,y)
    
    #Plot the function space
    levels = np.logspace(0.01, 3, 30)
    plt.contour(x, y, z, levels, cmap='gist_stern')
    plt.xlabel('x-Value')
    plt.ylabel('y-value')
    plt.title('Nelder Mead Downhil Symplex')
    plt.xticks([-6, -3, 0, 3, 6])
    plt.yticks([-6, -3, 0, 3, 6])
    plt.xlim([-6, 6])
    plt.ylim([-6, 6])
    
    #stop criteria
    c = 0
    
    while c < 200:     
        # 1. Sort
        triangle = sortt(triangle)
        #mark best worst corner
        plt.plot(triangle[2][0],triangle[2][1],'ro')
        #determine the middle value of all
        x_mid = midPoint(triangle)
        # 2. Reflect
        # x_ref = reflect(triangle,x_mid,alpha)
        x_ref = x_mid+alpha*(x_mid-triangle[2])
        # print(x_ref)
        if OptiFun(triangle[0][0],triangle[0][1]) <= OptiFun(x_ref[0],x_ref[1]) and OptiFun(x_ref[0],x_ref[1]) < OptiFun(triangle[1][0],triangle[1][1]):
            triangle[2] = x_ref
        
        # 3. Expansion
        elif OptiFun(x_ref[0],x_ref[1]) < OptiFun(triangle[0][0],triangle[0][1]):
            
            x_exp = x_mid+beta*(x_ref-x_mid)
            
            if OptiFun(x_exp[0],x_exp[1]) < OptiFun(x_ref[0],x_ref[1]):
                triangle[2] = x_exp
            else:
                triangle[2] = x_ref
        
        # 4. Outside Contration
        elif OptiFun(triangle[1][0],triangle[1][1]) <= OptiFun(x_ref[0],x_ref[1]) and OptiFun(x_ref[0],x_ref[1]) < OptiFun(triangle[2][0],triangle[2][1]): 
            
            x_oco = x_mid+gamma*(x_ref-x_mid)
            
            if  OptiFun(x_oco[0],x_oco[1])<=OptiFun(x_ref[0],x_ref[1]):
                triangle[2] = x_oco
            else:
                triangle = shrink(triangle,delta)
        
        # 5. Inside Contration
        elif OptiFun(x_ref[0],x_ref[1]) >= OptiFun(triangle[2][0],triangle[2][1]): 
            
            x_ico = x_mid-gamma*(x_ref-x_mid)
            
            if OptiFun(x_ico[0],x_ico[1]) <  OptiFun(triangle[2][0],triangle[2][1]):
                triangle[2] = x_ico[1]
            else:
                triangle = shrink(triangle,delta)
        
        c+=1
        plot3c(triangle)
        plt.annotate(f'{c}', (triangle[2][0],triangle[2][1]))
        
        #This break conditon makes sence in for this function since the minima should be 0 at 4 points in the given problem
        triangle_VAL = OptiFun(triangle[0][0],triangle[0][1])
        if triangle_VAL < 0.001:
            break
        
    print(f'\n\nPoint ({triangle[0][0]} {triangle[0][1]}) is a Minima of {OptiFun(triangle[0][0],triangle[0][1])}\nwhich was found after {c} iterations')  
    plt.plot(triangle[0][0],triangle[0][1],'*',color='lime')
    return OptiFun(triangle[0][0],triangle[0][1])

def sortt(triangle):
    """
    after sort: 
    array position      value
    0                   best
    1                   middle
    2                   worst
    """
    triangleval = []
    for valuepair in triangle:
        triangleval.append(OptiFun(valuepair[0],valuepair[1]))
    mini = triangleval.index(min(triangleval))
    maxi = triangleval.index(max(triangleval))
    if mini == maxi:
        midi = 1
        maxi = 2
    else:
        midi = 3-mini-maxi
    indicies = [mini,midi,maxi]
    sortedtriangle = triangle[indicies]
    print(f'-----------------\nTriangle old:\n{triangle}\n\nTriangle new:\n{sortedtriangle}\n-----------------')
    return sortedtriangle

def shrink(triangle,delta):
    triangle[1] = triangle[0] + delta*(triangle[1]-triangle[0])
    triangle[2] = triangle[0] + delta*(triangle[2]-triangle[0])
    return triangle

"""
------------------------------------------------------------------------------
Help functions
------------------------------------------------------------------------------
"""
def plot3c(triangle):
    xvals = []
    yvals = []
    for point in triangle:
        xvals.append(point[0])
        yvals.append(point[1])
    xvals.append(triangle[0][0])
    yvals.append(triangle[0][1])
    plt.plot(xvals,yvals,':o', color='deepskyblue',label='Triangle')
    
def midPoint(triangle):
    x = (triangle[0][0]+triangle[1][0])/2
    y = (triangle[0][1]+triangle[1][1])/2
    return np.array([x,y])

def triangleGen():
    triangle = np.zeros((3,2))
    for i in range(3):
        triangle[i][0] = np.random.rand(1,1)
        triangle[i][1] = np.random.rand(1,1)
    for i in range(len(triangle)):
        for j in range(len(triangle[i])):
            if np.random.rand(1,1) > 0.5:
                triangle[i][j] = triangle[i][j]*7 
            else:
                triangle[i][j] = triangle[i][j]*-7
    
    return triangle
    
"""
------------------------------------------------------------------------------
Example
------------------------------------------------------------------------------
"""
if __name__ == "__main__":
    hist_results = []
    tries = input('Howmany tries? Choose a number below 20!\n------------------------\n! YOU HAVE BEEN WARNED !\n------------------------\nYou will see many plots and you will need to close them)\nShow me: ')
    for i in range(int(tries)):    
        #starting triangle
        triangle = triangleGen()
        print(f'Random Triangle:\n{triangle}')
        hist_results.append(DownhillSimplexNelderMead(triangle))
        plt.show()
    print(f'There are {len(set(hist_results))} differnet results in the {tries} tries.\n With minimas of range {min(set(hist_results))} to {max(set(hist_results))}')
    input('After this step one could choose a new range of x and y values\nto determine the local minima of z.\n\nNote: The values of x and y should be chosen according to the problem\n\n\n----------------------\nHIT A KEY TO EXIT :-)\n----------------------')


    