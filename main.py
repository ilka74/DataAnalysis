import data_download as dd
import data_plotting as dplt
from datetime import datetime


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, "
          "с начала года, макс.")
    print("Вы можете выбрать предустановленны период или ввести свои даты.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):")

    # Запрос выбора периода
    period_choice = input("Выберите период (введите 'preset' для предустановленных периодов или 'custom' для "
                          "пользовательских дат): ").strip().lower()

    if period_choice == 'preset':
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        stock_data = dd.fetch_stock_data(ticker, period=period)
    elif period_choice == 'custom':
        start_date = input("Введите дату начала (формат YYYY-MM-DD): ")
        end_date = input("Введите дату окончания (формат YYYY-MM-DD): ")

        # Преобразование строковых дат в объекты datetime для валидации
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("Неверный формат даты. Пожалуйста, используйте формат YYYY-MM-DD.")
            return

        stock_data = dd.fetch_stock_data(ticker, start=start_date, end=end_date)

    else:
        print("Неверный выбор. Пожалуйста, используйте 'preset' или 'custom'.")
        return


    # Добавляем скользящее среднее значение к данным
    stock_data = dd.add_moving_average(stock_data)

    # Рассчитываем RSI и добавляем его к данным
    stock_data = dd.calculate_rsi(stock_data)

    # Рассчитываем MACD и добавляем его к данным
    stock_data = dd.calculate_macd(stock_data)

    # Строим график данных
    dplt.create_and_save_plot(stock_data, ticker, f"{start_date if period_choice == 'custom' else period} "
                                                  f"to {end_date if period_choice == 'custom' else period}")

    # Визуализация RSI
    dplt.plot_rsi(stock_data, ticker, f"{start_date if period_choice == 'custom' else period} "
                                      f"to {end_date if period_choice == 'custom' else period}")

    # Визуализация MACD
    dplt.plot_macd(stock_data, ticker, f"{start_date if period_choice == 'custom' else period} "
                                       f"to {end_date if period_choice == 'custom' else period}")


if __name__ == "__main__":
    main()
