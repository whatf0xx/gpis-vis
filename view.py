import pandas as pd
import matplotlib.pyplot as plt

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
df[cols].plot(logy=True)
plt.title("Historical wages and prices in England")
plt.show()
# plt.savefig("england-wages.png")
