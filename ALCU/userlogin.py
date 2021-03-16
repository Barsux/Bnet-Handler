class UserLogin():
    def FromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
    def create(self, user):
        self.__user = user
        return self
    def is_auntificated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.__user['id'])