# Данный модуль отвечает за загрузку данных об акциях, он содержит функции для извлечения данных
# об акциях из интернета и расчета скользящего среднего

import yfinance as yf
import logging

# Set up logging - добавляем логирование уровня INFO (выводим время логирования, уровень логирования, само сообщение)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_stock_data(ticker, period='1mo'):
    """
    Функция извлекает исторические данные о ценах акций.
    ticker: тикер акции, например, 'AAPL' для Apple.
    period: период времени для данных, например, '1mo' для одного месяца.
    data: исторические данные о цене акций за указанный период.
    """

    # Добавим исключение на тот случай, если мы запросили данные по несуществующему тикеру
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    logging.info("Данные успешно получены")
    return data


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций за период.
    data: DataFrame с данными акций, включая столбец 'Close'.
    """
    average_price = data['Close'].mean()
    logging.info(f"Расчетная средняя цена: {average_price:.2f}")
    print(f"Средняя цена закрытия акций за период: {average_price:.2f}")


def add_moving_average(data, window_size=5):
    """
    Добавляет столбец скользящего среднего к данным акций.
    data: DataFrame с данными акций, включая столбец 'Close'.
    window_size: размер окна для скользящего среднего.
    data['Moving_Average']: обновленный DataFrame с добавленным столбцом 'Moving_Average'.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    logging.info("Скользящее среднее успешно добавлено")
    return data


# Простое тестирование
if __name__ == "__main__":
    ticker = "AAPL"
    period = "1mo"

    # Получаем данные
    data = fetch_stock_data(ticker, period)

    # Выполняем расчет средней цены с выводом на консоль
    calculate_and_display_average_price(data)

    # Добавляем скользящее среднее и выводим на консоль
    data_with_ma = add_moving_average(data)
    print(data_with_ma.head())
