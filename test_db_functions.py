import sqlite3
from datetime import date
from unittest import TestCase, main

from db_fuctions import create_tables, add_user_max, update_user_max_reps, add_next_trainings, add_training, get_user_info


class TestTraining(TestCase):
    @classmethod
    def setUpClass(cls):
        # Создать тестовую базу данных
        cls.conn = sqlite3.connect(':memory:')
        create_tables(cls.conn)

    def test_a_add_user_max(self):
        # Добавить пользователя в базу данных
        add_user_max(self.conn, 1, "pushups", 20)

        # Получить максимальное количество повторений для добавленного пользователя
        c = self.conn.cursor()
        c.execute("SELECT max_pushups FROM pushups WHERE id = 1")
        result = c.fetchone()
        self.assertEqual(result[0], 20)

    def test_b_update_user_max_reps(self):
        # Обновить максимальное количество повторений для пользователя
        update_user_max_reps(self.conn, 1, "pushups", 25)

        # Получить максимальное количество повторений для обновленного пользователя
        c = self.conn.cursor()
        c.execute("SELECT max_pushups FROM pushups WHERE id = 1")
        result = c.fetchone()
        self.assertEqual(result[0], 25)

    def test_c_add_training(self):
        # Добавить тренировку для пользователя
        add_training(self.conn, 1, "pushups", 15, date.today())
        # Получить историю тренировок для пользователя
        c = self.conn.cursor()
        c.execute("SELECT reps, date FROM pushups_training_history WHERE user_id = 1")
        result = c.fetchall()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 15)
        self.assertEqual(result[0][1], date.today().strftime('%Y-%m-%d'))

    def test_d_add_next_trainings(self):
        add_next_trainings(self.conn, 1, [10, 12, 14, 16, 18], [20, 22, 24, 26, 28], [30, 32, 34, 36, 38])
        c = self.conn.cursor()
        c.execute("SELECT * FROM next_trainings WHERE user_id = 1")
        result = c.fetchall()
        expected_result = [
            (1, 1, 10, 1),
            (1, 1, 12, 2),
            (1, 1, 14, 3),
            (1, 1, 16, 4),
            (1, 1, 18, 5),
            (1, 2, 20, 1),
            (1, 2, 22, 2),
            (1, 2, 24, 3),
            (1, 2, 26, 4),
            (1, 2, 28, 5),
            (1, 3, 30, 1),
            (1, 3, 32, 2),
            (1, 3, 34, 3),
            (1, 3, 36, 4),
            (1, 3, 38, 5),
        ]
        self.assertEqual(result, expected_result)

    def test_e_get_user_info(self):
        # Получить информацию о пользователе
        result = get_user_info(self.conn, 1, "pushups")
        expected_result = {
            "user_id": 1,
            "exercise": "pushups",
            "max_reps": 25,
            "training_history": [(15, date.today().strftime('%Y-%m-%d'))]
        }
        self.assertEqual(result, expected_result)
    
    def test_f_get_new_user_info(self):
        # Получить информацию о новом пользователе
        result = get_user_info(self.conn, 10, "pushups")
        expected_result = {
            "user_id": 10,
            "exercise": "pushups",
            "max_reps": 0,
            "training_history": None,
            "message": "Чтобы начать тренироваться, сначала \
                установите свой максимум повторений на данный момент. Для этого отправьте сообщение \
                в формате: '<количество повторений>'. Например: '10'."
        }
        self.assertEqual(result, expected_result)

    @classmethod
    def tearDownClass(cls):
        # Закрыть соединение с базой данных
        cls.conn.close()


if __name__ == '__main__':
    main(argv=['first-arg-is-ignored'], exit=False)

