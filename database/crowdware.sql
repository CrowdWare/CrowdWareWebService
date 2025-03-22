DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `uuid` char(52) NOT NULL,
  `email` varchar(250) NOT NULL,
  `publisher` varchar(250) NOT NULL,
  `bio` varchar(250) NOT NULL,
  `locale` varchar(2) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `uuid` char(52) NOT NULL,
  `type` enum('course','book') NOT NULL,
  `name` char(250) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `pictureurl` varchar(250) NOT NULL,
  `account` char(52) NOT NULL,
  `locale` varchar(2) NOT NULL,
  `date` datetime DEFAULT NULL,
  `url` varchar(250) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `account` (`account`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`account`) REFERENCES `account` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;



INSERT INTO `account`(uuid,email,publisher,bio,locale,date) VALUES ('1c0bf2f6-0ba3-4183-9847-f98c947fcad2','japp.olaf@gmail.com','Adam Art Ananda','Bio','de',NOW());
INSERT INTO `item` (uuid,type,description,account,locale,date,pictureurl, url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc05','book',"**Die Reise zum wahren Leben** *Adam Art Ananda* Neuauflage von 'Die Kunst zu Leben und zu Lieben' Eigentlich habe ich es für meinen Sohn geschrieben. Da Du aber auch ein Sohn bist könnte es ja auch für Dich interessant sein, und wenn nicht, ist es ja auch nicht so schlimm.",'1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'');
INSERT INTO `item` (uuid,type,description,account,locale,date,pictureurl, url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc04','book','**Spiel des Leben** *Adam Art Ananda* Hier findest Du mehrere Bücher in einem Band. Du kannst in diesem Buch Deinen eigenen Weg wählen. Das erste interaktive Buch, das wir mit dem Free-Book-Designer her gestellt haben. Es dient auch als Beispiel des Machbaren.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'https://github.com/CrowdWare/FreeBookReader/blob/main/docs/images/SpielDesLebens.png','');
INSERT INTO `item` (uuid,type,description,account,locale,date,pictureurl, url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc03','book','**Spiel des Leben** *Adam Art Ananda* Hier findest Du mehrere Bücher in einem Band. Du kannst in diesem Buch Deinen eigenen Weg wählen. Das erste interaktive Buch, das wir mit dem Free-Book-Designer her gestellt haben. Es dient auch als Beispiel des Machbaren.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'https://github.com/CrowdWare/FreeBookReader/blob/main/docs/images/DieReiseZumWahrenLeben.png','');
INSERT INTO `item` (uuid,type,description,account,locale,date,pictureurl, url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc02','book','**Spiel des Leben** *Adam Art Ananda* Hier findest Du mehrere Bücher in einem Band. Du kannst in diesem Buch Deinen eigenen Weg wählen. Das erste interaktive Buch, das wir mit dem Free-Book-Designer her gestellt haben. Es dient auch als Beispiel des Machbaren.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'https://github.com/CrowdWare/FreeBookReader/blob/main/docs/images/DieReiseZumWahrenLeben.png','');
INSERT INTO `item` (uuid,type,description,account,locale,date, pictureurl, url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc01','book','**Spiel des Leben** *Adam Art Ananda* Hier findest Du mehrere Bücher in einem Band. Du kannst in diesem Buch Deinen eigenen Weg wählen. Das erste interaktive Buch, das wir mit dem Free-Book-Designer her gestellt haben. Es dient auch als Beispiel des Machbaren.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'https://github.com/CrowdWare/FreeBookReader/blob/main/docs/images/DieReiseZumWahrenLeben.png','');

