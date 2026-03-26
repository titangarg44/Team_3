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
starting_number = None
previous_number = None

def generate_numbers():
    generated_numbers = []
    while len(generated_numbers) < 5:
        number = random.randint(20000, 30000)
        if number % 12 == 0:
            generated_numbers.append(number)
    return generated_numbers

def start_game():
    start_frame.pack_forget()
    player_frame.pack(pady=20)

# a window to pick the starting player
def choose_beginner(player):
    global picked_player
    picked_player = player

    player_frame.pack_forget()
    numbers_frame.pack(pady=20)


def choose_number(number):
    global current_number, starting_number, pending_pc_move
    current_number = number
    starting_number = number

    numbers_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    label.config(text=f"Current Number: {current_number}")
    start_label.config(text=f"Starting number: {starting_number}")

    if picked_player == "ai":
        pending_pc_move = True
        make_pc_move()
        
      

root = tk.Tk()
root.title("Game")

window_width = 800
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="#c29fd5")  # Deep purple

# START SCREEN

start_frame = tk.Frame(root, bg="#c29fd5")
start_frame.pack(pady=20)

title = tk.Label(
    start_frame,
    text = "WELCOME",
    bg = "#c29fd5",
    fg = "black",
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

numbers_frame = tk.Frame(root, bg="#c29fd5")

title = tk.Label(
    numbers_frame,
    text = "Choose a starting number",
    bg = "#c29fd5",
    fg = "black",
    font = ("Arial", 20, "bold")
)
title.pack(pady=40)

numbers = generate_numbers()

button_frame = tk.Frame(numbers_frame, bg="#c29fd5")
button_frame.pack(pady=20)

for i, num in enumerate(numbers):
    row = i // 3        # 0,0,0,1,1
    col = i % 3         # 0,1,2,0,1

    btn = tk.Button(
        button_frame,
        text=str(num),
        font=("Arial", 14, "bold"),
        width=13,
        bg="white",
        height=4,
        command=lambda n=num: choose_number(n)
    )
    btn.grid(row=row, column=col, padx=10, pady=10)


# Who begins?

player_frame = tk.Frame(root, bg="#c29fd5")

player_title = tk.Label(
    player_frame,
    text="Choose who begins to play",
    bg="#c29fd5",
    fg="black",
    font=("Arial", 20, "bold")
)
player_title.pack(pady=40)

btn_human = tk.Button(
    player_frame,
    text="Human Player",
    font=("Arial", 16, "bold"),
    width=15,
    height=4,
    command=lambda: choose_beginner("human")
)

btn_ai = tk.Button(
    player_frame,
    text="Computer begins",
    font=("Arial", 16, "bold"),
    width=15,
    height=4,
    command=lambda: choose_beginner("ai")
)

btn_human.pack(side="left", padx=20)
btn_ai.pack(side="left", padx=20)

# PC THINKING FRAME

pc_thinking_frame = tk.Frame(root, bg="#c29fd5")
pc_thinking_title = tk.Label(
    pc_thinking_frame,
    text="PC is thinking...",
    bg="#c29fd5",
    fg="black",
    font=("Arial", 20, "bold")
)
pc_thinking_title.pack(pady=70)

pc_thinking_button = tk.Button(
    pc_thinking_frame,
    text="Next",
    bg="white",
    fg="black",
    state="disabled",
    width=10,
    height=3,
    font=("Arial", 16, "bold"),
    command=lambda: return_to_game()
)
pc_thinking_button.pack(padx=30)

def return_to_game():
    pc_thinking_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    divide(pc_divisor, is_player=False)

def show_pc_choice():
    pc_thinking_title.config(text=f"PC chose to divide by {pc_divisor}")
    pc_thinking_button.config(state="normal")

# Algorithm selection screen

algorithm_frame = tk.Frame(root, bg="#c29fd5")

algorithm_title = tk.Label(
    algorithm_frame,
    text="Choose algorithm for PC move",
    bg="#c29fd5",
    fg="black",
    font=("Arial", 20, "bold")
)
algorithm_title.pack(pady=40)

def choose_algorithm(algo):
    global algorithm, pending_pc_move

    algorithm = algo

    algorithm_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    if pending_pc_move:
        make_pc_move()

def make_pc_move():
    global pending_pc_move, pc_divisor

    game_frame.forget()
    pc_thinking_frame.pack(pady=20)

    pc_thinking_title.config(text="PC is thinking...")
    pc_thinking_button.config(state="disabled")

    tree_root = Node(current_number, player_score, pc_score, bank, True)
    build_tree(tree_root)

    if algorithm == "minimax":
        minimax(tree_root)
    elif algorithm == "alphabeta":
        alpha_beta(tree_root, -float("inf"), float("inf"))

    pc_divisor = get_best_move_from_tree(tree_root)

    print(f"PC chooses to divide by {pc_divisor}")

    root.after(1000, show_pc_choice)

    pending_pc_move = False

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

game_frame = tk.Frame(root, bg="#c3b4ca")

main_container = tk.Frame(game_frame, bg="#c3b4ca")
main_container.pack(fill="both", expand=True)

left_frame = tk.Frame(main_container, bg="#c3b4ca")
left_frame.pack(side="left", fill="y", anchor="nw", padx=10)

right_frame = tk.Frame(main_container, bg="#c29fd5")
right_frame.pack(side="right", fill="both", expand=True)

info_frame = tk.Frame(left_frame, bg="#758199", padx=10, pady=10)
info_frame.pack(anchor="nw", pady=20)

start_label = tk.Label(info_frame, text="Starting number: -", bg="#758199", fg="white", font=("Arial", 15))
start_label.grid(row=0, column=0, padx=15, sticky="w")

prev_number_label = tk.Label(info_frame, text="Number in a previous round: -", bg="#758199", fg="white", font=("Arial", 15))
prev_number_label.grid(row=1, column=0, padx=15, sticky="w")

player_move_label = tk.Label(info_frame, text="Your previous choice: -", bg="#758199", fg="white", font=("Arial", 15))
player_move_label.grid(row=2, column=0, padx=15, sticky="w")

pc_move_label = tk.Label(info_frame, text="PC's previous choice: -", bg="#758199", fg="white", font=("Arial", 15))
pc_move_label.grid(row=3, column=0, padx=15, sticky="w")


# Bank Label
bank_label = tk.Label(
    right_frame,
    text="Bank: 0",
    bg="#c29fd5",
    fg="black",
    font=("Arial", 18, "bold")
)
bank_label.pack(pady=20)

# Current Number Label
label = tk.Label(
    right_frame,
    text="Current Number: 0",
    bg="#c29fd5",
    fg="black",
    font=("Arial", 17, "bold")
)
label.pack(pady=5)

# Score Label
score_frame = tk.Frame(right_frame, bg="#c29fd5")
score_frame.pack(pady=15)

# PC Label
pc_label = tk.Label(
    score_frame,
    text="PC: 0",
    fg="black",
    bg="#c29fd5",
    font=("Arial", 15, "bold")
)
pc_label.pack(side="left", padx=50)

# Player Label
player_label = tk.Label(
    score_frame,
    text="You: 0",
    fg="black",
    bg="#c29fd5",
    font=("Arial", 15, "bold")
)
player_label.pack(side="right", padx=50)

pc_info_label = tk.Label(
    right_frame,
    text= "Please, select...",
    bg= "#c3b4ca",
    fg= "black",
    font= ("Arial", 14, "bold")
)
pc_info_label.pack(pady=10)

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

    before_move = current_number
    current_number //= divisor
    label.config(text=f"Current Number: {current_number}")

    prev_number_label.config(text=f"Number in a previous round: {previous_number}")

    update_score(current_number, is_player=is_player)

    if current_number % 10 in [0, 5]:
        bank += 1
        bank_label.config(text=f"Bank: {bank}")

    if current_number <= 10:
        end_game(is_player)
        return

    if is_player:
        player_move_label.config(text=f"Your previous choice: ÷{divisor}")
        prev_number_label.config(text=f"Number before your choice: {before_move}")
    else:
        pc_move_label.config(text=f"PC's previous choice: ÷{divisor}")
        prev_number_label.config(text=f"Number before PC choice: {before_move}")

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
btn2 = tk.Button(right_frame, text="Divide by 2", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)
btn3 = tk.Button(right_frame, text="Divide by 3", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)
btn4 = tk.Button(right_frame, text="Divide by 4", bg="white", fg="black", font=("Arial", 14, "bold"), width=15, height=2)

btn2.pack(pady=10)
btn3.pack(pady=10)
btn4.pack(pady=10)

btn2.config(command=lambda: divide(2))
btn3.config(command=lambda: divide(3))
btn4.config(command=lambda: divide(4))

root.mainloop()