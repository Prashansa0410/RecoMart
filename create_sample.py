import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample e-commerce data matching Kaggle dataset structure
np.random.seed(42)

n_rows = 30000
print(f"Generating {n_rows} sample rows...")

# Generate dates
base_date = datetime(2019, 10, 1)
dates = [base_date + timedelta(hours=int(x)) for x in np.random.uniform(0, 744, n_rows)]

# Create data
data = {
    'event_time': dates,
    'event_type': np.random.choice(['view', 'cart', 'purchase'], n_rows, p=[0.6, 0.3, 0.1]),
    'product_id': np.random.randint(1, 21, n_rows),
    'user_id': np.random.randint(1, 5001, n_rows),
    'price': np.random.uniform(10, 300, n_rows).round(2),
    'category': np.random.choice(['Electronics', 'Books', 'Clothing', 'Home'], n_rows),
}

df = pd.DataFrame(data)
df.to_csv('2019-Oct.csv', index=False)
print('[OK] Sample CSV created successfully: {} rows'.format(len(df)))
print('Columns: {}'.format(list(df.columns)))
print('File: 2019-Oct.csv')
print('File size: {:.2f} KB'.format(df.memory_usage(deep=True).sum() / 1024))
