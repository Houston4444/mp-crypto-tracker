import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import make_interp_spline
import threading

IMAGE_FILE_NAME = 'static/gain_evolution.png'

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

    PLOT_STYLE = {
        'axes.facecolor': 'black',
        'axes.edgecolor': 'white',
        'axes.labelcolor': 'white',
        'figure.facecolor': 'black',
        'ytick.color': 'white',
        'ytick.labelcolor': 'white'
    }

    for key, value in PLOT_STYLE.items():
        mpl.rcParams[key] = value
    
    plt.plot(x_, y_, color="#1fc36c")
    plt.xlabel('date')
    ax = plt.gca()

    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.axes.xaxis.set_label_coords(0.97, 0.48)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.savefig(IMAGE_FILE_NAME)
    plt.close()
    

if __name__ == '__main__':
    # quick testing
    make_graph([465.0, 487.0, 9502.41, 6873.51, -10.05, 456.0])