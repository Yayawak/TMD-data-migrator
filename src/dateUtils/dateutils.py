from datetime import datetime as libdatetime
from datetime import timedelta

thai_months = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม"
]

def thaiMonthToMonthOrderStartWithOne(thaimonth:str):
    if thaimonth.strip() not in thai_months:
        print("can t find matcheding thai month to indexing...")
        print("input = " + thaimonth)
        print("and thai_months are ...")
        print(thai_months)
        exit(0)
    for i in range(len(thai_months)):
        m = thai_months[i]
        if m == thaimonth:
            return i + 1
        
# def isDatetimeExistedInDatatimeRecordTable(datetimestr:str, db):
def isDatetimeExistedInDatatimeRecordTable(datetime:libdatetime, db):
    cs = db.db.cursor()
    cs.execute("select datetime from DatetimeRecord;")
    for x in cs.fetchall():
        dt: libdatetime = x[0]
        # dt.
        # print(x)
        dtformat = dt.strftime("%Y-%-m-%d %H:%M:%S")
        # print(f"{datetimestr} vs {dtformat}")
        if datetime.strftime("%Y-%-m-%d %H:%M:%S") == dtformat:
            return True
    return False


# def createDateOnDBIfNotExisted(datetimestr:str, db):
def createDateOnDBIfNotExisted(datetime:libdatetime, db):
    if isDatetimeExistedInDatatimeRecordTable(datetime, db):
        ...
        # print(f"date {datetime} already existed on db.")
        # exit()
    else:
        cs = db.db.cursor()
        sql = "insert into DatetimeRecord(datetime) values (%s);"
        # libdatetime()
        dtformat = datetime.strftime("%Y-%-m-%d %H:%M:%S")
        val = (dtformat,)
        cs.execute(sql, val)
        db.db.commit()
        print(f"inserted {datetime} to DatetimeRecord.")
    
    
# def datestr_to_formatdatetime(datestr)


def getNextNDay(dt:libdatetime, n):
    # n should be 1 -> 9
    return dt + timedelta(n)
