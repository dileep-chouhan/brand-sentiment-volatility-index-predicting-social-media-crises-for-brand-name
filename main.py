import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
dates = pd.date_range(start='2023-01-01', periods=365)
brand_sentiment = np.random.normal(loc=0, scale=1, size=365) # Normally distributed sentiment
brand_sentiment += np.sin(np.linspace(0, 2*np.pi, 365)) # Add seasonality
brand_sentiment += np.random.normal(loc=0, scale=0.5, size=365) # Add noise
# Simulate a crisis event
brand_sentiment[200:210] -= 5 # Negative spike in sentiment
# Introduce some positive events
brand_sentiment[100:105] += 3
brand_sentiment[300:305] += 2
df = pd.DataFrame({'Date': dates, 'Sentiment': brand_sentiment})
# --- 2. Data Cleaning & Feature Engineering ---
# No significant cleaning needed for synthetic data, but in real-world scenarios, this would be crucial.
df['Rolling_Mean'] = df['Sentiment'].rolling(window=7).mean() # 7-day rolling average
df['Volatility'] = df['Sentiment'].rolling(window=7).std() # 7-day rolling standard deviation
# --- 3. Analysis ---
# Identify periods of high volatility (potential crises)
high_volatility_threshold = df['Volatility'].mean() + df['Volatility'].std()
high_volatility_days = df[df['Volatility'] > high_volatility_threshold]
# --- 4. Visualization ---
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Sentiment'], label='Daily Sentiment')
plt.plot(df['Date'], df['Rolling_Mean'], label='7-Day Rolling Mean')
plt.plot(df['Date'], df['Volatility'], label='7-Day Rolling Volatility')
plt.axhline(y=high_volatility_threshold, color='r', linestyle='--', label=f'High Volatility Threshold')
plt.scatter(high_volatility_days['Date'], high_volatility_days['Sentiment'], color='red', label='High Volatility Periods')
plt.xlabel('Date')
plt.ylabel('Sentiment Score')
plt.title('Brand Sentiment Volatility Index')
plt.legend()
plt.grid(True)
plt.tight_layout()
output_filename = 'brand_sentiment_volatility.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")
# --- 5. Density Plot for Volatility ---
plt.figure(figsize=(8, 6))
kde = gaussian_kde(df['Volatility'].dropna()) #Handle potential NaN values from rolling calculations
x_grid = np.linspace(df['Volatility'].min(), df['Volatility'].max(), 100)
plt.plot(x_grid, kde(x_grid))
plt.xlabel('Volatility')
plt.ylabel('Density')
plt.title('Density Plot of Sentiment Volatility')
plt.grid(True)
plt.tight_layout()
output_filename2 = 'volatility_density.png'
plt.savefig(output_filename2)
print(f"Plot saved to {output_filename2}")