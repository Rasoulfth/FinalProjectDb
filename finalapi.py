from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import os
import time

DB_URL = "postgresql://postgres:1234@localhost:5432/Google_play"
engine = create_engine(DB_URL)

app = FastAPI()
class AppModel(BaseModel):
    app_id: str
    app_name: str
    category_id: int
    rating: float
    rating_count: int
    installs: int
    min_installs: int
    max_installs: int
    free: bool
    price: float
    currency: str
    size: str
    min_android: str
    developer_id: int
    released: str
    last_updated: str
    content_rating: str
    privacy_policy: str
    ad_supported: bool
    in_app_purchases: bool
    editors_choice: bool

@app.get("/apps/")
def get_apps(
    category: str = Query(None, description="Filter by category"),
    min_rating: float = Query(None, description="Minimum rating"),
    min_price: float = Query(None, description="minimum price"),
    min_installs: int = Query(None, description="Minimum installs"),
    limit: int = Query(10000, description="Limit number of results"),
    free: bool = Query(True,description="FreeApps")
):
    query = "SELECT *,CATEGORY_NAME FROM Apps INNER JOIN CATEGORIES\
    ON APPS.CATEGORY_ID=CATEGORIES.CATEGORY_ID WHERE 1=1"
    
    if category:
        #query += f" AND category_id = (SELECT category_id FROM Categories WHERE category_name = '{category}')"
        query += f" AND category_name = '{category}'"
    if min_rating:
        query += f" AND rating >= {min_rating}"
    if min_price is not None:
        query += f" AND price >= {min_price}"
    if min_installs:
        query += f" AND installs >= {min_installs}"
    
    if free:
        query+= f" AND free ={free}"

    query += f" LIMIT {limit};"
    start = time.time()
    df = pd.read_sql(query, engine)
    end = time.time()
    return {'data':df.to_dict(orient="records"), 'time':end-start}

@app.post("/apps/")
def create_app(app: AppModel):
    conn = psycopg2.connect(
        dbname="Google_play",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO Apps (app_id, app_name, category_id, rating, rating_count, installs, min_installs, max_installs, free,
                              price, currency, size, min_android, developer_id, released, last_updated, content_rating,
                              privacy_policy, ad_supported, in_app_purchases, editors_choice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            app.app_id, app.app_name, app.category_id, app.rating, app.rating_count, app.installs,
            app.min_installs, app.max_installs, app.free, app.price, app.currency, app.size,
            app.min_android, app.developer_id, app.released, app.last_updated, app.content_rating,
            app.privacy_policy, app.ad_supported, app.in_app_purchases, app.editors_choice
        ))
        conn.commit()
        return {"message": "App added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
@app.put("/apps/{app_id}")
def update_app(app_id: str, app: AppModel):
    conn = psycopg2.connect(
        dbname="Google_play",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM Apps WHERE app_id = %s;", (app_id,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="App not found")

        cur.execute("""
            UPDATE Apps
            SET app_name = %s, category_id = %s, rating = %s, rating_count = %s, installs = %s, 
                min_installs = %s, max_installs = %s, free = %s, price = %s, currency = %s, size = %s, 
                min_android = %s, developer_id = %s, released = %s, last_updated = %s, content_rating = %s, 
                privacy_policy = %s, ad_supported = %s, in_app_purchases = %s, editors_choice = %s
            WHERE app_id = %s
        """, (
            app.app_name, app.category_id, app.rating, app.rating_count, app.installs,
            app.min_installs, app.max_installs, app.free, app.price, app.currency, app.size,
            app.min_android, app.developer_id, app.released, app.last_updated, app.content_rating,
            app.privacy_policy, app.ad_supported, app.in_app_purchases, app.editors_choice,
            app_id
        ))
        conn.commit()
        return {"message": "App updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
@app.delete("/apps/{app_id}")
def delete_app(app_id: str):
    conn = psycopg2.connect(
        dbname="Google_play",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM Apps WHERE app_id = %s;", (app_id,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="App not found")

        cur.execute("DELETE FROM Apps WHERE app_id = %s", (app_id,))
        conn.commit()
        return {"message": "App deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
@app.get("/categories/")
def get_categories():
    query = "SELECT category_name FROM Categories;"
    df = pd.read_sql(query, engine)
    return df['category_name'].tolist()
