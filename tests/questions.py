import customtkinter as ctk
import tkinter as tk

class QuestionSlider(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Question Slider")
        self.geometry("400x200")

        self.questions = [
            "Is the sky blue?",
            "Do you like pizza?",
            "Is water wet?",
            "Are you having a good day?",
        ]
        self.current_question = 0

        self.frame = ctk.CTkFrame(self, width=300, height=100)
        self.frame.pack(pady=20)

        self.question_label = ctk.CTkLabel(self.frame, text=self.questions[0], font=("Arial", 16))
        self.question_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.yes_button = ctk.CTkButton(self.frame, text="Yes", command=lambda: self.next_question("Yes"))
        self.yes_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        self.no_button = ctk.CTkButton(self.frame, text="No", command=lambda: self.next_question("No"))
        self.no_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

    def next_question(self, answer):
        print(f"Question: {self.questions[self.current_question]}, Answer: {answer}")
        
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.animate_slide()
        else:
            self.question_label.configure(text="All questions answered!")
            self.yes_button.configure(state="disabled")
            self.no_button.configure(state="disabled")

    def animate_slide(self):
        new_frame = ctk.CTkFrame(self, width=300, height=100)
        new_frame.place(x=400, y=20)

        new_question_label = ctk.CTkLabel(new_frame, text=self.questions[self.current_question], font=("Arial", 16))
        new_question_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        new_yes_button = ctk.CTkButton(new_frame, text="Yes", command=lambda: self.next_question("Yes"))
        new_yes_button.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

        new_no_button = ctk.CTkButton(new_frame, text="No", command=lambda: self.next_question("No"))
        new_no_button.place(relx=0.7, rely=0.7, anchor=tk.CENTER)

        self.animate(new_frame, 400, -300, 20)

    def animate(self, widget, start_x, end_x, duration):
        def move():
            nonlocal start_x
            if start_x > end_x:
                start_x -= 10
                widget.place(x=start_x, y=20)
                self.after(10, move)
            else:
                self.frame.destroy()
                self.frame = widget

        move()

if __name__ == "__main__":
    app = QuestionSlider()
    app.mainloop()