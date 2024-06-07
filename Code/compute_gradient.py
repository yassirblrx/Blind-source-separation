  
#Cette fonction calcul le gradient du critère pénalisé : 
#information mutuelle + lambda pénalisation
#où lambda est un hyperparamètre de pénalisation
#l'information mutuelle caractérise l'indépendance
#la pénalisation normalise le vecteur et le force à avoir 
#un écart-type = 1    
          
import numpy as np
import numpy.linalg as nl

# Estimation polynomiale de la fonction score marginale (Psi) par moindres carrés
#Thèse Massoud Babaie Zadeh page 46   
def compute_gradient(y1,y2,x1,x2):
    y1=np.array(y1)
    y2=np.array(y2)
    x1=np.array(x1)
    x2=np.array(x2)
    
    N1=len(y1)
    N2=len(y2)


    m_y1=np.mean(y1)
    m_y12=np.mean(y1**2)
    m_y13=np.mean(y1**3)
    m_y14=np.mean(y1**4)
    m_y15=np.mean(y1**5)
    m_y16=np.mean(y1**6)
    m_y2=np.mean(y2)
    m_y22=np.mean(y2**2)
    m_y23=np.mean(y2**3)
    m_y24=np.mean(y2**4)
    m_y25=np.mean(y2**5)
    m_y26=np.mean(y2**6)        
 
    #Calcul des différents parametres (approximation des fonctions scores
    #par moindres carrées

    M1=np.array([[1,m_y1,m_y12,m_y13],[m_y1,m_y12,m_y13,m_y14],[m_y12,m_y13,m_y14,m_y15],[m_y13,m_y14,m_y15,m_y16]])
    M2=np.array([[1,m_y2,m_y22,m_y23],[m_y2,m_y22,m_y23,m_y24],[m_y22,m_y23,m_y24,m_y25],[m_y23,m_y24,m_y25,m_y26]])
    P1=np.array([0,1,2*m_y1,3*(m_y12)])
    P2=np.array([0,1,2*m_y2,3*(m_y22)])

    w1=-np.dot(nl.inv(M1),P1)
    w2=-np.dot(nl.inv(M2),P2)

    #calcul du Psi
    
    c=y1**2
    d=y2**2
    e=y1**3
    f=y2**3

    E1 = np.ones(len(y1), dtype=int)
    E2 = np.ones(len(y2), dtype=int)

    # print(len(y1))
    Psi_y1= w1[0]*E1 + w1[1]*y1 + w1[2]*c + w1[3]*e
    Psi_y2= w2[0]*E2 +w2[1]*y2+w2[2]*d+w2[3]*f
    
    #Calcul de la Jacobienne de l'information mutuelle
    M_Psi11=sum(Psi_y1*x1)/len(x1)
    M_Psi12=sum(Psi_y1*x2)/len(x2)
    M_Psi21=sum(Psi_y2*x1)/len(x1)
    M_Psi22=sum(Psi_y2*x2)/len(x2)
    Sep = [[M_Psi11,M_Psi12],[M_Psi21,M_Psi22]]

    #J'enlève la moyenne
    y1=y1-(sum(y1)/len(y1))
    y2=y2-(sum(y2)/len(y2))

    #Calcul de la Jacobienne de la normalisation (penalisation) 
    # papier Mohammed El Rhabi 2004
    temp1=np.dot(4*(sum(y1**2)/len(y1)-1),y1)
    temp2=np.dot((sum(y2**2)/len(y2))-1,y2)
    m_y1x1=sum(temp1*x1)/len(x1)
    m_y1x2=sum(temp1*x2)/len(x2)
    m_y2x1=sum(temp2*x1)/len(x1)
    m_y2x2=sum(temp2*x2)/len(x2)
    pen=[ [m_y1x1,m_y1x2],[m_y2x1, m_y2x2] ]

    return [Sep,pen]
 


 
