
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
#from deepface import DeepFace
import numpy as np
import tests.text_sentiment_analysis as text_sentiment_analysis
from scipy.io.wavfile import write
import time
import sounddevice as sd
import sys
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


# CustomTkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("300x300")
        

        # Create labels and entry widgets for username and password
        username_label = ctk.CTkLabel(self, text="Username")
        username_label.pack(pady=5)
        username_entry = ctk.CTkEntry(self)
        username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self, text="Password")
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack(pady=5)

        # # Create a label to show error messags
        error_label = ctk.CTkLabel(self, text="", fg_color="red")
        error_label.pack(pady=5)

        # Create a login button
        login_button = ctk.CTkButton(self,text="Login", command=lambda: self.validate_login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=10)

        # create a sign up label
        signup_button = ctk.CTkButton(self, text="sign up", command=self.open_sign_up_wondow)
        signup_button.pack(pady=10)

        # Create a Guest Login in button
        guest_button = ctk.CTkButton(self, text="Guest User", command=self.open_bool_question_window)
        guest_button.pack(pady=10)


        
    # Function to validate the login credentials
    def validate_login(self,username, password):
        with open('users.json', 'r') as file:
            users = json.load(file)

            
            # Check if the provided username and password match any entry in the JSON data
        for user in users:
            print(user)
            if user.get('username') == username and user.get('password').strip().lower() == password:
                print(user.get('username'))
                print(username)
                self.destroy()
                print("Welcome!")
                start_face_detection()
            
            
        
        self.error_label.configure(text="Invalid username or password.")

    def open_sign_up_wondow(self):
        self.destroy()
        import subprocess
        subprocess.run([sys.executable,".\\signup_window.py"])
    
    def open_bool_question_window(self):
        # Function to run the animation chart
        # this is a hack solution.
        def run_bool_question_window(self):
            self.destroy()
            import subprocess
            command_list = [sys.executable,".\\bool_res_questions.py"]
            
            subprocess.run(command_list)

        run_bool_question_window(self)


if __name__ == '__main__':
    loginwindow = LoginWindow()
    loginwindow.mainloop()