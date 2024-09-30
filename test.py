import meas_frequency_extra

file = open('Testdata.csv', mode = 'r')

data = file.read()

file.close()

data = data.split(',')

fixed_data = []
for i in data:
    fixed_data.append(float(i))

meas_frequency_extra.plot(fixed_data)