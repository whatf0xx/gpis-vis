import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from collections import deque
from view import basket_cost


def n_point_smooth(xs: np.ndarray, n: int) -> np.ndarray:
    d = deque(maxlen=n)
    initial_list = []
    ys = np.zeros_like(xs)
    average_over = n
    for i in range(n):
        d.appendleft(xs[i])
        initial_list.append(xs[i])
        av = [x for x in d if not np.isnan(x)]
        ys[i] = np.mean(av)

    for i in np.arange(start=n, stop=len(xs)):
        d.appendleft(xs[i])
        av = [x for x in d if not np.isnan(x)]
        ys[i] = np.mean(av)
        d.pop()

    return ys

pop = pd.read_csv(
    "data/england_population.csv",
    delimiter="\t",
    skiprows=1,
    names=["Year", "Population (mio.)"]).set_index("Year")
years, log_pop = pop.index, np.log(pop["Population (mio.)"].values)
zero_years = years - 1085

pop_trend = Polynomial.fit(zero_years, log_pop, deg=1).convert()

fig, ax = plt.subplots()
pop["Population (mio.)"].plot(ax=ax, logy=True, color="green", linestyle="dotted")
ax.plot(years, np.exp(pop_trend(zero_years)), label="Population trend")
ax.set_title("Historic trends in English population")
ax.set_ylabel("English population (mio.)")
ax.set_xlabel("Year")
ax.legend()

detrended_pop = pop["Population (mio.)"] / np.exp(pop_trend(zero_years))

df = pd.read_pickle("data/england_prices_wages.pkl")

basket_ratios = {
    "Barley (bushel)": 1.0,
    "Cheese (lb.)": 0.7,
    # "Cider (gallon)": 0.5,
    "Oats (bushel)": 0.7,
    "Peas (bushel)": 0.8
}

df["Basket (a.u.)"] = df.apply(lambda x: basket_cost(x, basket_ratios), axis=1)

# wages.plot(logy=True)
fig, axs = plt.subplots(nrows=1, ncols=2, layout="constrained")

df[[
    "Wage, craft (day)",
    "Wage, farm (day)",
    "Basket (a.u.)",
]].plot(ax=axs[0], logy=True)

df["Real wage, farm"] = df["Wage, farm (day)"] / df["Basket (a.u.)"]
df["Real wage, craft"] = df["Wage, craft (day)"] / df["Basket (a.u.)"]

n = 20
smooth_craft = n_point_smooth(df["Real wage, craft"].to_numpy(), n)
smooth_farm = n_point_smooth(df["Real wage, farm"].to_numpy(), n)
df[[
    "Real wage, craft",
    "Real wage, farm",
]].plot(ax=axs[1], logy=True, alpha=0.3)
axs[1].plot(df.index, smooth_craft, color="green")
axs[1].plot(df.index, smooth_farm, color="orange")
axs[1].plot(years, detrended_pop, color="gray", label="Detrended population")
    
ymin, ymax = axs[1].get_ylim()
axs[1].vlines(1348, ymin, ymax, linestyle="dotted", label="Black Death arrives in England (1348)")
axs[1].vlines(1361, ymin, ymax, linestyle="dotted", label="Black Death outbreak (1361)")
axs[1].vlines(1369, ymin, ymax, linestyle="dotted", label="Black Death outbreak(1369)")

axs[1].legend()
fig.suptitle("Historical wages and prices in England")
plt.show()
