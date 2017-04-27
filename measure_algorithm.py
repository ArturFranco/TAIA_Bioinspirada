##Measure performance
import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np

def graph_type(solutions):
# Data to plot
	labels = 'Mutation', 'Crossover', 'Randomly'
	sizes = [0,0,0]
	
	for i, l in enumerate(solutions):
		if l[2] == 0: #Randomly
			sizes[2] += 1
		elif l[2] == 1: #Crossover
			sizes[1] += 1
		elif l[2] == 2:
			sizes[0] += 1

	colors = ['gold', 'yellowgreen', 'lightcoral']
	explode = (0.1, 0.1, 0.1)  # explode 1st slice
 
	# Plot
	plt.pie(sizes, explode = explode, labels = labels, colors = colors, autopct = '%1.1f%%', shadow = True, startangle = 140)
	plt.suptitle('Types of solution', y = 0.99, fontsize = 17)
	plt.axis('equal')
	plt.show()

def config_individual(individual, size):
	grid = [[0]*len(individual) for n in range(len(individual))]
	nrows, ncols = size, size
	
	for i in xrange(len(grid)):
		grid[i][individual[i]] = 1

	col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

	plt.figure()
	im = plt.imshow(grid, cmap = plt.get_cmap('Greys'),
	                interpolation = 'none', vmin = 0, vmax = 1,  aspect ='equal');
	ax = plt.gca();
	ax = plt.gca();

	# Major ticks
	ax.set_xticks(np.arange(0, nrows, 1));
	ax.set_yticks(np.arange(0, ncols, 1));

	# Labels for major ticks
	ax.set_xticklabels(col_labels);
	ax.set_yticklabels(np.arange(1, nrows+1, 1));

	# Minor ticks
	ax.set_xticks(np.arange(-.5, ncols, 1), minor=True);
	ax.set_yticks(np.arange(-.5, nrows, 1), minor=True);

	# Gridlines based on minor ticks
	ax.grid(which = 'minor', color = 'black', linestyle = '--', linewidth = 1)
	subtitle_string = (" ".join(str(x) for x in individual))
	plt.suptitle("Best Individual", y = 0.99, fontsize = 17)
	plt.title(subtitle_string, fontsize = 8)
	plt.show()

def evolution_population(solutions, _halts):
	x = range(len(solutions))
	y = []

	for i, l in enumerate(solutions):
		y.append(l[0])

	plt.plot(x, y, 'bo', linewidth = 2)
	plt.title("Convergence")
	plt.ylabel("Iterations")
	plt.xlabel("Individuals")
	plt.axis([0, len(solutions), 0, _halts])
	plt.show()

def plot_fitness(mean, title):
	plt.plot(range(len(mean)), mean, 'r-', linewidth = 2)
	plt.ylabel('Fitness')
	plt.xlabel("Iteration")
	plt.yticks([min(mean), max(mean)])
	plt.title(title)
	plt.show()

# if __name__ == '__main__':
	# config_individual([5,2,4,7,0,3,1,6])