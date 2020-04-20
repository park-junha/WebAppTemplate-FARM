DROP DATABASE IF EXISTS SampleInventory;
CREATE DATABASE IF NOT EXISTS SampleInventory;
USE SampleInventory;

DROP TABLE IF EXISTS Inventory;
CREATE TABLE IF NOT EXISTS Inventory (
  item_uid INT NOT NULL AUTO_INCREMENT
  , item_name VARCHAR(64) UNIQUE
  , quantity INT
  , PRIMARY KEY (item_uid)
)
;

INSERT INTO Inventory
(
  item_name
  , quantity
)
VALUES
(
  'Apple'
  , 3
)
;
