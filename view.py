import pandas as pd
from pandas.core.series import Series
import matplotlib.pyplot as plt
import numpy as np


def basket_cost(row: Series, ratios: dict[str, float]) -> float:
    return np.sum([row[k] * v for k, v in ratios.items()])


basket_ratios = {
    "Barley (bushel)": 1.0,
    "Cheese (lb.)": 0.7,
    # "Cider (gallon)": 0.5,
    "Oats (bushel)": 0.7,
    "Peas (bushel)": 0.8
}

if __name__ == "__main__":
    df = pd.read_pickle("data/england_prices_wages.pkl")
    cols = [
        "Barley (bushel)",
        "Cheese (lb.)",
        "Cider (gallon)",
        "Linen cloth (yard)",
        "Oats (bushel)",
        "Peas (bushel)",
        "Wage, farm (day)",
        "Wage, craft (day)",
        ]

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

    df[[
        "Real wage, craft",
        "Real wage, farm",
    ]].plot(ax=axs[1], logy=True)
    
    fig.suptitle("Historical wages and prices in England")

    with open("data/england_population.csv", "r") as f:
        pop = pd.read_csv(f, delimiter="\t", skiprows=1, names=["Year", "Population (mio.)"])
    fig, ax = plt.subplots()
    # pop.plot(ax=ax, logy=True)
    c = pd.concat([df, pop.set_index("Year")], axis="columns")
    c[[
        "Wage, craft (day)",
        "Wage, farm (day)",
        "Basket (a.u.)",
        "Population (mio.)",
    ]].plot(ax=ax, logy=True)
    plt.show()
    # plt.savefig("england-wages.png")
