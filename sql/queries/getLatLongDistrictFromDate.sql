select wd.waterAmount, dr.`datetime`,
ll.lattitude,
ll.longtitude,
dst.name 
from WaterData wd 
join DatetimeLatLong dll on wd.datetimelatlongId = dll.id
join DatetimeRecord dr on dr.id = dll.datetimeId
join LatLong ll on ll.id = dll.latlongid 
join District dst on dst.districtId = ll.districtId 
where dr.`datetime` = '2567-03-31 01:00:00'