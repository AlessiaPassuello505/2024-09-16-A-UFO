from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getEstremi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select max(s.Lat ) as m_lat,min(s.Lat ) as min_lat,max(s.Lng ) as max_lng,min(s.Lng ) as min_lng
                        from state s  """
            cursor.execute(query)

            for row in cursor:
                result.append((row["m_lat"],row["min_lat"],row["max_lng"], row["min_lng"]))
            cursor.close()
            cnx.close()
        return result[0] if result else (0, 0, 0, 0)

    @staticmethod
    def getForma():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape 
                from sighting s 
            where s.shape <> "unknown"
            order by s.shape desc  """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(lat,lng,forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s1.*, SUM(si1.duration) as duration
                                   from state s1, sighting si1
                                   where s1.id = si1.state 
                                   and si1.shape=%s
                                   AND s1.Lat >%s and s1.Lng >%s
                                   GROUP BY s1.id """
            cursor.execute(query, (forma, lat, lng))

            for row in cursor:
                result.append(State(**row))
                if result[-1].Neighbors is None:
                    result[-1].Neighbors = []

            cursor.close()
            cnx.close()
        return result






