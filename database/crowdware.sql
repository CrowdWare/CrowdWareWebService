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
  `account` char(52) NOT NULL,
  `locale` varchar(2) NOT NULL,
  `date` datetime DEFAULT NULL,
  `url` varchar(250) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `account` (`account`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`account`) REFERENCES `account` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;



INSERT INTO `account`(uuid,email,publisher,bio,locale,date) VALUES ('1c0bf2f6-0ba3-4183-9847-f98c947fcad2','japp.olaf@gmail.com','Adam Art Ananda','Bio','de',NOW());
INSERT INTO `item` (uuid,type,name,description,account,locale,date,url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc05','book','Die Reise zum wahren Leben - Erwachen in einer neuen Welt','Die Reise zum wahren Leben: Erwachen in einer neuen Welt” In einer Zeit, in der die Welt von Krisen und Konflikten geprägt ist, ruft dieses Buch zu einem tiefen Umdenken auf. Es ist eine Einladung, die eigenen Wahrnehmungen zu hinterfragen und die innere Wahrheit zu entdecken. In einer Mischung aus persönlicher Erfahrung, spirituellen Erkenntnissen und visionären Gedanken beschreibt der Autor den Weg zu einer Gesellschaft des Teilens, der Verbundenheit und des Friedens. Mit einer klaren Vision für eine bessere Zukunft, in der der Mensch nicht mehr als Konsument, sondern als Teil des großen Ganzen lebt, zeigt dieses Buch auf, wie wir die Herausforderungen unserer Zeit mit Liebe, Achtsamkeit und einem gemeinsamen Bewusstsein überwinden können. Es ist ein Aufruf zur Selbstermächtigung und zur Verantwortung für das Wohl aller – eine Einladung, die Reise zu sich selbst zu beginnen und aktiv eine Welt zu schaffen, in der jeder Mensch in Fülle, Freiheit und Harmonie leben kann. “Die Reise zum wahren Leben” ist mehr als nur ein Buch. Es ist ein Geschenk. Ein Geschenk, das die Hoffnung auf eine neue Ära entfacht – eine Ära des Altruismus, der Zusammenarbeit und der unerschütterlichen Überzeugung, dass eine bessere Welt möglich ist.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'');
INSERT INTO `item` (uuid,type,name,description,account,locale,date,url) VALUES ('3171ac3f-b51a-464c-bb9d-690c4b28dc04','book','Spiel des Lebens','Mit diesem FreeBook möchten wir Dir die Geschichte deines Lebens erzählen. Du kannst während des Lesens deine eigene Geschichte erleben, denn Du hast die Wahl. In diesem Buch wirken mehrere Autoren mit und geben dir einige Möglichkeiten zur Auswahl, in welche Richtung wir weiter gehen könnten als Menschheit. Du entscheidest welchen Weg Du gehen willst. Und dieses Buch hilft Dir dabei, Entscheidungen zu treffen. Lass Dich von uns überraschen. Möchtest Du Deinen ganz eigenen Weg hier beschreiben, dann melde Dich bitte bei uns.','1c0bf2f6-0ba3-4183-9847-f98c947fcad2','de',NOW(),'');
