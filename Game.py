import tkinter as tk
import random

current_number = None

def generate_numbers():
    numbers = []
    while len(numbers) < 5:
        num = random.randint(20000, 30000)
        if num % 12 == 0:
            numbers.append(num)
    return numbers

def choose_number(num):
    global current_number
    current_number = num
    label.config(text=f"Current Number: {current_number}")

root = tk.Tk()
root.title("Game")
root.geometry("1000x500")
root.configure(bg="#6A0DAD")  # Deep purple

title = tk.Label(
    root,
    text = "Choose a starting number",
    bg = "#6A0DAD",
    fg = "white",
    font = ("Arial", 16, "bold")
)
title.pack(pady=20)

# Label
label = tk.Label(
    root,
    text="Current Number: 0",
    bg="#6A0DAD",
    fg="white",
    font=("Arial", 14)
)
label.pack(pady=10)

numbers = generate_numbers()

frame = tk.Frame(root, bg="#6A0DAD")
frame.pack(pady=20)

for i, num in enumerate(numbers):
    btn = tk.Button(
        frame,
        text=str(num),
        font=("Arial", 12, "bold"),
        width=15,
        height=2,
        command=lambda n=num: choose_number(n)
    )
    btn.grid(row=0, column=i, padx=10)

# Button
btn2 = tk.Button(root, text="Divide by 2", bg="white", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
btn3 = tk.Button(root, text="Divide by 3", bg="white", fg="black", font=("Arial", 12, "bold"), width=15, height=2)
btn4 = tk.Button(root, text="Divide by 4", bg="white", fg="black", font=("Arial", 12, "bold"), width=15, height=2)

btn2.pack(pady=10)
btn3.pack(pady=10)
btn4.pack(pady=10)

root.mainloop()