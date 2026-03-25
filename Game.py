import tkinter as tk
import random
from Node import Node
from minimax import build_tree, minimax, get_best_move_from_tree
from alphabeta import alpha_beta

current_number = None

player_score = 0
pc_score = 0 
algorithm = None
bank = 0
pending_pc_move = False

def generate_numbers():
    generated_numbers = []
    while len(generated_numbers) < 5:
        number = random.randint(20000, 30000)
        if number % 12 == 0:
            generated_numbers.append(number)
    return generated_numbers

def start_game():
    start_frame.pack_forget()
    numbers_frame.pack(pady=20)

def choose_number(number):
    global current_number
    current_number = number

    numbers_frame.pack_forget()
    game_frame.pack(pady=20)

    label.config(text=f"Current Number: {current_number}")




root = tk.Tk()
root.title("Game")

window_width = 1000
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#6A0DAD")  # Deep purple

# START SCREEN

start_frame = tk.Frame(root, bg="#6A0DAD")
start_frame.pack(pady=20)

title = tk.Label(
    start_frame,
    text = "WELCOME",
    bg = "#6A0DAD",
    fg = "white",
    font = ("Arial", 40, "bold")
)
title.pack(pady=60)

start_btn = tk.Button(
    start_frame,
    text="Start the game!",
    bg="white",
    fg="black",
    font=("Arial", 17, "bold"),
    width=15,
    height=2,
    command=start_game
)
start_btn.pack(pady=40)

# 5 NUMBERS SCREEN

numbers_frame = tk.Frame(root, bg="#6A0DAD")

title = tk.Label(
    numbers_frame,
    text = "Choose a starting number",
    bg = "#6A0DAD",
    fg = "white",
    font = ("Arial", 20, "bold")
)
title.pack(pady=40)

numbers = generate_numbers()

button_frame = tk.Frame(numbers_frame, bg="#6A0DAD")
button_frame.pack(pady=20)

for i, num in enumerate(numbers):
    btn = tk.Button(
        button_frame,
        text=str(num),
        font=("Arial", 14, "bold"),
        width=13,
        height=4,
        command=lambda n=num: choose_number(n)
    )
    btn.grid(row=0, column=i, padx=10)

# Algorithm selection screen

algorithm_frame = tk.Frame(root, bg="#6A0DAD")

algorithm_title = tk.Label(
    algorithm_frame,
    text="Choose algorithm for PC move",
    bg="#6A0DAD",
    fg="white",
    font=("Arial", 20, "bold")
)
algorithm_title.pack(pady=40)

def choose_algorithm(algo):
    global algorithm, pending_pc_move

    algorithm = algo

    algorithm_frame.pack_forget()
    game_frame.pack(pady=20)

    if pending_pc_move:
        make_pc_move()

def make_pc_move():
    global pending_pc_move

    tree_root = Node(current_number, player_score, pc_score, bank, True)
    build_tree(tree_root)

    if algorithm == "minimax":
        minimax(tree_root)
    elif algorithm == "alphabeta":
        alpha_beta(tree_root, -float("inf"), float("inf"))

    pc_divisor = get_best_move_from_tree(tree_root)

    print(f"PC chooses to divide by {pc_divisor}")
    pc_info_label.config(text=f"PC divides by {pc_divisor}")

    pending_pc_move = False
    divide(pc_divisor, is_player=False)

btn_minimax = tk.Button(
    algorithm_frame,
    text="Minimax",
    font=("Arial", 16, "bold"),
    width=15,
    height=4,
    command=lambda: choose_algorithm("minimax")
)

btn_alphabeta = tk.Button(
    algorithm_frame,
    text="Alpha-Beta",
    font=("Arial", 16, "bold"),
    width=15,
    height=4,
    command=lambda: choose_algorithm("alphabeta")
)

btn_minimax.pack(side="left", padx=20)
btn_alphabeta.pack(side="left", padx=20)


# GAME SCREEN

game_frame = tk.Frame(root, bg="#6A0DAD")

# Bank Label
bank_label = tk.Label(
    game_frame,
    text="Bank: 0",
    bg="#6A0DAD",
    fg="white",
    font=("Arial", 20, "bold")
)
bank_label.pack(pady=10)

# Current Number Label
label = tk.Label(
    game_frame,
    text="Current Number: 0",
    bg="#6A0DAD",
    fg="white",
    font=("Arial", 17, "bold")
)
label.pack(pady=30)

pc_info_label = tk.Label(
    game_frame,
    text= "PC's move...",
    bg= "#6A0DAD",
    fg= "white",
    font= ("Arial", 14, "bold")
)
pc_info_label.pack(pady=10)
# Score Label
score_frame = tk.Frame(game_frame, bg="#6A0DAD")
score_frame.pack(pady=10)

# PC Label
pc_label = tk.Label(
    score_frame,
    text="PC: 0",
    fg="white",
    bg="#6A0DAD",
    font=("Arial", 14, "bold")
)
pc_label.pack(side="left", padx=50)

# Player Label
player_label = tk.Label(
    score_frame,
    text="You: 0",
    fg="white",
    bg="#6A0DAD",
    font=("Arial", 14, "bold")
)
player_label.pack(side="right", padx=50)


# Score Function
def update_score(number, is_player=True):
    global player_score, pc_score

    if number % 2 == 0:
        if is_player:
            player_score -= 1
        else:
            pc_score -= 1
    else:
        if is_player:
            player_score += 1
        else:
            pc_score += 1

    pc_label.config(text=f"PC:{pc_score}")
    player_label.config(text=f"You:{player_score}")


# Game Function

def divide(divisor, is_player=True):
    global current_number, bank

    current_number //= divisor
    label.config(text=f"Current Number: {current_number}")

    update_score(current_number, is_player=is_player)

    if current_number % 10 in [0, 5]:
        bank += 1
        bank_label.config(text=f"Bank: {bank}")

    if current_number <= 10:
        end_game(is_player)
        return

    if is_player:
        global pending_pc_move
        pending_pc_move = True

        game_frame.pack_forget()
        algorithm_frame.pack(pady=20)

# End Frame

result_frame = tk.Frame(root, bg="#6A0DAD")

result_label = tk.Label(result_frame, text="", bg="#6A0DAD", fg="white", font=("Arial", 17, "bold"))
result_label.pack(pady=20)


def end_game(last_player):
    global player_score, pc_score, bank

    if last_player:
        player_score += bank
    else:
        pc_score += bank

    bank = 0
    # bank_label.config(text="Bank: 0")

    result_text = f"Your Score: {player_score} vs  PC Score: {pc_score}\n"
    if player_score > pc_score:
        result_text += "You Win!"
    elif pc_score > player_score:
        result_text += "\nPC Win!"
    else:
        result_text += "\nDraw"

    import tkinter.messagebox as msg
    msg.showinfo("Game Over", result_text)


# Button
btn2 = tk.Button(game_frame, text="Divide by 2", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)
btn3 = tk.Button(game_frame, text="Divide by 3", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)
btn4 = tk.Button(game_frame, text="Divide by 4", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)

btn2.pack(pady=10)
btn3.pack(pady=10)
btn4.pack(pady=10)

btn2.config(command=lambda: divide(2))
btn3.config(command=lambda: divide(3))
btn4.config(command=lambda: divide(4))

root.mainloop()