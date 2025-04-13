"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from elements import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def get_current_datetime():
    return str(datetime.now().strftime("%Y_%m_%d %H_%M_%S"))

class PDFReport:

    def __init__(self, filename):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=letter)
        self.width, self.height = letter  # Page size
        self.y_position = self.height - 50  # Start from the top

    def add_text(self, text, font="Helvetica", size=12, spacing=20):
        """Add text dynamically and move down"""
        if self.y_position < 50:  # Check if we need a new page
            self.new_page()
        
        self.canvas.setFont(font, size)
        self.canvas.drawString(100, self.y_position, text)
        self.y_position -= spacing  # Move cursor down for next element

    def add_plot(self, plot_filename="plot.png", width=400, height=250, spacing=30):
        """Generate a plot using a function, save it, and insert it into the PDF"""
        if self.y_position - height < 50:  # Check if the plot fits
            self.new_page()

        image = ImageReader(plot_filename)
        self.canvas.drawImage(image, 100, self.y_position - height, width=width, height=height)
        
        self.y_position -= (height + spacing)  # Move cursor down

    def new_page(self):
        """Create a new page and reset the position"""
        self.canvas.showPage()
        self.y_position = self.height - 50  # Reset y position for new page

    def save_pdf(self):
        """Save the final PDF"""
        self.canvas.save()

def time_serie_plot(time, mean, median, q1, q3, X_label, Y_Label, title, img_path, filename, figsize =(10, 5), evidence_mean = True):

    plt.figure(figsize = figsize)
    plt.plot(time, mean, label="mean", color='blue')
    plt.plot(time, median, label="median", color="orange", linestyle="--")
    if evidence_mean:
        mean_value = np.mean(mean)
        plt.axhline(y=mean_value, color='red', linestyle='--', label=f'Mean of mean: {mean_value:.2f}')
    plt.fill_between(time, q1, q3, color = "blue", alpha = 0.2, label='Interquartile Range (Q1–Q3)')
    
    plt.xlabel(X_label)
    plt.ylabel(Y_Label)
    plt.title(title)
    plt.legend()

    plt.savefig(img_path+filename+".png")  # Save plot as an image
    plt.close()  # Close the figure to free memory

def parameters_plot(x, s, a, n, filename, figsize =(10, 5)):

    plt.figure(figsize=figsize)
    plt.plot(x, s, label = "Selfishness", color = "red")
    plt.plot(x, a, label = "Altruism", color = "green")
    plt.plot(x, n, label = "Normality", color = "blue")
    plt.xlabel('Time')
    plt.ylabel("Social Parameters Mean")
    plt.title("Mean Social Parameters over Time")
    plt.legend()

    plt.savefig(filename)  # Save plot as an image
    plt.close()  # Close the figure to free memory

def time_series_data_analysis(data, time, X_label, Y_label, title, filename, img_path, pdf, max_len):
                data = np.array([row + [0]*(max_len -len(row)) for row in data])
                means = np.mean(data, axis = 0)
                medians = np.median(data, axis = 0)
                q1 = np.quantile(data, q = 0.25, axis = 0)
                q3 = np.quantile(data, q = 0.75, axis = 0)
                time_serie_plot(time, means, medians, q1, q3, X_label, Y_label, title, img_path, filename)
                pdf.add_plot(plot_filename= img_path+filename+".png")
                pdf.add_text(f"Mean : {np.mean(means)}", size = 8, spacing = 8)
                pdf.add_text(f"Variance : {np.var(means)}", size = 8, spacing = 8)

class StatsReporter:

    def __init__(self, initial_condition,  n_simulation, file_path = "REPORT/", folder_name_mode = 'Date_Time', time_window = 1):
        
        self.current_time = get_current_datetime()
        if folder_name_mode == 'Date_Time': # Date time name
            self.folder_name = self.current_time
        else: # folder_name_mode == 'Console': # Console input
            self.folder_name = input("Insert the name for the folder where to save the report: ")

        # Create the folder (if it doesn't exist)
        os.makedirs(file_path + self.folder_name, exist_ok=True)

        self.n_simulation = n_simulation
        self.time_window = time_window
        
        self.t = 0
        self.alive_population = [[] for s in range(self.n_simulation)]
        self.alive_cell = [[] for s in range(self.n_simulation)]
        self.mean_population_energy = [[] for s in range(self.n_simulation)]
        self.mean_world_energy = [[] for s in range(self.n_simulation)]
        self.selfish_mean_param = [[] for s in range(self.n_simulation)]
        self.altruism_mean_param = [[] for s in range(self.n_simulation)]
        self.normal_mean_param = [[] for s in range(self.n_simulation)]
        self.mean_population_age = [[] for s in range(self.n_simulation)]
        self.heritage = [[] for s in range(self.n_simulation)]
        self.different_heritage = [[] for s in range(self.n_simulation)]
        self.initial_condition = str(initial_condition) # it will be done by the initial condition handler everything to make it rigth
        self.file_path = file_path + self.folder_name + "/stats report.pdf"
        self.img_path = file_path + self.folder_name +"/"
        self.positions = [[] for s in range(self.n_simulation)]
        self.horizons = [0 for s in range(self.n_simulation)]
        self.windows_horizons = [0 for s in range(self.n_simulation)]
    
    def update(self,  population : Population, world : World, simulation_number : int):
        self.t += 1
        s = simulation_number
        if self.t % self.time_window == 0:
            self.alive_population[s].append(population.alive())
            self.alive_cell[s].append(world.alive())
            self.mean_population_energy[s].append(population.mean_energy)
            self.mean_world_energy[s].append(world.mean_energy)
            social_mean_param = population.get_behaviors()
            self.selfish_mean_param[s].append(social_mean_param.count("S"))
            self.altruism_mean_param[s].append(social_mean_param.count("A"))
            self.normal_mean_param[s].append(social_mean_param.count("N"))
            self.heritage[s].append(population.heritage)
            self.different_heritage[s].append(len(set(population.heritage)))
            self.mean_population_age[s].append(population.mean_age)
            p = [1 if w_p else 0 for w_p in world.get_position()]
            self.positions[s].append(p)
    
    def report(self, simulation_number, forced_end = False):

        self.horizons[simulation_number] = self.t
        self.windows_horizons[simulation_number] = self.t//self.time_window
        
        if simulation_number == (self.n_simulation - 1) or forced_end:

            # -> needed to PAD (with 0) DATA IN ORDER TO OBTAIN HOMOGENEOUS MATRIX
            max_len = max(self.windows_horizons)
            # ACTUAL TIME
            time = np.linspace(0, max_len - 1, max_len)

            pdf = PDFReport(self.file_path)
            # DATE TIME
            pdf.add_text(text=f"Test done {self.current_time.split(" ")[0]} at {self.current_time.split(" ")[1]}", size = 10)
            pdf.add_text(text=f"Number of simulation done : {simulation_number + 1}. The window time of the simulation is {self.time_window}", size = 6)
            if forced_end:
                pdf.add_text(text=f"!!! THIS SIMULATION HAS BEEN EARLY STOPPED !!!", size = 6)

            # INITIAL CONDITION - note that they are not really all the initial condition
            pdf.add_text("Initial condition", size = 9, spacing = 10)
            for cond in self.initial_condition.split("\n"):
                pdf.add_text(text=cond, size=8, spacing=10)

            # HORIZONS OF ALL SIMULATIONS

            ts = np.array(self.horizons)
            plt.figure(figsize = (10, 5))
            plt.scatter([i for i in range (len(ts))], ts, label="Horizons", color='blue')
            plt.xlabel("Simulations")
            plt.ylabel("Horizons")
            plt.title("Horizons over simulations")
            plt.legend()
            plt.savefig(self.img_path + "Horizons.png")  # Save plot as an image
            plt.close()  # Close the figure to free memory

            pdf.add_plot(plot_filename=self.img_path+"Horizons.png")
            pdf.add_text(f"Mean : {np.mean(ts)}", size = 8, spacing = 8)
            pdf.add_text(f"Variance : {np.var(ts)}", size = 8, spacing = 8)

            # POPULATION OVER TIME PLOT
            time_series_data_analysis(self.alive_population, time, "Time", "Population", "Average Population over time", "Pops over time", self.img_path, pdf, max_len)

            """
            # POPULATION OVER TIME PLOT

            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.alive_population), "Population", "Population over time", filename=self.img_path+"Population over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Population over time.png")
            pdf.add_text(f"Mean : {np.mean(np.array(self.alive_population))}", size = 8, spacing = 8)
            pdf.add_text(f"Variance : {np.var(np.array(self.alive_population))}", size = 8, spacing = 8)
            pdf.add_text(f"Min : {np.min(np.array(self.alive_population))}", size = 8, spacing = 8)
            pdf.add_text(f"Max : {np.max(np.array(self.alive_population))}", size = 8, spacing = 8)

            # CELL OVER TIME PLOT
            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.alive_cell), "Cell", "Cell over time", filename=self.img_path+"Cell over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Cell over time.png")
            
            # MEAN POPULATION ENERGY OVER TIME
            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.mean_population_energy), "Mean Population Energy", "Mean Population Energy over time", filename=self.img_path+"Mean Population Energy over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Mean Population Energy over time.png")
            pdf.add_text(f"Mean : {np.mean(np.array(self.mean_population_energy))}", size = 8, spacing = 8)
            pdf.add_text(f"Variance : {np.var(np.array(self.mean_population_energy))}", size = 8, spacing = 8)

            # MEAN POPULATION AGE OVER TIME
            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.mean_population_age), "Mean Population Age", "Mean Population Age over time", filename=self.img_path+"Mean Population Age over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Mean Population Age over time.png")
            pdf.add_text(f"Mean : {np.mean(np.array(self.mean_population_age))}", size = 8, spacing = 8)
            pdf.add_text(f"Variance : {np.var(np.array(self.mean_population_age))}", size = 8, spacing = 8)

            # MEAN WORLD ENERGY OVER TIME
            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.mean_world_energy), "Mean World Energy", "Mean World Energy over time", filename=self.img_path+"Mean World Energy over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Mean World Energy over time.png")

            # MEAN SOCIAL PARAMETERS OVER TIME
            parameters_plot(np.linspace(0, self.t, self.t), np.array(self.selfish_mean_param), np.array(self.altruism_mean_param), np.array(self.normal_mean_param), filename=self.img_path+"Mean Social Parameters over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Mean Social Parameters over time.png")

            # DIFFERENT HERITAGE COUNT OVER TIME
            time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.different_heritage), "Different Heritage", "Different Heritage over time", filename=self.img_path+"Different Heritage over time.png")
            pdf.add_plot(plot_filename=self.img_path+"Different Heritage over time.png")
            """
            # META DATA
            pdf.add_text(text="Author : Francesco Bredariol", size = 7, spacing = 7)
            pdf.add_text(text="Year : 2024/2025", size = 7, spacing = 7)
            pdf.add_text(text="This Project is done for the academic purpose of implementing the practical part of the Degree Thesis in Artificial Intelligence and Data Analytics.", size = 7, spacing = 7)
            
            pdf.save_pdf()
            print(f"Pdfcreated succesfully. You can find it at {self.file_path}")

        self.t = 0

if __name__ == "__main__":
    pass




