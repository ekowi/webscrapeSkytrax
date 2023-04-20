import pandas as pd

data = pd.read_csv('reviews.csv', on_bad_lines='skip', sep='|')
df = data["Ratings"]
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
print(data.columns)