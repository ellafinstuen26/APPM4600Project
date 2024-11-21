import matplotlib.pyplot as plt
import numpy as np
import math
from numpy.linalg import inv
from numpy.linalg import norm

def driver():
    #THIS CODE IS FOR LINEARLY CONVERGENT NEWTON'S
    Nmax = 100
    x0 = np.array([1.0, -2.0, 2.0])
    tol = 1e-6
    
    [xstar, gval, ier,errors] = NewtonMethod(x0, tol, Nmax)
    print("The Newton method found the solution:", xstar)
    print("g evaluated at this point is:", gval)
    print("ier is:", ier)

    # Plotting log(error) vs. iterations
    iterations = range(len(errors))
    log_errors = np.log(errors)  # Compute log of errors
    
    # plt.figure(figsize=(8, 6))
    # plt.plot(iterations, log_errors, marker='o')
    # plt.xlabel('Iteration $k$', fontsize=14)
    # plt.ylabel(r'$\log(e_k)$', fontsize=14)
    # plt.title("Newton's Method Performance", fontsize=16)
   
    plt.figure(figsize=(8, 6))
    plt.plot(iterations, errors, marker='o')
    plt.xlabel('Iteration $k$', fontsize=14)
    plt.ylabel(r'$e_k$', fontsize=14)
    plt.title("Newton's Method Performance", fontsize=16)
    plt.show()

def evalF(x):
    F = np.zeros(3)
    F[0] = x[0] * np.exp(x[1]) - x[2]**2 + 1
    F[1] = x[1]**3 - 4*x[1] + x[0] - 1
    F[2] = x[0]**2 + x[2]**2 - 4*x[2] + 2
    return F



def evalJ(x):
    J = np.array([
        [1,np.exp(x[1]),-2*x[2]],
        [1,3*x[1]**2-4,0],
        [2*x[0],0,2*x[2]-4]
    ])
    return J

def evalf(x):
    F = evalF(x)
    return np.dot(F,F)

def evalg(x):
    F = evalF(x)
    g = F[0]**2 + F[1]**2 + F[2]**2
    return g

def eval_gradg(x):
    F = evalF(x)
    J = evalJ(x)
    return 2 * np.dot(J.T, F)

def eval_hessianf(x):
    F = evalF(x)
    J = evalJ(x)
    
    n = len(F)
    m = len(x)
    second_derivatives = np.zeros((m, m))
    for i in range(n):
        Fi_hessian = eval_hessianFi(x, i)  # Hessian of each F_i
        second_derivatives += 2 * F[i] * Fi_hessian
    
    # Full Hessian
    return 2 * np.dot(J.T, J) + second_derivatives

def eval_hessianFi(x, i):

    H = np.zeros((3, 3))  # Replace with second derivatives of F_i
    return H

###############################
### Newton's method

def NewtonMethod(x, tol, Nmax):
    errors = []
    for its in range(Nmax):
        gradf = eval_gradg(x)
        H = eval_hessianf(x)

        try:
            delta = -np.linalg.solve(H, gradf)
        except np.linalg.LinAlgError:
            print("Singular Hessian matrix")
            ier = 1
            return [x, evalf(x), ier, errors]
        
        # Update solution
        x = x + delta
        
        # Evaluate the function norm to check convergence
        
        gval = norm(gradf)
        errors.append(gval)
        if gval < tol:
            ier = 0
            return [x, gval, ier,errors]
    
    print('Max iterations exceeded')
    ier = 1
    return [x, evalg(x), ier,errors]

if __name__ == '__main__':
    driver()
