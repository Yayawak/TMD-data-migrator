# import sys
# sys.path.insert(0, "./scrapper")

from src.scrapper.scrapper import Scrapper
from src.nakornnayok_latlong_loader.latlong_loader import getLatLongOfNakornnayok
from src.database.dbconnector import DB
import pandas as pd
from threading import Thread
from datetime import datetime as libdatetime
from datetime import timedelta
from src.dateUtils.dateutils import thaiMonthToMonthOrderStartWithOne, isDatetimeExistedInDatatimeRecordTable, createDateOnDBIfNotExisted,getNextNDay
from src.utils.utils import *

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
            # value = (5, 5, 1)
            value = (row[0], row[1], districtId)
            cs.execute(sql, value)
            db.db.commit()

        # df['']
        print()
    

# def create


if __name__ == "__main__":
    print("Start program.")
    db = DB()
    

    latlongs_nk_data = getLatLongOfNakornnayok()

    # insertLatLongDistrictToDB(latlongs_nk_data, db)

    scp = Scrapper()
    dtc_df = scp.getDateTimeCSVDataFrame()
    scp.release()


    # csv_urls = df['csv url']
    # pd.read_csv(csv_urls[0]).to_csv("out.csv")

    # csv_urls[0]
    # for i, url in enumerate(csv_urls[:3]):


    # for i, row in dtc_df.iterrows():
    #     url = row['csv url']
    #     date = row['date']
    #     time = row['time']
    #     if i > 3:
    #         break
    #     # row['']
    #     print(url)
    # #     csv_df = pd.read_csv(url)
    #     # csv_df.
    #     # print(csv_df)

    #     trd = Thread(target=targetFN, args=(i, url, date, time))
    #     trd.start()
    
    print(dtc_df)
    # exit()

    for i, row in dtc_df.iterrows():
        url = row['csv url']
        date = row['date']
        d, m, y = date.split("-")
        time = row['time']
        # time += ":00"


        datev2 = f"{y}-{thaiMonthToMonthOrderStartWithOne(m)}-{d}"
        # datetime = f"{datev2} {time}"
        tsplited = time.split(":")
        datetime = libdatetime(*[int(x) for x in [y, thaiMonthToMonthOrderStartWithOne(m), d, tsplited[0], tsplited[1]]])
        print(f"datetime = {datetime}")

        csv_df = pd.read_csv(url)
        print(f"reading csv {i}")

        # createDateOnDBIfNotExisted(datetime, db)
        # for k in range(9): # 9 includes today too
        #     somenextday = getNextNDay(datetime, k)
        #     createDateOnDBIfNotExisted(somenextday, db)

        
        # trd = Thread(target=targetFN, args=(i, url, date, time))
        # trd.start()

        # if i > 1:
        #     break

        # datetimeLatLongMatrix = getDatetimeLatLongMatrix(db)
        nine_days = []
        for k in range(9): # 9 includes today too
            somenextday = getNextNDay(datetime, k)
            createDateOnDBIfNotExisted(somenextday, db)
            nine_days.append(somenextday)

        for j, (sheet_name, latlong2d) in enumerate(latlongs_nk_data):
            ...
            print(f"consider sheet {j} : {sheet_name}")
            for latlong_row in latlong2d:
                # lat_nk = latlong_row[0].strip()
                # long_nk = latlong_row[1].strip()
                # for j, csv_row in csv_df.iterrows():
                #     lat_c = csv_row['lat'].strip()
                #     long_c = csv_row['lon'].strip()
                lat_nk = latlong_row[0]
                long_nk = latlong_row[1]

                for j, csv_row in csv_df.iterrows():
                    lat_c = csv_row['lat']
                    long_c = csv_row['lon']


                    if lat_nk == lat_c and long_nk == long_c:
                        # print(f"matched latlon \n\t{lat_nk}\n\t{long_nk}")

                        # print(f"matched latlon {lat_nk} | {long_nk}", end="")
                        # print(f"\n\t {datetime}", end="")
                        # +9 becasued if use 2: then it will use till end but if some csv file have more than that lol
                        ninesNextDaysWater = csv_row[2:2+9].to_numpy()
                        # print(f"\t{ninesNextDaysWater}")


                        # for k in range(len(ninesNextDaysWater)):
                        # print(f"\t{csv_row[3:]}")
                        # print(f"\t{csv_row[3:][0]}")

                        # createDateOnDBIfNotExisted(datetime, db)

                        # for k in range(9): # 9 includes today too
                        # may be not 9 lol noob csv from website
                        for k, waterAmount in enumerate(ninesNextDaysWater):
                            # print(nine_days)
                            # print(k)
                            # print(ninesNextDaysWater)
                            somenextday = nine_days[k]
                            # ---------------------------------------------------------------------------- #
                            #                        insert data to DatetimeLatLong                        #
                            # ---------------------------------------------------------------------------- #
                            # print(ninesNextDaysWater)
                            # waterAmount = ninesNextDaysWater[k]
                            

                            cs = db.db.cursor()
                            datetime_id = getDatetimeId(db, somenextday)
                            latlong_id = getLatLongId(db, lat_nk, long_nk)
                            if not checkIfDatetimeLatLongExistedOnDB(db, datetime_id, latlong_id):
                                sql_insert = """
                                    insert into DatetimeLatLong(datetimeId, latlongId) values (%s, %s)
                                """
                                val = (datetime_id, latlong_id)
                                cs.execute(sql_insert, val)
                                db.db.commit()

                                # cs.execute("select last_insert_id()")
                                # ddll_inserted_id = cs.fetchone()[0]
                                # print(ddll_inserted_id)

                                # exit()
                            else:
                                # print(f"these datetimelatlong pair id date[{datetime_id}] & ll[{latlong_id}] was found on db -> dont create new !!!!!")
                                ...
                                # exit()
                            

                            # ---------------------------------------------------------------------------- #
                            #                        insert water data to WaterData                        #
                            # ---------------------------------------------------------------------------- #

                            dtll_id = getDatetimeLatLongId(db, datetime_id, latlong_id)
                            sql = """
                                insert into WaterData (datetimelatlongId, waterAmount)
                                values (%s, %s)
                            """
                            val = (dtll_id, waterAmount)
                            cs.execute(sql, val)
                            db.db.commit()




                        # csv_row
                        
                        # read next 9 days
            print()
        print("--------------------\n")