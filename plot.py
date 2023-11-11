import matplotlib.pyplot as plt
import numpy as np

# Read data from the file
data = np.loadtxt('output.txt')

# Assuming data has three columns
a = data[:, 0]
b = data[:, 1]
c = data[:, 2]

# Create a new array for the combined values of (b + c)
b_plus_c = b + c

# Plotting a vs (b + c) with a smooth curve
plt.plot(a, b_plus_c, label='a vs (b + c)')
plt.title('a vs (b + c)')
plt.xlabel('a')
plt.ylabel('b + c')
plt.legend()

# Show the plot
plt.show()
