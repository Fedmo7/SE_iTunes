from database.DB_connect import DBConnect
from model.song import Song
from model.album import Album

class DAO:

    @staticmethod
    def query_album():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select a.id,a.artist_id ,a.title ,sum(t.milliseconds) as durata
                   from album a,track t 
                   where a.id =t.album_id 
                   group by a.id,a.artist_id ,a.title """

        cursor.execute(query)

        for row in cursor:
            result[row['id']]=Album(row['id'],row['artist_id'],row['title'],float(row['durata']/1000/60))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def query_archi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.id, t.album_id ,pt.playlist_id 
                   from track t ,playlist_track pt 
                   where pt.track_id =t.id 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(Song(row['id'],row['album_id'],row['playlist_id']))

        cursor.close()
        conn.close()
        return result


