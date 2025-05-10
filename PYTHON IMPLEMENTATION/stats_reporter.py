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
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
from datetime import datetime
import seaborn as sns
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
        """Given a plot image insert it into the PDF"""
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

def time_serie_plot(time, mean, median, q1, q3, X_label, Y_label, title, img_path, filename, figsize =(10, 5), evidence_mean = True):

    plt.figure(figsize = figsize)
    plt.plot(time, mean, label="mean", color='blue')
    plt.plot(time, median, label="median", color="orange", linestyle="--")
    if evidence_mean:
        mean_value = np.mean(mean)
        plt.axhline(y=mean_value, color='red', linestyle='--', label=f'Mean of mean: {mean_value:.2f}')
    plt.fill_between(time, q1, q3, color = "blue", alpha = 0.2, label='Interquartile Range (Q1–Q3)')
    
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(title)
    plt.legend()

    plt.savefig(img_path+filename+".png")
    plt.close()

def single_simulation_plot(time, data, X_label, Y_label, title, img_path, filename, figsize =(10, 5), evidence_mean = True):
    plt.figure(figsize = figsize)
    plt.plot(time, data, label="mean", color='blue')
    if evidence_mean:
        mean_value = np.mean(data)
        plt.axhline(y=mean_value, color='red', linestyle='--', label=f'Mean of mean: {mean_value:.2f}')
    
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(img_path + filename +".png") 
    plt.close()

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

def time_series_data_analysis(data, time, X_label, Y_label, title, filename, img_path, pdf, max_len, single_simulation = False):
                if single_simulation:
                    data = np.array(data)
                    single_simulation_plot(time, data, X_label, Y_label, title, img_path, filename)
                    means = np.mean(data)
                else:
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

    def __init__(self, initial_condition,  n_simulation, file_path = "REPORT/", folder_name_mode = 'Date_Time', time_window = 10):
        
        self.current_time = get_current_datetime()
        if folder_name_mode == 'Date_Time': # Date time name
            self.folder_name = self.current_time
        else: # folder_name_mode == 'Console': # Console input
            self.folder_name = input("Insert the name for the folder where to save the report: ")
        
        self.root = file_path + self.folder_name

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

            n = population.alive() if population.alive() > 0 else 1
            self.selfish_mean_param[s].append(social_mean_param.count("S")/n)
            self.altruism_mean_param[s].append(social_mean_param.count("A")/n)
            self.normal_mean_param[s].append(social_mean_param.count("N")/n)

            self.heritage[s].append(population.heritage)
            self.different_heritage[s].append(len(set(population.heritage)))
            self.mean_population_age[s].append(population.mean_age)
            p = [[1 if p else 0 for p in w_p] for w_p in world.get_position()]
            self.positions[s].append(p)
    
    def report(self, simulation_number, forced_end = False):

        self.horizons[simulation_number] = self.t
        self.windows_horizons[simulation_number] = self.t//self.time_window

        # Create the folder for the single simulation
        folder = f"{self.root}/simulation {simulation_number}"
        os.makedirs(folder, exist_ok=True)

        print("Processing stats for the current simulation. Please wait a few moments...")

        time = np.linspace(0, self.windows_horizons[simulation_number]-1, self.windows_horizons[simulation_number])

        pdf = PDFReport(folder+f"/stats report {simulation_number}.pdf")

        pdf.add_text(text=f"Simulation number {simulation_number}", size = 10)
        pdf.add_text(text=f"Test done {self.current_time.split(" ")[0]} at {self.current_time.split(" ")[1]}", size = 10)
        pdf.add_text(text=f"Horizon reached {self.t}", size = 10)

        time_series_data_analysis(self.alive_population[simulation_number], time, "Time", "Population", "Population over time", f"Population Over Time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        time_series_data_analysis(self.alive_cell[simulation_number], time, "Time", "Cells", "Cells over time", f"Cell Over Time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        time_series_data_analysis(self.mean_population_energy[simulation_number], time, "Time", "Mean Population Energy", "Mean Population Energy Over Time", f"Mean Population Energy Over Time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        time_series_data_analysis(self.mean_population_age[simulation_number], time, "Time", "Mean Population Age", "Mean Population Age Over Time", f"Mean Population Age Over Time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        time_series_data_analysis(self.mean_world_energy[simulation_number], time, "Time", "Mean World Energy", "Mean World Energy over time", f"World Energy over time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        time_series_data_analysis(self.different_heritage[simulation_number], time, "Time", "Different Heritage", "Different Heritage over time", f"Heritage over time {simulation_number}", folder + "/", pdf, time, single_simulation=True)
        parameters_plot(time, self.selfish_mean_param[simulation_number], self.altruism_mean_param[simulation_number], self.normal_mean_param[simulation_number], f"{folder}/Social Parameters Over Time {simulation_number}.png")
        pdf.add_plot(f"{folder}/Social Parameters Over Time {simulation_number}.png")

        data = self.positions[simulation_number]

        indexes = [0]
        for t in [0.25, 0.5, 0.75, 1]:
            indexes.append(min(int(self.t//self.time_window*(t)), self.t//self.time_window-1))


        for t in range (5):
            index = indexes[t]
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.heatmap(data[index], cbar=True, ax=ax)
            ax.set_title(f"Time = {t/4}")
            plt.savefig(folder + "/" + f"Spatial Distribution At time {t/4} _ {simulation_number}.png")
            pdf.add_plot(folder + "/" + f"Spatial Distribution At time {t/4} _ {simulation_number}.png")
            plt.close()

        pdf.save_pdf()
        print(f"PDF for the simulation number {simulation_number} is ready and readable at {folder}")

        if simulation_number == (self.n_simulation - 1) or forced_end:

            print("Processing all the stats. Please wait a few moments...")

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
            
            # CELL OVER TIME PLOT
            time_series_data_analysis(self.alive_cell, time, "Time", "Energy Cells", "Average Energy Cells over time", "EC over time", self.img_path, pdf, max_len)

            # MEAN POPULATION ENERGY OVER TIME
            time_series_data_analysis(self.mean_population_energy, time, "Time", "Mean Population Energy", "Average Mean Population Energy over time", "AVG Pop Energy over time", self.img_path, pdf, max_len)
            
            # MEAN POPULATION AGE OVER TIME
            time_series_data_analysis(self.mean_population_age, time, "Time", "Mean Population Age", "Average Mean Population Age over time", "AVG Pop Age over time", self.img_path, pdf, max_len)
            
            # MEAN WORLD ENERGY OVER TIME
            time_series_data_analysis(self.mean_world_energy, time, "Time", "Mean World Energy", "Average Mean World Energy over time", "AVG World Energy over time", self.img_path, pdf, max_len)

            # HERITAGE
            time_series_data_analysis(self.different_heritage, time, "Time", "Different Heritage", "Average Different Heritage over time", "Heritage over time", self.img_path, pdf, max_len)
            
            # SELFHISHNESS
            time_series_data_analysis(self.selfish_mean_param, time, "Time", "Selfishness", "Average Selfishness over time", "Selfishness over time", self.img_path, pdf, max_len)

            # ALTRUISM 
            time_series_data_analysis(self.altruism_mean_param, time, "Time", "Altruism", "Average Altruism over time", "Altruism over time", self.img_path, pdf, max_len)

            # NORMALITY
            time_series_data_analysis(self.normal_mean_param, time, "Time", "Normality", "Average Normality over time", "Normlaity over time", self.img_path, pdf, max_len)

            # SPATIAL DISTRIBUTION DENSITY
            a = self.positions

            matrix_shape = (len(a[0][0]), len(a[0][0][0]))
            for sublist in a:
                while len(sublist) < max_len:
                    sublist.append([[0] * matrix_shape[1] for _ in range(matrix_shape[0])])
            data = np.sum(a, axis = 0, dtype=float)
            for i, m in enumerate(data):
                data[i] = data[i]/np.sum(m)

            pdf.add_text("Spatial Distribution Density Heatmap", size = 8, spacing = 8)
            # 5 POINTS (T = 0, T = 0.25, T = 0.5, T=0.75, T = 1) where T is t/max_len

            indexes = [0]
        for t in [0.25, 0.5, 0.75, 1]:
            indexes.append(min(int(max_len*t), max_len - 1))

            for t in range (5):
                index = indexes[t]
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(data[index], cbar=True, ax=ax)
                ax.set_title(f"Time = {t/4}")
                plt.savefig(self.img_path + f"Spatial Distribution At time {t/4}.png")
                pdf.add_plot(self.img_path + f"Spatial Distribution At time {t/4}.png")
                plt.close()

            # GIF 
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.heatmap(data[0], cbar=True, ax=ax)
            ax.set_title("Time = 0")
            def update(frame):
                ax.clear()
                sns.heatmap(data[frame], cbar=False, ax=ax)
                ax.set_title(f"Time = {frame}")
            ani = FuncAnimation(fig, update, frames=range(max_len), interval=300)
            ani.save(self.img_path + "Spatial Distribution Over Time.gif", writer=PillowWriter(fps=3))
            plt.close()

            # META DATA
            pdf.add_text(text="Author : Francesco Bredariol", size = 7, spacing = 7)
            pdf.add_text(text="Year : 2024/2025", size = 7, spacing = 7)
            pdf.add_text(text="This Project is done for the academic purpose of implementing the practical part of the Degree Thesis in Artificial Intelligence and Data Analytics.", size = 7, spacing = 7)
            
            pdf.save_pdf()
            print(f"Pdfcreated succesfully. You can find it at {self.file_path}")

        self.t = 0

if __name__ == "__main__":
    pass

    






