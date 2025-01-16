import numpy as np
from roblib import *

class robot():

    def __init__(self, x0, y0, vx0,vy0,theta0):
        self.X = np.array([[x0],
                           [y0],
                           [vx0],
                           [vy0],
                           [theta0]])
        

def evolue():
    robA.X = A@robA.X + mvnrnd2(np.array([0,0,0,0,0]), Galpha)
    robB.X = A@robB.X + mvnrnd2(np.array([0,0,0,0,0]), Galpha)

    

def affichage():
    xA,yA,_,_,thetaA = robA.X.flatten()
    xB,yB,_,_,thetaB = robB.X.flatten()
    clear(ax)
    scatter(xA, yA, color="blue")
    ax.quiver(xA, yA, cos(thetaA), sin(thetaA), angles='xy', scale_units='xy', scale=1,color="blue")
    scatter(xB, yB, color="red")
    ax.quiver(xB, yB, cos(thetaB), sin(thetaB), angles='xy', scale_units='xy', scale=1,color="red")

def g(rob): # à revoir, est-ce que je mets des valeurs parfaites vues par les capteurs ?
    xA,yA,_,_,thetaA = robA.X.flatten()
    x,y,_,_,theta = rob.X.flatten()

    return np.array([[(y-yA)**2+(x-xA)**2],
                     [np.arctan2(y-yA,x-xA)]])

def evolueKalman():
    #/!\ attentio ndans mon cas je dois faire un kalman étendu donc je n'ai pas z=g(x)+alpha mais j'ai y = g(xchap)+dg(xchap)/dx * (xchap-x)
    # si j'appelle C dg(xchap)/dx alors j'ai z = y-g(xchap)+Cxchap = Cx (tous ce qui dépend de x d'un côté, le reste de l'autre) 

    xA,yA,_,_,thetaA = robA.X.flatten()
    xB,yB,_,_,thetaB = robB.X.flatten()

    y = g(robB)+mvnrnd2(np.array([0,0]), Gbeta)

    xhat,yhat,_,_,thetahat =robhat.X.flatten()

    C = np.array([[2*(xhat-xA), 2*(yhat-yA),0,0,0],
                  [-(yhat-yA)/((xhat-xA)**2+(yhat-yA)**2), (xhat-xA)/((xhat-xA)**2+(yhat-yA)**2),0,0,0]]) #TODO revoir ça
    z= y-g(robhat)+C@robhat.X
    

    robhat.X,robhat.Gx = kalman(robhat.X,robhat.Gx,0,z,Galpha,Gbeta,A,C)
    print(robhat.X)

def affichageKalman():
    xxhat,yxhat,_,_,_ = robhat.X.flatten()
    draw_ellipse_cov(ax,[xxhat,yxhat],robhat.Gx[:2,:2],0.99,[0.8,0.8,1])

if __name__ == "__main__":
    robA = robot(0,0,0,0,0)
    robB = robot(5,10,0,0,0)

    robhat = robot(5,5,0,0,0) #vecteur d'état approximé par Kalman de B (d'après A)
    robhat.Gx = 10**4*np.eye(5)

    dt = 0.001
    
    A = np.array([[1, 0, dt, 0, 0],
                  [0, 1, 0, dt, 0],
                  [0, 0, 1-dt**2, 0, 0],
                  [0, 0, 0, 1-dt**2, 0],
                  [0, 0, 0, 0, 1]])
    Galpha = np.diag([0,0,dt,dt,dt])
    Gbeta = np.diag([16,5*np.pi/180])
    ax=init_figure(-15,15,-15,15)

    while True:
        
        #Le filtre de Kalman de A calcule la position prédite de B
        evolueKalman()
        affichageKalman()
        #Chaque robot se déplace aléatoirement
        evolue()
        affichage()

        
        
    show()



        