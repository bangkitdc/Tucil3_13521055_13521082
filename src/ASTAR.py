from geopy.distance import geodesic

def ASTAR(G, start, end, coords):
    # Init
    queue = []
    cur_node = start
    visited={}
    parent={}
    path=[]
    dist={}
    for node in G.nodes():
        visited[node] = False
        parent[node] = -1
        dist[node] = -1
        
    queue.append([0,start,start])
    
    # Djikstra-like algorithm, adding to priority queue for every new node 
    while (len(queue) > 0):
        queue.sort()
        top = queue[0] 
        queue.pop(0)
        
        cur_length = top[0]
        cur_node = top[1]
        cur_parent = top[2]
                
        if dist[cur_node]==-1 or dist[cur_node] > (cur_length - geodesic(coords[cur_node],coords[end]).km) :
            visited[cur_node] = True
            parent[cur_node] = cur_parent
            
            dist[cur_node] = cur_length - geodesic(coords[cur_node],coords[end]).km
            
            # Add to priority queue
            for neighbor in G[cur_node]:
                hn = geodesic(coords[neighbor],coords[end]).km
                gn = dist[cur_node] + G[cur_node][neighbor]['weight']
                fn = gn + hn
                if(dist[neighbor] == -1 or dist[neighbor] > gn):
                    queue.append([fn, neighbor, cur_node])
    
    # If path found, return path
    if(visited[end]):
        temp = end
        
        while temp != start:
            #print(temp)
            path.append(temp)
            temp = parent[temp]
            
        path.append(temp)
        
        path.reverse()
        
        return path
    # Raise error if no path found
    else:
        raise ValueError('no path found')
