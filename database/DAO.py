from database.DB_connect import DBConnect


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
    def getAllActors():
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
