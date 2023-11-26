import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

file_path = 'patients.xlsx'
df = pd.read_excel(file_path)

# Columns to be used for similarity comparison
columns = ['Height (cm)', 'Weight (kg)', 'fraction number', 'fraction time']

# One-hot encode the 'Cancer Type' column
df = pd.get_dummies(df, columns=['Cancer Type'])

# New user's data
new_user = pd.DataFrame([{'Height (cm)': 170, 'Weight (kg)': 70, 'fraction number': 10, 'fraction time': 15, 'Cancer Type': 'Breast'}])

# One-hot encode the new user's data
new_user = pd.get_dummies(new_user, columns=['Cancer Type'])

# Ensure that both DataFrames have the same columns, fill missing with 0s
df, new_user = df.align(new_user, join='outer', axis=1, fill_value=0)

# Exclude 'Cancer Type' from the columns for scaling
scale_columns = columns + [col for col in df.columns if 'Cancer Type' in col]

# Normalize the numerical data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[scale_columns])
new_user_scaled = scaler.transform(new_user[scale_columns])

# Calculate Euclidean distances
distances = euclidean_distances(df_scaled, new_user_scaled)

# Find the index of the smallest distance
min_index = distances.argmin()

# Retrieve the most similar patient's data
most_similar_patient = df.iloc[min_index]
print(most_similar_patient)
