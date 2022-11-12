import tkinter as tk
import random


root = tk.Tk()

entry_label = tk.Label(root, text = "Guess a number between 1 and 5: ")
entry_label.grid(row = 0, column = 0)

#Entry field for user guesses.
user_entry = tk.Entry(root)
user_entry.grid(row = 0, column = 1)

text_box = tk.Text(root, width = 25, height = 2)
text_box.grid(row = 1, column = 0, columnspan = 2)

text_box.insert("end-1c", "simple guessing game!")

random_num = random.randint(1, 5)

def guess_number(event = None):
    #Get the string of the user_entry widget
    guess = user_entry.get() 

    if guess == str(random_num):
        text_box.delete(1.0, "end-1c") # Clears the text box of data
        text_box.insert("end-1c", "You win!") # adds text to text box

    else:
        text_box.delete(1.0, "end-1c")
        text_box.insert("end-1c", "Try again!")

        user_entry.delete(0, "end")
# binds the enter widget to the guess_number function
# while the focus/cursor is on the user_entry widget
user_entry.bind("<Return>", guess_number) 

root.mainloop()