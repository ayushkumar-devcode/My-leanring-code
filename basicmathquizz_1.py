import tkinter as tk
from tkinter import messagebox
import random

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Game")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.score = 0
        self.total_questions = 0
        self.current_answer = 0
        self.level = "Easy"
        
        self.setup_ui()
        self.generate_question()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Math Quiz Game", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Level selection frame
        level_frame = tk.Frame(self.root)
        level_frame.pack(pady=10)
        
        tk.Button(level_frame, text="Easy", command=lambda: self.set_level("Easy"), bg="lightgreen", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(level_frame, text="Medium", command=lambda: self.set_level("Medium"), bg="yellow", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(level_frame, text="Hard", command=lambda: self.set_level("Hard"), bg="orange", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # Question label
        self.question_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.question_label.pack(pady=20)
        
        # Answer entry
        self.entry = tk.Entry(self.root, font=("Arial", 16), justify="center", width=10)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.check_answer())
        
        # Check button
        tk.Button(self.root, text="Check Answer", command=self.check_answer, bg="blue", fg="white", font=("Arial", 14)).pack(pady=10)
        
        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.result_label.pack(pady=5)
        
        # Score label
        self.score_label = tk.Label(self.root, text="Score: 0/0", font=("Arial", 14))
        self.score_label.pack(pady=10)
    
    def set_level(self, new_level):
        self.level = new_level
        self.generate_question()
    
    def generate_question(self):
        if self.level == "Easy":
            num1, num2 = random.randint(1, 10), random.randint(1, 10)
            op = random.choice(['+', '-'])
        elif self.level == "Medium":
            num1, num2 = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(['+', '-', '*'])
        else:  # Hard
            num1, num2 = random.randint(1, 50), random.randint(1, 50)
            op = random.choice(['+', '-', '*', '/'])
            if op == '/':
                num1 = num2 * random.randint(1, 10)  # Ensure integer division
        
        self.question_text = f"{num1} {op} {num2} = ?"
        self.question_label.config(text=self.question_text)
        
        if op == '+':
            self.current_answer = num1 + num2
        elif op == '-':
            self.current_answer = num1 - num2
        elif op == '*':
            self.current_answer = num1 * num2
        else:
            self.current_answer = num1 // num2
        
        self.entry.delete(0, tk.END)
        self.entry.focus()
    
    def check_answer(self):
        try:
            user_answer = int(self.entry.get())
            self.total_questions += 1
            
            if user_answer == self.current_answer:
                self.result_label.config(text="Correct! ✅", fg="green")
                self.score += 1
            else:
                self.result_label.config(text=f"Wrong! Correct: {self.current_answer} ❌", fg="red")
            
            self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
            self.root.after(1500, self.generate_question)  # Next question after 1.5s
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def run(self):
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MathQuiz(root)
    game.run()