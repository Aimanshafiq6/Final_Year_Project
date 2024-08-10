import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

class AnimatedPieChart(ctk.CTkFrame):
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

# Example usage in another CTk program:
class MainApp(ctk.CTk):
    def __init__(self,hap,sad,ang,fear,sur):
        super().__init__()

        self.title("Emotion Wheel")
        self.geometry("800x600")

        self.start_animation(hap,sad,ang,fear,sur)      
        self.protocol("WM_DELETE_WINDOW", self.quit)
        # Add a quit button
        quit_button = ctk.CTkButton(self, text="Quit", command=self.quit, fg_color="darkred", hover_color="red")
        quit_button.pack(side=ctk.BOTTOM, pady=10)
    def start_animation(self,hap,sad,ang,fear,sur):
        initial_data = [0,0,0,0,0,100]
        target_data = [hap,sad,ang,fear,sur,0]
        colors = ['gold', 'yellowgreen', 'red', 'limegreen','magenta','white']
        labels = ['happiness', 'sadness', 'anger', 'fear','surprise',""]

        # Create and pack the AnimatedPieChart
        self.pie_chart = AnimatedPieChart(self, initial_data, target_data, colors, labels)

if __name__ == "__main__":
    app = MainApp(hap=20,sad=30,ang=20,fear=20,sur=10)
    app.mainloop()