import rdflib as r


def lane_counting(cur_lane,rt_turn,lt_turn):
    g = r.Graph()
    g.parse(r'E:\M Sc Intelligent systems\Semester 2\SDT\Web Interface\Integration\flask_app_3\ltademo.owl',format="ttl")

    qres = g.query("""
    SELECT ?subject ?value

    WHERE 
    { 
    :National_Highway	:hasLanes	?value

    }
    """)

    for row in qres:
        max_lanes = int(row["value"])
        
    if rt_turn == 1 and cur_lane < max_lanes:
        cur_lane = cur_lane + 1
        return cur_lane
    elif lt_turn == 1 and cur_lane > 0:
        cur_lane = cur_lane - 1
        return cur_lane
    else:
        return cur_lane


   