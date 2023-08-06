import matplotlib.pyplot as plt
import numpy as np
import time

# Welcome to the Spoonful Library - an attempt/passion project to combine all
# of the most essential tools in scientific methods!

# This package contains the beginnings of a journey to efficiency in

# - Numerical Integration
# - Root Finding
# - Differential Equations

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# General Integrator Class

class Integrator(object):
    
    """A general class of numerical integration techniques
    
    
    Parameters
    __________
    
    a : float
    
        start of interval
    
    b : float
    
        end of interval
    
    n : int
        
        number of evaluation points
        
    f : function
        
        (single-variable) function to be integrated
    
    
    Returns
    _______
    
    float
        
        numerical result for the area under the function over [a, b]
    """
    
    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n
        self.dx = (b - a)/n
    
    def Simpson(self, f):
        
        """Numerical integration via Simpson's 1/3 Rule
        
        Parameters
        __________
        
        f : function
        
            (single-variable) function to be integrated
        
        
        Returns
        _______
        
        float
            
            numerical result for the area under the function over [a, b]
        """
        
        start = time.perf_counter()
        # Evaluation Points
        xvals = np.linspace(self.a + self.dx, self.b - self.dx, self.n)
        # Initial Sum
        S = (self.dx/3)*(f(self.a) + f(self.b)) 
        # Integrated Sum
        for j in xvals[::2]:
            S += (4*self.dx/3)*f(j)
        for k in xvals[1::2]:
            S += (2*self.dx/3)*f(k)
        
        end = time.perf_counter()
        
        print("Finished in {} second(s)".format(end - start))
        return S

    def Trapezoid(self, f):
        
        """Numerical integration via Trapezoidal Sums
        
        Parameters
        __________
        
        f : function
        
            (single-variable) function to be integrated
        
        
        Returns
        _______
        
        float
            
            numerical result for the area under the function over [a, b]
        """
        
        start = time.perf_counter()
        # Evaluation Points 
        # Use Generators since we don't need list operations
        xvals = np.linspace(self.a + self.dx, self.b - self.dx, self.n)
        # Initial Sum
        S = (self.dx/2)*(f(self.a) + f(self.b))
        # Integrated Sum
        for xval in xvals:
            S += (self.dx/2)*f(xval)
        
        end = time.perf_counter()
        
        print("Finished in {} second(s)".format(end - start))
        return S


# General ODE Integration Class

class ODE(object):
    
    """A general class of numerical techniques to integrating ODEs
    
    
    Parameters
    __________
    
    t_0 : float
        
        initial time
    
    t_f : float
    
        final time
    
    n : int
    
        number of evaluation points
    
    IC : float / list
        
        function evaluation at t_0 ; Initial Condition
    
    Returns
    _______
    
    list
        
        list of function evaluations corresponding to the solution of the ODE.
            
    Optional
    
        returns plot of function evaluations
    """

    def __init__(self, t_0, t_f, n, IC):
        self.t_0 = t_0 
        self.t_f = t_f 
        self.IC = IC 
        self.t = np.linspace(t_0, t_f, n)
        self.h = self.t[1] - self.t[0]
    
    def RK4(self, f, plot=True, label='', color=''):
        
        """Runge Kutta Method of 4th Order
    
    
        Parameters
        __________
        
        f : function
            
            dy/dt = f(y, t)
        
        Optional Parameters
        ___________________
        
        plot = True
        
            automatically returns matplotlib graph of the solution over [t_0, t_f]
        
        label = ''
        
            title of auto-generated plot
        
        color = ''
            
            color of the resulting plot
        
        Returns
        _______
        
        list
        
            list of function evaluations corresponding to the solution of the ODE.
                
        Optional
        
            returns plot of function evaluations
            
        """
        
        start = time.perf_counter()
        
        # Initialize list-solution
        self.y = np.zeros(len(self.t))
        
        for i in range(len(self.t) - 1):
            K1 = f( self.t[i], self.y[i] )
            K2 = f( self.t[i] + self.h/2, self.y[i] + self.h*K1/2 )
            K3 = f( self.t[i] + self.h/2, self.y[i] + self.h*K2/2 )
            K4 = f( self.t[i] + self.h, self.y[i] + self.h*K3 )
            
            self.y[i + 1] = self.y[i] + (self.h/6)*(K1 + 2*K2 + 2*K3 + K4)
        
        if plot==True:
            # Include all special commands for plotting in here
            self.label = label
            self.color = color
            if color!='':
                plt.plot(self.t, self.y, color=self.color)
                plt.title("{}".format(self.label))
                plt.grid()
                plt.show()
            else:
                plt.plot(self.t, self.y)
                plt.title("{}".format(self.label))
                plt.grid()
                plt.show()
        
        end = time.perf_counter()
        
        print("Finished in {} second(s)".format(end - start))
        return self.y

    def CoupledRK4(self, f_1, f_2, plot=True, label=''):
        
        """N-variable system of Coupled ODEs - Uses Runge Kutta of 4th Order
    
    
        Parameters
        __________
        
        f_1 : function
            
            f_1(t, x, v) - first derivative function
        
        f_2 : function
            
            f_2(t, x, v) - second derivative function
            
            pass f_1 and f_2 as functions of (t, x, v) even if they do not depend
            on some of those variables
            
            rewrite the ODE to be of N coupled 1st-order ODEs pass the list of 
            functions to be integrated in order
        
        Optional Parameters
        ___________________
        
        plot = True
        
            automatically returns matplotlib graph of the solution over [t_0, t_f]
        
        label = ''
        
            title of auto-generated plot
        
        Returns
        _______
        
        list
        
            list of function evaluations corresponding to the solution of the ODE.
        
        Optional
        
            returns plot of function evaluations
            
        """
        
        start = time.perf_counter()
        
        # Initialize list-solution
        self.y = np.zeros(len(self.t))
        self.f_1 = f_1
        self.f_2 = f_2
        
        self.x = np.zeros(len(self.t))
        self.v = np.zeros(len(self.t))
        
        # Initial Conditions pulled from IC list in ODE()
        self.x[0] = self.IC[0]
        self.v[1] = self.IC[1]
        
        for i in range(len(self.t) - 1):
            # Hard coding beware - it's fine with a system of 2 coupled ODEs, 
            # but for nth order systems be more clever
            K1x = f_1( self.t[i], self.x[i], self.v[i] )
            K1v = f_2( self.t[i], self.x[i], self.v[i] )
            K2x = f_1( self.t[i] + self.h/2, self.x[i] + self.h*K1x/2, self.v[i] + self.h*K1v/2 )
            K2v = f_2( self.t[i] + self.h/2, self.x[i] + self.h*K1x/2, self.v[i] + self.h*K1v/2 )
            K3x = f_1( self.t[i] + self.h/2, self.x[i] + self.h*K2x/2, self.v[i] + self.h*K2v/2 )
            K3v = f_2( self.t[i] + self.h/2, self.x[i] + self.h*K2x/2, self.v[i] + self.h*K2v/2 )
            K4x = f_1( self.t[i] + self.h, self.x[i] + self.h*K3x, self.v[i] + self.h*K3v )
            K4v = f_2( self.t[i] + self.h, self.x[i] + self.h*K3x, self.v[i] + self.h*K3v )
            
            self.x[i+1] = self.x[i] + (self.h/6)*(K1x + 2*K2x + 2*K3x + K4x)
            self.v[i+1] = self.v[i] + (self.h/6)*(K1v + 2*K2v + 2*K3v + K4v)
            
        if plot==True:
            # Include all special commands for plotting in here
            self.label = label
            plt.plot(self.t, self.y)
            plt.title("{}".format(self.label))
            plt.grid()
            plt.show()
        
        end = time.perf_counter()
        
        print("Finished in {} second(s)".format(end - start))
        return self.y



def eq_1(x, y, y_dot): #this is basically to say y' = y'
    return y_dot

def eq_2(x, y, y_dot):
    return (-0.5*y + 2.5*y_dot)

ODE(3, 10, 100, [6, -1]).CoupledRK4(eq_1, eq_2)










