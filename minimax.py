from Node import Node

"""
Builds a game tree from the current node to the max depth
@param node - the current node
@param depth - current depth
@param max_depth - the maximal depth that can be rechead in the tree
"""
def build_tree(node, depth=0, max_depth=6):
    if node.number <= 10 or depth >= max_depth:
        return

    Node.generate_children(node)

    for child in node.children:
        build_tree(child, depth + 1, max_depth)

"""
Evaluates the game tree, based on the minimax algorithm
@param node - current node to evaluate
@return - value of the nodes
"""
def minimax(node):
    # terminal node
    if node.number <= 10 or not node.children:
        # give bank to last player
        pc_score = node.pc_score
        player_score = node.player_score

        if node.is_pc_turn:
            pc_score += node.bank
        else:
            player_score += node.bank

        node.value = pc_score - player_score
        return node.value

    if node.is_pc_turn:
        best = -float("inf")

        for child in node.children:
            val = minimax(child)
            best = max(best, val)

        node.value = best
        return best

    else:
        best = float("inf")

        for child in node.children:
            val = minimax(child)
            best = min(best, val)

        node.value = best
        return best

"""
Picks the best move for the pc from the root note
@param root - root node of game tree
@return returns the best move for 
"""
def get_best_move_from_tree(root):
    best_value = -float("inf")
    best_move = None

    for child in root.children:
        if child.value > best_value:
            best_value = child.value
            best_move = child.move

    return best_move