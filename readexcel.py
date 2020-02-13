import pandas as pd

data = pd.ExcelFile('./FOB.xlsx')
print(data)
print(data.sheet_names)
df = data.parse(data.sheet_names[0])
print(df)