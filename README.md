Этот проект предназначен для загрузки исторических данных об акциях и их визуализации 
=====================================================================================
Он использует библиотеку yfinance для получения данных и matplotlib для создания графиков. 

Пользователи могут выбирать различные тикеры и временные периоды для анализа, а также просматривать движение цен и скользящие средние на графике.

Структура и модули проекта
--------------------------

1. data_download.py:

- Отвечает за загрузку данных об акциях.

- Содержит функции для извлечения данных об акциях из интернета и расчёта скользящего среднего, а экспорта загруженных данных в файл формата CSV. 
- Также содержит функции для расчёта и отображения на графике дополнительных технических индикаторов RSI и MACD. 



2. main.py:

- Является точкой входа в программу.

- Запрашивает у пользователя тикер акции и временной период, загружает данные, обрабатывает их и выводит результаты в виде графика.



3. data_plotting.py:

- Отвечает за визуализацию данных.

- Содержит функции для создания и сохранения графиков цен закрытия и скользящих средних, а также графиков дополнительных технических индикаторов RSI и MACD


Описание функций
----------------


1. data_download.py:

- fetch_stock_data(ticker, period): Получает исторические данные об акциях для указанного тикера и временного периода. Возвращает DataFrame с данными. В функции также заложена проверка тикера: если указанный тикер отсутствует, то срабатывает исключение, в консоли выводится соответствующее сообщение и программа прерывает свою работу.

- calculate_and_display_average_price(data): Вычисляет и выводит среднюю цену закрытия акций за период.
  
- add_moving_average(data, window_size): Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.

- notify_if_strong_fluctuations(data, threshold): Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
 
- export_data_to_csv(data, filename): позволяет сохранить загруженные данные об акциях в CSV файл.

- calculate_rsi(data, window=14): вычисляет RSI (индекс относительной силы) и добавляет столбец RSI в DataFrame.
 
- calculate_macd(data, short_window=12, long_window=26, signal_window=9): вычисляет MACD (схождение/расхождение скользящих средних) и добавляет столбцы MACD и Signal_Line в DataFrame.



2. main.py:

- main(): Основная функция, управляющая процессом загрузки, обработки данных и их визуализации. Запрашивает у пользователя ввод данных, вызывает функции загрузки и обработки данных, а затем передаёт результаты на визуализацию.



3. data_plotting.py:

- plot_rsi(data, ticker, period, filename=None): для построения графика RSI (индекс относительной силы). График сохраняется в файл и выводится на экран
 
- plot_macd(data, ticker, period, filename=None): для построения графика MACD (схождения и расхождения скользящих средних). График также сохраняется в файл и выводится на экран
 
- create_and_save_plot(data, ticker, period, filename): создаёт график, отображающий цены закрытия и скользящие средние. Предоставляет возможность сохранения графика в файл. Параметр filename опционален; если он не указан, имя файла генерируется автоматически.


Пошаговое использование проекта
-------------------------------
1. Запустите main.py.

2. Введите интересующий вас тикер акции (например, 'AAPL' для Apple Inc).

3. Введите желаемый временной период для анализа (например, '1mo' для данных за один месяц).

4. Программа обработает введённые данные, загрузит соответствующие данные об акциях, рассчитает скользящее среднее, сохранит данные в CSV файл и отобразит график
