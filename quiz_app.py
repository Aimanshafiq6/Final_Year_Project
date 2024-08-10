import cProfile
from tkinter import *
import customtkinter as ct
import ttkbootstrap as tw
import time
import threading
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

class AnimatedPieChart(ct.CTkFrame):
    def __init__(self, master, initial_data, target_data, colors, labels):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        # Create the figure and axis for the pie chart
        self.fig, self.ax = plt.subplots()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Set data
        self.data = initial_data
        self.colors = colors
        self.labels = labels
        self.target = target_data

        # Create the animation
        self.anim = FuncAnimation(self.fig, self.update_chart, frames=200, interval=50, repeat=False)
    
    
    # Custom formatting function
    def my_format(self,pct):
        val = int(round(pct * len(self.target) / 100.0))
        return '{:.1f}%\n'.format(pct)
    
    
    
    def update_chart(self, frame):
        # Clear the previous chart
        self.ax.clear()

        # Update the data
        for i in range(len(self.data)):
            if self.data[i] < self.target[i]:
                self.data[i] += 1
            elif self.data[i] > self.target[i]:
                self.data[i] -= 1

        # Create the pie chart
        wedges, texts, autotexts = self.ax.pie(self.data, colors=self.colors, autopct=lambda pct: '' if pct < 1 else self.my_format(pct), startangle=90, labels=self.labels)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Check if all segments have reached their target
        if self.data == self.target:
            self.anim.event_source.stop()


ct.set_appearance_mode("dark")
ct.set_default_color_theme("theme.json")
ct.set_widget_scaling(1.3)
root = ct.CTk(fg_color="#001e4d")
root.title("Quiz App")
root.geometry("850x600+450+100")
root.resizable(False, False)

class Quiz:
    def __init__(self, root, **kwargs):
        self.root = root
        self.score = 0
        self.quiz_fram = ct.CTkFrame(self.root, fg_color="#fff")

        self.title_frame = ct.CTkFrame(self.quiz_fram, fg_color="#fff")

        self.simple_quiz = ct.CTkLabel(self.title_frame, text="Simple Quiz", font=("Poppins", 20, "bold"), text_color="black")
        self.simple_quiz.pack(side=TOP, anchor="nw", pady=0, padx=0)

        self.score_lbl = ct.CTkLabel(self.root, text=f"Score : {self.score}", font=("Poppins", 20, "bold"), text_color="black", fg_color="#fff")
        # self.score_lbl.place(x=450, y=50)

        self.line = Label(self.title_frame, text="__________________________________________________", fg="black", font=("consolas", 20, "bold"),
                          bg="#fff")
        self.line.pack(side=TOP, pady=0)

        self.title_frame.pack(side=TOP, pady=10)

        self.option_fram = ct.CTkFrame(self.quiz_fram, fg_color="#fff")


        # List of questions with associated emotions
        self.questions_with_emotions = [
            {"question": "Are you happy with your current job?", "emotion": "happiness"},
            {"question": "Did you enjoy your vacation?", "emotion": "happiness"},
            {"question": "Are you feeling sad today?", "emotion": "sadness"},
            {"question": "Did something upset you recently?", "emotion": "sadness"},
            {"question": "Are you angry about the recent news?", "emotion": "anger"},
            {"question": "Did someone make you upset today?", "emotion": "anger"},
            {"question": "Are you afraid of the dark?", "emotion": "fear"},
            {"question": "Do you worry about the future?", "emotion": "fear"},
            {"question": "Did the surprise party make you happy?", "emotion": "surprise"},
            {"question": "Were you surprised by the announcement?", "emotion": "surprise"},
        ]

        self.emotions_list = [
            "happiness",
            "sadness",
            "anger",
            "fear",
            "surprise"
        ]
        self.emotions = {
            "happiness":0.0,
            "sadness":0.0,
            "anger":0.0,
            "fear":0.0,
            "surprise":0.0
        }

        
        self.emotion_counts = {}

        for e in self.emotions_list:
            self.emotion_counts[e] = {"Yes":0, "No":0}

        self.question1 = kwargs["question_1"]
        self.q1option_1 = kwargs["q1option_1"]
        self.q1option_2 = kwargs["q1option_2"]

        self.question2 = kwargs["question_2"]
        self.q2option_1 = kwargs["q2option_1"]
        self.q2option_2 = kwargs["q2option_2"]

        self.question3 = kwargs["question_3"]
        self.q3option_1 = kwargs["q3option_1"]
        self.q3option_2 = kwargs["q3option_2"]

        self.question4 = kwargs["question_4"]
        self.q4option_1 = kwargs["q4option_1"]
        self.q4option_2 = kwargs["q4option_2"]

        self.question5 = kwargs["question_5"]
        self.q5option_1 = kwargs["q5option_1"]
        self.q5option_2 = kwargs["q5option_2"]

        self.question6 = kwargs["question_6"]
        self.q6option_1 = kwargs["q6option_1"]
        self.q6option_2 = kwargs["q6option_2"]

        self.question7 = kwargs["question_7"]
        self.q7option_1 = kwargs["q7option_1"]
        self.q7option_2 = kwargs["q7option_2"]

        self.question8 = kwargs["question_8"]
        self.q8option_1 = kwargs["q8option_1"]
        self.q8option_2 = kwargs["q8option_2"]

        self.question9 = kwargs["question_9"]
        self.q9option_1 = kwargs["q9option_1"]
        self.q9option_2 = kwargs["q9option_2"]
     
        self.question10 = kwargs["question_10"]
        self.q10option_1 = kwargs["q10option_1"]
        self.q10option_2 = kwargs["q10option_2"]

        self.question_1 = ct.CTkLabel(self.option_fram, text=f"{self.question1}", text_color="black", font=("consolas", 20, "normal"))
        self.question_1.pack(side=TOP, anchor="nw", padx=27, pady=20)

        self.option_padding_y = 3
        self.option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q1option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q1option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        
        self.option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.option_2.pack(fill=X, padx=25, pady=self.option_padding_y)

        self.next = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_2)

        self.option_1.bind("<Enter>", lambda e: self.option_1.configure(fg_color="black", text_color="white"))
        self.option_1.bind("<Leave>", lambda e: self.option_1.configure(fg_color="white", text_color="black"))
        self.option_2.bind("<Enter>", lambda e: self.option_2.configure(fg_color="black", text_color="white"))
        self.option_2.bind("<Leave>", lambda e: self.option_2.configure(fg_color="white", text_color="black"))

        self.option_1.configure(command=lambda: self.test_answer("option1"))
        self.option_2.configure(command=lambda: self.test_answer("option2"))

        self.option_fram.pack(side=TOP, fill=BOTH, expand=True) 
        self.quiz_fram.pack(side=TOP, pady=40, ipadx=40, ipady=100)

    def test_answer(self, selected_answer):
        self.my_correct_option = "option1"
        self.selected_answer = selected_answer

        if self.my_correct_option == self.selected_answer:
            print("Correct !!! yes selected!")
            self.emotion_counts[self.questions_with_emotions[0]["emotion"]]["Yes"] += 1
            self.option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.option_1.unbind()  
            self.option_2.unbind()
            self.next.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[0]["emotion"]]["No"] += 1

            self.option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.option_1.unbind()
            self.option_2.unbind()
            self.next.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_2(self):
        self.question_1.configure(text=f"{self.question2}")

        self.option_1.pack_forget()
        self.option_2.pack_forget()

        self.next.pack_forget()

        self.q2option_1_ = ct.CTkButton(self.option_fram, text=f"  {self.q2option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q2option_2_ = ct.CTkButton(self.option_fram, text=f"  {self.q2option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)

        self.next2 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_3)

        self.q2option_1_.pack(fill=X, padx=25, pady=self.option_padding_y)
        #self.q2option_4_.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q2option_2_.pack(fill=X, padx=25, pady=self.option_padding_y)
        #self.q2option_3_.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q2option_1_.bind("<Enter>", lambda e: self.q2option_1_.configure(fg_color="black", text_color="white"))
        self.q2option_1_.bind("<Leave>", lambda e: self.q2option_1_.configure(fg_color="white", text_color="black"))
        self.q2option_2_.bind("<Enter>", lambda e: self.q2option_2_.configure(fg_color="black", text_color="white"))
        self.q2option_2_.bind("<Leave>", lambda e: self.q2option_2_.configure(fg_color="white", text_color="black"))
        self.q2option_1_.configure(command=lambda: self.test_answer_2("option1"))
        self.q2option_2_.configure(command=lambda: self.test_answer_2("option2"))

    def test_answer_2(self, selected_answer2):
        self.my_correct_option = "option1"
        self.selected_answer2 = selected_answer2

        if self.my_correct_option == self.selected_answer2:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[1]["emotion"]]["Yes"] += 1
            self.q2option_1_.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q2option_2_.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q2option_1_.unbind()  
            self.q2option_2_.unbind()
            # self.q2option_3_.unbind()
            # self.q2option_4_.unbind()
            self.next2.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[1]["emotion"]]["No"] += 1
            self.q2option_1_.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q2option_2_.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q2option_1_.unbind()
            self.q2option_2_.unbind()
            
            self.next2.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_3(self):
        self.question_1.configure(text=f"{self.question3}")

        self.q2option_1_.pack_forget()
        self.q2option_2_.pack_forget()
        
        self.next2.pack_forget()

        self.q3option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q3option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q3option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q3option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        
        self.next3 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_4)

        self.q3option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q3option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q3option_1.bind("<Enter>", lambda e: self.q3option_1.configure(fg_color="black", text_color="white"))
        self.q3option_1.bind("<Leave>", lambda e: self.q3option_1.configure(fg_color="white", text_color="black"))
        self.q3option_2.bind("<Enter>", lambda e: self.q3option_2.configure(fg_color="black", text_color="white"))
        self.q3option_2.bind("<Leave>", lambda e: self.q3option_2.configure(fg_color="white", text_color="black"))
        
        self.q3option_1.configure(command=lambda: self.test_answer_3("option1"))
        self.q3option_2.configure(command=lambda: self.test_answer_3("option4"))
        
    def test_answer_3(self, selected_answer3):
        self.my_correct_option = "option1"
        self.selected_answer3 = selected_answer3

        if self.my_correct_option == self.selected_answer3:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[2]["emotion"]]["Yes"] += 1
            self.q3option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q3option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q3option_1.unbind()  
            self.q3option_2.unbind()
            self.next3.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[2]["emotion"]]["No"] += 1
            self.emotion_counts["happiness"]["Yes"] += 1
            self.q3option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q3option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
           
            self.q3option_1.unbind()
            self.q3option_2.unbind()
           
            self.next3.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_4(self):
        self.question_1.configure(text=f"{self.question4}")

        self.q3option_1.pack_forget()
        self.q3option_2.pack_forget()

        self.next3.pack_forget()

        self.q4option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q4option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q4option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q4option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
       
        self.next4 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_5)

        
        self.q4option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q4option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q4option_1.bind("<Enter>", lambda e: self.q4option_1.configure(fg_color="black", text_color="white"))
        self.q4option_1.bind("<Leave>", lambda e: self.q4option_1.configure(fg_color="white", text_color="black"))
        self.q4option_2.bind("<Enter>", lambda e: self.q4option_2.configure(fg_color="black", text_color="white"))
        self.q4option_2.bind("<Leave>", lambda e: self.q4option_2.configure(fg_color="white", text_color="black"))
       
        self.q4option_1.configure(command=lambda: self.test_answer_4("yes"))
        self.q4option_2.configure(command=lambda: self.test_answer_4("no"))
       
    def test_answer_4(self, selected_answer4):
        self.my_correct_option = "option1"
        self.selected_answer4 = selected_answer4

        if self.my_correct_option == self.selected_answer4:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[3]["emotion"]]["Yes"] += 1
            self.q4option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q4option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q4option_1.unbind()  
            self.q4option_2.unbind()
            
            self.next4.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[3]["emotion"]]["No"] += 1
            self.emotion_counts["happiness"]["Yes"] += 1
            self.q4option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q4option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q4option_1.unbind()
            self.q4option_2.unbind()
            
            self.next4.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
  

    def question_5(self):
        self.question_1.configure(text=f"{self.question5}")

        self.q4option_1.pack_forget()
        self.q4option_2.pack_forget()
        
        self.next4.pack_forget()

        self.q5option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q5option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q5option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q5option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        
        self.next5 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_6)

        self.q5option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q5option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
         
        self.q5option_1.bind("<Enter>", lambda e: self.q5option_1.configure(fg_color="black", text_color="white"))
        self.q5option_1.bind("<Leave>", lambda e: self.q5option_1.configure(fg_color="white", text_color="black"))
        self.q5option_2.bind("<Enter>", lambda e: self.q5option_2.configure(fg_color="black", text_color="white"))
        self.q5option_2.bind("<Leave>", lambda e: self.q5option_2.configure(fg_color="white", text_color="black"))
       
        self.q5option_1.configure(command=lambda: self.test_answer_5("option1"))
        self.q5option_2.configure(command=lambda: self.test_answer_5("option2"))
       
    def test_answer_5(self, selected_answer5):
        self.my_correct_option = "option1"
        self.selected_answer5 = selected_answer5

        if self.my_correct_option == self.selected_answer5:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[4]["emotion"]]["Yes"] += 1

            self.q5option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q5option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q5option_1.unbind()  
            self.q5option_2.unbind()
           
            self.next5.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[4]["emotion"]]["No"] += 1
            self.q5option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q5option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q5option_1.unbind()
            self.q5option_2.unbind()
            
            self.next5.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_6(self):
        self.question_1.configure(text=f"{self.question6}")

        self.q5option_1.pack_forget()
        self.q5option_2.pack_forget()
        
        self.next5.pack_forget()

        self.q6option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q6option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q6option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q6option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        
        self.next6 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_7)

        self.q6option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
       
        self.q6option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q6option_1.bind("<Enter>", lambda e: self.q6option_1.configure(fg_color="black", text_color="white"))
        self.q6option_1.bind("<Leave>", lambda e: self.q6option_1.configure(fg_color="white", text_color="black"))
        self.q6option_2.bind("<Enter>", lambda e: self.q6option_2.configure(fg_color="black", text_color="white"))
        self.q6option_2.bind("<Leave>", lambda e: self.q6option_2.configure(fg_color="white", text_color="black"))
       
        self.q6option_1.configure(command=lambda: self.test_answer_6("option1"))
        self.q6option_2.configure(command=lambda: self.test_answer_6("option4"))
       
    def test_answer_6(self, selected_answer6):
        self.my_correct_option = "option1"
        self.selected_answer6 = selected_answer6

        if self.my_correct_option == self.selected_answer6:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[5]["emotion"]]["Yes"] += 1
            self.q6option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q6option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q6option_1.unbind()  
            self.q6option_2.unbind()
            
            self.next6.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[5]["emotion"]]["No"] += 1
            self.q6option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q6option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q6option_1.unbind()
            self.q6option_2.unbind()
            
            self.next6.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_7(self):
        self.question_1.configure(text=f"{self.question7}")

        self.q6option_1.pack_forget()
        self.q6option_2.pack_forget()

        self.next6.pack_forget()

        self.q7option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q7option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q7option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q7option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)

        self.next7 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_8)

        self.q7option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q7option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q7option_1.bind("<Enter>", lambda e: self.q7option_1.configure(fg_color="black", text_color="white"))
        self.q7option_1.bind("<Leave>", lambda e: self.q7option_1.configure(fg_color="white", text_color="black"))
        self.q7option_2.bind("<Enter>", lambda e: self.q7option_2.configure(fg_color="black", text_color="white"))
        self.q7option_2.bind("<Leave>", lambda e: self.q7option_2.configure(fg_color="white", text_color="black"))

        self.q7option_1.configure(command=lambda: self.test_answer_7("option1"))
        self.q7option_2.configure(command=lambda: self.test_answer_7("option4"))

    def test_answer_7(self, selected_answer7):
        self.my_correct_option = "option1"
        self.selected_answer7 = selected_answer7

        if self.my_correct_option == self.selected_answer7:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[6]["emotion"]]["Yes"] += 1
            self.q7option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q7option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q7option_1.unbind()  
            self.q7option_2.unbind()
            self.next7.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[6]["emotion"]]["No"] += 1
            self.q7option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q7option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q7option_1.unbind()
            self.q7option_2.unbind()
            self.next7.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_8(self):
        self.question_1.configure(text=f"{self.question8}")

        self.q7option_1.pack_forget()
        self.q7option_2.pack_forget()

        self.next7.pack_forget()

        self.q8option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q8option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q8option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q8option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)

        self.next8 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_9)

        self.q8option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q8option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q8option_1.bind("<Enter>", lambda e: self.q8option_1.configure(fg_color="black", text_color="white"))
        self.q8option_1.bind("<Leave>", lambda e: self.q8option_1.configure(fg_color="white", text_color="black"))
        self.q8option_2.bind("<Enter>", lambda e: self.q8option_2.configure(fg_color="black", text_color="white"))
        self.q8option_2.bind("<Leave>", lambda e: self.q8option_2.configure(fg_color="white", text_color="black"))

        self.q8option_1.configure(command=lambda: self.test_answer_8("option1"))
        self.q8option_2.configure(command=lambda: self.test_answer_8("option4"))

    def test_answer_8(self, selected_answer8):
        self.my_correct_option = "option1"
        self.selected_answer8 = selected_answer8

        if self.my_correct_option == self.selected_answer8:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[7]["emotion"]]["Yes"] += 1
            self.q8option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q8option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q8option_1.unbind()  
            self.q8option_2.unbind()
            
            self.next8.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[7]["emotion"]]["No"] += 1
            self.q8option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q8option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q8option_1.unbind()
            self.q8option_2.unbind()
            
            self.next8.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_9(self):
        self.question_1.configure(text=f"{self.question9}")

        self.q8option_1.pack_forget()
        self.q8option_2.pack_forget()
        
        self.next8.pack_forget()
        
        self.source_img = Image.open("exit.png")
        self.close_image = ImageTk.PhotoImage(self.source_img.resize((40, 40)))

        self.exit = ct.CTkButton(self.option_fram, text="Exit Quiz", fg_color="red", hover_color="#cd2222", 
                                 text_color="white", width=120, height=35, image=self.close_image, compound=LEFT, command=self.root.destroy)
        
        self.q9option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q9option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q9option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q9option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        
        self.next9 = ct.CTkButton(self.option_fram, text="Next", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.question_10)

        self.q9option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q9option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q9option_1.bind("<Enter>", lambda e: self.q9option_1.configure(fg_color="black", text_color="white"))
        self.q9option_1.bind("<Leave>", lambda e: self.q9option_1.configure(fg_color="white", text_color="black"))
        self.q9option_2.bind("<Enter>", lambda e: self.q9option_2.configure(fg_color="black", text_color="white"))
        self.q9option_2.bind("<Leave>", lambda e: self.q9option_2.configure(fg_color="white", text_color="black"))
        
        self.q9option_1.configure(command=lambda: self.test_answer_9("option1"))
        self.q9option_2.configure(command=lambda: self.test_answer_9("option4"))
        
    def test_answer_9(self, selected_answer9):
        self.my_correct_option = "option1"
        self.selected_answer9 = selected_answer9

        if self.my_correct_option == self.selected_answer9:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[8]["emotion"]]["Yes"] += 1
            self.q9option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q9option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
          
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q9option_1.unbind()  
            self.q9option_2.unbind()
          
            self.next9.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[8]["emotion"]]["No"] += 1
            self.q9option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q9option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            
            self.q9option_1.unbind()
            self.q9option_2.unbind()
            
            self.next9.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)

    def question_10(self):
        self.question_1.configure(text=f"{self.question10}")

        self.q9option_1.pack_forget()
        self.q9option_2.pack_forget()

        self.next9.pack_forget()

        self.q10option_1 = ct.CTkButton(self.option_fram, text=f"  {self.q10option_1}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)
        self.q10option_2 = ct.CTkButton(self.option_fram, text=f"  {self.q10option_2}", fg_color="#fff", text_color="black", border_color="black", border_width=1, font=("Poppins", 15), height=40, anchor=W)

        self.next10 = ct.CTkButton(self.option_fram, text="Finish", fg_color="#001e4d", text_color="white", width=120, height=120, command=self.finish)

        self.q10option_1.pack(fill=X, padx=25, pady=self.option_padding_y)
        self.q10option_2.pack(fill=X, padx=25, pady=self.option_padding_y)
        
        self.q10option_1.bind("<Enter>", lambda e: self.q10option_1.configure(fg_color="black", text_color="white"))
        self.q10option_1.bind("<Leave>", lambda e: self.q10option_1.configure(fg_color="white", text_color="black"))
        self.q10option_2.bind("<Enter>", lambda e: self.q10option_2.configure(fg_color="black", text_color="white"))
        self.q10option_2.bind("<Leave>", lambda e: self.q10option_2.configure(fg_color="white", text_color="black"))

        self.q10option_1.configure(command=lambda: self.test_answer_10("option1"))
        self.q10option_2.configure(command=lambda: self.test_answer_10("option4"))

    def test_answer_10(self, selected_answer10):
        self.my_correct_option = "option1"
        self.selected_answer10 = selected_answer10

        if self.my_correct_option == self.selected_answer10:
            print("Correct !!!")
            self.emotion_counts[self.questions_with_emotions[9]["emotion"]]["Yes"] += 1
            self.q10option_1.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.q10option_2.configure(fg_color="white", text_color="black", border_width=1.5, state="disabled")
            self.score += 1
            self.score_lbl.configure(text=f"Score : {self.score}")
            print(f"Score : {self.score}")
            self.q10option_1.unbind()  
            self.q10option_2.unbind()
            self.next10.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)
        else:
            self.emotion_counts[self.questions_with_emotions[9]["emotion"]]["No"] += 1
            self.q10option_1.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q10option_2.configure(fg_color="#ff9393", text_color="black", border_width=1.5, state="disabled")
            self.q10option_1.unbind()
            self.q10option_2.unbind()
            self.next10.pack(side=BOTTOM, pady=7, ipadx=5, ipady=10)


    def calculate_percentage_responses(self,emotion_counts):
        percentage_responses = {}
        
        for emotion, counts in emotion_counts.items():
            total_responses = counts["Yes"] + counts["No"]
            if total_responses > 0:
                percentage_yes = (counts["Yes"] / total_responses) * 100
            else:
                percentage_yes = 0.0
            
            percentage_responses[emotion] = round(percentage_yes, 2)
        
        return percentage_responses


    def normalize_percentages(self,percentage_responses):
        total_percentage = sum(percentage_responses.values())
        normalized_percentages = {emotion: (percentage / total_percentage) * 100 for emotion, percentage in percentage_responses.items()}
        return normalized_percentages

    def finish(self):
        print(self.emotion_counts)
        normalized_data = self.normalize_percentages(self.calculate_percentage_responses(self.emotion_counts))
        print(normalized_data)
        self.question_1.pack_forget()
        self.q10option_1.pack_forget()
        self.q10option_2.pack_forget()
        self.next10.pack_forget()
        self.line.pack_forget()
        self.score = 1;
        initial_data = [0, 0, 0, 0, 0,100]
        target_data = [
            normalized_data["happiness"],
            normalized_data["sadness"],
            normalized_data["anger"],
            normalized_data["fear"],
            normalized_data["surprise"],
            0
            ]
        labels = ["happiness","sadness","anger","fear","surprise",""]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen', 
          'red', 'navy', 'blue', 'magenta', 'crimson']
        
        import animated_pie_chart_test as pie_chart
        chart_window = pie_chart.MainApp(hap=int(normalized_data["happiness"]),
                                         sad=int(normalized_data["sadness"]),
                                         ang=int(normalized_data["anger"]),
                                         fear=int(normalized_data["fear"]),
                                         sur=int(normalized_data["surprise"]))
        
        chart_window.mainloop()
        self.root.quit()



        self.exit.pack(side=BOTTOM, pady=7, ipadx=5, ipady=0)

        global count
        count = 0
        
           
    
my_question_1 = "1. Are you happy with your current job ?"
my_question_2 = "2. Do you enjoy your free time ?"
my_question_3 = "3. Are you feeling sad to day"
my_question_4 = "4. Did something upset you recently?"
my_question_5 = "5. Are you angry about the recent news?"
my_question_6 = "6. Did someone make you upset today?"
my_question_7 = "7. Are you feeling afraid"
my_question_8 = "8. Do you worry about the future?"
my_question_9 = "9. Did the surprise party make you happy?"
my_question_10 = "10. Were you surprised by the announcement?"

Quiz(root, 
    question_1=my_question_1, q1option_1 = "Yes", q1option_2 = "No", q1correct_option = "Yes",
    question_2=my_question_2, q2option_1 = "Yes", q2option_2 = "No", q2correct_option = "Yes",
    question_3=my_question_3, q3option_1 = "Yes", q3option_2 = "No", q3correct_option = "Yes",
    question_4=my_question_4, q4option_1 = "Yes", q4option_2 = "No", q4correct_option = "Yes",
    question_5=my_question_5, q5option_1 = "Yes", q5option_2 = "No", q5correct_option = "Yes",
    question_6=my_question_6, q6option_1 = "Yes", q6option_2 = "No", q6correct_option = "Yes",
    question_7=my_question_7, q7option_1 = "Yes", q7option_2 = "No", q7correct_option = "Yes",
    question_8=my_question_8, q8option_1 = "Yes", q8option_2 = "No",  q8correct_option = "Yes",
    question_9=my_question_9, q9option_1 = "Yes", q9option_2 = "No",  q9correct_option = "Yes",
    question_10=my_question_10, q10option_1 = "Yes", q10option_2 = "No", q10correct_option = "Yes")


def start_quiz():
    root.mainloop()

if __name__ == '__main__':
    root.mainloop()
# cProfile.run("root.mainloop()")


#TODO:
# 1. give proper colors to pie chart animation
# 2. clear button for voice and text emotion analysis
# 3. convert this large humongus software into  