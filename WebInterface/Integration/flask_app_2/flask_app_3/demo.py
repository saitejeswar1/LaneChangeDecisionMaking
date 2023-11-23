from flask_app_3.dynamicQuery import dq
import importlib


import keras
import numpy as np

def final_result(seg_vals,count,filename):

    inArgs = "seg_vals"                             #take input from ...
    outArgs = "lane_info,r_depth,l_depth,a_depth"
    
    [module,func_name] = dq(inArgs,outArgs)
    module = 'flask_app_3.' + module
    mod = importlib.import_module(module)                                   #m_model

    [lane_info,r_depth,l_depth,a_depth]=getattr(mod,func_name)(seg_vals)
    
    inArgs = "lane_info,r_depth,l_depth,a_depth" #take input from ...
    outArgs = "lt_sd,lt_veh,rt_sd,rt_veh,a_sd,ah_veh"
    
    [module,func_name] = dq(inArgs,outArgs)
    module = 'flask_app_3.' + module
    mod = importlib.import_module(module)                                #set_vars
    
    [lt_sd,lt_veh,rt_sd,rt_veh,a_sd,ah_veh]=getattr(mod,func_name)(lane_info,r_depth,l_depth,a_depth)
    
    lane_inc,lane_dec = 0,0
    ll_edge,rl_edge = 0,0
    
    if filename == "test_video.mp4":
        if count < 219:
            rl_edge,ll_edge = 0,1
            cur_lane = 1
        elif count >= 219 and count < 1096:
            rl_edge,ll_edge = 0,0
            cur_lane = 2
        elif count >= 1096:
            rl_edge,ll_edge = 1,0
            cur_lane = 3

    elif filename == "road_car_view.mp4":
        if count == 629:
            lane_inc,lane_dec = 0,1
        elif count == 1678:                 #frame number to be present in KB
            lane_inc,lane_dec = 1,0
        elif count == 2517:
            lane_inc,lane_dec = 1,0
        else:
            lane_inc,lane_dec = 0,0  
        
        cur_lane = 2

        if count < 629:
            ll_edge,rl_edge = 0,1
        
        elif count >= 629 and count < 1678:
            ll_edge,rl_edge = 1,1
            cur_lane = 1
        
        elif count >= 1678 and count < 2247:
            ll_edge,rl_edge = 1,0
            cur_lane = 2
        
        elif count >= 2247 and count < 2337:
            ll_edge,rl_edge = 0,0
        
        elif count >= 2337 and count < 2547:
            ll_edge,rl_edge = 0,1
            
        elif count >= 2547:
            ll_edge,rl_edge = 0,0
    
    ip = [lane_dec,lane_inc,lt_sd,lt_veh,rt_sd,rt_veh,a_sd,ah_veh,ll_edge,rl_edge]

    

    model = keras.models.load_model(r"E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\weights_matrix_updated.h5")
    op = model.predict(np.array([[lane_dec,lane_inc,lt_sd,lt_veh,rt_sd,rt_veh,a_sd,ah_veh,ll_edge,rl_edge]]))
    
    message = ["Steer Right","Do not Steer","Steer Left"] #Output neurons
    output = op[0]

    

    for i in range(len(output)):
        if output[i]==max(output):   #activation function
            print(message[i])
            msg = message[i]
            break

    lt_turn,rt_turn = 0,0
    if message[i] == "Steer Right":
        rt_turn = 1
        
    elif message[i] == "Steer Left":
        lt_turn = 1

    inArgs = "cur_lane,rt_turn,lt_turn" #take input from ...
    outArgs = "cur_lane"

    [module,func_name] = dq(inArgs,outArgs)
    module = 'flask_app_3.' + module
    mod = importlib.import_module(module)           #lane_counting
    
    cur_lane = getattr(mod,func_name)(cur_lane,rt_turn,lt_turn)
    
    return ip,msg,i
