class Node:
    def __init__(self, number, player_score, pc_score, bank, is_pc_turn):
        self.number = number
        self.player_score = player_score
        self.pc_score = pc_score
        self.bank = bank
        self.is_pc_turn = is_pc_turn

        self.children = []
        self.value = None
        self.move = None  # 2 or 3 or 4

    def generate_children(self):
        for move in [2, 3, 4]:
            number = self.number // move
            player_score = self.player_score
            pc_score = self.pc_score
            bank = self.bank

            if number % 2 == 0:
                if self.is_pc_turn:
                    pc_score -= 1
                else:
                    player_score -= 1
            else:
                if self.is_pc_turn:
                    pc_score += 1
                else:
                    player_score += 1

            if number % 10 in [0, 5]:
                bank += 1

            child = Node(
                number,
                player_score,
                pc_score,
                bank,
                not self.is_pc_turn
            )

            child.move = move
            self.children.append(child)

