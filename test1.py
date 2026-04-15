import pandas as pd

df = pd.read_csv("data/raw/sample_data.csv")
api = pd.read_csv("data/raw/api_products.csv")

print(df.shape, api.shape)