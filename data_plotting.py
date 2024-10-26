import matplotlib.pyplot as plt
import pandas as pd


def plot_rsi(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title(f"{ticker} RSI ({period})")
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_rsi_chart.png"

    plt.savefig(filename)
    print(f"График RSI сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def plot_macd(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='orange')
    plt.title(f"{ticker} MACD ({period})")
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_macd_chart.png"

    plt.savefig(filename)
    print(f"График MACD сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))

    if pd.api.types.is_datetime64_any_dtype(data.index):
        dates = data.index.to_numpy()
        plt.plot(dates, data['Close'].values, label='Close Price')
        plt.plot(dates, data['Moving_Average'].values, label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()
