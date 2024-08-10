
#import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
#from deepface import DeepFace
#import numpy as np
#import tests.text_sentiment_analysis as text_sentiment_analysis
#from scipy.io.wavfile import write
#import time
import sounddevice as sd
#import sys
import os
#import speech_recognition as sr
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


# CustomTkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vibe Vision.")
        self.geometry("600x480")
        
        self.resizable(0,0)

        # images path
        image_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"images")

        # load these images
        side_image_data = Image.open(os.path.join(image_dir_path,'side-img.png'))
        user_icon_data = Image.open(os.path.join(image_dir_path,'user_dark.png'))
        add_user_icon_data = Image.open(os.path.join(image_dir_path,'add_user_dark.png'))
        guest_user_icon_data = Image.open(os.path.join(image_dir_path,'guest-user.png'))
        password_icon_data = Image.open(os.path.join(image_dir_path,'password-icon.png'))

        self.side_img = ctk.CTkImage(dark_image=side_image_data, light_image=side_image_data, size=(300,480))
        self.user_img = ctk.CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20,20))
        self.add_user_img = ctk.CTkImage(dark_image=add_user_icon_data, light_image=add_user_icon_data, size=(17,17))
        self.guest_user_img = ctk.CTkImage(dark_image=guest_user_icon_data, light_image=guest_user_icon_data, size=(17,17))
        self.password_icon_img = ctk.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

        ctk.CTkLabel(master=self, text="", image=self.side_img).pack(expand=True, side="left")
        

        self.frame = ctk.CTkFrame(master=self, width=300, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="right")

        ctk.CTkLabel(master=self.frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        ctk.CTkLabel(master=self.frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        ctk.CTkLabel(master=self.frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.user_img, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        username_entry = ctk.CTkEntry(self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        username_entry.pack(anchor="w", padx=(25, 0))

        ctk.CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon_img, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        password_entry = ctk.CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        password_entry.pack(anchor="w", padx=(25, 0))
        v = ctk.CTkEntry(self)
        print(v.get())
        print(password_entry.get())
        loginbutton = ctk.CTkButton(master=self.frame, text="Login", command=lambda: self.validate_login(username_entry.get(),password_entry.get()), fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        signup_button = ctk.CTkButton(master=self.frame, text="add new user",command=self.open_sign_up_window, fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=self.add_user_img).pack(anchor="w", pady=(20, 0), padx=(25, 0))
        signup_button = ctk.CTkButton(master=self.frame, text="guest session",command=self.open_bool_question_window, fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=self.add_user_img).pack(anchor="w", pady=(20, 0), padx=(25, 0))


        # # Create labels and entry widgets for username and password
        # username_label = ctk.CTkLabel(self, text="Username")
        # username_label.pack(pady=5)
        # username_entry = ctk.CTkEntry(self)
        # username_entry.pack(pady=5)

        # password_label = ctk.CTkLabel(self, text="Password")
        # password_label.pack(pady=5)
        # password_entry = ctk.CTkEntry(self, show="*")
        # password_entry.pack(pady=5)

        # # # Create a label to show error messags
        # error_label = ctk.CTkLabel(self, text="", fg_color="red")
        # error_label.pack(pady=5)

        # # Create a login button
        # login_button = ctk.CTkButton(self,text="Login", command=lambda: self.validate_login(username_entry.get(), password_entry.get()))
        # login_button.pack(pady=10)

        # # create a sign up label
        # signup_button = ctk.CTkButton(self, text="sign up", command=self.open_sign_up_wondow)
        # signup_button.pack(pady=10)

        # # Create a Guest Login in button
        # guest_button = ctk.CTkButton(self, text="Guest User", command=self.open_bool_question_window)
        # guest_button.pack(pady=10)


        
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
                from main_app import app
                window = app()
                window.mainloop()

                
            
            
        
        self.error_label.configure(text="Invalid username or password.")

    def open_sign_up_window(self):
        self.destroy()
        import subprocess
        from signup_form import SignUpForm
        window = SignUpForm()
        window.run()
        #subprocess.run([sys.executable,".\\signup_window.py"])
    
    def open_bool_question_window(self):
        # Function to run the animation chart
        # this is a hack solution.
        self.destroy()

        import quiz_app as qa
        qa.start_quiz()


if __name__ == '__main__':
    loginwindow = LoginWindow()
    loginwindow.mainloop()