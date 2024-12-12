import math
import csv
import pandas as pd
from matplotlib import pyplot as plt
import scipy.io as sio
from config import WORKLOADS_FOLDER_PATH, IMAGES_FOLDER_PATH


def save_data_to_csv(data, filename):
    """Save the data in a .csv file in the WORKLOADS_FOLDER_PATH.
    """
    with open(f"{WORKLOADS_FOLDER_PATH}/{filename}.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)



def plot_workload_png(filename):
    """Save a simple plot for filename.csv in a filename.png file.

    :param filename:    The input .csv file to plot (without .csv extension).
    """
    data = pd.read_csv(f"{WORKLOADS_FOLDER_PATH}/{filename}.csv")
    plt.plot(data)
    plt.title(filename)
    plt.savefig(f"{IMAGES_FOLDER_PATH}/{filename}.png")
    plt.close()


def convert_mat_to_csv(mat_path, csv_path, index):
    """Convert a .mat file into a .csv file.

    :param mat_path:    The path to the input .mat file.
    :param csv_path:    The path to the output .csv file.
    :param index:       The index of the column of the .mat file to convert.
    """
    data = sio.loadmat(mat_path)
    data_to_convert = data[index].T

    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data_to_convert)


def generate_sin_csv(min_value, max_value, phase_shift, period, num_entries, filename):
    """Generate a workload csv file of a sin (values stored are rounded to the closest integer).

    :param min_value:   The minimum value of the sin function.
    :param max_value:   The maximum value of the sin function.
    :param phase_shift: The phase shift of the sin function.
    :param period:      The period of the sin function.
    :param num_entries: The number of samples in the sin function.
    :param filename:    The output filename (without .csv extension)
    """
    amplitude = (max_value - min_value) / 2
    vertical_shift = min_value + amplitude
    frequency = num_entries / period

    data = []

    # Generate data points for the sin wave
    for i in range(num_entries):
        x = i / (num_entries - 1)  # Normalize x-axis values between 0 and 1
        y = amplitude * math.sin(2 * math.pi * frequency * x + phase_shift) + vertical_shift
        data.append([int(y)])  # Store x and y values in a list
    save_data_to_csv(data, filename)


def generate_step_function(value1, value2, value3, value4, duration, filename):
    """generate_step_function.

    :param value1:
    :param value2:
    :param value3:
    :param value4:
    :param duration:
    :param filename:
    """
    data = []
    for i in range(duration):
        if i < duration / 4:
            data.append([int(value1)])
        elif duration / 4 <= i < duration / 2:
            data.append([int(value2)])
        elif duration / 2 <= i < 3 * duration / 4:
            data.append([int(value3)])
        else:
            data.append([int(value4)])
    save_data_to_csv(data, filename)
    # with open(f"./{filename}", 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerows(data)  # Write data points


def set_mid_value(filename, value, start, end):
    """
    This function opens a csv file containing one column,
    replaces lines 'start' - 'end' with 'value', and overwrites the file.

    Args:
        filename: Path to the csv file.
        value: The value to replace lines with.
        start: The starting line index (0-based).
        end: The ending line index (0-based).
    """

    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if start <= count <= end:
                data.append([int(value)])
            else:
                data.append([int(row[0])])
            count += 1
            print(row)

    with open(f"./{filename}", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)  # Write data points



generate_sin_csv(10, 80, 0, 200, 2000, 'sin200_2')

generate_step_function(10, 30, 15, 5, 200, 'step3')

plot_workload_png('sin200_2')
plot_workload_png('step3')

# generate_sin('sin_80-10_p200_tot2000.csv', 10, 80, 0, 200, 2000)

# file1 = 'sin_p400.csv'
# generate_sin(file1, 10, 80, 0, 400, 2000)
# plot_workload(file1)

# file2 = 'sin_p800.csv'
# generate_sin(file2, 10, 80, 0, 800, 2000)
# plot_workload(file2)

# file = 'sin200.csv'
# generate_sin(file, 10, 80, 300, 200, 200)
# plot_workload(file)

# filename = 'twitter.csv'
# convert_mat_to_csv('./twitter_new.mat', filename, 'tweets')
# plot_workload(filename)

# filename = 'step.csv'
# generate_step_function(10, 100, 40, 70, 3600, filename)
# plot_workload(filename)


#generate_step_function(10, 40, 100, 70, 3600, filename)
