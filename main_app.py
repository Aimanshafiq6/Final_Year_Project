import sys, os, time
import json
import threading
from collections import Counter



import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from deepface.DeepFace import analyze
import numpy as np
import tests.text_sentiment_analysis as text_sentiment_analysis
import text2emotion as te
#from scipy.io.wavfile import write

import sounddevice as sd

#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import speechrecognizor as sr
#from transformers import pipeline
from autocorrect import Speller
from win11toast import toast

#classifer = pipeline('text-classification',model='bhadresh-savani/distilbert-base-uncased-emotion'); 

class WordCounter:
    def __init__(self):
        self.word_counts = Counter()
        self.max_word = None
        self.max_count = 0

    def add_word(self, word):
        self.word_counts[word] += 1
        count = self.word_counts[word]
        
        if count > self.max_count:
            self.max_word = word
            self.max_count = count
        
        return self.max_word

    def get_max_word(self):
        return self.max_word

    def get_count(self, word):
        return self.word_counts[word]

    def zero_all_counts(self):
        self.word_counts.clear()
        self.max_word = None
        self.max_count = 0

class app(ctk.CTk):
    def __init__(self,age_group):
        super().__init__()

        self.title("VibeVision")
        self.geometry("1090x690")

        

        if age_group < 14:
            self.age_range = "kid"
        else:
            self.age_range = "teen"
        
        print(self.age_range)

        # TODO:
        # 1. Integrate speech to text in GUI
        # 2. make guest user GUI pretty
        # 3. video recomation notification
        # 4. still the focus on camera 10 - 15 seconds
        # 5. make the software installable.
        # 6. build website that download executable.
        # 7. don't make emotion wheel labels overlap.
        # 8. Make it faster by using multi threading
        # 9. Why are the widges disappering on switiching between frames??
        

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # frames settings
        self.isCameraNetwork = False
        self.isHomeRendered = False
        self.recognizer = sr.SpeechRecognizer(language="en-us")



        # Networked Camera
        self.camera_url = "" # empty string means no network camera camera.

        # emotion counter
        self.accumulator = WordCounter()
        # load images with light and dark mode image
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "sentiment-detection.png")), size=(50, 46))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(self.image_path, "image_icon_light.png")), size=(20, 20))
        self.camera_img = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "camera-dark.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "camera-dark.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "chat_light.png")), size=(20, 20))
        self.microphone_img = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "microphone.png")),
                                                     dark_image=Image.open(os.path.join(self.image_path, "microphone-dark.png")), size=(20, 20))
        self.setting_img = ctk.CTkImage(light_image=Image.open(os.path.join(self.image_path, "setting_logo.png")),
                                                     dark_image=Image.open(os.path.join(self.image_path, "settings_color.png")), size=(20, 20))
        
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Sentiment detection", text_color="#601E88",image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button= ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_spacing=10, text="Video", fg_color="#EEEEEE", border_color="#601E88", border_width=2,
                                                   text_color=("gray10", "gray90"), hover_color=("#7a5db0", "#6c4ca6"),
                                                   image=self.camera_img, anchor="w", command=self.home_button_event, compound="left", )
        self.home_button.grid(row=1, column=0,padx=10, pady=15, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, border_color="#601E88" , height=40, border_spacing=10, text="text", border_width=2,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#7a5db0", "#6c4ca6"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_color="#601E88", border_spacing=10, text="Voice", border_width=2,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#7a5db0", "#6c4ca6"),
                                                      image=self.microphone_img, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0,padx=10, pady=15, sticky="ew")

        self.frame_4_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=40, border_color="#601E88", border_spacing=10, text="Settings", border_width=2,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("#7a5db0", "#6c4ca6"),
                                                      image=self.setting_img, anchor="w", command=self.frame_4_button_event )
        self.frame_4_button.grid(row=4, column=0, padx=10, pady=15, stick="ew")

        
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        # second frame 
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.fourth_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.recom_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # select default frame        
        # self.render_home()
        # self.render_frame2_text()
        # self.render_frame3_voice()
        # self.render_frame4_settings()
        

        # TODO: in next 2 hours implement the following:
        # 1. Text emotion detection
        # 2. redmentry setting for camera 
        # 3. add another frame 
        # 4. complete the sign up GUI functionality.

        # self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        # self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)


        
        # self.home_frame_button_1 = ctk.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        # self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_3 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.home_frame_button_4 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        # self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

       
        self.render_home()
        self.select_frame_by_name("home")

    def play_vid(self,emotion):
        import webbrowser
        import random
        file_path = "./recom_vids.json"
        try:
            # Open and read the JSON file
            with open("recom_vids.json", 'r') as file:
                data = json.load(file)
            
            # Extract the URLs and select a random one
            
            if self.age_range == "kid":
                urls = data.get("kid")
            else:
                urls = data.get(emotion)
            random_url = random.choice(urls)
                
            # Open the URL in the default web browser
            webbrowser.open(random_url)
            print(f"Opening: {random_url}")
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def render_home(self):
        # Function to start the video feed
        def start_video():
            update_frame()

        # Function to stop the video feed
        def stop_video():
            cap.release()
            self.quit()
        
        #frame = self.home_frame
        video_label = ctk.CTkLabel(self.home_frame,text="")
        video_label.pack()
        
        # Create buttons to start and stop the video feed
        start_button = ctk.CTkButton(self.home_frame, text="Start", command=start_video, text_color="#601E88", font=ctk.CTkFont(size=15, weight="bold"))
        start_button.pack(pady=10)

        stop_button = ctk.CTkButton(self.home_frame, text="Stop", command=stop_video)
        stop_button.pack(padx=100, pady=10)

        recom_button = ctk.CTkButton(self.home_frame, text="Recomand Video", command=self.play_vid)
        recom_button.pack(padx=120,pady=10)
        if self.isCameraNetwork:
            print("yeah its active")
            # IP camera se ahe ga
            self.video_url = self.camera_url + "/video"
            cap = cv2.VideoCapture(self.video_url)
        else:
            print("wrong cam")
            # laptop ka camera
            cap = cv2.VideoCapture(0)

         # Load the pre-trained face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        last_face_detected_time = time.time()
        last_stable_time_detected = time.time()
        timer_gap_last = time.time()
        
        detected_emotion = "neutral"
        # Function to update the video feed
        def update_frame():
            nonlocal last_face_detected_time
            nonlocal last_stable_time_detected 
            nonlocal detected_emotion
            nonlocal timer_gap_last
            ret, frame = cap.read()
           

            if ret:
                frame = cv2.resize(frame, (640,420))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if len(faces) > 0:
                    last_face_detected_time = time.time()
                else:
                    elepsed_time = time.time() - last_face_detected_time
                    if elepsed_time > 15:
                        cap.release()
                        self.home_frame.destroy()
                        return


                for (x, y, w, h) in faces:
                    if type(faces) == np.ndarray:
                        stablelize_label_elepsed_time = time.time() - last_stable_time_detected
                        if stablelize_label_elepsed_time > 3:
                            result = analyze(frame, enforce_detection=False, actions=['emotion'])
                            detected_emotion = result[0]['dominant_emotion']
                            last_stable_time_detected = time.time()
                            self.accumulator.add_word(detected_emotion)

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                        cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        
                        
                        if self.age_range == "kid":
                            if self.accumulator.get_count("happy") >= 4 or self.accumulator.get_count("surprise"):
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid())
                                self.accumulator.zero_all_counts()
                            if self.accumulator.get_count("sad") >= 4 or self.accumulator.get_count("angry") >= 3 or self.accumulator.get_count("fear") >= 2:
                                print("got here!!")
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid())
                                self.accumulator.zero_all_counts()
                        else:
                            if self.accumulator.get_count("happy") >= 4:
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid("happy"))
                                self.accumulator.zero_all_counts()
                            
                            if self.accumulator.get_count("angry") >= 4:
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid("happy"))
                                self.accumulator.zero_all_counts()

                            if self.accumulator.get_count("surprise") >= 4:
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid("surprise"))
                                self.accumulator.zero_all_counts()

                            if self.accumulator.get_count("sad") >= 4:
                                print("got here!!")
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid("sad"))
                                self.accumulator.zero_all_counts()

                            if self.accumulator.get_count("fear") >= 4:
                                toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid("fear"))

                    else:
                        elepsed_time = time.time() - last_face_detected_time
                        if elepsed_time > 15:
                            cap.release()
                            frame.destroy()
                            return
                        
                       


                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)

            video_label.after(10, update_frame)

        # update_frame()
    
    def render_frame2_text(self):
         # create second frame
        # 
        # self.sometext = ctk.CTkLabel(self.second_frame,text="hello world")
        # self.sometext.grid(row=1, column=0, padx=20,pady=10)
        self.text_entry = ctk.CTkTextbox(self.second_frame, height=130, width=800,border_color="#62e2f0",border_width=1)
        self.text_entry.grid(row=1, column=0, padx=20, pady=10)

        self.emotion_label = ctk.CTkLabel(self.second_frame, text="Emotion: ")
        self.emotion_label.grid(row=3, column=0, padx=20, pady=10)

        self.detect_emotion_button =  ctk.CTkButton(self.second_frame, text="Detect Emotion", command=self.button_detect_emotion_from_text)
        self.detect_emotion_button.grid(row=2,column=0, padx=50, pady=20)
        
    def button_detect_emotion_from_text(self):
        self.detect_emotion_button.configure(state="disabled")
        thread = threading.Thread(target=self.detect_emotion_from_text)
        thread.start()


    
    def get_top_two_emotions(self,emotions):
        # Sort the dictionary by values in descending order
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    
        # Return the keys of the first two items
        return [sorted_emotions[0][0], sorted_emotions[1][0]]


    # Function to detect emotion from text
    def detect_emotion_from_text(self):
         
        spell = Speller()
        self.text = self.text_entry.get("1.0", ctk.END).strip()

        corrected_text = spell(self.text)
        self.text_entry.delete(1.0,ctk.END)
        self.text_entry.insert(ctk.END,corrected_text)
        emotion_dict = te.get_emotion(corrected_text)
        top_two_emotions = self.get_top_two_emotions(emotion_dict)
        
        toptwo_emo = top_two_emotions[0] 
        #print(emotion)
        
        self.emotion_label.configure(text=f"Emotion: {toptwo_emo}")
        
        self.detect_emotion_button.configure(state="normal")

    def clear_text_box(self):
        self.text_box.delete(1.0,ctk.END)

    def render_frame3_voice(self):
        self.isrecording = False
        self.mic_image = ctk.CTkImage(Image.open(os.path.join(self.image_path,"small_mic_logo.png")))

        self.record_button = ctk.CTkButton(master=self.third_frame, image=self.mic_image, text="Start Recording", command=self.toggle_recording, width=40, height=40)
        self.record_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.stop_button = ctk.CTkButton(self.third_frame, text="Stop", command=self.stop_recognition, width=100)
        self.stop_button.grid(row=1, column=1, padx=20, pady=10)

        self.text_box = ctk.CTkTextbox(self.third_frame, width=380, height=150)
        self.text_box.grid(row=2, column=0, padx=20, pady=10)

        self.analyize_button = ctk.CTkButton(self.third_frame, text="Analysis", command=self.analysis, width=100)
        self.analyize_button.grid(row=3, column=0,padx=20, pady=10)

        self.voice_emotion_label = ctk.CTkLabel(self.third_frame, text = "Emotion: ")
        self.voice_emotion_label.grid(row=3,column=1,padx=20,pady=10)
        
        self.clear_button = ctk.CTkButton(self.third_frame,text="Clear",command=self.clear_text_box)
        self.clear_button.grid(row=3, column=2,padx=10,pady=10)

    def toggle_recording(self):
        if not self.isrecording:
            self.isrecording = True
            self.record_button.configure(text="Stop Recording")
            thread = threading.Thread(target=self.record)   
            thread.start()
        else:
            self.isrecording = False
            self.record_button.configure(text="Start Recording")
        
    
    def stop_recognition(self):
        self.stop_event.set()
        return

    def record(self,stop=False):
        self.recognizer.start()
        if not self.isrecording:
           self.recognizer.stop() 
        import json
        try:
            while self.isrecording:
                result = self.recognizer.process_audio()
                if result:
                    try:
                        text_recon = json.loads(result)["text"]
                        print(json.loads(result)["text"])
                        self.text_box.insert(ctk.END,text_recon+" ")
                    except KeyError:
                        pass
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.recognizer.stop()

        return
    
    def analysis(self):
        spell = Speller()
        user_text = self.text_box.get("1.0", ctk.END).strip()
        self.text_box.delete(1.0,ctk.END)

        corrected_text = spell(user_text)
        self.text_box.insert(ctk.END,corrected_text)
        emotion_dict = te.get_emotion(corrected_text)
        top_two = self.get_top_two_emotions(emotion_dict)
        top_two_str = top_two[0]
        self.voice_emotion_label.configure(text=f"Emotion: {top_two_str}")
        if top_two[0].lower().startswith("sad") or top_two[0].lower().startswith("ang"):
            toast('Vibe Vision', 'You seems a bit sad, should i suggest a video that would help you up?', on_click=lambda args: self.play_vid())
        return

    def render_frame4_settings(self):
        self.fourth_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(self.fourth_frame, text="Settings", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        # Camera Selection
        camera_label = ctk.CTkLabel(self.fourth_frame, text="Camera Selection")
        camera_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.camera_var = ctk.StringVar(value="laptop")
        laptop_radio = ctk.CTkRadioButton(self.fourth_frame, text="Laptop Camera", variable=self.camera_var, value="laptop", command=self.toggle_network_entry)
        laptop_radio.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")

        network_radio = ctk.CTkRadioButton(self.fourth_frame, text="Network Camera", variable=self.camera_var, value="network", command=self.toggle_network_entry)
        network_radio.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="w")

        # Network Camera Link Entry
        self.network_entry = ctk.CTkEntry(self.fourth_frame, placeholder_text="Enter network camera link")
        self.network_entry.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.network_entry.configure(state="disabled")  # Initially disabled
        #self.network_entry.bind("<FocusOut>", self.validate_ip)
        
        # Volume Slider
        volume_label = ctk.CTkLabel(self.fourth_frame, text="Volume")
        volume_label.grid(row=5, column=0, padx=20, sticky="w")
        volume_slider = ctk.CTkSlider(self.fourth_frame, from_=0, to=100, number_of_steps=10)
        volume_slider.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Theme Switch
        theme_switch = ctk.CTkSwitch(self.fourth_frame, text="Dark Mode")
        theme_switch.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        # Notifications Checkbox
        notifications_checkbox = ctk.CTkCheckBox(self.fourth_frame, text="Enable Notifications")
        notifications_checkbox.grid(row=8, column=0, padx=20, pady=10, sticky="w")

        # Save Button
        save_button = ctk.CTkButton(self.fourth_frame, text="Save Settings",command=self.save_settings)
        save_button.grid(row=9, column=0, padx=20, pady=10, sticky="ew")
        
    def toggle_network_entry(self):
        if self.camera_var.get() == "network":
            self.network_entry.configure(state="normal")
        else:
            self.network_entry.configure(state="disabled")

    def save_settings(self):
        from ping3 import ping
        from urllib.parse import urlparse

        if self.camera_var.get() == "network":
            self.network_camera_link = self.network_entry.get()
            self.isCameraNetwork = True
            self.camera_url = self.network_camera_link
            self.camera_url_hostname = urlparse(self.camera_url).hostname
            if not ping(self.camera_url_hostname):
                self.network_entry.configure(border_color="red",border_width=2, placeholder_text="Enter correct IP");
                self.isCameraNetwork = False
                print("rejected!!")
                self.camera_url = ""

            print(f"Network camera link saved: {self.network_camera_link}")
            for widget in self.home_frame.winfo_children():
                widget.destroy()
            self.render_home()
        else:
            self.isCameraNetwork = False
            self.network_camera_link = ""
            print("Using laptop camera")
        
        

        # Here you can add code to save other settings as well
        print("Settings saved")
        
       


    def select_frame_by_name(self, name):
        # set button color for selected butt
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        grid_forgotten = 0 
        # show selected frame
        if name == "home":
            # self.render_home()
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
            grid_forgotten += 1
            print("grid forgotten!!"+str(grid_forgotten))

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:

            self.second_frame.grid_forget()
            grid_forgotten += 1
            print("grid forgotten!!"+str(grid_forgotten))

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
            grid_forgotten += 1
            print("grid forgotten!!"+str(grid_forgotten))

        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
            grid_forgotten += 1
            print("grid forgotten!!"+str(grid_forgotten))

    def home_button_event(self):
        self.select_frame_by_name("home")
        # NO! you weren't suppose to render the widges
        # every time user press the home button.
        # self.render_home()

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        self.render_frame2_text()

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        self.render_frame3_voice()

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        self.render_frame4_settings()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

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



if __name__ == '__main__':
    window = app()
    window.mainloop()