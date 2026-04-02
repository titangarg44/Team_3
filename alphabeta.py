"""
Alpha-beta pruning, based on the generated nodes
@param node
@param alpha
@param beta
"""
def alpha_beta(node,alpha,beta):
    if node.number <= 10 or not node.children:
        pc_score = node.pc_score
        player_score = node.player_score

        # Adds score to the bank
        if node.is_pc_turn:
            pc_score += node.bank
        else:
            player_score += node.bank

        # Checks for the value of a node, if its higher than 0, its better for the pc, if it's lower than 0, it's better for the player
        node.value = pc_score - player_score
        return node.value

    # Maximizer
    if node.is_pc_turn:
        best = -float("inf") #if it's the pc's turn, start with the worse possible value so that it any value found after this will be better

        for child in node.children:
            val = alpha_beta(child,alpha,beta) # Checks for the value of the child
            best = max(best,val)

            alpha = max(alpha, best) #change the value to best value found

            if beta <= alpha:
                break #cutoff, if beta <= alpha, the path wont be considered

        node.value = best #node value now to be the best value now
        return best

    # Minimizer
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

