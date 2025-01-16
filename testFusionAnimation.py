from roblib import *
from tools import *
import time
import matplotlib.pyplot as plt

class Amer():
    def __init__(self,id, x,y,col):
        self.id = id
        self.x, self.y = x,y
        self.color = col
        self.theta = 0
    
    def display(self,ax):
        draw_rov2D(ax,array([[self.x],[self.y],[self.theta]]), col=self.color, facing = "right")
        #ax.scatter(self.x, self.y, color=self.color)

class BlueROV2D():
    def __init__(self,id, x0,y0, theta0,col="blue"):
        self.X = array([[x0],
                        [y0],
                        [theta0]])
        self.tracking = False
        self.kp = 3.
        self.id = id
        self.col = col
        self.FOV = 90
        self.distOfView = 100
        self.LrobInFOV = []
        self.cpt = 0 # compter of iteration without new order
        self.t0 = time.time()
        self.vMax, self.wMax = 30, 1
        self.v,self.w = 0,0
        self.control_input = np.array([[0],
                                       [0],
                                       [0]]) 
        self.turn = np.random.uniform(-pi,pi)
        self.doDisplayQuiver = False
        self.U = np.array([[0],
                           [0],
                           [0]])
        
    def control(self):
        v1,v2,w = self.U.flatten()
        x,y,theta = self.X.flatten()
        Xp = np.array([[v1],
                       [v2],
                       [w]])
        return Xp
    
    def integration(self,Xp):
        X = self.X + Xp*dt
        return X
                       
    def display(self, ax): 
        x,y,theta = self.X.flatten()
        
        #ax.scatter(x,y,color="blue")
        draw_rov2D(ax,array([[x],[y],[theta]]), col=self.col, facing = "right")

    def displayFOV(self,ax):
        x,y,theta = self.X.flatten()
        dx,dy,dtheta = 0,0,0
        xcamera, ycamera,thetacamera = x+dx, y+dy, theta+dtheta
        FOV = self.FOV*pi/180
        r = self.distOfView
        triangle_x = [xcamera, xcamera+r*cos(thetacamera+FOV/2),xcamera+r*cos(thetacamera-FOV/2),xcamera]
        triangle_y = [ycamera, ycamera+r*sin(thetacamera+FOV/2),ycamera+r*sin(thetacamera-FOV/2),ycamera]
        ax.fill(triangle_x, triangle_y, self.col, alpha=0.2)


        

def initDisplay():
    ax=init_figure(Wxmin-5,Wxmax+5,Wymin-5,Wymax+5)
    return ax



    

class RobEgo():
    def __init__(self,robGeo, amer):
        self.FOV = 90
        self.distOfView = 100
        self.col = "purple"
        self.X = np.array([[amer.x-robGeo.X.flatten()[0]],
                        [amer.x-robGeo.X.flatten()[1]]])
    
        self.U = np.array([[robGeo.U.flatten()[0]],   #v1
                        [robGeo.U.flatten()[1]], #v2
                        [robGeo.U.flatten()[2]], #w
                        [robGeo.X.flatten()[2]]])#cap
        
        self.Xp = np.array([[0],
                            [0]])

    def control(self,robGeo,amer):
        self.X = np.array([[amer.x-robGeo.X.flatten()[0]],
                        [amer.x-robGeo.X.flatten()[1]]])
    
        self.U = np.array([[robGeo.U.flatten()[0]],   #v1
                        [robGeo.U.flatten()[1]], #v2
                        [robGeo.U.flatten()[2]], #w
                        [robGeo.X.flatten()[2]]])#cap
        
        p1,p2 = self.X.flatten()
        v1,v2,w,cap = self.U.flatten()
        
        Rot = np.array([[np.cos(cap), -np.sin(cap)],
                        [np.sin(cap), np.cos(cap)]])
        print(Rot)
        V = np.array([[v1],
                      [v2]])
        self.Xp = Rot@V

        #integration
        self.X = self.X + self.Xp*dt
        
    def displayRobAmerFOV(self,ax,robGeo, amer):
        p1,p2 = self.X.flatten()
        xrob = np.array([[0],[0],[0]])
        draw_rov2D(ax,xrob,col='blue',scale=1,w=2, facing="right")
        self.displayFOV(ax)
    
        xa,ya,theta = amer.x, amer.y, amer.theta
        xr,yr,thetar = robGeo.X.flatten()
        theta = np.arctan2(ya-yr, xa-xr)

        Rot = np.array([[cos(theta), -sin(theta)],
                        [sin(theta), cos(theta)]])
        
        X = -Rot@np.array([[p1],[p2]]) 
        xamer = np.array([[X.flatten()[0]],[X.flatten()[1]],[-thetar]])
        draw_rov2D(ax,xamer,col='red',scale=1,w=2, facing="right")
        

    def displayFOV(self,ax):
        FOV = self.FOV*pi/180
        r = self.distOfView
        triangle_x = [0, 0+r*cos(0+FOV/2),0+r*cos(0-FOV/2),]
        triangle_y = [0, 0+r*sin(0+FOV/2),0+r*sin(0-FOV/2),]
        ax.fill(triangle_x, triangle_y, self.col, alpha=0.2)

def main():
    plt.ion()
    fig, (axGeo, axEgo) = plt.subplots(1, 2, figsize=(8, 6))
    axEgo.xmin, axEgo.xmax, axEgo.ymin, axEgo.ymax = Wxmin,Wxmax,Wymin,Wymax
    axGeo.xmin, axGeo.xmax, axGeo.ymin, axGeo.ymax = Wxmin,Wxmax,Wymin,Wymax
    axGeo.set_aspect('equal', adjustable='box')  # Rapport d'aspect 1:1
    axEgo.set_aspect('equal', adjustable='box')  # Rapport d'aspect 1:1

    t0 = time.time()
    amer = Amer(0,0,0,"red")
    robGeo = BlueROV2D(0,0,0,0,col="purple") 
    robEgo = RobEgo(robGeo,amer)
    
        
    while(True):
        k=1
        if  0/k < time.time()- t0 < 10/k: robGeo.U = np.array([[10],[0],[0]])
        if 10/k < time.time()- t0 < 20/k: robGeo.U = np.array([[0],[0],[1]])
        if 20/k < time.time()- t0 < 30/k: robGeo.U = np.array([[0],[10],[0]])
        if 30/k < time.time()- t0 < 50/k: robGeo.U = np.array([[0],[0],[-1]])
        
        Xp = robGeo.control()
        robGeo.X = robGeo.integration(Xp)
        
        axGeo.cla()
        axEgo.cla()
        axEgo.set_xlim(axEgo.xmin,axEgo.xmax)
        axEgo.set_ylim(axEgo.ymin,axEgo.ymax)
        axGeo.set_xlim(axGeo.xmin,axGeo.xmax)
        axGeo.set_ylim(axGeo.ymin,axGeo.ymax)
        robEgo.control(robGeo,amer)

        # display Geo
        robGeo.display(axGeo)
        robGeo.displayFOV(axGeo)
        amer.display(axGeo)

        # display Ego
        robEgo.displayRobAmerFOV(axEgo,robGeo, amer)
        
        
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Pause pour simuler un délai en temps réel
        time.sleep(1/60)
        
        
        

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    deltaT = 1
    Wxmin,Wxmax,Wymin,Wymax = -15,15,-15,15
    dt = 0.01
    main()