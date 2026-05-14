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
