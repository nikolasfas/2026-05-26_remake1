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
        query = """select n.id , n.name , n.date_of_birth
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
        query = """select rm1.name_id as a1,
                   rm2.name_id as a2,
                   m.worlwide_gross_income as income
            from movie m, ratings r, role_mapping rm1, role_mapping rm2, names n1, names n2
            where r.movie_id = m.id
            and rm1.movie_id = m.id
            and rm2.movie_id = m.id
            and rm1.name_id < rm2.name_id
            and rm1.name_id = n1.id
            and rm2.name_id = n2.id
            and n1.date_of_birth is not null
            and n2.date_of_birth is not null
            and r.avg_rating >= %s
            and r.avg_rating <= %s
            and m.worlwide_gross_income like '$%'"""


        cursor.execute(query, (min_rate, max_rate,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
