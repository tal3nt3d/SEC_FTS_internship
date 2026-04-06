# SEC_FTS_internship

## Локальный запуск

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# или
venv\Scripts\activate  #Windows
# Установка зависимостей
pip install -r requirements.txt
# Настройка переменных окружения
cp .env.example .env
# Запуск сервиса
python main.py
```