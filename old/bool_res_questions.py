import customtkinter as ctk
from tkinter import messagebox
import json
import sys

# Initialize the main window
ctk.set_appearance_mode("dark")  # Set dark mode
ctk.set_default_color_theme("dark-blue")  # You can choose other themes as well
root = ctk.CTk()
root.title("Sentiment Analysis Questions")
root.geometry("600x700")

# Add a heading
heading = ctk.CTkLabel(root, text="Guest Questions", font=("Arial", 24))
heading.pack(pady=20)

# List of questions with associated emotions
questions_with_emotions = [
    {"question": "Are you happy with your current job?", "emotion": "happiness"},
    {"question": "Did you enjoy your vacation?", "emotion": "happiness"},
    {"question": "Do you feel satisfied with your achievements?", "emotion": "happiness"},
    {"question": "Are you looking forward to the weekend?", "emotion": "happiness"},
    {"question": "Did you have a good day today?", "emotion": "happiness"},
    {"question": "Are you feeling sad today?", "emotion": "sadness"},
    {"question": "Did something upset you recently?", "emotion": "sadness"},
    {"question": "Do you miss someone right now?", "emotion": "sadness"},
    {"question": "Are you feeling down because of the weather?", "emotion": "sadness"},
    {"question": "Do you feel lonely sometimes?", "emotion": "sadness"},
    {"question": "Are you angry about the recent news?", "emotion": "anger"},
    {"question": "Did someone make you upset today?", "emotion": "anger"},
    {"question": "Are you frustrated with your work situation?", "emotion": "anger"},
    {"question": "Did you have a disagreement with someone?", "emotion": "anger"},
    {"question": "Are you annoyed by the traffic?", "emotion": "anger"},
    {"question": "Are you afraid of the dark?", "emotion": "fear"},
    {"question": "Do you worry about the future?", "emotion": "fear"},
    {"question": "Are you scared of heights?", "emotion": "fear"},
    {"question": "Do you feel anxious about your health?", "emotion": "fear"},
    {"question": "Are you concerned about your safety?", "emotion": "fear"},
    {"question": "Did the surprise party make you happy?", "emotion": "surprise"},
    {"question": "Were you surprised by the announcement?", "emotion": "surprise"},
    {"question": "Did the unexpected gift delight you?", "emotion": "surprise"},
    {"question": "Were you shocked by the sudden change?", "emotion": "surprise"},
    {"question": "Did the news catch you off guard?", "emotion": "surprise"}
]

# List to store the responses
responses = []


def count_emotion_responses(data):
    # Initialize a dictionary to store counts of yes and no responses for each emotion
    emotion_counts = {}
    
    for entry in data:
        emotion = entry["emotion"]
        response = entry["response"]
        
        if emotion not in emotion_counts:
            emotion_counts[emotion] = {"Yes": 0, "No": 0}
        
        if response == "Yes":
            emotion_counts[emotion]["Yes"] += 1
        elif response == "No":
            emotion_counts[emotion]["No"] += 1
    
    return emotion_counts


def calculate_percentage_responses(emotion_counts):
    percentage_responses = {}
    
    for emotion, counts in emotion_counts.items():
        total_responses = counts["Yes"] + counts["No"]
        if total_responses > 0:
            percentage_yes = (counts["Yes"] / total_responses) * 100
        else:
            percentage_yes = 0.0
        
        percentage_responses[emotion] = round(percentage_yes, 2)
    
    return percentage_responses


def normalize_percentages(percentage_responses):
    total_percentage = sum(percentage_responses.values())
    normalized_percentages = {emotion: (percentage / total_percentage) * 100 for emotion, percentage in percentage_responses.items()}
    return normalized_percentages


# Function to save responses to a JSON file
def save_responses():
    root.destroy()
    def run_piechart_animation(data_emotion_list:list):
        
        import subprocess
        command_list = [sys.executable,".\\pie_chart_anim.py"]
        for cmd in data_emotion_list:
            command_list.append(str(cmd))
        subprocess.run(command_list)
    # Ensure all questions have a response
    for item in questions_with_emotions:
        question = item["question"]
        emotion = item["emotion"]
        if not any(resp['question'] == question for resp in responses):
            responses.append({"question": question, "emotion": emotion, "response": "No"})


    with open('responses.json', 'w') as file:
        json.dump(responses, file, indent=4)
    messagebox.showinfo("Saved", "Responses saved successfully!")

    normalized_per1 = normalize_percentages(calculate_percentage_responses(count_emotion_responses(responses)))
    print(normalized_per1);

    run_piechart_animation([normalized_per1['happiness'],normalized_per1['sadness'],
                             normalized_per1['anger'],normalized_per1['fear'], 
                             normalized_per1['surprise']])

# Function to handle checkbox click
def on_checkbox_click(question, emotion, response_var):
    #response = "Yes" if response_var.get() == 1 else "No"
    if response_var.get() == 1:
        response = "Yes"
    else:
        response = "No"
    # Update the response if already exists, else append a new one
    for resp in responses:
        if resp['question'] == question:
            resp['response'] = response
            return
    responses.append({"question": question, "emotion": emotion, "response": response})

# Create a scrollable frame for the questions
scrollable_frame = ctk.CTkScrollableFrame(root, width=580, height=500)
scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create checkboxes for each question
for item in questions_with_emotions:
    frame = ctk.CTkFrame(scrollable_frame)
    frame.pack(pady=10, padx=10, fill="x")
    
    label = ctk.CTkLabel(frame, text=item["question"], wraplength=450, justify="left")
    label.pack(anchor='center', pady=5)
    
    response_frame = ctk.CTkFrame(frame)
    response_frame.pack(pady=5)
    
    var_yes = ctk.IntVar(value=0)
    checkbox_yes = ctk.CTkCheckBox(response_frame, text="Yes", variable=var_yes, command=lambda q=item["question"], e=item["emotion"], v=var_yes: on_checkbox_click(q, e, v))
    checkbox_yes.pack(side='left', padx=20)
    
    var_no = ctk.IntVar(value=0)
    checkbox_no = ctk.CTkCheckBox(response_frame, text="No", variable=var_no, command=lambda q=item["question"], e=item["emotion"], v=var_no: on_checkbox_click(q, e, v))
    checkbox_no.pack(side='left', padx=20)

# Save button
save_button = ctk.CTkButton(root, text="Save Responses", command=save_responses)
save_button.pack(pady=20)

# Run the main loop
root.mainloop()
