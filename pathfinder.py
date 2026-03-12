"""
pathfinder.py - A* Algorithm for HJJJ
Finds shortest route from apron to holding point
"""

import networkx as nx
from airport_data import create_hjjj_airport


def heuristic(a, b, G):
    """Euclidean distance between two nodes"""
    pos_a = G.nodes[a]['pos']
    pos_b = G.nodes[b]['pos']
    return ((pos_a[0] - pos_b[0])**2 + (pos_a[1] - pos_b[1])**2)**0.5


def find_route(G, start, end):
    """
    Returns: (path, time_seconds, distance_meters)
    """
    try:
        path = nx.astar_path(G, start, end, 
                            heuristic=lambda x,y: heuristic(x,y,G), 
                            weight='weight')
        
        total_cost = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
        total_dist = sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
        
        time = total_cost / 8.33  # 30 km/h taxi speed
        
        return path, round(time, 2), round(total_dist, 2)
    
    except:
        return None, 0, 0


if __name__ == "__main__":
    print("🧭 A* Pathfinding - HJJJ")
    print("=" * 40)
    
    G = create_hjjj_airport()
    
    routes = [
        ('APRON_PAX', 'HOLD_13'),
        ('APRON_PAX', 'HOLD_31'),
        ('APRON_CARGO', 'HOLD_13'),
        ('APRON_CARGO', 'HOLD_31'),
    ]
    
    for start, end in routes:
        path, time, dist = find_route(G, start, end)
        if path:
            print(f"\n{start} → {end}")
            print(f"  Route: {' → '.join(path)}")
            print(f"  Time: {time}s | Distance: {dist}m")
    
    print("\n✅ Pathfinding Complete")