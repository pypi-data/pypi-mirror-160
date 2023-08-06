import numpy as np
import matplotlib.pyplot as plt

class Julia:
    r"""
    Author: Kanak Dhotre
    Email: dhotrekanak@gmail.com
    Documentation & Examples: https://github.com/kanakdhotre99/HDynamics
    
    UTILITY:
    HDynamics offers comprehensive functions relevant to the field of
    holomorphic dynamics. Given a rational function, f, defined on the Riemann
    sphere, using this package you can,
    
    1. Find the fixed points points of f.
    
    2. Compute the orbit of a seed under f.
    
    3. Plot approximate filled-julia & julia sets corresponding to f.
 
    4. Find the Koenigs coordinates of points in the attracting basin of f.
    
    5. Plot the Newton-fractal of f (provided f is a polynomial defined over C).
    
    EXAMPLES:
    Julia.fixed_points([0,0,0,0,4,0,-4,0,1],[1,0,-4,0,2])
    >> [(-1.2469796037+0j),(-1+0j),(-0.6623589786-0.5622795121j), ... ]
    
    Julia.orbit(complex(1,1),[complex(0,1),0,1],[1],50,1000)
    >> [(1+1j),3j,(-9+1j),(80-17j),(-207256402585089-1990664248298239j), ... ]
    
    Julia.filled_plot([0,0,0,4,-1],[-1,4],-2,5,-2,2,1080,1080,depth=50,glow=5,
                      grid=False,scale=2)
    >> A 24-bit RGB image of the filled Julia set.
    
    Julia.plot([complex(0,1),0,1],[1],resx=1080,resy=1080)
    >> A 24-bit RGB image of the Julia set.
    
    Julia.phi(0.1,[0,complex(0,0.7),1])
    >> (0.10773758664985353-0.010877096597030775j)
    
    Julia.newton([1,-1,1,0,0,1],[1],-1,1,-1,1,1080,1080)
    >> A 24-bit RGB image of the Newton fractal.
    """
    def fixed_points(p,q):
        r"""
        UTILITY:
        Returns all finite complex-valued fixed points of the given rational
        map.
        
        ALGORITHM:
        Given f = (p/q)(z), we solve for the roots of p(z)-z*q(z) using NumPy.
        
        INPUT:
        - "p" -- list, numerator coefficients in order of increasing
        degree.
        - "q" -- list, denominator coefficients in order of increasing degree.
        
        OUTPUT:
        - "roots" -- list, a list of all finite complex-valued fixed points of
        the given rational map in increasing order
        """
        p,q,r = np.polynomial.Polynomial(p), np.polynomial.Polynomial(q), np.polynomial.Polynomial([0,1])
        s = p - r*q
        fp = sorted(list(set(s.roots())))
        roots = [np.round(i,10) for i in fp]
        return(roots)
    def grid(a,b,c,d,resx,resy):
        r"""
        UTILITY:
        Returns all discrete grid of points in the complex plane.
        
        ALGORITHM:
        Given [a,b] and [c,d] with resx and resy number of points respectively,
        we find [a,b]x[c,d] with resx*resy number of points using two for loops.
        
        INPUT:
        - "a" -- float, real part of the minimum value in the discrete grid.
        - "b" -- float, real part of the maximum value in the discrete grid.
        - "resx" -- int, number of points to be included in [axb].
        - "c" -- float, imaginary part of the minimum value in the grid.
        - "d" -- float, imaginary part of the maximum value in the grid.
        - "resy" -- int, number of points to be included in [cxd].
        
        OUTPUT:
        - "points" -- list, a list of allowed points in [a,b]x[c,d].
        """
        xvals = np.linspace(a,b,resx)
        yvals = np.linspace(c,d,resy)
        points = []
        for i in yvals:
            for j in xvals:
                points.append(complex(j,i))
        return(points)
    def orbit(seed,p,q,depth,bail_out):
        r"""
        UTILITY:
        Returns the orbit of a seed under a given rational map.
        
        ALGORITHM:
        Given seed z, we initialize a counter and recursively find f(z) while
        the counter value is less that a user-defined depth value.
        
        INPUT:
        - "seed" -- complex128, initial value of the orbit.
        - "p" -- list, numerator coefficients in order of increasing degree.
        - "q" -- list, denominator coefficients in order of increasing degree.
        - "depth" -- int, number of iterates to be computed.
        - "bail_out" -- complex128, maximum allowed value in the orbit.
        
        OUTPUT:
        - "o" -- list, a list of all points in the forward orbit of the given
        seed.
        """
        fp = Julia.fixed_points(p,q)
        def f(p,q,z):
            return( sum([p[n]*z**n for n in range(len(p))])/sum([q[n]*z**n for n in range(len(q))])    )
        o = [seed]
        for i in range(depth):
            try:
                if f(p,q,o[-1]) not in fp:
                    o.append( f(p,q,o[-1]) )
                else:
                    break
            except Exception:
                pass
        o = [i for i in o if i.real<bail_out and i.imag<bail_out]
        return(o)
    def closest(x,arr,p,q):
        r"""
        UTILITY:
        Returns the closest value in a given array to a given point.
        
        ALGORITHM:
        Given x, we iterate through all the values arr=[a1,a2, ... an] and find
        the one value, ap, which is closest x. If ap and x are not sufficiently
        close and f=p/q fixes infinity, we return np.inf instead of ap. 
        
        INPUT:
        - "x" -- complex128.
        - "arr" -- list.
        - "p" -- list, numerator coefficients in order of increasing degree.
        - "q" -- list, denominator coefficients in order of increasing degree.
        
        OUTPUT:
        - "can" -- complex128, closest value to x in arr.
        """
        degp = np.polynomial.Polynomial(p).degree()
        degq = np.polynomial.Polynomial(q).degree()
        can = arr[0]
        for i in range(len(arr)):
            if np.abs(x-arr[i])<np.abs(x-can):
                can = arr[i]     
        if degp<=degq :
            return(can)
        elif degp>degq and np.abs(x-can)<1:
            return(can)
        elif degp>degq and np.abs(x-can)>1:
            return(np.inf)
    def filled_plot(p,q,a=-1,b=1,c=-1,d=1,resx=300,resy=300,depth=25,bail_out=1000,cols=
             [(38, 70, 83), (42, 157, 143),(233, 196, 106),(244, 162, 97),
              (231, 111, 81),(255, 255, 255),(114, 9, 183),(156, 102, 68),(182,198,73)],glow=0,grid=True,scale=1):
        r"""
        UTILITY:
        Plots the filled-julia set of a rational function defined on the Riemann
        sphere.
        
        CAVEATS:
        1. The time taken to return the plot grows exponentially with the resx,
        resy and depth parameters. For exploration purposes a resolution of
        300x300 to 500x500 with unit scale is recommended. 
        
        2. Not all rational functions have attracting behaviour. If the plot is
        suspiciously blank, or not detailed enough you can introduce a glow
        parameter (recommended value = 5) and/or increase the values of resx, 
        resy and depth.
        
        ALGORITHM:
        (The algorithm is better explained over at: 
         https://github.com/kanakdhotre99)
        
        Given a rational function f=p/q we store a list of fixed points of f
        and a corresponding list of RGB tuples. Next, for each point in a user
        -dictated discrete grid we compute it's foward orbit and store the last
        iterate along with the number of iterates it took to complete the orbit.
        Based on which fixed point the last iterate is closest to, we pick an
        RGB tuple from our pallete, change it's lightness value depending on the
        length of the orbit and color the discrete grid in question.
        
        INPUT:
        - "p" -- list, numerator  coefficients in order of increasing degree.
        - "q" -- list, denominator  coefficients in order of increasing degree.
        - "a" -- float, (optional, default=-1) real part of the minimum value
        in the grid.
        - "b" -- float, (optional, default=1) real part of the maximum value
        in the grid.
        - "resx" -- int, (optional, default=300) number of points to be
        included in [axb].
        - "c" -- float, (optional, default=-1) imaginary part of the minimum
        value in the discrete grid.
        - "d" -- float, (optional, default=1) imaginary part of the maximum
        value in the discrete grid.
        - "resy" -- int, (optional, default=300) number of points to be
        included in [cxd].
        - "depth" -- int, (optional, default=25) number of iterates to be
        computed.
        - "bail_out" -- complex128, (optional, 1000) maximum allowed value in
        the orbit.
        - "cols" -- list, (optional, default=
        [(38, 70, 83), (42, 157, 143),(233, 196, 106),(244, 162, 97), (53,53,53)
         (231, 111, 81),(255, 255, 255),(114, 9, 183),(156, 102, 68),(182,198,73)])
        a list of RGB tuples
        - "glow" -- float, (optional, default=0) determines the magnitude by
        which the picked RGB tuple's ligtness value
        is increased.
        - "grid" -- bool, (optional, default=True), determines whether or not
        the grid axes need to be visible.
        - "scale" -- int, (optional, default=1), determines the scaling factor
        of the plot.
        
        OUTPUT:
        - "im" -- image, image of the filled-julia set corresponding to f=p/q
        in [a,b]x[c,d]
        """
        fps = Julia.fixed_points(p,q)
        pallete = cols[0:len(fps)]
        pallete.extend([(53,53,53)])
        if np.polynomial.Polynomial(p).degree()>np.polynomial.Polynomial(q).degree():
            fps.append(np.inf)  
        it = []
        ln = []
        points = Julia.grid(a,b,c,d,resx,resy)
        for i in points:
            o = Julia.orbit(i,p,q,depth,bail_out)
            it.append(Julia.closest(o[-1],fps,p,q))
            ln.append(len(o))
        colors = [ (int(pallete[fps.index(it[i])][0]+(ln[i]*glow*0.299)),
                    int(pallete[fps.index(it[i])][1]+(ln[i]*glow*0.587)),
                    int(pallete[fps.index(it[i])][2]+(ln[i]*glow*0.114) )) for i in range(len(it)) ]
        colors = np.asarray(colors).reshape(resy,resx,-1)
        ydim,xdim = colors.shape[:2]
        plt.imshow(colors,aspect=(d-c)/(b-a))
        ax = plt.gca()
        ax.set_xlim(0,xdim)
        ax.set_ylim(0,ydim)
        ax.set_yticks([0,ydim/2,ydim])
        ax.set_yticklabels([c, (d+c)/2, d])
        ax.set_xticks([0,xdim/2,xdim])
        supress = ax.set_xticklabels([a, (a+b)/2, b])
        fig = plt.gcf()
        fig.set_figheight( scale*10 )
        fig.set_figwidth( scale*10 )
        if grid:
            pass
        else:
            plt.axis('off')
    def plot(p,q,a=-1,b=1,c=-1,d=1,resx=300,resy=300,cmap='binary',depth=25,bail_out=1000,grid=True,scale=1):
        r"""
        UTILITY:
        Plots the julia set of a rational function defined on the Riemann
        sphere.
        
        ALGORTIHM, INPUT & OUTPUT:
        Refer to Julia.filled_plot()??
        """
        fps = Julia.fixed_points(p,q)
        if np.polynomial.Polynomial(p).degree()>np.polynomial.Polynomial(q).degree():
            fps.append(np.inf)  
        it = []
        ln = []
        points = Julia.grid(a,b,c,d,resx,resy)
        for i in points:
            o = Julia.orbit(i,p,q,depth,bail_out)
            it.append(Julia.closest(o[-1],fps,p,q))
            ln.append(len(o))
        colors = np.asarray(ln).reshape(resy,resx)
        ydim,xdim = colors.shape[:2]
        plt.imshow(colors,aspect=(d-c)/(b-a),cmap=cmap)
        ax = plt.gca()
        ax.set_xlim(0,xdim)
        ax.set_ylim(0,ydim)
        ax.set_yticks([0,ydim/2,ydim])
        ax.set_yticklabels([c, (d+c)/2, d])
        ax.set_xticks([0,xdim/2,xdim])
        supress = ax.set_xticklabels([a, (a+b)/2, b])
        fig = plt.gcf()
        fig.set_figheight( scale*10 )
        fig.set_figwidth( scale*10 )
        if grid:
            pass
        else:
            plt.axis('off')
    def phi(z,p,q=[1],depth=20,bail_out=1000):
        r"""
        UTILITY:
        Returns the Koenigs coordinate of a point in the basin of attraction of
        rational function, f,  which is locally expressed as a polynomial
        mapping the fixed point of f to 0.
        
        ALGORTIHM, INPUT & OUTPUT:
        Refer to the section on "Koenigs Linearization" in "Dynamics of one
        complex variable - John Milnor (2006)"
        """
        if p[0]!=0 or q!=[1]:
            raise Exception("Express your map in terms of a local uniformizing parameter which maps the fixed point to 0")
        elif np.abs(p[1])>=1:
            raise Exception("Your map does not have attracting behaviour")
        poly = np.polynomial.Polynomial(p)
        multip = poly.deriv()(0)
        z = Julia.orbit(z,p,q,depth,bail_out)[-1]
        z = z*((multip)**(-depth))
        return(z)
    def newton(p,q=[1],a=-1,b=1,c=-1,d=1,resx=300,resy=300,depth=50,cols=
               [(38, 70, 83), (42, 157, 143),(233, 196, 106),(244, 162, 97),
                (231, 111, 81),(255, 255, 255),(114, 9, 183),(156, 102, 68),(182,198,73)],grid=True,scale=1):
        r"""
        UTILITY:
        Plots the newton-fractal corresponding to a polynomial defined over the
        complex plane.
        
        ALGORTIHM, INPUT & OUTPUT:
        Refer to Julia.filled_plot()??
        """
        if q!=[1]:
            raise Exception("Map must be a polynomial")
        pp = np.polynomial.Polynomial(p)
        fps = list(set(pp.roots()))
        def newton_orb(z):
            o = [z]
            for i in range(depth):
                z = z-(pp(z)/pp.deriv()(z))
                o.append(z)
            return(o)
        pallete = cols[0:len(fps)]
        pallete.extend([(53,53,53)])
        points = Julia.grid(a,b,c,d,resx,resy)
        it=[]
        for i in points:
            o = newton_orb(i)
            it.append(Julia.closest(o[-1],fps,p,q))
        colors = [ (int(pallete[fps.index(it[i])][0]),
                    int(pallete[fps.index(it[i])][1]),
                    int(pallete[fps.index(it[i])][2])) for i in range(len(it)) ]
        colors = np.asarray(colors).reshape(resy,resx,-1)
        ydim,xdim = colors.shape[:2]
        plt.imshow(colors,aspect=(d-c)/(b-a))
        ax = plt.gca()
        ax.set_xlim(0,xdim)
        ax.set_ylim(0,ydim)
        ax.set_yticks([0,ydim/2,ydim])
        ax.set_yticklabels([c, (d+c)/2, d])
        ax.set_xticks([0,xdim/2,xdim])
        supress = ax.set_xticklabels([a, (a+b)/2, b])
        fig = plt.gcf()
        fig.set_figheight( scale*10 )
        fig.set_figwidth( scale*10 )
        if grid:
            pass
        else:
            plt.axis('off')