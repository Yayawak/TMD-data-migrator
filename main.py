from src.scrapper.scrapper import Scrapper
from src.nakornnayok_latlong_loader.latlong_loader import getLatLongOfNakornnayok
from src.database.dbconnector import DB
import pandas as pd
from threading import Thread
from datetime import datetime as libdatetime
from datetime import timedelta
from src.dateUtils.dateutils import thaiMonthToMonthOrderStartWithOne, isDatetimeExistedInDatatimeRecordTable, createDateOnDBIfNotExisted,getNextNDay
from src.utils.utils import *
import json

def targetFN(threadIndex, csv_url, date, time):
    print(f"{threadIndex} : Downloading {csv_url}...")
    csv_df = pd.read_csv(csv_url)
    name = f"{threadIndex}-{date}-{time}"
    name = f"resources/csv/{name}.csv"
    print(f"saving csv file to {name}")
    # csv_df.to_csv(name)

# NOTE : use once 
def insertLatLongDistrictToDB(latlongs_nk_data, db):
    print("Inserting lat long district id to DB.")
    for sheet_name, latlong2d in latlongs_nk_data:
        # latlong2d[0][0]
        print(sheet_name)
        print(latlong2d[0])
        # print(latlong2d)

        cs = db.db.cursor()

        cs.execute(f"select districtId from District where name = '{sheet_name}'")
        out = cs.fetchall()
        districtId = out[0][0]

        for row in latlong2d:
            sql = """
            insert into LatLong (lattitude, longtitude, districtId)
            values (%s, %s, %s)
            """
            value = (row[0], row[1], districtId)
            cs.execute(sql, value)
            db.db.commit()

        # df['']
        print()
    

# thread_index = 0

def manageMatchedLatLong(lat, long, db, csv_row, nine_days):
    # global thread_index
    # print(f"start thread[{thread_index}] for manage matched lat long")
    # thread_index += 1
    # +9 becasued if use 2: then it will use till end but if some csv file have more than that lol
    ninesNextDaysWater = csv_row[2:2+9].to_numpy()
    # may be not 9 lol noob csv from website
    pivot_dtll_id = ""
    for k, waterAmount in enumerate(ninesNextDaysWater):
        somenextday = nine_days[k]
        # ---------------------------------------------------------------------------- #
        #                        insert data to DatetimeLatLong                        #
        # ---------------------------------------------------------------------------- #
        # cs = db.db.cursor()
        datetime_id = getDatetimeId(db, somenextday)
        latlong_id = getLatLongId(db, lat, long)
        if not checkIfDatetimeLatLongExistedOnDB(db, datetime_id, latlong_id):
            sql_insert = """
                insert into DatetimeLatLong(datetimeId, latlongId) values (%s, %s)
            """
            val = (datetime_id, latlong_id)
            cs = db.db.cursor()
            cs.execute(sql_insert, val)
            db.db.commit()
        # ---------------------------------------------------------------------------- #
        #                        insert water data to WaterData                        #
        # ---------------------------------------------------------------------------- #
        dtll_id = getDatetimeLatLongId(db, datetime_id, latlong_id)
        sql = ""
        if k > 0:
            sql = f"""
                insert into WaterData (datetimelatlongId, waterAmount, pivot_datetimelatlong_id)
                values (%s, %s, {pivot_dtll_id})
            """
        else:
            pivot_dtll_id = dtll_id
            sql = f"""
                insert into WaterData (datetimelatlongId, waterAmount)
                values (%s, %s)
            """
            
        val = (dtll_id, waterAmount)
        cs = db.db.cursor()
        cs.execute(sql, val)
        db.db.commit()




if __name__ == "__main__":
    print("Start program.")
    db = DB()

    config_file_path = "resources/config.json"
    configfile = open(config_file_path)
    config_data = json.load(configfile)

    latlongs_nk_data = getLatLongOfNakornnayok()

    if config_data["isInitNakornnayokLatLong"] == False:
        insertLatLongDistrictToDB(latlongs_nk_data, db)
        config_data["isInitNakornnayokLatLong"] = True
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f)




    scp = Scrapper()
    dtc_df = scp.getDateTimeCSVDataFrame()
    scp.release()


    
    print(dtc_df)
    # exit()

    # threads = []

    for i, row in dtc_df.iterrows():
        url = row['csv url']
        date = row['date']
        d, m, y = date.split("-")
        time = row['time']

        datev2 = f"{y}-{thaiMonthToMonthOrderStartWithOne(m)}-{d}"
        # datetime = f"{datev2} {time}"
        tsplited = time.split(":")
        datetime = libdatetime(*[int(x) for x in [y, thaiMonthToMonthOrderStartWithOne(m), d, tsplited[0], tsplited[1]]])
        print(f"datetime = {datetime}")

        csv_df = pd.read_csv(url)
        print(f"reading csv {i}")

        nine_days = []
        for k in range(9): # 9 includes today too
            somenextday = getNextNDay(datetime, k)
            createDateOnDBIfNotExisted(somenextday, db)
            nine_days.append(somenextday)

        for j, (sheet_name, latlong2d) in enumerate(latlongs_nk_data):
            ...
            print(f"consider sheet {j} : {sheet_name}")
            for latlong_row in latlong2d:
                lat_nk = latlong_row[0]
                long_nk = latlong_row[1]

                for j, csv_row in csv_df.iterrows():
                    lat_c = csv_row['lat']
                    long_c = csv_row['lon']


                    if lat_nk == lat_c and long_nk == long_c:
                        # trd = Thread(target=manageMatchedLatLong, args=(lat_nk, long_nk, db, csv_row, nine_days))
                        # threads.append(trd)
                        # trd.start()

                        manageMatchedLatLong(lat_nk, long_nk, db, csv_row, nine_days)

        print("--------------------\n")
    # for t in threads:
    #     t.join()
    # print("end of all threads.")