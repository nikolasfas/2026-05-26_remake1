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
                    order by avg_rating desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllActors(startR, endR):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.id, n.name , n.date_of_birth 
                    from role_mapping dm , names n , ratings r 
                    where r.movie_id = dm.movie_id 
                    and dm.name_id = n.id 
                    and r.avg_rating between %s and %s
                    and n.date_of_birth is not null """

        cursor.execute(query, (startR, endR,))

        for row in cursor:
            result.append(Actor(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnections(startR, endR):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with links as(
                    select dm.movie_id , dm.name_id , m.worlwide_gross_income as wgi, r.avg_rating
                    from movie m , role_mapping dm , ratings r , names n 
                    where m.id = dm.movie_id
                    and m.id = r.movie_id
                    and n.id = dm.name_id
                    and r.avg_rating between %s and %s
                    and n.date_of_birth is not null 
                    and m.worlwide_gross_income like '$%'
                    )
                    select l1.name_id as id1, l2.name_id as id2 , l1.wgi as wgi
                    from links l1, links l2
                    where l1.movie_id = l2.movie_id
                    and l1.name_id < l2.name_id"""

        cursor.execute(query, (startR, endR,))

        for row in cursor:
            result.append((row["id1"], row["id2"], row["wgi"]))

        cursor.close()
        conn.close()
        return result


