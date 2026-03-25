from Node import Node
visited_edges = [] #for seeing the edges that are visited

def build_tree(node, depth=0, max_depth=6): # this is defining the function for the tree where node is node, depth is the current depth and maax_depth is 6
    if node.number <= 10 or depth >= max_depth: # this is fo the depth that if <=10 which is the final condition of game is reached or max depth which is 6 is reached then stop
        return

    Node.generate_children(node) #makes node

    for child in node.children:
        build_tree(child, depth + 1, max_depth) #for each node level increase the depth level by 1 

def alpha_beta(node,alpha,beta): #definining alpha beta algorithm
    global visited_edges
    if node.number <= 10 or not node.children: 
        if node.is_pc_turn:
            node.pc_score += node.bank
        else:
            node.player_score += node.bank #these statement are mainly for the bank 

        node.value = node.pc_score - node.player_score #this checks for the value of a node, if its higher than 0, its better for pc, if lower than 0 then better for player
        return node.value
    
    if node.is_pc_turn:
        best = -float("inf") #if is pc turn, start with the worse possible value so that it any value found after this will be better

        for child in node.children:
            visited_edges.append((node.name,child.name, "visit")) #append each node as visited
            val = alpha_beta(child,alpha,beta)# checks for the value of the child
            best = max(best,val)
            alpha = max(alpha, best) #change the value to best value found
            if beta <= alpha:
                visited_edges.append((node.name, child.name, "cut"))
                break #cutoff, if beta <= then it wont be considered
        node.value = best #node value now to be the best value now
        return best

    else:
        best = float("inf") # same as before but for player turn where the worse value is +inf
        
        for child in node.children:
            visited_edges.append((node.name,child.name, "visit"))
            val = alpha_beta(child,alpha,beta)
            best = min(best,val)
            beta = min(beta, best) #similar thing like before, but take the minimum value instead of max for beta
            if beta <= alpha:
                visited_edges.append((node.name, child.name, "cut"))
                break #same, if beta is less than alpha then break
        node.value = best
        return best

def best_move(root):
    best_value = -float("inf") #so -inf because  so it assumes the worst case, any value found will be better
    best_move = None #none is basically a placeholder

    for child in root.children: 
        if child.value > best_value: #this checks if the value of the node is better than the value of the previous node, which at the start will be true as best_value will be -inf 
            best_value = child.value #now if the value is better, it will then be considered as the child node
            best_move = child.move #and the best move will be considered

    return best_move
