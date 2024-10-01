import numpy as np
import matplotlib.pyplot as plt

def open_file():
    file_path = input('Enter filename: ')

    file = open(file_path, mode = 'r')
    raw_data = file.read()
    file.close()
    file_path = file_path.split('/')
    file_name = file_path[(len(file_path) - 1)]
    return raw_data, file_name


def plot(raw_data,file_name):
    raw_data = raw_data.split(',')
    raw_data.pop(0)

    data = []
    for data_point in raw_data:
        data.append(float(data_point))

    plt.figure(figsize=(10, 6))
    amount_of_values = len(data)
    x_label = range(0,amount_of_values)
    plt.plot(x_label, data, label='Curve', color='blue')
    plt.title(file_name)
    plt.xlabel('Datapoints')
    plt.ylabel('Amplitud [V]')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    data = open_file()
    plot(data[0],data[1])


if __name__ == "__main__":
    main()