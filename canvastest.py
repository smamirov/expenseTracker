'''from tkinter import *
from matplotlib import figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


root = Tk()
root.title("Embeded Matplotlib Plot")
root.geometry('800x700')



categoryChart = Figure(figsize=(5,5), dpi=100)
categorySubplot = categoryChart.add_subplot(211)

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]

categorySubplot.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
categorySubplot.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

myCanvas = FigureCanvasTkAgg(categoryChart, root)
myCanvas.draw()
myCanvas.get_tk_widget().grid(row=0, column=0)

root.mainloop()'''