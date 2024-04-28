from datetime import datetime as libdatetime
from typing import List


def getLatLongId(db, lat, long):
    cs = db.db.cursor()
    sql_get_latlong_id = f"select id from LatLong where lattitude = '{lat}' and longtitude = '{long}'"
    cs.execute(sql_get_latlong_id)
    row = cs.fetchone()
    latlong_id = row[0]
    return latlong_id

def getDatetimeId(db, datetime:libdatetime):
    cs = db.db.cursor()
    dt_str = datetime.strftime("%Y-%-m-%d %H:%M:%S")
    sql_get_datetime_id = f"select id from DatetimeRecord where datetime = '{dt_str}'"
    cs.execute(sql_get_datetime_id)
    row = cs.fetchone()
    datetime_id = row[0]
    return datetime_id

# def getDatetimeLatLongMatrix(db) -> List[List[float, float, libdatetime]]:
def getDatetimeLatLongMatrix(db):
    cs = db.db.cursor()

    sql_get_datetime_and_latlong = """
    select lattitude lat,
    longtitude as "long",
    dr.`datetime` 
from DatetimeLatLong dll join LatLong ll on dll.latlongId = ll.id
join DatetimeRecord dr on dr.id = dll.datetimeId 
    """
    cs.execute(sql_get_datetime_and_latlong)
    return cs.fetchall()
    # for row in cs.fetchall():
        # row[0]

        
def checkIfDatetimeLatLongExistedOnDB(db, datetimeId:int, latlongId:int) -> bool:
    sql = f"""
    select count(*) as count_existed
from DatetimeLatLong dll 
where dll.datetimeId = {datetimeId}
and dll.latlongid = {latlongId}
    """
    cs = db.db.cursor()
    cs.execute(sql)
    count = cs.fetchone()[0]
    return True if count == 1 else False

    
def getDatetimeLatLongId(db, datetimeId:int, latlongId:int):
    sql = f"""
    select id
from DatetimeLatLong dll 
where dll.datetimeId = {datetimeId}
and dll.latlongid = {latlongId}
    """
    cs = db.db.cursor()
    cs.execute(sql)
    id = cs.fetchone()[0]
    return id
