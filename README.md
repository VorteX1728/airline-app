# Решись Авиа - сервис прогноза спроса и продаж

Веб-приложение с backend на FastAPI. Принимает `my_forecast.csv` и `routes.csv`, маршрут, дату и цену. Для каждого из 9 квантилей вычисляет спрос по формуле:

`wanted = max(0, base_demand - price_sensitivity * (price - base_price))`

` sold = min(seats, wanted) `

## Запуск локально

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Откройте `http://127.0.0.1:8000`. Загрузите `my_forecast.csv` и исходный `routes.csv` из набора данных

## Формат данных

`my_forecast.csv`: `route`, `date`, `seats`, `0.1_base_demand` ... `0.9_base_demand`.
`routes.csv`: `route`, `base_price`, `price_sensitivity` (остальные столбцы допускаются).

## Что реализовано

- форма выбора маршрута, даты и цены;
- загрузка прогнозного CSV и справочника;
- серверный расчёт сценарного спроса и продаж с ограничением по местам;
- медианный KPI, загрузка рейса, таблица квантилей и график;
- проверка отсутствующих маршрутов/дат и ошибок входных файлов.

Python 3, FastAPI, pandas, HTML, CSS, JavaScript; модель AutoGluon используется в отдельном ML-ноутбуке для построения исходного прогноза
