class defs():
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
        except sqlite3.Error as e:
            print('ошибка получения данных из б')