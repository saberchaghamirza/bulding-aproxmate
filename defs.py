# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 13:33:51 2022

@author: Saber
"""
from math import  pi,atan2
def angle(A, B, C):
    Ax, Ay = A[0]-B[0], A[1]-B[1]
    Cx, Cy = C[0]-B[0], C[1]-B[1]
    a = atan2(Ay, Ax)
    c = atan2(Cy, Cx)
    if a < 0: a += pi*2
    if c < 0: c += pi*2
    return (pi*2 + c - a)*180/pi if a > c else (c - a)*180/pi

def angle_status_points(angle,c):
    new_a=[]
    for a in angle :
          if 45<a<135:
              a=a-90
          elif 135<a<225:
              a=a-180
          elif 225<a<315:
              a=a-270
          new_a.append(abs(a))
    min_A=min(new_a)
    for a,c1 in zip(new_a,c) : 
         if a==min_A:
             out=c1
    return out
    
        
def generate_point(a,b,xy,d) :
           c0=xy         
           angle0=angle(a,b,c0)
           c1=[xy[0]+d,xy[1]+d]
           angle1=angle(a,b,c1)
           c2=[xy[0]-d,xy[1]-d]
           angle2=angle(a,b,c2)
           c3=[xy[0]+d,xy[1]-d]
           angle3=angle(a,b,c3)
           c4=[xy[0]-d,xy[1]+d]
           angle4=angle(a,b,c4)               
           c5=[xy[0]+d,xy[1]]
           angle5=angle(a,b,c5)
           c6=[xy[0]-d,xy[1]]
           angle6=angle(a,b,c6)
           c7=[xy[0],xy[1]-d]
           angle7=angle(a,b,c7)
           c8=[xy[0],xy[1]+d]
           angle8=angle(a,b,c8)  
           angles=[angle0,angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8]
           c=[c0,c1,c2,c3,c4,c5,c6,c7,c8]
           
           return angles,c
def find_condadate(a,b,xy,square_side): 
        total_point=[]
        total_angles=[]
        for d in square_side:
            angles,points=generate_point(a,b,xy,d)
            total_angles.extend(angles)
            total_point.extend(points)

        condatae_point=angle_status_points(total_angles,total_point)  
        
        return  (condatae_point)
 
def find_first_condadate(a,b,c,square_side): 
            total_point=[]
            total_angles=[]
            for d in square_side:
                angles,points=generate_point(a,b,c,d)
                total_angles.extend(angles)
                total_point.extend(points)
            c=angle_status_points(total_angles,total_point) 
            total_point=[]
            total_angles=[]
            for d in square_side:
                angles,points=generate_point(c,b,a,d)
                total_angles.extend(angles)
                total_point.extend(points)
            a=angle_status_points(total_angles,total_point) 
            return  a,b,c
        
        
def genrate_new_points_square_grid(points,square_side):
    result=[]
    for j,xy in enumerate(points):
        if j ==0 :
                  a=xy  
        elif j ==1 :
                  b=xy
        elif j ==2 :
               c=xy
               a,b,c=find_first_condadate(a,b,c,square_side)
               result.append(list(a)) 
               result.append(list(b)) 
               result.append(list(c)) 
        else:     
                a=result[-2]
                b=result[-1]
                c=xy
                
                condatae_point=find_condadate(a,b,c,square_side)
                result.append(condatae_point)          

    return result
