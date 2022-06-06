import fbprophet
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['figure.figsize'] = [20, 10]
df = pd.read_csv('data/Processed_D202.csv')
df.head(10)
df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
df_copy = df.set_index('ds')

df_copy.plot(kind='line', 
                        xlabel='Datetime', 
                        ylabel='Energy Consumption (KWh)', 
                        )

plt.title('Household Energy Consumption over Time', fontweight='bold', fontsize=20)

energy_prophet = fbprophet.Prophet(changepoint_prior_scale=0.0005)
energy_prophet.fit(df)

# generate dataframe for prediction
energy_forecast = energy_prophet.make_future_dataframe(periods=365, freq='D')
# Make predictions
energy_forecast = energy_prophet.predict(energy_forecast)

# Plot predictions
energy_prophet.plot(energy_forecast, xlabel = 'Date', ylabel = 'Energy Usage (KWh)') # 0.0005
plt.title('Household Energy Usage')

energy_prophet.plot(energy_forecast, xlabel = 'Date', ylabel = 'Energy Usage (KWh)') # 0.005
plt.title('Household Energy Usage')

plt.show()