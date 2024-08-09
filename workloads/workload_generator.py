import math
import csv
import pandas as pd
from matplotlib import pyplot as plt
import scipy.io as sio


def convert_mat_to_csv(in_path, out_path, index):
    data = sio.loadmat(in_path)
    data_to_convert = data[index].T

    with open(out_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data_to_convert)


def generate_sin(filename, min_value, max_value, phase_shift, period, num_entries):
    amplitude = (max_value - min_value) / 2
    vertical_shift = min_value + amplitude

    frequency = num_entries / period
    data = []

    # Generate data points for the sin wave
    for i in range(num_entries):
        x = i / (num_entries - 1)  # Normalize x-axis values between 0 and 1
        y = amplitude * math.sin(2 * math.pi * frequency * x + phase_shift) + vertical_shift
        data.append([int(y)])  # Store x and y values in a list

    # Open a CSV file for writing
    with open(f"./{filename}", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)  # Write data points


def generate_step_function(value1, value2, value3, value4, duration, filename):
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
    with open(f"./{filename}", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)  # Write data points


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


def plot_workload(filename):
    data = pd.read_csv(filename)
    plt.plot(data)
    plt.title(filename)
    plt.show()


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


filename = 'step2.csv'
generate_step_function(10, 40, 100, 70, 3600, filename)
plot_workload(filename)