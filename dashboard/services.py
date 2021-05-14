import requests
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 20, 10


def my_historical_prices_api(from_time, to_time, interval, market, fiat):
    if to_time == "now":
        to_timestamp = str(round(datetime.timestamp(datetime.now()))) + "000"
    else:
        to_timestamp = str(round(datetime.timestamp(datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")))) + "000"
    from_timestamp = str(round(datetime.timestamp(datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")))) + "000"

    url = f"https://api.bitbay.net/rest/trading/candle/history/{market}-{fiat}/{interval}?from={from_timestamp}&to={to_timestamp}"
    response = requests.request("GET", url)

    historical_prices = []
    for item in response.json()['items']:
        historical_prices.append([datetime.fromtimestamp(int(item[0][0:10])), item[1]['o'], item[1]['c'], item[1]['v']])

    return historical_prices


# --- PREDICTING MODEL ---
def predict_prices():
    from keras.models import Sequential
    from keras.layers import LSTM, Dropout, Dense
    # creating data
    bitcoin_data = my_historical_prices_api('2016-01-01 00:00:00', 'now', 86400, 'BTC', 'PLN')
    date_array = [x[0] for x in bitcoin_data]
    close_prices = [y[2] for y in bitcoin_data]
    data = {'Date': date_array, 'Prices': close_prices}
    df = pd.DataFrame(data, columns=['Date', 'Prices'])
    # df = df.astype({"Prices": float})
    # df.index = df['Date']
    # # plt.plot(df["Prices"], label='Close Price history')
    # # plt.show()

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Prices'].values.reshape(-1, 1))

    prediction_days = 60

    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # create neural network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    # testing data
    test_bitcoin_data = my_historical_prices_api('2020-01-01 00:00:00', 'now', 86400, 'BTC', 'PLN')
    test_date_array = [x[0] for x in test_bitcoin_data]
    test_close_prices = [y[2] for y in test_bitcoin_data]
    test_data = {'Date': test_date_array, 'Prices': test_close_prices}
    test_df = pd.DataFrame(test_data, columns=['Date', 'Prices'])
    actual_prices = test_df['Prices'].values

    total_dataset = pd.concat((df['Prices'], test_df['Prices']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_df) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.fit_transform(model_inputs)

    x_test = []

    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x - prediction_days:x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)

    plt.plot(actual_prices, color='black', label='Actual prices')
    plt.plot(prediction_prices, color='green', label='Predicted prices')
    plt.title('Prediction BTC')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.show()

    # predict next day
    real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs) + 1, 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    return prediction[0]