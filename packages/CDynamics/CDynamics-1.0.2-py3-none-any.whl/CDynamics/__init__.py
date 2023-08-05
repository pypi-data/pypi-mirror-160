import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

class Julia:
    """
    Author: Kanak Dhotre
    Email: dhotrekanak@gmail.com
    Documentation & Examples: https://github.com/kanakdhotre99/CDynamics
    """
    def __init__(f,p,q=[1],init=True):
        f.num = np.array(p)
        f.den = np.array(q)
        f.numdeg = len(p)-1
        f.dendeg = len(q)-1
        if init:
            f.nsym, f.dsym = np.polynomial.Polynomial(p),np.polynomial.Polynomial(q)
            f.ndsym, f.ddsym = f.nsym.deriv(), f.dsym.deriv()
            f.dernum = (f.ndsym*f.dsym - f.ddsym*f.nsym).coef
            f.derden = (f.dsym**2).coef
            f.critical_points = np.asarray( list(set(np.polynomial.Polynomial(f.dernum).roots())) )
        else:
            pass
    def eval_(arr,a):
        z = 0
        for i in range(len(arr)-1,-1,-1):
            z = arr[i]+(a*z)
        return(z)
    def derivative(f,z):
            return(Julia.eval_(f.dernum,z)/Julia.eval_(f.derden,z))
    def fixed_points(f):
        roots = list(set((f.nsym-(np.polynomial.Polynomial([0,1])*f.dsym)).roots()))
        multipliers = [f.derivative(i) for i in roots]
        return([x for _, x in sorted(zip(multipliers, roots))])
    def grid(a,b,c,d,resx,resy):
        xvals = np.linspace(a,b,resx)
        yvals = np.linspace(c,d,resy)
        points = []
        for i in yvals:
            for j in xvals:
                points.append(complex(j,i))
        return(points)
    def orbit(f,seed,depth,bail_out):
        o = [seed]
        for i in range(depth):
            z = Julia.eval_(f.num,o[-1])/Julia.eval_(f.den,o[-1])
            if abs(z)<bail_out:
                o.append(z)
            else:
                break
        return(np.asarray(o))
    def plot(f,a=-1,b=1,c=-1,d=1,resx=300,resy=300,depth=25,bail_out=1000,filled=True,glow=0,cmap='binary',
             scale=1,grid=True,critical_orbit_depth=0,fixed_points=True,
             cols=[(61, 64, 91),(244, 241, 222), (224, 122, 95),(129, 178, 154),(242, 204, 143)]):
        def plot_orbit(orb):
            orb_mod = [[(orb[i].real+b)*(resx/(b-a)),(orb[i].imag+d)*(resy/(d-c))] for i in range(len(orb))]
            for i in range(len(orb_mod)-1):
                ax.add_artist(ConnectionPatch(orb_mod[i],orb_mod[i+1],"data","data",arrowstyle="->"))
        def find_nearest(arr, z):
            arr = np.asarray(arr)
            idx = (np.abs(arr - z)).argmin()
            return(arr[idx])
        fps = Julia.fixed_points(f)
        points = Julia.grid(a,b,c,d,resx,resy)
        if filled:
            ol = []
            cfp = []
            for i in points:
                o = Julia.orbit(f,i,depth,bail_out)
                ol.append(len(o))
                can = find_nearest(fps,o[-1])
                if (f.numdeg<=f.dendeg) or (f.numdeg>f.dendeg and np.abs(can-o[-1])<1):
                    cfp.append(can)
                else:
                    cfp.append(np.inf)
            if f.numdeg>=f.dendeg:
                fps.insert(0, np.inf)
            colors = [ (int(cols[fps.index(cfp[i])][0]+(ol[i]*glow*0.299)),
                        int(cols[fps.index(cfp[i])][1]+(ol[i]*glow*0.587)),
                        int(cols[fps.index(cfp[i])][2]+(ol[i]*glow*0.114) )) for i in range(len(points)) ]
            colors = np.asarray(colors).reshape(resy,resx,-1)
            ydim,xdim = colors.shape[:2]
            plt.imshow(colors,aspect=(d-c)/(b-a))
        else:
            colors = []
            for i in points:
                colors.append(len(Julia.orbit(f,i,depth,bail_out)))
            colors = np.asarray(colors).reshape(resy,resx)
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
        if critical_orbit_depth<=0:
            pass
        elif critical_orbit_depth==1:
            crits = f.critical_points
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in crits],[(z.imag+d)*(resy/(d-c)) for z in crits],c='Black')
        else:
            crits = f.critical_points
            orbs = [Julia.orbit(f,crits[i],critical_orbit_depth,1000) for i in range(len(crits))]
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in crits],[(z.imag+d)*(resy/(d-c)) for z in crits],c='Black')
            [plot_orbit(orbs[i]) for i in range(len(orbs))]
        if fixed_points == True:
            plt.scatter([(z.real+b)*(resx/(b-a)) for z in fps],[(z.imag+d)*(resy/(d-c)) for z in fps],c='Black',marker='x')