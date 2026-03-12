"""
airport_data.py - Juba International Airport (HJJJ) Digital Twin
Based on Official ICAO Aerodrome Chart
Runway: 13/31 (3,100m) | Taxiway Width: 23m
"""

import networkx as nx

def create_hjjj_airport():
    G = nx.DiGraph()
    
    # ========== NODES (From Official Map) ==========
    
    # Aprons (2 - as per AIP)
    G.add_node('APRON_PAX', pos=(0, 100), type='apron')
    G.add_node('APRON_CARGO', pos=(-200, 150), type='apron')
    
    # Taxiway Intersections (5 - from chart)
    G.add_node('TWY_A', pos=(0, 50), type='taxiway')
    G.add_node('TWY_B', pos=(0, 0), type='taxiway')
    G.add_node('TWY_C', pos=(150, 0), type='taxiway')
    G.add_node('TWY_D', pos=(-150, 0), type='taxiway')
    G.add_node('TWY_E', pos=(300, 0), type='taxiway')
    
    # Holding Points (2 - before each runway threshold)
    G.add_node('HOLD_13', pos=(450, -50), type='hold')
    G.add_node('HOLD_31', pos=(-300, -50), type='hold')
    
    # Runway Thresholds (2)
    G.add_node('THR_13', pos=(450, -150), type='threshold')
    G.add_node('THR_31', pos=(-300, -150), type='threshold')
    
    # ========== EDGES (Taxiway Connections) ==========
    # Format: (from, to, distance_in_meters)
    
    edges = [
        # From Passenger Apron
        ('APRON_PAX', 'TWY_A', 50),
        
        # From Cargo Apron
        ('APRON_CARGO', 'TWY_D', 100),
        
        # Main Taxiway Chain (A to E)
        ('TWY_A', 'TWY_B', 50),
        ('TWY_B', 'TWY_C', 150),
        ('TWY_B', 'TWY_D', 150),
        ('TWY_C', 'TWY_E', 150),
        
        # To Holding Points
        ('TWY_E', 'HOLD_13', 150),
        ('TWY_D', 'HOLD_31', 150),
        
        # To Runway Thresholds
        ('HOLD_13', 'THR_13', 100),
        ('HOLD_31', 'THR_31', 100),
    ]
    
    # Add edges (bidirectional for taxiways)
    for src, dst, dist in edges:
        G.add_edge(src, dst, weight=dist + 10, distance=dist)
        G.add_edge(dst, src, weight=dist + 10, distance=dist)
    
    return G


if __name__ == "__main__":
    print("🛫 HJJJ Airport Model")
    print("=" * 40)
    
    G = create_hjjj_airport()
    
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    
    print("\nTaxiways:")
    for node, data in G.nodes(data=True):
        if data['type'] == 'taxiway':
            print(f"  - {node}")
    
    print("\n✅ Model Ready")