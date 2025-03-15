
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `uuid` char(52) NOT NULL,
  `email` varchar(250) NOT NULL,
  `publisher` varchar(250) NOT NULL,
  `locale` varchar(2) NOT NULL,
  `license` char(7) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `uuid` char(52) NOT NULL,
  `name` varchar(250) NOT NULL,
  `pwd` varchar(250) NOT NULL,
  `email` varchar(250) NOT NULL,
  `dob` datetime NOT NULL,
  `locale` varchar(2) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `uuid` char(52) NOT NULL,
  `type` enum('course','book') NOT NULL,
  `name` char(250) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `account` char(52) NOT NULL,
  `locale` varchar(2) NOT NULL,
  `date` datetime DEFAULT NULL,
  `url` varchar(250) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `account` (`account`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`account`) REFERENCES `account` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `session_data`;
CREATE TABLE `session_data` (
  `session_id` varchar(128) NOT NULL,
  `user_uuid` varchar(36) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `subtopic`;
CREATE TABLE `subtopic` (
  `uuid` char(52) NOT NULL,
  `name` char(250) NOT NULL,
  `sortorder` int NOT NULL,
  `topic` char(52) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `topic` (`topic`),
  CONSTRAINT `subtopic_ibfk_1` FOREIGN KEY (`topic`) REFERENCES `topic` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `subtopic_readed`;
CREATE TABLE `subtopic_readed` (
  `uuid` char(52) NOT NULL,
  `subtopic` char(52) NOT NULL,
  `account` char(52) NOT NULL,
  `readed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uuid`),
  KEY `subtopic` (`subtopic`),
  KEY `account` (`account`),
  CONSTRAINT `subtopic_readed_ibfk_1` FOREIGN KEY (`subtopic`) REFERENCES `subtopic` (`uuid`),
  CONSTRAINT `subtopic_readed_ibfk_2` FOREIGN KEY (`account`) REFERENCES `account` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  `uuid` char(52) NOT NULL,
  `name` char(250) NOT NULL,
  `page` char(250) NOT NULL,
  `sortorder` int NOT NULL,
  `item` char(52) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `item` (`item`),
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`item`) REFERENCES `item` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


DROP TABLE IF EXISTS `topic_readed`;
CREATE TABLE `topic_readed` (
  `uuid` char(52) NOT NULL,
  `topic` char(52) NOT NULL,
  `account` char(52) NOT NULL,
  `readed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uuid`),
  KEY `topic` (`topic`),
  KEY `account` (`account`),
  CONSTRAINT `topic_readed_ibfk_1` FOREIGN KEY (`topic`) REFERENCES `topic` (`uuid`),
  CONSTRAINT `topic_readed_ibfk_2` FOREIGN KEY (`account`) REFERENCES `account` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;