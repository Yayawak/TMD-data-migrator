-- tmd_water_db.DatetimeRecord definition

CREATE TABLE `DatetimeRecord` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- tmd_water_db.District definition

CREATE TABLE `District` (
  `districtId` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`districtId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- tmd_water_db.LatLong definition

CREATE TABLE `LatLong` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `lattitude` double NOT NULL,
  `longtitude` double NOT NULL,
  `districtId` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LatLong_District_FK` (`districtId`),
  CONSTRAINT `LatLong_District_FK` FOREIGN KEY (`districtId`) REFERENCES `District` (`districtId`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- tmd_water_db.DatetimeLatLong definition

CREATE TABLE `DatetimeLatLong` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `datetimeId` int unsigned NOT NULL,
  `latlongid` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DatetimeLatLong_LatLong_FK` (`latlongid`),
  KEY `DatetimeLatLong_DatetimeRecord_FK` (`datetimeId`),
  CONSTRAINT `DatetimeLatLong_DatetimeRecord_FK` FOREIGN KEY (`datetimeId`) REFERENCES `DatetimeRecord` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `DatetimeLatLong_LatLong_FK` FOREIGN KEY (`latlongid`) REFERENCES `LatLong` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7404 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- tmd_water_db.WaterData definition

CREATE TABLE `WaterData` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `datetimelatlongId` int unsigned NOT NULL,
  `waterAmount` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `WaterData_DatetimeLatLong_FK` (`datetimelatlongId`),
  CONSTRAINT `WaterData_DatetimeLatLong_FK` FOREIGN KEY (`datetimelatlongId`) REFERENCES `DatetimeLatLong` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43730 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;