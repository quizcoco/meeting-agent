import json
from src.config.settings import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT
)
import psycopg2

def save_minutes(meeting_text, meeting_json):

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO meeting_minutes
        (
            raw_text,
            summary,
            title,
            purpose,
            discussion,
            decision,
            action_items
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        RETURNING id

        """,
        (
            meeting_text,
            meeting_json["summary"],
            meeting_json["title"],
            meeting_json["purpose"],
            meeting_json["discussion"],
            meeting_json["decision"],
            json.dumps(meeting_json["action_items"])
        )
    )
    meeting_id = cur.fetchone()[0]


    conn.commit()

    cur.close()
    conn.close()
    return meeting_id

def get_recent_minutes(limit=3):

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            title,
            summary,
            purpose,
            discussion,
            decision,
            action_items,
            created_at
        FROM meeting_minutes
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall() # 튜플

    cur.close()
    conn.close()

    meetings = []

    for r in rows:
        meetings.append({
            "id": r[0],
            "title": r[1],
            "summary": r[2],
            "purpose": r[3],
            "discussion": r[4],
            "decision": r[5],
            "action_items": r[6],
            "created_at": r[7]
        })

    return meetings # 리스트 안에 딕셔너리 형태로 반환

def get_meeting(meeting_id):

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            title,
            summary,
            purpose,
            discussion,
            decision,
            action_items,
            created_at
        FROM meeting_minutes
        WHERE id = %s
        """,
        (meeting_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
            "id": row[0],
            "title": row[1],
            "summary": row[2],
            "purpose": row[3],
            "discussion": row[4],
            "decision": row[5],
            "action_items": row[6],
            "created_at": row[7]
        }