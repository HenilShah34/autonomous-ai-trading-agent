import psycopg2
from backend.db.postgres import get_connection


def insert_market_data(symbol, data):
    query = """
        INSERT INTO market_data
        (time, symbol, timeframe, open, high, low, close, ma20, ma50, ma100, ma200)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["time"],
        symbol,
        data["timeframe"],
        data["open"],
        data["high"],
        data["low"],
        data["close"],
        data["ma20"],
        data["ma50"],
        data["ma100"],
        data["ma200"],
    )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()