import networkx as nx

def UCS(G, start, end):
    # Init
    queue = []
    n = len(G.nodes())
    cur_node = start
    visited={}
    parent={}
    path=[]
    for node in G.nodes():
        visited[node] = False
        parent[node] = -1
        
    queue.append([0,start,start])
    
    # Djikstra-like algorithm, adding to priority queue for every new node 
    while (len(queue) > 0):
        queue.sort()
        top = queue[0] 
        queue.pop(0)
        
        cur_length = top[0]
        cur_node = top[1]
        cur_parent = top[2]
        
        visited[cur_node]=True
        parent[cur_node]=cur_parent
        
        # Path found
        if top[1]==end:
            break
        
        # Add to priority queue
        for neighbor in G[cur_node]:
            if(not visited[neighbor]):
                queue.append([cur_length + G[cur_node][neighbor]['weight'], neighbor, cur_node])
    
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
