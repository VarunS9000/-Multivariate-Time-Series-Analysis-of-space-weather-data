from flask import Flask, render_template
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shutil


app = Flask(__name__)

global current_data
global current_col



# Perform time series decomposition
def seasonal_decompose(data):
    data_mean = np.convolve(data, np.ones(7)/7, mode='same')
    data_seasonal = data - data_mean
    data_trend = np.convolve(data, np.ones(30)/30, mode='same')
    data_residual = data_seasonal - data_trend
    return data_trend, data_seasonal, data_residual


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/outerspace/<col_name>')
def outerspace(col_name):
    global current_data
    global current_col
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT DateTime,{col_name} FROM data")
    data = c.fetchall()
    conn.close()
    data = data[:150]
    current_data = data
    current_col = col_name
    x = []
    y = []
    for d in data:
        x.append(d[0])
        y.append(d[1])

    plt.figure(figsize=(10, 8))
    plt.plot(x, y)

    plt.title(f'Time Series Plot of {col_name}')
    plt.xticks(x[::70],x[::70])
    plt.xlabel('Date-Time')
    plt.ylabel(col_name)
    plt.savefig('static/plot1.png')
    result = seasonal_decompose(np.array(y))
    
    # Plot the decomposed components

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    ax1.plot(result[0])
    ax1.set_ylabel('Trend')
    ax2.plot(result[1])
    ax2.set_ylabel('Seasonal')
    ax3.plot(result[2])
    ax3.set_ylabel('Residual')

    plt.savefig('static/plot2.png')


    return render_template('outerspace.html')

@app.route('/outerspace/projection')
def projection_out():
    global current_col
    source_path = f'static/{current_col}.png'
    destination_path = 'static/plot1.png'
    shutil.copyfile(source_path, destination_path)

    return render_template('outerspace.html')

@app.route('/ionosphere/projection')
def projection_in():
    global current_col
    x = ''
    if current_col == 'satellite':
        x = 'flux'
    else:
        x = 'energy'
    source_path = f'static/{x}.png'
    destination_path = 'static/plot1.png'
    shutil.copyfile(source_path, destination_path)

    return render_template('ionosphere.html')


@app.route('/ionosphere/<col_name>')
def ionosphere(col_name):
    global current_data
    global current_col
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT time_tag,{col_name} FROM data2")
    data = c.fetchall()
    conn.close()

    data = data[:150]
    current_data = data
    current_col = col_name
    x = []
    y = []
    for d in data:
        y.append(d[1])
        x.append(d[0])
    y_final = []
    if col_name == 'energy':

        for e in y:
            t1 = e.split()
            t2 = t1[0].split('-')

            y_final.append((int(t2[0])+int(t2[1]))/2)
    else:
        for e in y:
            y_final.append(float(e))

    if col_name =='satellite':
        col_nam = 'flux'

    plt.figure(figsize=(10, 8))
    plt.plot(x, y_final)
    plt.title(f'Time Series Plot of Electron Flux')
    plt.xticks(x[::50], x[::50])
    plt.xlabel('Date-Time')
    plt.savefig('static/plot1.png')

    result = seasonal_decompose(np.array(y_final))

    # Plot the decomposed components
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    ax1.plot(result[0])
    ax1.set_ylabel('Trend')
    ax2.plot(result[1])
    ax2.set_ylabel('Seasonal')
    ax3.plot(result[2])
    ax3.set_ylabel('Residual')
    plt.tight_layout()
    plt.savefig('static/plot2.png')


# Perform seasonal decomposition

    return render_template('ionosphere.html')
"""
@app.route('/outerspace/<time>')
def projection_space(time):
    global current_data
    global model_dict
    x = []
    y = []
    for d in current_data:
        x.append(d[0])
        y.append(d[1])
    data_ = {'Index': x, 'Value': y}
    df = pd.DataFrame(data_)
    df['Index'] = pd.to_datetime(df['Index'])

    df.set_index('Index', inplace=True)

    if current_col not in model_dict:
        model = SARIMAX(df[current_col], order=(2, 1, 2), seasonal_order=(2, 1, 2, 24))
        model_fit = model.fit()
        model_dict[current_col] = model_fit
    
    else:
        model_fit = model_dict[current_col]

    start_index = len(df)

    end_index = start_index + int(time)
    predictions = model_fit.predict(
        start=start_index, end=end_index, typ='levels')


    # Plot actual and predicted values
    plt.plot(df[current_col], label='Actual')
    plt.plot(predictions, label='Predicted')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('/static/plot1.png')

    return render_template('outerspace.html')
"""
if __name__ == '__main__':
    app.run(debug=True)
