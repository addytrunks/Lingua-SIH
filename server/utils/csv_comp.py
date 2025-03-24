import pandas as pd

df = pd.read_csv('final_coordinates.csv')

df['word'] = df['word'].str.lower()

df.to_csv('final_coordinates.csv', index=False)
