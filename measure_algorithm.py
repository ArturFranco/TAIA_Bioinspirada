##Measure performance
import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np

def evolution_population(solutions, _halts):
	x = range(len(solutions))
	plt.plot(x, solutions, 'gx', linewidth = 0.5)
	plt.title("Convergence")
	plt.ylabel("Fitness")
	plt.xlabel("Individuals")
	plt.axis([0, len(solutions), 0, _halts])
	plt.show()

def plot_mean_std(x, mean, std, best, title):
	plt.plot(x, mean,'red') # plotting t,a separately 
	plt.plot(x, std,'yellow') # plotting t,b separately
	plt.plot(x, best, 'green')
	plt.ylabel('Fitness')
	plt.xlabel("Iteration")
	plt.grid()
	plt.title(title)
	plt.show()