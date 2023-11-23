import numpy as np

def m_model(seg_vals):
    r_depth = {}
    l_depth = {}
    a_depth = {}
    lane_info = []
    
    if seg_vals[0]['rois'] is not None:
        car = 0
        
        for vals in seg_vals[0]["class_ids"]:
            
            if vals == 8:
                h_m = 4 #avg height of car 4.5m
                
            if vals == 3:
                 h_m = 1.8 #avg height of car 1.6m (swift)
            
            f = 600
            #f = 1130
            h_p = seg_vals[0]['rois'][car][2]-seg_vals[0]['rois'][car][0]
            
            
            depth = h_m*f/h_p
            depth = np.round(depth,decimals=2)
            
            
            """def eqn_lt(x):
                return 0.0799*x*x-5.1818*x+660.26

            def eqn_rt(x):
                return 0.4508*x*x-26.357*x+955.38
            
            def eqn_ilt(x):
                return -0.0002*x*x*x*x + 0.0349*x*x*x - 2.4799*x*x + 74.82*x -293.07
            
            def eqn_irt(x):
                return 0.0003*x*x*x*x - 0.0577*x*x*x + 3.4442*x*x - 87.108*x + 1520.2"""
            
            def eqn_lt(x):
                return 100*(0.000000451634970*x**5-0.000068466154009*x**4+0.003961508965860*x**3-0.109350788939381*x*x+1.468743169695631*x-2.241943129953762)
                                

            def eqn_rt(x):
                return 1000*(-0.000000052704060*x**5+0.000007989736221*x**4-0.000462292823840*x**3+0.012760815498220*x*x-0.171438735311443*x+1.663153300843994)
                        
            def eqn_ilt(x):
                return 1000*(0.000000128368409*x**5-0.000019460165463*x**4+0.001125981458659*x**3-0.031080823468170*x*x+0.417331197141561*x-1.823357541371203)
                        
            def eqn_irt(x):
                return 1000*(-0.000000164792945*x**5+0.000024981987411*x**4-0.001445478697383*x**3+0.039900007122568*x*x-0.536117174978811*x+3.829616024874668)


            print(depth)
           

            if depth <= 50:
                i_lt = eqn_ilt(depth)
                lt = eqn_lt(depth)
                
                i_rt = eqn_irt(depth)
                rt = eqn_rt(depth)
                
                if seg_vals[0]['rois'][car][1] >= rt and seg_vals[0]['rois'][car][1] < i_rt  :
                    print("vehicle is to the immediate right lane of ego")
                    lane_info.append(1)
                    
                    r_depth[car] = depth
                elif seg_vals[0]['rois'][car][3] <= lt and seg_vals[0]['rois'][car][3] > i_lt :
                    print("vehicle is to the immediate left lane of ego")
                    lane_info.append(-1)
                    l_depth[car] = depth
                    
                elif seg_vals[0]['rois'][car][3] < rt and seg_vals[0]['rois'][car][1] > lt:
                    print("vehicle is ahead")
                    lane_info.append(0)
                    a_depth[car] = depth
                else:
                    print("Not in ROI")
                    
                car = car + 1
            
    return lane_info,r_depth,l_depth,a_depth


def set_vars(lane_info,r_depth,l_depth,a_depth):
    SD = 0
    rt_veh,lt_veh,ah_veh = 0,0,0
    rt_sd,lt_sd,a_sd = 0,0,0
    if 1 in lane_info:
        rt_veh = 1
        if min(r_depth.values()) > 30:
            rt_sd = 1
    if -1 in lane_info:
        lt_veh = 1
        if min(l_depth.values()) > 30:
            lt_sd = 1
    if 0 in lane_info:
        ah_veh = 1
        if min(a_depth.values()) > 30:
            a_sd = 1
    return lt_sd,lt_veh,rt_sd,rt_veh,a_sd,ah_veh


