#DB operations

from ..model.databases import conn
from ..model.models import Lift,Log,Request

class LiftRepository:
    def get_lift(self,lift_id:int):
        """fetch by id"""
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM lifts WHERE lift_id=%s',(lift_id,))
        result=cursor.fetchone()
        cursor.close()
        return result
    def get_all_lifts(self)->list[Lift]:
        """get all lifts"""
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM lifts')
        result=cursor.fetchall()#return tuple 
        print(type(result))
        cursor.close()
        return [Lift(*row) for row in result]#since row 
        # is tuple by doing *row we unpack tuples
        #[
    #Lift(1, 5, "up", "open"),
    #Lift(2, 3, "down", "closed")
    #]
    def move_lift(self,lift_id:int,floor:int,direction:str,door_status:str)->bool:
        """update lift position"""
        cursor=conn.cursor()
        try:
            cursor.execute(
                "UPDATE lifts SET current_floor = %s, direction = %s, door_status = %s WHERE lift_id = %s",
                (floor, direction, door_status, lift_id)
            )
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            conn.rollback()
            cursor.close()
            print("Error",e)
            return False
    def add_request(self,floor:int)->int:
        """add new request"""
        cursor=conn.cursor()
        try:
            cursor.execute(
                           "INSERT into requests (floor,status) VALUES (%s,%s) returning request_id",
                           (floor,'pending'))
            request_id=cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return request_id
        except Exception as e:
            conn.rollback()
            cursor.close()
            print(f"Error: {e}")
            return None
    def get_pending_request(self)->list[Request]:
        """Get all pending request for the lift"""
        cursor=conn.cursor()
        cursor.execute(
            "SELECT request_id, floor,request_time,status,lift_id from requests where status='Pending'"
        )
        res=cursor.fetchall()
        cursor.close()
        return [Request(*row) for row in res]
    def mark_served(self,request_id:int)->bool:
        "Mark request as served"
        cursor=conn.cursor()
        try:
            cursor.execute(
                "UPDATE requests SET status='served' WHERE request_id=%s",
                (request_id)
            )
            cursor.commit()
            cursor.close()
            return True
        except Exception as e:
            conn.rollback()
            cursor.close()
            print(f"Error {e}")
            return False
