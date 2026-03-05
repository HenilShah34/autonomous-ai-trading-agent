from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db.postgres import get_connection

app = FastAPI()

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/latest/{symbol}")
def get_latest_data(symbol: str):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT DISTINCT ON (timeframe)
            time,
            timeframe,
            open,
            high,
            low,
            close,
            ma20,
            ma50,
            ma100,
            ma200
        FROM market_data
        WHERE symbol = %s
        ORDER BY timeframe, time DESC;
    """

    cur.execute(query, (symbol,))
    rows = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    return result