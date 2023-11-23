import pandas as pd

from rdflib import URIRef, Literal,Namespace,Graph


def write_to_ttl():
    df = pd.read_excel(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx', sheet_name='My sheet2',usecols="A:J")
    d = pd.read_excel(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx', sheet_name='My sheet2',usecols="L")
    r = pd.read_excel(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\log_file.xlsx', sheet_name='My sheet2',usecols="N")


    ip = df.to_numpy()
    op = d.to_numpy()
    res = r.to_numpy()

    n = Namespace("http://example.org/ttab/")
    g = Graph()
    g.parse(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\ltademo.owl',format="ttl")
    g.bind("ttab", n)

    count = 1
    message = ["Steer Right","Do not Steer","Steer Left"]

    for rows,vals,k in zip(ip,op,res):
        print(k)
        if k[0] == 1:    
            id = URIRef("http://example.org/ttab/{}".format(count))
            
            count += 1

            lane_dec = Literal(rows[0])
            lane_inc = Literal(rows[1])
            lt_sd = Literal(rows[2])
            lt_veh = Literal(rows[3])
            rt_sd = Literal(rows[4])
            rt_veh = Literal(rows[5])
            a_sd = Literal(rows[6])
            ah_veh = Literal(rows[7])
            ll_edge = Literal(rows[8])
            rl_edge = Literal(rows[9])

            g.add((id,n.lane_dec,lane_dec))
            g.add((id,n.lane_inc,lane_inc))
            g.add((id,n.lt_sd,lt_sd))
            g.add((id,n.lt_veh,lt_veh))
            g.add((id,n.rt_sd,rt_sd ))
            g.add((id,n.rt_veh,rt_veh ))
            g.add((id,n.a_sd,a_sd))
            g.add((id,n.ah_veh,ah_veh))
            g.add((id,n.ll_edge,ll_edge))
            g.add((id,n.rl_edge,rl_edge))
            g.add((id,n.message,Literal(message[vals[0]])))
            
                   
    g.serialize('output_file.ttl',format='ttl')



