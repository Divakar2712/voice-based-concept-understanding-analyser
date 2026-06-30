import sqlite3
import os

DB_PATH = "database/analysis.db"


# -----------------------------------------
# Database Connection
# -----------------------------------------

def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DB_PATH)


# -----------------------------------------
# Create Table
# -----------------------------------------

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

        transcript TEXT,

        reference_text TEXT,

        similarity REAL,

        duration REAL,

        rms_energy REAL,

        zero_crossing_rate REAL,

        pause_ratio REAL,

        speech_rate REAL,

        filler_count INTEGER,

        filler_density REAL,

        final_score REAL,

        grade TEXT,

        gemini_feedback TEXT

    )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# Save Analysis Result
# -----------------------------------------

def save_result(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO analysis(

        transcript,
        reference_text,
        similarity,
        duration,
        rms_energy,
        zero_crossing_rate,
        pause_ratio,
        speech_rate,
        filler_count,
        filler_density,
        final_score,
        grade,
        gemini_feedback

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

    """, (

        data["transcript"],
        data["reference_text"],
        data["similarity"],
        data["duration"],
        data["rms_energy"],
        data["zero_crossing_rate"],
        data["pause_ratio"],
        data["speech_rate"],
        data["filler_count"],
        data["filler_density"],
        data["final_score"],
        data["grade"],
        data["gemini_feedback"]

    ))

    conn.commit()
    conn.close()


# -----------------------------------------
# Fetch All Results
# -----------------------------------------

def fetch_all_results():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM analysis

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------------------
# Fetch Recent Results
# -----------------------------------------

def fetch_recent_results(limit=10):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        timestamp,

        similarity,

        final_score,

        grade

    FROM analysis

    ORDER BY id DESC

    LIMIT ?

    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------------------
# Delete All Results
# -----------------------------------------

def delete_all_results():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM analysis")

    conn.commit()

    conn.close()


# -----------------------------------------
# Initialize Database
# -----------------------------------------

create_table()