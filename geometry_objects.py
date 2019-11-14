#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:11:48 2017

@author: Wojciech chacholski

Copyright Wojciech chacholski, 2018
This software is to be used only for activities related 
to SF2956 TDA course at KTH.
"""

import stableRANK as sr

import numpy as np
inf=float("inf")
import scipy.stats as st

import matplotlib.pyplot as plt
#plt.clf()
#plt.cla()
#plt.close()
plt.style.use('ggplot')

import itertools as it
############
# CIRCLE
############    
class circle(sr.euc_object):
    
    def __init__(self,arg, number_points, error, pdistribution="Gauss"):
        r=arg #radious
        T = np.random.uniform(high=2*np.pi, size=number_points)
        if pdistribution=="Gauss":
            sd=error*0.635
            pdf=st.norm(loc=[0,0],scale=(sd,sd))
            N=pdf.rvs((number_points,2))
        else:
            N1 = np.random.uniform(high=2*error, size=(number_points,2))   
            N=N1-error       
        Y= np.sin(T)*(r)
        X= np.cos(T)*(r)
        self.points=N+np.vstack((X,Y)).transpose()
        self.arg=arg
        self.number_points=number_points
        self.error=error
        self.pdistribution=pdistribution
        self.name="circle"
        self.type="circle"
        self.radious=r
        self.dim=2
        self.area=np.pi * r * r
        self.length=2 * np.pi * r
        
        
############
# SQUARE
############   
class square(sr.euc_object):

    def __init__(self,arg,number_points, error, pdistribution="Gauss"):
        a=arg #half of the side
        T = np.random.uniform(high=8*a,size=number_points)
        N=np.empty([0, 2])
        if pdistribution=="Gauss":
            sd=error*0.635
            pdf=st.norm(loc=[0,0],scale=(sd,sd))
            N=pdf.rvs((number_points,2))
        else:
            N1 = np.random.uniform(high=2*error, size=(number_points,2))   
            N=N1-error        
        X=np.array([])
        Y=np.array([])
        for t in T:
            if t>=0 and t<=2*a:
                X=np.concatenate([X,np.array([t - a])])
                Y=np.concatenate([Y,np.array([a])])
            elif t>=2*a and t<=4*a:
                X=np.concatenate([X,np.array([a])])
                Y=np.concatenate([Y,np.array([3*a - t])])
            elif t>=4*a and t<=6*a:
                X=np.concatenate([X,np.array([5*a  - t])])
                Y=np.concatenate([Y,np.array([-a])])
            elif t>=6*a and t<=8*a:
                X=np.concatenate([X,np.array([-a])])
                Y=np.concatenate([Y,np.array([t - 7*a ])])
        self.points=N+np.vstack((X,Y)).transpose()
        self.arg=arg
        self.number_points=number_points
        self.error=error
        self.pdistribution=pdistribution
        self.name="square"
        self.type="square"
        self.side=2*a
        self.dim=2
        self.area=4 * a * a
        self.length=8 * a 
     
############
# RECTANGLE
############   
class rectangle(sr.euc_object):
    
    def __init__(self, arg, number_points, error, pdistribution="Gauss"):
        a=arg[0] #half of one side
        b=arg[1] #half of the other side
        T = np.random.uniform(high=4*a+4*b,size=number_points)

        X=np.array([])
        Y=np.array([])
        for t in T:
            if t>=0 and t<=2*a:
                X=np.concatenate([X,np.array([t - a])])
                Y=np.concatenate([Y,np.array([b])])
            elif t>=2*a and t<=2*a + 2*b:
                X=np.concatenate([X,np.array([a])])
                Y=np.concatenate([Y,np.array([2*a + b - t])])
            elif t>=2*a + 2*b and t<=4*a + 2*b:
                X=np.concatenate([X,np.array([3*a + 2*b - t])])
                Y=np.concatenate([Y,np.array([-b])])
            elif t>=4*a + 2*b and t<=4*a + 4*b:
                X=np.concatenate([X,np.array([-a])])
                Y=np.concatenate([Y,np.array([t - 4*a -3*b])])
        N=np.empty([0, 2])
        if pdistribution=="Gauss":
            sd=error*0.635
            pdf=st.norm(loc=[0,0],scale=(sd,sd))
            N=pdf.rvs((number_points,2))
        else:
            N1 = np.random.uniform(high=2*error, size=(number_points,2))   
            N=N1-error        
        self.points=N+np.vstack((X,Y)).transpose()
        self.arg=arg
        self.sidea=a
        self.sideb=b
        self.number_points=number_points
        self.pdistribution=pdistribution
        self.error=error
        if a==b:
            self.name="square"
        else:
            self.name="rectangle"
        self.type="rectangle"
        self.dim=2
        self.area=4 * a * b
        self.length=4 * a + 4 * b   

############
# NGON
############
class ngon(sr.euc_object):      

    def __init__(self, arg, number_points, error, pdistribution="Gauss"):   
        vertices=arg
        number_vertices=len(vertices)
        L1=np.linalg.norm(vertices[1:,:]-vertices[:-1,:], axis=1)
        L=np.concatenate([L1,np.array([np.linalg.norm(vertices[0]-vertices[-1])])])
        accum_L=np.asarray(list(it.accumulate(L)))
        T = np.random.uniform(high=accum_L[-1],size=number_points)        
        points=np.empty([0,2])
        for t in T:
            index=np.searchsorted(accum_L,t)
            coef=(accum_L[index]-t)/(L[index])
            if index==number_vertices-1:
                points=np.vstack((points,(coef*vertices[0] + (1-coef) * vertices[-1])))
            else:
                points=np.vstack((points,(coef*vertices[index+1] + (1-coef) * vertices[index])))
        N=np.empty([0, 2])
        if pdistribution=="Gauss":
            sd=error*0.635
            pdf=st.norm(loc=[0,0],scale=(sd,sd))
            N=pdf.rvs((number_points,2))
        else:
            N1 = np.random.uniform(high=2*error, size=(number_points,2))   
            N=N1-error
        self.points=N+points
        self.arg=arg
        self.number_points=number_points
        self.error=error
        self.pdistribution=pdistribution
        if arg.shape[0]==2:
            self.name="interval"
        elif arg.shape[0]==3:
            self.name="triangle"
        else:
            self.name=str(arg.shape[0])+"-gon"
        self.type="ngon"
        self.dim=2
        L1= np.linalg.norm(vertices[1:,:]-vertices[:-1,:], axis=1)
        #L1= np.linalg.norm(self.points[1:,:]-self.points[:-1,:], axis=1)
        self.length=sum(L1)+np.linalg.norm(vertices[0]-vertices[-1])

#############
# POINTS
#############
class points(sr.euc_object):
    def __init__(self,arg, number_points, error, pdistribution="Gauss"):
        vertices=arg
        self.number_points=number_points*len(vertices)
        N=np.empty([0, 2])
        if pdistribution=="Gauss":
            sd=error*0.635
            for i in vertices:
                pdf=st.norm(loc=i,scale=(sd,sd))
                N=np.concatenate([N,pdf.rvs((number_points,2))])
        else:
            for i in vertices:
                N1 = i+np.random.uniform(high=2*error, size=(number_points,2))   
                N=np.concatenate([N,N1])
        self.points=N
        self.error=error
        self.pdistribution=pdistribution
        self.name=str(number_points)+"points"
        self.type="points"
        self.dim=2

#############
## PINE
############# 
class pine(sr.euc_object):
    
    def __init__(self, arg, number_points, error, pdistribution="Gauss"):
        vertices=arg
        L=np.linalg.norm(vertices,axis=1)
        accum_L=np.asarray(list(it.accumulate(L)))
        T = np.random.uniform(high=accum_L[-1],size=number_points)        
        N=np.empty([0, 2])
        if pdistribution=="Gauss":
            sd=error*0.635
            pdf=st.norm(loc=[0,0],scale=(sd,sd))
            N=pdf.rvs((number_points,2))
        else:
            N1 = np.random.uniform(high=2*error, size=(number_points,2))   
            N=N1-error
        points=np.empty([0,2])
        for t in T:
            index=np.searchsorted(accum_L,t)
            points=np.vstack((points,((accum_L[index]-t)/(L[index])) * vertices[index]))
        self.points=N+points
        self.arg=arg
        self.number_points=number_points
        self.error=error
        self.name=str(len(vertices))+"-pine"
        self.type="pine"
        self.dim=2
        self.length=np.sum(np.linalg.norm(self.arg,axis=1))
        self.pdistribution=pdistribution


########################################
#### FUNCTIONS        
########################################

def shape(obj_arg=("circle",1), number_points=100, error=0.1,pdistribution="Gauss"):
    object_type=obj_arg[0]
    arg=obj_arg[1]
    if object_type=="circle":
        return circle(arg, number_points,error,pdistribution)
    elif object_type=="square":
        return square(arg,number_points,error,pdistribution)
    elif object_type=="rectangle":
        return rectangle(arg, number_points,error,pdistribution)
    elif object_type=="pine":
        return pine(arg, number_points,error,pdistribution)
    elif object_type=="ngon":
        return ngon(arg, number_points,error,pdistribution)
    elif object_type=="points":
        return points(arg, number_points,error,pdistribution)
    else:
        raise ValueError("There is no plane shape with that name") 

def shapes_data(obj_arg_dict,number_points, error, pdistribution, number, file_name=None,date="no"):
    """INPUT:
    1.arg_dict:dictionary of plane object arguments. Its keys are called labels. 
    2.number_points: a list of how many points should be sampled.
    3.error: a list of erorr at which the points are sampled at
    4.pdistribution: a list of distribiution from "Gauss" or "square"
    4.number: a number of repetition of each plane object. Associated number is called index.
    OUTPUT: a panda series of euc objects"""
    labels=np.asarray([*obj_arg_dict])
    numbers=np.arange(number)
    X=pd.MultiIndex.from_product([labels,number_points,error,pdistribution, numbers])
    points={}
    for i in X:
        print("Generating geo_object: ",i)
        points[i]=shape(obj_arg_dict[i[0]],i[1],i[2],i[3])
    outcome=pd.Series(points)
    outcome.index.names=["Label","Number_points","Error","pdistribution","Index"]
    if file_name!=None:
        if date!="no":
            A=str(datetime.now().strftime('%Y_%m_%d_(%H_%M)'))
            pickle.dump(outcome, open(file_name+A, "wb"),protocol=2)
        else:   
            pickle.dump(outcome, open(file_name, "wb"),protocol=2)
    return outcome
    
if __name__ == "__main__":
    object_type="circle"
    arg=100
    number_points=70
    error=2
    pdistribution="Gauss"    
    C=shape((object_type,arg),number_points,error,pdistribution)
    
    C.plot()
    maxdim=1
    thresh=inf
    coeff=2
    distance_matrix=False
    do_cocycles=False
    metric='euclidean'
    br=C.barcode(maxdim, thresh, coeff, distance_matrix, do_cocycles, metric)

    br.plot()
    
    contours={"H0": [  [[0],[1]], ("dist", inf, inf)] }
