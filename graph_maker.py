import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

IMAGE_FILE_NAME = 'gain_evolution.png'

def make_graph(summed_gains: list[float]):
    ''' Writes the evolution graph with matplotlib.
        Saves the file my_plot.png '''
    # smooth the curve helped with 
    # https://www.geeksforgeeks.org/how-to-plot-a-smooth-curve-in-matplotlib/
    if len(summed_gains) >= 4:
        x = np.array([i for i in range(len(summed_gains))])
        y = np.array(summed_gains)

        x_y_spline = make_interp_spline(x, y)

        x_ = np.linspace(x.min(), x.max(), 500)
        y_ = x_y_spline(x_)
    else:
        x_, y_ = [i for i in range(len(summed_gains))], summed_gains

    plt.plot(x_, y_)
    plt.xlabel('Day')
    plt.ylabel('gains')
    
    ax = plt.gca()

    ax.axes.xaxis.set_ticks([])
    # ax.axes.xaxis.set_visible(False)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    # ax.plot(1, 0, '>k', transform=ax.get_yaxis_transform(), clip_on=False)
    plt.savefig(IMAGE_FILE_NAME)
    plt.close()