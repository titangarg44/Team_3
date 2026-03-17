from Node import Node

def build_tree(node, depth=0, max_depth=6):
    if node.number <= 10 or depth >= max_depth:
        return

    Node.generate_children(node)

    for child in node.children:
        build_tree(child, depth + 1, max_depth)

def minimax(node):
    # terminal node
    if node.number <= 10 or not node.children:
        # give bank to last player
        if node.is_pc_turn:
            node.pc_score += node.bank
        else:
            node.player_score += node.bank

        node.value = node.pc_score - node.player_score
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

def get_best_move_from_tree(root):
    best_value = -float("inf")
    best_move = None

    for child in root.children:
        if child.value > best_value:
            best_value = child.value
            best_move = child.move

    return best_move

