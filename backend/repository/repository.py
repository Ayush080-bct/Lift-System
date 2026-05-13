#DB operations

from model.databases import conn
from model.models import Lift,Log,Request
class LiftRepository:
    def get_lift(self,lift_id:int):
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM lifts WHERE lift_id=%s',)