import cv2
import numpy as np

def eqn_lt(x):
    return 100*(0.000000451634970*x**5-0.000068466154009*x**4+0.003961508965860*x**3-0.109350788939381*x*x+1.468743169695631*x-2.241943129953762)
                       

def eqn_rt(x):
    return 1000*(-0.000000052704060*x**5+0.000007989736221*x**4-0.000462292823840*x**3+0.012760815498220*x*x-0.171438735311443*x+1.663153300843994)
            
def eqn_ilt(x):
    return 1000*(0.000000128368409*x**5-0.000019460165463*x**4+0.001125981458659*x**3-0.031080823468170*x*x+0.417331197141561*x-1.823357541371203)
            
def eqn_irt(x):
    return 1000*(-0.000000164792945*x**5+0.000024981987411*x**4-0.001445478697383*x**3+0.039900007122568*x*x-0.536117174978811*x+3.829616024874668)


image =cv2.imread( r"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\static\Output_Frames\test_video\frames1000.jpg")

x = 561
y = 382

image = cv2.circle(image, (x,y), radius=0, color=(0, 0, 255), thickness=21)
cv2.imshow('',image)
cv2.waitKey(0)


