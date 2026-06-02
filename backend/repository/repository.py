#DB operations

from ..model.databases import get_connection, put_connection
from ..model.models import Lift, Log, Request

class LiftRepository:
    def get_lift(self, lift_id: int):
        """fetch by id"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lifts WHERE lift_id=%s', (lift_id,))
        result = cursor.fetchone()
        cursor.close()
        put_connection(conn)  # ✅ Return to pool
        return result

    def get_all_lifts(self) -> list[Lift]:
        """get all lifts"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lifts')
        result = cursor.fetchall()  # return tuple 
        print(type(result))
        cursor.close()
        put_connection(conn)  # ✅ Return to pool
        return [Lift(*row) for row in result]  # since row 
        # is tuple by doing *row we unpack tuples
        # [
        # Lift(1, 5, "up", "open"),
        # Lift(2, 3, "down", "closed")
        # ]

    def move_lift(self, lift_id: int, floor: int, direction: str, door_status: str) -> bool:
        """update lift position"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE lifts SET current_floor = %s, direction = %s, door_status = %s WHERE lift_id = %s",
                (floor, direction, door_status, lift_id)
            )
            conn.commit()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool
            return True
        except Exception as e:
            conn.rollback()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool even on error
            print("Error", e)
            return False

    def add_request(self, floor: int) -> int:
        """add new request"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT into requests (floor,status) VALUES (%s,%s) returning request_id",
                (floor, 'pending'))
            request_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool
            return request_id
        except Exception as e:
            conn.rollback()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool even on error
            print(f"Error: {e}")
            return None

    def get_pending_request(self) -> list[Request]:
        """Get all pending request for the lift"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        cursor.execute(
            "SELECT request_id, floor,request_time,status,lift_id from requests where status='pending'"
        )
        res = cursor.fetchall()
        cursor.close()
        put_connection(conn)  # ✅ Return to pool
        return [Request(*row) for row in res]

    def assign_request_to_lift(self, request_id: int, lift_id: int) -> bool:
        """Assign a request to a specific lift"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE requests SET lift_id = %s WHERE request_id = %s",
                (lift_id, request_id)
            )
            conn.commit()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool
            return True
        except Exception as e:
            conn.rollback()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool even on error
            print(f"Error: {e}")
            return False

    def mark_served(self, request_id: int) -> bool:
        "Mark request as served"
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM requests WHERE request_id=%s",
                (request_id,)
            )
            conn.commit()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool
            return True
        except Exception as e:
            conn.rollback()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool even on error
            print(f"Error {e}")
            return False

    def log_event(self, lift_id: int, event_type: str) -> int:
        """Log an event"""
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO logs(lift_id,event_type) VALUES (%s,%s) RETURNING log_id", (lift_id, event_type)
            )
            log_id = cursor.fetchone()[0]  # return immediately a serial or autoincrement pk for each row
            conn.commit()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool
            return log_id
        except Exception as e:
            conn.rollback()
            cursor.close()
            put_connection(conn)  # ✅ Return to pool even on error
            print(f"Error:{e}")
            return None

    def get_all_logs(self):
        "Get all Record"
        conn = get_connection()  # ✅ Get fresh connection from pool
        cursor = conn.cursor()
        cursor.execute("Select * from logs")
        result = cursor.fetchall()
        cursor.close()
        put_connection(conn)  # ✅ Return to pool
        return [Log(*row) for row in result]