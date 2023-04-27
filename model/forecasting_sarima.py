import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm
def outerspace_SARIMA():
    df = pd.read_csv('sun_magnetic.csv')

    df['DateTime'] = pd.to_datetime(df['DateTime'])

    df.set_index('DateTime', inplace=True)


    dict_ = {}
    
    df = df[:150]
    for c in df.columns:
        model = SARIMAX(df[c], order=(2, 1, 2), seasonal_order=(2, 1, 2, 24),freq='12T')
        model_fit = model.fit()
        dict_[c] = model_fit

    for c in dict_.keys():
        start_index = len(df)
        end_index = start_index + 120 # 120 time steps is equivalent to 1 day according to 12T frequency

        predictions = dict_[c].predict(start=start_index, end=end_index, typ='levels')
        fig = plt.figure()
        # Plot actual and predicted values
        plt.plot(df[c], label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.xticks(rotation=30)
        plt.title(f'24 hour forecast of {c}')
        plt.legend()
        fig.savefig(f'{c}.png')
        plt.close(fig)

def ionosphere_SARIMA():

    df = pd.read_csv('ionosphere_final.csv')

    df['time_tag'] = pd.to_datetime(df['time_tag'])

    # Set DateTime as index
    df.set_index('time_tag', inplace=True)

   

    dict_ = {}
    list_ = []
    for e in df['energy']:
        t1 = e.split()
        t2 = t1[0].split('-')

        list_.append((int(t2[0])+int(t2[1]))/2)

    df = df[:150]
    for c in df.columns:
        model = SARIMAX(df[c], order=(2, 1, 2), seasonal_order=(2, 1, 2, 24),freq='5T')
        model_fit = model.fit()
        dict_[c] = model_fit

    for c in dict_.keys():
        start_index = len(df)
        end_index = start_index + 288 # 288 time steps is equivalent to 1 day according to 12T frequency

        predictions = dict_[c].predict(start=start_index, end=end_index, typ='levels')
        fig = plt.figure()
        # Plot actual and predicted values
        plt.plot(df[c], label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.xticks(rotation=30)
        plt.title(f'24 hour forecast of {c}')
        plt.legend()
        fig.savefig(f'{c}.png')
        plt.close(fig)
