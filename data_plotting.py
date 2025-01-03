"""
Данный модуль отвечает за визуализацию данных.
Он содержит функции для создания и сохранения графиков цен закрытия и скользящих средних
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go

# Путь к папке для сохранения изображений
images_dir = "images"

# Создаем папку, если она не существует
os.makedirs(images_dir, exist_ok=True)


def plot_rsi(data, ticker, period, filename=None, style='default'):
    """
    Функция для построения графика RSI (индекс относительной силы):
    plt.figure: устанавливает размер графика;
    plt.plot: непосредственное построение графика RSI;
    plt.axhline: горизонтальные линии на уровнях 70 (перекупленность) и 30 (перепроданность);
    plt.title: устанавливаем заголовок графика;
    plt.xlabel и plt.ylabel: подписи соответственно оси Х и оси Y;
    plt.legend: отображает легенду.

    Визуализация графика:
    plt.savefig: сохранение графика в файл
    plt.show: отображение графика на экране
    """
    plt.style.use(style)
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title(f"{ticker} RSI ({period})")
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    if filename is None:
        # Присваиваем имя файла по умолчанию
        filename = f"{ticker}_{period}_rsi_chart.png"

    # Объединяем путь к папке и имя файла
    filepath = os.path.join(images_dir, filename)

    plt.savefig(filepath)
    print(f"График RSI сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def plot_macd(data, ticker, period, filename=None, style='default'):
    """
    Функция для построения графика MACD (схождения и расхождения скользящих средних).
    Описание аналогично функции для построения графика RSI.
    Отличие состоит в том, что строится одна сигнальная линия, а не две (как было в RSI).
    """
    plt.style.use(style)
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='orange')
    plt.title(f"{ticker} MACD ({period})")
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_macd_chart.png"

    filepath = os.path.join(images_dir, filename)

    plt.savefig(filepath)
    print(f"График MACD сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def plot_standard_deviation(data, ticker, period, std_dev, filename=None, style='default'):
    """
    Функция для построения графика стандартного отклонения:
    """
    plt.style.use(style)
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.axhline(std_dev, color='red', linestyle='--', label=f'Standard Deviation: {std_dev:.2f}')
    plt.title(f"{ticker} Цена акций и стандартное отклонение ({period})")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_std_dev_chart.png"

    filepath = os.path.join(images_dir, filename)

    plt.savefig(filepath)
    print(f"График стандартного отклонения сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Функция для создания и сохранения графика цен акций и скользящей средней:
    dates: преобразовывает даты в массив numpy;
    plt.plot: для построения графика цены закрытия (Close) и графика скользящей средней (Moving_Average);
    style: пользователь может выбирать стиль оформления графика. Если введённый стиль не поддерживается,
    будет использоваться стиль по умолчанию...
    Все остальное реализовано по аналогии с двумя предыдущими функциями.
    """
    plt.style.use(style)
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
    filepath = os.path.join(images_dir, filename)

    plt.savefig(filepath)
    print(f"График сохранен как {filename}")
    print("Закройте график для продолжения...")
    plt.show()


def plot_interactive_stock_data(data, ticker, period):
    """
    Функция для построения интерактивного графика цен акций с использованием Plotly.
    data: DataFrame с данными о ценах акций.
    ticker: тикер акции, например, 'AAPL'
    period: период времени для данных
    fig.add_trace: линии для цен закрытия 'Close' и для скользящего среднего 'Moving_Average', если она присутствует
    fig.update_layout: настройки графика
    fig.show: отображение интерактивного графика

    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

    if 'Moving_Average' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Moving Average'))

    fig.update_layout(title=f"{ticker} Цена акций ({period})",
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      legend_title='Легенда',
                      hovermode='x unified')

    fig.show()
