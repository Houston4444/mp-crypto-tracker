
from operator import sub
from mpl_toolkits.axisartist.axislines import SubplotZero
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.interpolate import make_interp_spline

mpl.rcParams['lines.linewidth'] = 4
# mpl.rcParams['axes.edgecolor'] = '#00000000'


stock = {
    'bitcoin': {'buyed': 0.0, 'last_euro_value': 100.0},
    'erethum': {'buyed': 0.0, 'last_euro_value': 100.0},
    'ripple': {'buyed': 0.0, 'last_euro_value': 100.0}    
}


gains = list[float]()

def buy(money: str, quantity: float):
    if money in stock.keys():
        stock[money]['buyed'] += quantity

def count_today_gain(new_values: dict[str, float]) -> int:
    gain = 0.0
    for money, value in new_values.items():
        if money not in stock.keys():
            continue
        gain += (value - stock[money]['last_euro_value']) * stock[money]['buyed']
    return gain

def each_day(new_values: dict[str, float]):
    gains.append(count_today_gain(new_values))
    for money, value in new_values.items():
        if money in stock.keys():
            stock[money]['last_euro_value'] = value
    update_summed_gains()

def update_summed_gains():
    summed_gains = list[float]()
    for i in range(len(gains)):
        if i == 0:
            summed_gains.append(gains[i])
        else:
            summed_gains.append(gains[i] + summed_gains[-1])
    print(summed_gains)
    make_graph(summed_gains)

def make_graph(summed_gains: list[float]):
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
    plt.savefig('my_plot.png')
    plt.close()

buy('bitcoin', 50)
buy('erethum', 120)
each_day({'bitcoin': 100.0, 'erethum': 100.0})
each_day({'bitcoin': 130.0, 'erethum': 100.0})
buy('bitcoin', -30)
each_day({'bitcoin': 130.0, 'erethum': 100.0})
buy('bitcoin', 550)
each_day({'bitcoin': 132.0, 'erethum': 110.0})

