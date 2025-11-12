import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/england_prices_wages.pkl")
cols = ["Barley (bushel)", "Cheese (lb.)", "Wage, farm (day)", "Wage, craft (day)"]
df[cols].plot(logy=True)
plt.show()
