import sqlite3
from sqlite3 import Error
from datetime import date
import logging

logging.basicConfig(level=logging.DEBUG, filename='training.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Создать подключение к базе данных
def create_connection():
    try:
        conn = sqlite3.connect('db/training.db')
        return conn
    except Error as e:
        logging.error(f"Unable to connect to database: {e}")

# Функция для создания необходимых таблиц, если их нет
def create_tables(conn):
    create_pushups_table = """
        CREATE TABLE IF NOT EXISTS pushups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        max_pushups INTEGER NOT NULL
    );
    """
    create_crunches_table = """
        CREATE TABLE IF NOT EXISTS crunches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        max_crunches INTEGER NOT NULL
    );
    """
    create_planka_table = """
        CREATE TABLE IF NOT EXISTS planka (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        max_planka INTEGER NOT NULL
    );
    """
    sql_pushups_history_table = """
        CREATE TABLE IF NOT EXISTS pushups_training_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        date DATE NOT NULL
    );
    """
    sql_crunches_history_table = """
        CREATE TABLE IF NOT EXISTS crunches_training_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        date DATE NOT NULL
    );
    """
    sql_planka_history_table = """
        CREATE TABLE IF NOT EXISTS planka_training_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        date DATE NOT NULL
    );
    """
    next_trainings_table = """
        CREATE TABLE next_trainings (
        user_id INTEGER NOT NULL,
        training_num INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        set_num INTEGER NOT NULL,
        PRIMARY KEY (user_id, training_num, set_num)
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_pushups_table)
        c.execute(create_crunches_table)
        c.execute(create_planka_table)
        c.execute(sql_pushups_history_table)
        c.execute(sql_crunches_history_table)
        c.execute(sql_planka_history_table)
        c.execute(next_trainings_table)
        conn.commit()
        logging.info('Tables successfully created')
    except Error as e:
        logging.error(f"Unable to create tables: {e}")

#
def add_user_max(conn, user_id, cur_train, max_reps):
    insert_sql = f"INSERT INTO {cur_train} (user_id, max_{cur_train}) VALUES (?, ?)"
    try:
        c = conn.cursor()
        c.execute(insert_sql, (user_id, max_reps))
        conn.commit()
        logging.info(f"User {user_id} has been added to the table {cur_train}.")
    except Error as e:
        logging.error(f"Unable to add user to {cur_train} table: {e}")

# Обновить максимальное количество повторений одной из тренировок пользователя
def update_user_max_reps(conn, user_id, cur_train, max_reps):
    update_sql = f"UPDATE {cur_train} SET max_{cur_train} = {max_reps} WHERE id = {user_id}"
    try:
        c = conn.cursor()
        c.execute(update_sql)
        conn.commit()
        logging.info(f"Max_{cur_train} for user {user_id} has been updated to {max_reps}")
    except Error as e:
        logging.error(f"Unable to update user max_reps to {cur_train} database: {e}")

#
def add_next_trainings(conn, user_id, tr1, tr2, tr3):
    try:
        c = conn.cursor()
        for i, tr in enumerate([tr1, tr2, tr3], 1):
            for j, rep in enumerate(tr, 1):
                c.execute("REPLACE INTO next_trainings (user_id, training_num, reps, set_num) VALUES (?, ?, ?, ?)", 
                          (user_id, i, rep, j))
        conn.commit()
        logging.info(f"Next_trainings data for user {user_id} has been added.")
    except Error as e:
        logging.error(f"Unable to add training data for user {user_id} to the next_trainings table: {e}")

#
def get_next_training():
    pass

# Добавить тренировку
def add_training(conn, user_id, cur_train, reps, date):
    insert_sql = f"INSERT INTO {cur_train}_training_history (user_id, reps, date) VALUES ({user_id}, {reps}, '{date}')"
    try:
        c = conn.cursor()
        c.execute(insert_sql)
        conn.commit()
        logging.info(f"Training for user {user_id} has been added in {cur_train}_history_table .")
    except Error as e:
        logging.error(f"Unable to add training for user {user_id} in {cur_train}_history_table : {e}")

# Функция для получения информации о пользователе
def get_user_info(conn, user_id, cur_train):
    logging.info(f"Getting user info for user {user_id} and exercise {cur_train}")
    # Получить максимальное количество повторений упражнения пользователя
    select_max_sql = f"SELECT max_{cur_train} FROM {cur_train} WHERE user_id = {user_id} ORDER BY id DESC LIMIT 1"
    # Получить последние 10 тренировок пользователя
    select_training_sql = f"SELECT reps, date FROM {cur_train}_training_history WHERE user_id = {user_id} ORDER BY date DESC LIMIT 10"
    try:
        c = conn.cursor()
        c.execute(select_max_sql)
        max_reps = c.fetchone()
        if max_reps:
            max_reps = max_reps[0]
        else:
            # Добавляем сообщение для нового пользователя
            return {
                "user_id": user_id,
                "exercise": cur_train,
                "max_reps": 0,
                "training_history": None,
                "message": "Чтобы начать тренироваться, сначала \
                установите свой максимум повторений на данный момент. Для этого отправьте сообщение \
                в формате: '<количество повторений>'. Например: '10'."
            }
        c.execute(select_training_sql)
        training_history = c.fetchall()
        # Сформировать результат и вернуть его
        result = {
            "user_id": user_id,
            "exercise": cur_train,
            "max_reps": max_reps,
            "training_history": training_history
        }
        logging.info(f"Info for user {user_id} and exercise {cur_train} has been retrieved successfully")
        return result
    except Error as e:
        logging.error(f"Error getting info for user {user_id} and exercise {cur_train}: {e}")