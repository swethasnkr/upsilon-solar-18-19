#----------------------------------------------------------------#
#                                                                #
# Solar Cell Power Grapher GUI                                   #
#                                                                #
#----------------------------------------------------------------#

import math
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import webbrowser

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import matplotlib.animation as animation
import numpy as np
from matplotlib import style

from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import time as clock
import random
import sys


#----------------------------------------------------------------#
#                                                                #
# Debugging                                                      #
#                                                                #
#----------------------------------------------------------------#

'''
print('Python version ' + sys.version)
print('Matplotlib version ' + matplotlib.__version__)
print('Numpy version ' + np.version.version)
'''


#----------------------------------------------------------------#
#                                                                #
# MatPlotLib styling                                             #
#                                                                #
#----------------------------------------------------------------#

# style.use('fivethirtyeight')


#----------------------------------------------------------------#
#                                                                #
# GUI Settings                                                   #
#                                                                #
#----------------------------------------------------------------#

class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        ### Splash window setup
        self.title("Splash")
        self.overrideredirect(True)
        width = 900
        height = 700
        self.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))
        
        ### Image loading for splash
        splash_img = "solar_splash.png"
        image = PhotoImage(file = splash_img)
        
        canvas = Canvas(self, height = height*0.8, width = width*0.8)
        canvas.create_image(width*0.8/2, height*0.8/2, image = image)
        canvas.pack()
        
        self.update()

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		### Splash screen setup
		self.withdraw()
		splash = Splash(self)

		### App window setup
		self.title("Solar Cell Power Grapher GUI")
		self.config(bg = "#ffffaa")

		### Menu and commands for window
		self.menu = Menu(self)

		new_item = Menu(self.menu, tearoff = 0)
		new_item.add_command(label = "Clear All", command = self.clearFields)
		new_item.add_separator()
		new_item.add_command(label = "Exit", command = self.appDestroy)
		self.menu.add_cascade(label = "File", menu = new_item)

		new_item = Menu(self.menu, tearoff = 0)
		new_item.add_command(label = "PVEducation.Org", command = self.openHelp)
		new_item.add_separator()
		new_item.add_command(label = "About...", command = self.aboutPop)
		self.menu.add_cascade(label = "Help", menu = new_item)

		self.config(menu = self.menu)
		
		### Data arrays for MatPlotLib scatter plot
		self.Data3 = {'Interest_Rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
			'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]}
		self.df3 = DataFrame(self.Data3, columns = ['Interest_Rate', 'Stock_Index_Price'])

		### Label widget to describe GUI purpose
		self.caption_root = "This program accepts various parameters (pertaining to technical properties,\nand enviromental factors like cloud cover and location)\nto calculate the ideal power output of the solar panel.\n\nSpecify each variable as decimals in the fields colored white below.\nThe Calculate All button will export calculations in the fields colored yellow;\nit will also output a MatPlotLib graph detailing the power output over time.\n\nThe Incoming Solar Intensity is on average defined as 1367 W/m^2.\nThe Solar Panel Area is currently not used in any calculation yet."

		self.lbl_main = Label(self, bg = "#ffffaa", text = self.caption_root, padx = 10, pady = 10)
		self.lbl_main.config(font=("Arial", 11))
		self.lbl_main.grid(columnspan = 3, row = 1)

		self.grid_columnconfigure(0, minsize = 400)
		self.grid_rowconfigure(2, minsize = 20)

		### Entry widgets to receive input for variables
		self.lbl_panelA = Label(self, bg = "#ffffaa", text = "Solar Panel Area (m^2)", padx = 5, pady = 5)
		self.lbl_panelA.grid(column = 0, row = 3, sticky = W)
		self.ent_panelA = Entry(self, width = 30)
		self.ent_panelA.grid(column = 1, row = 3)

		self.lbl_vOC = Label(self, bg = "#ffffaa", text = "Open Circuit Voltage (V)", padx = 5, pady = 5)
		self.lbl_vOC.grid(column = 0, row = 4, sticky = W)
		self.ent_vOC = Entry(self, width = 30)
		self.ent_vOC.grid(column = 1, row = 4)

		self.lbl_iSC = Label(self, bg = "#ffffaa", text = "Short Circuit Current (A)", padx = 5, pady = 5)
		self.lbl_iSC.grid(column = 0, row = 5, sticky = W)
		self.ent_iSC = Entry(self, width = 30)
		self.ent_iSC.grid(column = 1, row = 5)

		self.lbl_ff = Label(self, bg = "#ffffaa", text = "Fill Factor (decimal)", padx = 5, pady = 5)
		self.lbl_ff.grid(column = 0, row = 6, sticky = W)
		self.ent_ff = Entry(self, width = 30)
		self.ent_ff.grid(column = 1, row = 6)

		self.lbl_solInt = Label(self, bg = "#ffffaa", text = "Incoming Solar Intensity (W/m^2)", padx = 5, pady = 5)
		self.lbl_solInt.grid(column = 0, row = 7, sticky = W)
		self.ent_solInt = Entry(self, width = 30)
		self.ent_solInt.insert(END, "1367")
		# self.ent_solInt.config(state = "disabled")
		self.ent_solInt.grid(column = 1, row = 7)

		self.grid_rowconfigure(8, minsize = 20)

		### Output labels from calculations
		self.lbl_effic = Label(self, bg = "#ffffaa", text = "Efficiency (decimal)", padx = 5, pady = 5)
		self.lbl_effic.grid(column = 0, row = 9, sticky = W)
		self.ent_effic = Entry(self, bg = "#ffff70", width = 30)
		self.ent_effic.grid(column = 1, row = 9)

		self.lbl_pwrMax = Label(self, bg = "#ffffaa", text = "Maximum Power (W)", padx = 5, pady = 5)
		self.lbl_pwrMax.grid(column = 0, row = 10, sticky = W)
		self.ent_pwrMax = Entry(self, bg = "#ffff70", width = 30)
		self.ent_pwrMax.grid(column = 1, row = 10)

		self.grid_rowconfigure(11, minsize = 20)

		### Create Button widget to initiate calculations
		self.btn = Button(self, text = "Calculate All", command = self.massCalculate, padx = 5, pady = 5)
		self.btn.grid(columnspan = 3, row = 12)

		self.grid_rowconfigure(13, minsize = 10)

		self.grid_columnconfigure(2, minsize = 20)

		### MatPlotLib scatter plot setup
        ### Need to update variable names
		plt.ion()
		self.fig = plt.Figure(figsize = (7, 4), dpi = 100)
		self.a = self.fig.add_subplot(111)
		self.a.scatter(self.df3['Interest_Rate'], self.df3['Stock_Index_Price'], color='red')
		self.a.invert_yaxis()

		self.a.set_title ("Power Output", fontsize = 16)
		self.a.set_ylabel("Y", fontsize = 14)
		self.a.set_xlabel("X", fontsize = 14)
		self.plotS = FigureCanvasTkAgg(self.fig, self)
        
		self.plotS.get_tk_widget().grid(column = 3, row = 0, rowspan = 13)
		self.grid_columnconfigure(3, minsize = 400)
		self.grid_columnconfigure(4, minsize = 10)
		
		### Sleep and show app after splash screen
		clock.sleep(4)
		splash.destroy()
		self.deiconify()
		
	#define parameters for function
	def volt_current_plot(photoelec_current, T, sc_volt):
		saturation_current = math.pow(10, -12)
		#short circuit current (current generated by the sun? what is the relation)
		photoelec_current = 9.37 # short circuit current
		k = 0.00234
		q = 1
		T = 319.65
		n = 1

		sc_volt = 38.6 # open circuit voltage
		voltage_diode = np.linspace(start=0, stop=sc_volt, num=10000000) 
		#calculation of current across the diode
		current_diode = photoelec_current - saturation_current * (np.exp((voltage_diode * q )/(n * k * T)) - 1)
		#calculation of power produced across diode 
		pv_power = current_diode * voltage_diode


		#plot I-V Graph with power across diode and current across diode on the y-axes and voltage  
		#across diode on the x-axis
		fig, ax1 = plt.subplots()

		plt.title("I-V Graph")

		#customizing x-axis and the y-axis for current
		color = 'tab:red'
		ax1.set_xlabel('Voltage (V) ')
		ax1.set_ylabel('Current (A) ', color=color)
		ax1.plot(voltage_diode, current_diode, color=color, label = 'Voltage-Current Curve')
		ax1.set_ylim([0, 30])
		ax1.set_xlim([0, 50])
		ax1.tick_params(axis='y', labelcolor=color)
		plt.legend(loc = 'lower right')
		plt.grid()

		ax2 = ax1.twinx()

		#customizing the y-axis for power output
		color = 'tab:blue'
		ax2.set_ylabel('Power (W) ', color=color)
		ax2.plot(voltage_diode, pv_power, color=color, label = 'Power Curve (W)')
		ax2.set_ylim([0, 200])
		ax2.set_xlim([0, 50])
		ax2.tick_params(axis='y', labelcolor=color)
		plt.legend(loc = 'upper right')
		plt.grid()
		
		plt.show()
		
	### Define in-app functions
	def appDestroy(self):
		self.destroy()
        
	def openHelp(self):
		webbrowser.open_new("https://www.pveducation.org/")
    
	def aboutPop(self):
		messagebox.showinfo("About", "This GUI was made by Braden Lem from Emma Peavler's Solar Batteries and Charging Analysis team. The project for the GUI was originally started in Winter 2019.\n\nLast updated 2019-05-16.\n\nTeam members: Braden Lem, Emma Peavler, Raymond Ramlow, Swetha Sankar, William Zhu")
	
	def clearFields(self):
		self.ent_panelA.delete(0, END)
		self.ent_ff.delete(0, END)
		self.ent_vOC.delete(0, END)
		self.ent_iSC.delete(0, END)
		self.ent_solInt.delete(0, END)
		self.ent_solInt.insert(END, "1367")

		self.ent_effic.delete(0, END)
		self.ent_pwrMax.delete(0, END)
		
	def efficCalc(self):
		vOC   = float(self.ent_vOC.get())
		iSC   = float(self.ent_iSC.get())
		ff    = float(self.ent_ff.get())
		pwrIn = float(self.ent_solInt.get())
		
		res = (vOC * iSC * ff) / pwrIn
		self.ent_effic.delete(0, END)
		self.ent_effic.insert(END, res)
		
	def massCalculate(self):
		self.efficCalc()
		self.pwrMaxCalc()
		
        ### Placeholder data update to demonstrate plot updating
		newData = [0] * 10
		i = 0
		for i in range(10):
			newData[i] = random.randint(0, 1000)
			i += 1
		
		self.Data3 = {'Interest_Rate': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
			'Stock_Index_Price': newData
		   }
		self.df3 = DataFrame(self.Data3, columns = ['Interest_Rate', 'Stock_Index_Price'])
		self.plot()
		
	def pwrMaxCalc(self):
		pwrIn = float(self.ent_solInt.get())
		effic = float(self.ent_effic.get())
		
		# res = (vOC * iSC * ff)
		# The "pwrIn" that is used here is a parameter in Emma's code...?
		res = (effic * pwrIn)
		self.ent_pwrMax.delete(0, END)
		self.ent_pwrMax.insert(END, res)
			
	def plot(self):
		self.a.cla()
		self.a.set_title ("Power Output", fontsize = 16)
		self.a.scatter(self.df3['Interest_Rate'], self.df3['Stock_Index_Price'], color='red')
		self.plotS.draw()


#----------------------------------------------------------------#
#                                                                #
# GUI Launch                                                     #
#                                                                #
#----------------------------------------------------------------#

### Enter Tkinter event loop
if __name__ == "__main__":
    app = App()
    app.mainloop()
