from database.DAO import DAO


class Model:
    def __init__(self):
        self._ratings = []

    def getAllRatings(self):
        self._ratings = DAO.getAllRatings()
        return self._ratings