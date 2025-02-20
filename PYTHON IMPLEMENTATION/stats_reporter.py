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

def time_serie_plot(x, y, label, title, filename, figsize =(10, 5), evidence_mean = True):

    plt.figure(figsize = figsize)
    plt.plot(x, y, label=label, color='blue')
    if evidence_mean:
        mean_value = np.mean(y)
        plt.axhline(y=mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
    
    plt.xlabel('Time')
    plt.ylabel(label)
    plt.title(title)
    plt.legend()

    plt.savefig(filename)  # Save plot as an image
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

class StatsReporter:

    def __init__(self, initial_condition, file_path = "REPORT/"):
        
        self.current_time = get_current_datetime()
        self.folder_name = self.current_time
        # Create the folder (if it doesn't exist)
        os.makedirs(file_path + self.folder_name, exist_ok=True)

        self.t = 0
        self.alive_population = []
        self.alive_cell = []
        self.birth = []
        self.death = []
        self.mean_population_energy = []
        self.mean_world_energy = []
        self.selfish_mean_param = []
        self.altruism_mean_param = []
        self.normal_mean_param = []
        self.heritage = []
        self.different_heritage = []
        self.initial_condition = str(initial_condition) # it will be done by the initial condition handler everything to make it rigth
        self.file_path = file_path + self.folder_name + "/stats report.pdf"
        self.img_path = file_path + self.folder_name +"/"
    
    def update(self,  population : Population, world : World):
        self.alive_population.append(population.alive())
        self.alive_cell.append(world.alive())
        self.birth.append(population.born) # Born at every time stamp
        self.death.append(population.dead) # Dead at every time stamp
        self.mean_population_energy.append(population.mean_energy)
        self.mean_world_energy.append(world.mean_energy)
        social_mean_param = population.mean_parameters
        self.selfish_mean_param.append(social_mean_param[0])
        self.altruism_mean_param.append(social_mean_param[1])
        self.normal_mean_param.append(social_mean_param[2])
        self.heritage.append(population.heritage)
        self.different_heritage.append(len(set(population.heritage)))
        self.t += 1
    
    def report(self):
        pdf = PDFReport(self.file_path)
        # DATE TIME
        pdf.add_text(text=f"Test done {self.current_time.split(" ")[0]} at {self.current_time.split(" ")[1]}", size = 10)

        # INITIAL CONDITION - note that they are not really all the initial condition
        pdf.add_text("Initial condition", size = 9, spacing = 10)
        for cond in self.initial_condition.split("\n"):
            pdf.add_text(text=cond, size=8, spacing=10)
        
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

        # BIRTH OVER TIME PLOT
        time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.birth), "Birth", "Birth over time", filename=self.img_path+"Birth over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Birth over time.png")
        pdf.add_text(f"Mean : {np.mean(np.array(self.birth))}", size = 8, spacing = 8)
        pdf.add_text(f"Variance : {np.var(np.array(self.birth))}", size = 8, spacing = 8)
        pdf.add_text(f"Min : {np.min(np.array(self.birth))}", size = 8, spacing = 8)
        pdf.add_text(f"Max : {np.max(np.array(self.birth))}", size = 8, spacing = 8)

        # DEATH OVER TIME PLOT
        time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.death), "Death", "Death over time", filename=self.img_path+"Death over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Death over time.png")
        pdf.add_text(f"Mean : {np.mean(np.array(self.death))}", size = 8, spacing = 8)
        pdf.add_text(f"Variance : {np.var(np.array(self.death))}", size = 8, spacing = 8)
        pdf.add_text(f"Min : {np.min(np.array(self.death))}", size = 8, spacing = 8)
        pdf.add_text(f"Max : {np.max(np.array(self.death))}", size = 8, spacing = 8)
        
        # MEAN POPULATION ENERGY OVER TIME
        time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.mean_population_energy), "Mean Population Energy", "Mean Population Energy over time", filename=self.img_path+"Mean Population Energy over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Mean Population Energy over time.png")
        pdf.add_text(f"Mean : {np.mean(np.array(self.mean_population_energy))}", size = 8, spacing = 8)
        pdf.add_text(f"Variance : {np.var(np.array(self.mean_population_energy))}", size = 8, spacing = 8)

        # MEAN WORLD ENERGY OVER TIME
        time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.mean_world_energy), "Mean World Energy", "Mean World Energy over time", filename=self.img_path+"Mean World Energy over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Mean World Energy over time.png")

        # MEAN SOCIAL PARAMETERS OVER TIME
        parameters_plot(np.linspace(0, self.t, self.t), np.array(self.selfish_mean_param), np.array(self.altruism_mean_param), np.array(self.normal_mean_param), filename=self.img_path+"Mean Social Parameters over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Mean Social Parameters over time.png")

        # DIFFERENT HERITAGE COUNT OVER TIME
        time_serie_plot(np.linspace(0, self.t, self.t), np.array(self.different_heritage), "Different Heritage", "Different Heritage over time", filename=self.img_path+"Different Heritage over time.png")
        pdf.add_plot(plot_filename=self.img_path+"Different Heritage over time.png")

        # META DATA
        pdf.add_text(text="Author : Francesco Bredariol", size = 7, spacing = 7)
        pdf.add_text(text="Year : 2024/2025", size = 7, spacing = 7)
        pdf.add_text(text="This Project is done for the academic purpose of implementing the practical part of the Degree Thesis in Artificial Intelligence and Data Analytics.", size = 7, spacing = 7)
        
        pdf.save_pdf()
        print(f"Pdfcreated succesfully. You can find it at {self.file_path}")

if __name__ == "__main__":
    pass

