def alpha_beta(node,alpha,beta): #definining alpha beta algorithm
    if node.number <= 10 or not node.children:
        pc_score = node.pc_score
        player_score = node.player_score

        if node.is_pc_turn:
            pc_score += node.bank
        else:
            player_score += node.bank #these statement are mainly for the bank

        node.value = pc_score - player_score #this checks for the value of a node, if its higher than 0, its better for pc, if lower than 0 then better for player
        return node.value

    # MAXIMIZER
    if node.is_pc_turn:
        best = -float("inf") #if is pc turn, start with the worse possible value so that it any value found after this will be better

        for child in node.children:
            val = alpha_beta(child,alpha,beta)# checks for the value of the child
            best = max(best,val)

            alpha = max(alpha, best) #change the value to best value found

            if beta <= alpha:
                break #cutoff, if beta <= then it wont be considered

        node.value = best #node value now to be the best value now
        return best

    #MINIMIZER
    else:
        best = float("inf") # same as before but for player turn where the worse value is +inf
        
        for child in node.children:
            val = alpha_beta(child,alpha,beta)
            best = min(best,val)

            beta = min(beta, best) #similar thing like before, but take the minimum value instead of max for beta
            if beta <= alpha:
                break #same, if beta is less than alpha then break

        node.value = best
        return best

