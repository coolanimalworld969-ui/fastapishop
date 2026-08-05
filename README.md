# 🛒 FastAPI Shop API

REST API интернет-магазина, разработанное с использованием **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, **Alembic** и **Docker**.

---

## 🚀 Стек технологий

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT Authentication
- Docker & Docker Compose

---

# ⚙️ Быстрый запуск

### 1. Клонируйте репозиторий

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Создайте файл `.env`

Скопируйте файл `.env.example` и переименуйте его в `.env`.

Заполните необходимые переменные окружения.

### 3. Запустите контейнеры

```bash
docker compose up --build
```

### 4. Примените миграции

Откройте новый терминал и выполните:

```bash
docker compose exec app alembic upgrade head
```

После этого приложение будет доступно по адресу:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

# 📁 Структура проекта

```
.
├── src/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── .env.example
├── README.md
└── main.py
```

---

# 🔐 Переменные окружения

Файл `.env.example`:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=fastapi
DB_USER=postgres
DB_PASS=password

SECRET_KEY=your_secret_key
```

---

# 📖 Документация API

После запуска автоматически доступны:

- **Swagger UI** — `/docs`
- **ReDoc** — `/redoc`

---

# 📝 Примечание

После первого запуска необходимо выполнить миграции:

```bash
docker compose exec app alembic upgrade head
```

Без выполнения миграций таблицы в базе данных созданы не будут.