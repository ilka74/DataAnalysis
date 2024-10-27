# Данный модуль отвечает за загрузку данных об акциях, он содержит функции для извлечения данных
# об акциях из интернета и расчета скользящего среднего

import yfinance as yf
import logging
from data_plotting import plot_rsi, plot_macd

# Set up logging - добавляем логирование уровня INFO (выводим время логирования, уровень логирования, само сообщение)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_stock_data(ticker, period='1mo', start=None, end=None):
    """
    Функция извлекает исторические данные о ценах акций.
    ticker: тикер акции, например, 'AAPL' для Apple.
    period: период времени для данных, например, '1mo' для одного месяца.
    data: исторические данные о цене акций за указанный период.
    start: дата начала в формате 'YYYY-MM-DD'.
    end: дата окончания в формате 'YYYY-MM-DD'.
    """

    # Добавим исключение на тот случай, если мы запросили данные по несуществующему тикеру
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, start=start, end=end)
        if data.empty:
            raise ValueError(f"Данные для тикера {ticker} не найдены.")
        logging.info("Данные успешно получены")
        return data
    except Exception as e:
        logging.error(f"Ошибка при получении данных для тикера {ticker}: {e}")
        raise


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


def notify_if_strong_fluctuations(data, threshold):
    """
    Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
    data: DataFrame с данными акций, включая столбец 'Close'.
    threshold: порог в процентах для уведомления о сильных колебаниях.
    fluctuation: реальные колебания
    """
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    fluctuation = ((max_price - min_price) / min_price) * 100

    if fluctuation > threshold:
        logging.info(f"Сильные колебания: {fluctuation:.2f}% превышают порог {threshold}%")
        print(f"Внимание! Цена акций колебалась более чем на {threshold}% за период.")
    else:
        logging.info(f"Колебания в пределах нормы: {fluctuation:.2f}%")


def export_data_to_csv(data, filename):
    """
    Экспортирует данные в CSV файл.
    :data: DataFrame с данными об акциях
    :filename: Имя файла для сохранения
    """
    try:
        data.to_csv(filename, index=False)  # Сохраняем DataFrame в CSV файл без индексов
        logging.info(f"Данные успешно сохранены в {filename}")
        print(f"Данные успешно сохранены в файл: {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных: {e}")
        print(f"Ошибка при сохранении данных: {e}")


def calculate_rsi(data, window=14):
    """
    Вычисляет RSI (индекс относительной силы) и добавляет его к данным акций.
    Рассчитывается по формуле, используя средние приросты и потери за определенное окно.
    Данная функция добавляет столбец RSI в DataFrame.
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data['RSI'] = rsi
    logging.info("RSI успешно добавлен")
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Вычисляет MACD (схождение/расхождение скользящих средних) и добавляет его к данным акций.
    MACD рассчитывается как разница между двумя экспоненциальными скользящими средними (EMA) — короткой и длинной.
    Добавляется сигнал (EMA от MACD).
    Данная функция добавляет столбцы MACD и Signal_Line в DataFrame.
    """
    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    logging.info("MACD успешно добавлен")
    return data


# Простое тестирование
if __name__ == "__main__":
    ticker = "AMZN"
    period = "6mo"
    threshold = 5  # Порог в процентах для уведомления

    try:
        # Получаем данные
        data = fetch_stock_data(ticker, period)

        # Выполняем расчет средней цены с выводом на консоль
        calculate_and_display_average_price(data)

        # Добавляем скользящее среднее и выводим на консоль
        data_with_ma = add_moving_average(data)
        print(data_with_ma.head())

        # Рассчитываем RSI
        data_with_rsi = calculate_rsi(data_with_ma)
        print(data_with_rsi[['Close', 'RSI']].head())

        # Визуализация RSI
        plot_rsi(data_with_rsi, ticker, period)

        # Рассчитываем MACD
        data_with_macd = calculate_macd(data_with_rsi)
        print(data_with_macd[['Close', 'MACD', 'Signal_Line']].head())

        # Визуализация MACD
        plot_macd(data_with_macd, ticker, period)

        # Проверяем на сильные колебания
        notify_if_strong_fluctuations(data, threshold)

        # Выполняем экспорт данных с добавленным скользящим средним в CSV
        export_data_to_csv(data_with_ma, 'stock_data.csv')

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)
