import pandas as pd
import numpy as np

data = {
    'company_size': np.random.choice(['small', 'medium', 'large'], size=100),
    'industry': np.random.choice(['tech', 'finance', 'healthcare'], size=100),
    'email_opens': np.random.randint(0, 10, 100),
    'website_visits': np.random.randint(0, 20, 100),
    'converted': np.random.choice([0, 1], 100, p=[0.7, 0.3])
}

df = pd.DataFrame(data)
df.to_csv('data/mock_data.csv', index=False)