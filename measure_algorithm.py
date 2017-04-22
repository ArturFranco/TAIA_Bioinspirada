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

def config_individual(individual):
	grid = [[0]*len(individual) for n in range(len(individual))]
	nrows, ncols = 8,8
	
	for i in xrange(len(grid)):
		grid[i][individual[i]] = 1

	row_labels = range(nrows)
	col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	plt.matshow(grid, cmap = plt.get_cmap('Greys'), interpolation = 'none')
	plt.xticks(range(ncols), col_labels)
	plt.yticks(range(nrows), row_labels)
	subtitle_string = (" ".join(str(x) for x in individual))
	plt.suptitle("Best Individual", y = 0.99, fontsize = 17)
	plt.title(subtitle_string, fontsize = 8)
	plt.show()

def evolution_population(solutions, _halts):
	print len(solutions)

	x = range(len(solutions))
	y = []

	for i, l in enumerate(solutions):
		y.append(l[0])

	plt.plot(x, y, 'ro')
	plt.axis([0, len(solutions), 0, _halts])
	plt.show()

def no_solutions(population, solutions):
	no_solutions = []

	if len(solutions) == 0:
		return population

	else:	
		for i, sol in enumerate(population):
			for j, pop in enumerate(population):
				if pop[0] is not sol[1]:
					no_solutions.append(pop[0])

	return no_solutions

def plot_fitness(fitness, title):
	x = []

	for i, l in enumerate(fitness):
		# print l[1], "f"
		x.append(l[1])

	plt.plot(x)
	plt.ylabel('Fitness')
	plt.xlim((0,len(fitness)))
	plt.ylim((0,1.5))
	plt.title(title)
	plt.show()

# if __name__ == '__main__':
	# graph_config_individual([5,2,4,7,0,3,1,6])