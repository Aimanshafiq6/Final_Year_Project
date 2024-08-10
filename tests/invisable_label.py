import matplotlib.pyplot as plt

# Data for the pie chart
sizes = [30, 30, 40]
labels = ['A', 'B', 'C']
colors = ['#ff9999', '#66b3ff', '#99ff99']

# Custom function to hide one label
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        # Return empty string for the first slice (index 0)
        return f'{pct:.1f}%\n({val:d})' if pct > values[0] else ''
    return my_autopct

# Create the pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct=make_autopct(sizes), startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')  

# Add a title
plt.title("Pie Chart with One Invisible Label")

# Show the plot
plt.show()