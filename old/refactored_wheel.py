import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class EmotionWheel:
    def __init__(self, root, max_data):
        self.root = root
        self.max_data = max_data
        self.data = {emotion: 0 for emotion in self.max_data}
        self.emotions_name = list(self.max_data.keys())
        self.colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen']

        self.setup_window()
        self.setup_plot()
        self.create_animation()
        self.embed_plot()
        self.add_quit_button()

    def setup_window(self):
        self.root.title("Animated Pie Chart in CustomTkinter")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1f26')  # Dark blue background

    def setup_plot(self):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#1e1f26')  # Set the figure background color
        self.ax.set_facecolor('#1e1f26')         # Set the axis background color

    def create_animation(self):
        self.ani = FuncAnimation(self.fig, self.update, frames=range(200), repeat=False, interval=30)

    def embed_plot(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    def add_quit_button(self):
        quit_button = ctk.CTkButton(self.root, text="Quit", command=self.root.quit, fg_color="darkred", hover_color="red")
        quit_button.pack(side=ctk.BOTTOM, pady=10)

    def update(self, num):
        self.ax.clear()
        self.ax.axis('equal')
        for k in self.data.keys():
            if self.data[k] < self.max_data[k]:
                self.data[k] += 1.5

        wedges, texts, autotexts = self.ax.pie(
            list(self.data.values()), 
            colors=self.colors, 
            labels=self.emotions_name, 
            autopct='%1.1f%%', 
            shadow=True, 
            startangle=0
        )
        for text in texts + autotexts:
            text.set_color('white')  # Set text color to white for better contrast
        self.ax.set_title("Emotion Wheel", color='white')  # Set title color to white
        plt.text(0, -1.5, self.get_max_emo_from_data(), ha='center', va='center', fontsize=12, color='white')

    def get_max_emo_from_data(self):
        return max(self.max_data, key=self.max_data.get)

    def run(self):
        self.root.mainloop()

def main():
    
    max_data = {
        'happy': float(sys.argv[1]),
        'sad': float(sys.argv[2]),
        'angry': float(sys.argv[3]),
        'fear': float(sys.argv[4]),
        'surprise': float(sys.argv[5])
    }

    root = ctk.CTk()
    emotion_wheel = EmotionWheel(root, max_data)
    emotion_wheel.run()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Proper args not given")
        sys.exit(0)
main()