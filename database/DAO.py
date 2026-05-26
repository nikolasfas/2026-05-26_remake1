from database.DB_connect import DBConnect
from model.actor import Actor
from model.movie import Movie


class DAO():
    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct avg_rating 
                    from ratings r
                    order by avg_rating """

        cursor.execute(query)

        for row in cursor:
            result.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllActors(min_rate, max_rate):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.id , n.name , n.date_of_birth, m.id as movieId
                    from ratings r , names n , movie m , role_mapping rm 
                    where r.movie_id = m.id 
                    and m.id = rm.movie_id 
                    and rm.name_id = n.id 
                    and r.avg_rating >= %s and r.avg_rating <= %s
                    and n.date_of_birth is not null """

        cursor.execute(query, (min_rate, max_rate,))

        for row in cursor:
            result.append((Actor(**row)))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(min_rate, max_rate):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select m.id , m.title , m.worlwide_gross_income as income
                from movie m, ratings r 
                where r.movie_id = m.id 
                and r.avg_rating >= %s and r.avg_rating <= %s
                and m.worlwide_gross_income like '$%'"""


        cursor.execute(query, (min_rate, max_rate,))

        for row in cursor:
            result.append((Movie(**row)))

        cursor.close()
        conn.close()
        return result
