from contextlib import contextmanager
from pathlib import Path
import sys
project_root=Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from model.databases import get_connection, put_connection
from model.models import Lift, Log, Request


class LiftRepository:
    @contextmanager
    def _cursor(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            yield conn, cursor
        finally:
            cursor.close()
            put_connection(conn)

    def get_lift(self, lift_id: int) -> Lift | None:
        with self._cursor() as (_, cursor):
            cursor.execute(
                "SELECT lift_id, current_floor, direction, door_status FROM lifts WHERE lift_id = %s",
                (lift_id,),
            )
            row = cursor.fetchone()
            return Lift(*row) if row else None

    def get_all_lifts(self) -> list[Lift]:
        with self._cursor() as (_, cursor):
            cursor.execute(
                "SELECT lift_id, current_floor, direction, door_status FROM lifts ORDER BY lift_id"
            )
            return [Lift(*row) for row in cursor.fetchall()]

    def move_lift(self, lift_id: int, floor: int, direction: str, door_status: str) -> bool:
        with self._cursor() as (conn, cursor):
            try:
                cursor.execute(
                    """UPDATE lifts
                       SET current_floor = %s, direction = %s, door_status = %s
                       WHERE lift_id = %s""",
                    (floor, direction, door_status, lift_id),
                )
                conn.commit()
                return cursor.rowcount > 0
            except Exception:
                conn.rollback()
                return False

    def add_request(self, floor: int) -> int | None:
        with self._cursor() as (conn, cursor):
            try:
                cursor.execute(
                    "INSERT INTO requests (floor, status) VALUES (%s, %s) RETURNING request_id",
                    (floor, "pending"),
                )
                request_id = cursor.fetchone()[0]
                conn.commit()
                return request_id
            except Exception:
                conn.rollback()
                return None

    def get_pending_request(self) -> list[Request]:
        with self._cursor() as (_, cursor):
            cursor.execute(
                """SELECT request_id, floor, request_time, status, lift_id
                   FROM requests WHERE status = 'pending'"""
            )
            return [Request(*row) for row in cursor.fetchall()]

    def assign_request_to_lift(self, request_id: int, lift_id: int) -> bool:
        with self._cursor() as (conn, cursor):
            try:
                cursor.execute(
                    "UPDATE requests SET lift_id = %s WHERE request_id = %s",
                    (lift_id, request_id),
                )
                conn.commit()
                return cursor.rowcount > 0
            except Exception:
                conn.rollback()
                return False

    def mark_served(self, request_id: int) -> bool:
        with self._cursor() as (conn, cursor):
            try:
                cursor.execute(
                    "UPDATE requests SET status = 'served' WHERE request_id = %s",
                    (request_id,),
                )
                conn.commit()
                return cursor.rowcount > 0
            except Exception:
                conn.rollback()
                return False

    def log_event(self, lift_id: int, event_type: str) -> int | None:
        with self._cursor() as (conn, cursor):
            try:
                cursor.execute(
                    "INSERT INTO logs (lift_id, event_type) VALUES (%s, %s) RETURNING log_id",
                    (lift_id, event_type),
                )
                log_id = cursor.fetchone()[0]
                conn.commit()
                return log_id
            except Exception:
                conn.rollback()
                return None

    def get_all_logs(self, limit: int = 50) -> list[Log]:
        with self._cursor() as (_, cursor):
            cursor.execute(
                "SELECT log_id, lift_id, event_type, event_time FROM logs ORDER BY event_time DESC LIMIT %s",
                (limit,),
            )
            return [Log(*row) for row in cursor.fetchall()]
