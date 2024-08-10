import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from deepface import DeepFace
import numpy as np
import tests.text_sentiment_analysis as text_sentiment_analysis
from scipy.io.wavfile import write
import time
import sounddevice as sd
import sys
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from transformers import pipeline
#from autocorrect import Speller

import json

# Dummy implementation of the emotion detection function
def detect_emotion_from_text(string):
    data_str = ''
    data = text_sentiment_analysis.analysis(string)
    data_str = data_str + data['sentiment']

    top_two_emotions_list = list(data)[1:]
    for e in top_two_emotions_list:
        if data[e] == 0:
            data_str = data_str + ". "
            break
        else:
            data_str = data_str + " ," + str(e)

    return data_str

def get_two_max_val_emotions(emotion):
    max1 = 0
    max2 = 0
    name1 = ""
    name2 = ""
    for k, v in emotion.items():
        if v >= max1:
            name2 = name1
            name1 = k
            max2 = max1
            max1 = v
    return {name1: max1, name2: max2}

# Dummy function to process audio file (e.g., calculate file size)
def process_audio_file(file_path):
    r = sr.Recognizer()
    msgs = ''

    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

        try:
            transcript = r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError:
            print("Could not request results from the speech recognition service")

    sentences = [transcript]
    analyser = SentimentIntensityAnalyzer()

    for sen in sentences:
        v = analyser.polarity_scores(sen)

        if v['compound'] >= 0.05:
            msgs = msgs + 'positive'
        elif v['compound'] <= -0.05:
            msgs = msgs + 'negative'
        else:
            msgs = msgs + 'neutral'

        text = sen
        emotions_found = te.get_emotion(text)
        topemotions = get_two_max_val_emotions(emotions_found)
        for k, v in topemotions.items():
            if v != 0:
                msgs = msgs + ' , ' + k

    return msgs

# CustomTkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Initialize the CustomTkinter window for login
login_root = ctk.CTk()
login_root.title("Login")
login_root.geometry("300x300")

# Dummy user info for validation
VALID_USERNAME = "user"
VALID_PASSWORD = "pass"


def open_sign_up_wondow():
    login_root.destroy()
    import subprocess
    subprocess.run([sys.executable,".\\signup_window.py"])
    


def open_bool_question_window():
     # Function to run the animation chart
    # this is a hack solution.
    def run_bool_question_window():
        login_root.destroy()
        import subprocess
        command_list = [sys.executable,".\\bool_res_questions.py"]
        
        subprocess.run(command_list)

    run_bool_question_window()


def open_questionnaire_window():
    login_root.destroy()
    
    
    print("hi");
    # Initialize the CustomTkinter window Guest Session
    guest_root = ctk.CTk()
    guest_root.title("Guest User")
    guest_root.geometry("500x600")

    ## please keep the following three lines commented out, to the interperator from complaining
    # guest_window = ctk.CTkToplevel(root)
    # guest_window.title("Guest User Questionnaire")
    # guest_window.geometry("400x300")

    from transformers import pipeline

    classifer = pipeline('text-classification',model='bhadresh-savani/distilbert-base-uncased-emotion'); 



    ctk.CTkLabel(guest_root, text="What was the best part of your day today?").pack(pady=5)
    happy_entry = ctk.CTkEntry(guest_root, width=250)
    happy_entry.pack(pady=5)

    ctk.CTkLabel(guest_root, text="Did you miss anyone or anything today that made you feel sad?").pack(pady=5)
    sad_entry = ctk.CTkEntry(guest_root, width=250)
    sad_entry.pack(pady=5)

    ctk.CTkLabel(guest_root, text="Was there a situation today that made you feel like your patience was tested?").pack(pady=5)
    angry_entry = ctk.CTkEntry(guest_root,width=250)
    angry_entry.pack(pady=5)


    # doing this in vim would be a walk in park but unfortunatly,
    # my stupid brain doesn't know how to configure vim for python
    # and therefore why i am stuck with vs-code.
    # i geneuenly hope that after this i never get to write another windows UI again.
    ctk.CTkLabel(guest_root, text="Did you experience anything today that made you feel scared or anxious?").pack(pady=5)
    fear_entry = ctk.CTkEntry(guest_root,width=250)
    fear_entry.pack(pady=5)
    
    ctk.CTkLabel(guest_root, text="Was there anything unexpected that happened today?").pack(pady=5)
    surprise_entry = ctk.CTkEntry(guest_root,width=250)
    surprise_entry.pack(pady=5)


    # Function to run the animation chart
    # this is a hack solution.
    def run_piechart_animation(data_emotion_list:list):
        guest_root.destroy()
        import subprocess
        command_list = [sys.executable,".\\pie_chart_anim.py"]
        for cmd in data_emotion_list:
            command_list.append(str(cmd))
        subprocess.run(command_list)


    def submit_answers():
        responses = [ happy_entry.get() , sad_entry.get(), angry_entry.get(), fear_entry.get(), surprise_entry.get()]
        happy_response = happy_entry.get()
        sad_response = sad_entry.get()
        angry_response = angry_entry.get()
        fear_response = fear_entry.get()
        surprise_response = surprise_entry.get()
       
        happy_response_raw_val = classifer(happy_response)[0]['score']*100
        sad_response_raw_val = classifer(sad_response)[0]['score']*100
        angry_response_raw_val = classifer(angry_response)[0]['score']*100
        fear_response_raw_val = classifer(fear_response)[0]['score']*100
        surprise_response_raw_val = classifer(surprise_response)[0]['score']*100

        sum_raw_val = happy_response_raw_val + sad_response_raw_val + angry_response_raw_val + fear_response_raw_val + surprise_response_raw_val

        happy_norm_val = (happy_response_raw_val / sum_raw_val) * 100;
        sad_norm_val = (sad_response_raw_val / sum_raw_val) * 100
        angry_norm_val = (angry_response_raw_val / sum_raw_val) * 100
        fear_norm_val = (fear_response_raw_val / sum_raw_val) * 100
        surprise_norm_val = (surprise_response_raw_val / sum_raw_val) * 100

        print(str(happy_norm_val) + " : " + str(sad_norm_val) + " : " + str(angry_norm_val) + " : " + str(fear_norm_val))

        # it should be a crime against humanity for me to write a UI next time.
        run_piechart_animation([happy_norm_val,sad_norm_val, angry_norm_val, fear_norm_val, surprise_norm_val])

        

    submit_button = ctk.CTkButton(guest_root, text="Submit", command=submit_answers)
    submit_button.pack(pady=20)
    guest_root.mainloop()

def start_face_detection():

    #classifer = pipeline('text-classification',model='bhadresh-savani/distilbert-base-uncased-emotion');
    # Initialize the CustomTkinter window
    root = ctk.CTk()
    root.title("OpenCV Face Detection with CustomTkinter")
    root.geometry("800x600")

    # Create frames for the left and right sections
    left_frame = ctk.CTkFrame(root)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = ctk.CTkFrame(root)
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Create a Label widget to display the video feed
    video_label = ctk.CTkLabel(left_frame)
    video_label.pack()

    # Initialize the video capture object
    cap = cv2.VideoCapture(0)

    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    last_face_detected_time = time.time()

    # Function to update the video feed
    def update_frame():
        nonlocal last_face_detected_time

        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > 0:
                last_face_detected_time = time.time()
            else:
                elepsed_time = time.time() - last_face_detected_time
                if elepsed_time > 15:
                    cap.release()
                    root.destroy()
                    return

            for (x, y, w, h) in faces:
                if type(faces) == np.ndarray:
                    result = DeepFace.analyze(frame, enforce_detection=False, actions=['emotion'])
                    detected_emotion = result[0]['dominant_emotion']

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    elepsed_time = time.time() - last_face_detected_time
                    if elepsed_time > 15:
                        cap.release()
                        root.destroy()
                        return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        video_label.after(10, update_frame)

    # Function to start the video feed
    def start_video():
        update_frame()

    # Function to stop the video feed
    def stop_video():
        cap.release()
        root.quit()

    # Function to detect emotion from text
    def detect_emotion(self):
        return 
        spell = Speller()
        user_text = text_entry.get("1.0", ctk.END).strip()
        # text_entry.delete(1.0,ctk.END)

        # corrected_text = spell(user_text)
        # text_entry.insert(ctk.END,corrected_text)
        # emotion = classifer(corrected_text)
        # emotion_label.configure(text=f"Emotion: {emotion[0]['label']}")

    # Function to record audio and submit to dummy function
    def record_audio():
        duration = 5  # seconds
        fs = 44100  # Sample rate
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        audio_file = "output.wav"
        write(audio_file, fs, recording)  # Save as WAV file
        print("Recording finished. Processing audio file...")
        file_size = process_audio_file(audio_file)
        audio_label.config(text=f"Audio File Size: {file_size} bytes")

    # Create buttons to start and stop the video feed
    start_button = ctk.CTkButton(left_frame, text="Start", command=start_video)
    start_button.pack(side="left", padx=10, pady=10)

    stop_button = ctk.CTkButton(left_frame, text="Stop", command=stop_video)
    stop_button.pack(side="left", padx=10, pady=10)

    # Create a text entry field for emotion detection
    text_entry = ctk.CTkTextbox(right_frame, height=130, width=800)
    text_entry.pack(pady=18)

    # Create a button to detect emotion from the text
    detect_emotion_button = ctk.CTkButton(right_frame, text="Detect Emotion", command=detect_emotion)
    detect_emotion_button.pack(pady=5)

    # Label to display the detected emotion
    emotion_label = ctk.CTkLabel(right_frame, text="Emotion: ")
    emotion_label.pack(pady=8)

    # Button to record audio
    record_button = ctk.CTkButton(right_frame, text="Record Audio", command=record_audio)
    record_button.pack(pady=10, side="bottom")

    audio_label = ctk.CTkLabel(right_frame, text="Audio File Size: ")
    audio_label.pack(pady=5, side="bottom")

    # Run the CustomTkinter event loop
    root.mainloop()

# Function to validate the login credentials
def validate_login(username, password):
    with open('users.json', 'r') as file:
        users = json.load(file)

        
        # Check if the provided username and password match any entry in the JSON data
    for user in users:
        print(user)
        if user.get('username') == username and user.get('password').strip().lower() == password:
            print(user.get('username'))
            print(username)
            login_root.destroy()
            start_face_detection()
        
        
    
    #error_label.configure(text="Invalid username or password.")


# Create labels and entry widgets for username and password
username_label = ctk.CTkLabel(login_root, text="Username")
username_label.pack(pady=5)
username_entry = ctk.CTkEntry(login_root)
username_entry.pack(pady=5)

password_label = ctk.CTkLabel(login_root, text="Password")
password_label.pack(pady=5)
password_entry = ctk.CTkEntry(login_root, show="*")
password_entry.pack(pady=5)

# # Create a label to show error messages
# error_label = ctk.CTkLabel(login_root, text="", fg_color="red")
# error_label.pack(pady=5)

# Create a login button
login_button = ctk.CTkButton(login_root, text="Login", command=lambda: validate_login(username_entry.get(), password_entry.get()))
login_button.pack(pady=10)

# create a sign up label
signup_button = ctk.CTkButton(login_root, text="sign up", command=open_sign_up_wondow)
signup_button.pack(pady=10)

# Create a Guest Login in button
guest_button = ctk.CTkButton(login_root, text="Guest User", command=open_bool_question_window)
guest_button.pack(pady=10)
# Run the CustomTkinter event loop for login
login_root.mainloop()

input()
