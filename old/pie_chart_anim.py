import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys

# Data for the pie chart
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen', 
          'red', 'navy', 'blue', 'magenta', 'crimson']
explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Initialize the CustomTkinter window
root = ctk.CTk()
root.title("Animated Pie Chart in CustomTkinter")
root.geometry("800x600")
root.configure(bg='#1e1f26')  # Dark blue background

# Create a figure and axis for the pie chart
fig, ax = plt.subplots()
fig.patch.set_facecolor('#1e1f26')  # Set the figure background color
ax.set_facecolor('#1e1f26')         # Set the axis background color

data = {
    'happy':0,
    'sad':0,
    'angry':0,
    'fear':0,
    'surprise':0
}

# happy_norm_val = (happy_response_raw_val / sum_raw_val) * 100;
# sad_norm_val = (sad_response_raw_val / sum_raw_val) * 100
# angry_norm_val = (angry_response_raw_val / sum_raw_val) * 100
# fear_norm_val = (fear_response_raw_val / sum_raw_val) * 100
# surprise_norm_val = (surprise_response_raw_val / sum_raw_val) * 100

emotions_name = ['happy','sad','angry','fear','surprise']

if len(sys.argv) < 6:
    print("proper args not given")
    sys.exit(0);

max_Data = {
    'happy': float(sys.argv[1]) ,
    'sad': float(sys.argv[2]),
    'angry': float(sys.argv[3]),
    'fear': float(sys.argv[4]),
    'surprise': float(sys.argv[5])
}

def get_max_emo_from_data(max_data:dict):

    max_found = 0
    key_found = ''
    for k,v in max_data.items():
        if v > max_found:
            max_found = v
            key_found = k
    
    return key_found


def update(num):
    ax.clear()
    ax.axis('equal')
    for k in data.keys():
        if data[k] < max_Data[k]:
            data[k] += 1.5
        



    wedges, texts, autotexts = ax.pie( list(data.values()), colors=colors, labels = emotions_name, 
                                      autopct='%1.1f%%', shadow=True, startangle=0)
    for text in texts + autotexts:
        text.set_color('white')  # Set text color to white for better contrast
    ax.set_title(f"Emotion Wheele: " , color='white')  # Set title color to white
    plt.text(0, -1.5,get_max_emo_from_data(max_Data), ha='center', va='center', fontsize=12, color='white')

# Create the animation
ani = FuncAnimation(fig, update, frames=range(200), repeat=False,interval=30)

# Embed the plot into CustomTkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

# Add a quit button
quit_button = ctk.CTkButton(root, text="Quit", command=root.quit, fg_color="darkred", hover_color="red")
quit_button.pack(side=ctk.BOTTOM, pady=10)

# Run the CustomTkinter event loop
root.mainloop()
