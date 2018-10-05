-- MySQL dump 10.16  Distrib 10.3.9-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: packMan
-- ------------------------------------------------------
-- Server version	10.3.9-MariaDB-1:10.3.9+maria~bionic-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `packMan`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `packMan` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `packMan`;

--
-- Table structure for table `pM_DigitalInputs`
--

DROP TABLE IF EXISTS `pM_DigitalInputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pM_DigitalInputs` (
  `s_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `inputID` int(10) unsigned NOT NULL DEFAULT 0,
  `state` bit(1) NOT NULL DEFAULT b'0',
  `description` tinytext NOT NULL DEFAULT '0',
  PRIMARY KEY (`s_id`),
  UNIQUE KEY `inputID` (`inputID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='Statustabelle';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pM_DigitalInputs`
--

LOCK TABLES `pM_DigitalInputs` WRITE;
/*!40000 ALTER TABLE `pM_DigitalInputs` DISABLE KEYS */;
INSERT INTO `pM_DigitalInputs` VALUES (1,0,'\0','\0'),(2,1,'\0','0'),(3,2,'\0','0'),(4,3,'\0','0'),(5,4,'\0','0'),(6,5,'\0','0'),(7,6,'\0','0'),(8,7,'\0','0');
/*!40000 ALTER TABLE `pM_DigitalInputs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pM_Events`
--

DROP TABLE IF EXISTS `pM_Events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pM_Events` (
  `ev_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `eventtext` tinytext NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  KEY `ev_id` (`ev_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pM_Events`
--

LOCK TABLES `pM_Events` WRITE;
/*!40000 ALTER TABLE `pM_Events` DISABLE KEYS */;
INSERT INTO `pM_Events` VALUES (1,'Input switched to HIGH','A Digital-Input switched to HIGH signals an inbound Package'),(2,'Input switched to LOW','A Digital-Input switched to LOW signals a Package fetched by someone'),(3,'E-Mail -Package inbound- sent','An E-Mail notifying an inbound Package has been sent'),(4,'E-Mail -Package fetched - sent','An E-Mail notifying an fetched Package has been sent'),(5,'packMan-Sensor started','The sensor-software on the Raspberry-Pi has been started'),(6,'Frontend accessed','The Webfrontend was accessed. Log-Extra-info may contain the IP-Adress');
/*!40000 ALTER TABLE `pM_Events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pM_Logs`
--

DROP TABLE IF EXISTS `pM_Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pM_Logs` (
  `l_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ev_id` int(10) unsigned NOT NULL DEFAULT 0,
  `extra_info` varchar(255) DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`l_id`),
  KEY `FK_pM_Logs_pM_Events` (`ev_id`),
  CONSTRAINT `FK_pM_Logs_pM_Events` FOREIGN KEY (`ev_id`) REFERENCES `pM_Events` (`ev_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Protokollierung';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pM_Logs`
--

LOCK TABLES `pM_Logs` WRITE;
/*!40000 ALTER TABLE `pM_Logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `pM_Logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pM_MailNotify`
--

DROP TABLE IF EXISTS `pM_MailNotify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pM_MailNotify` (
  `pk_MailingID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Mailaddress` varchar(255) NOT NULL,
  `Messagetext` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pk_MailingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pM_MailNotify`
--

LOCK TABLES `pM_MailNotify` WRITE;
/*!40000 ALTER TABLE `pM_MailNotify` DISABLE KEYS */;
/*!40000 ALTER TABLE `pM_MailNotify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pM_definitions`
--

DROP TABLE IF EXISTS `pM_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pM_definitions` (
  `d_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `AName` tinytext NOT NULL,
  `DigitalInput` int(10) unsigned NOT NULL,
  `fk_MailID` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`d_id`),
  KEY `FK_pM_definitions_pM_DigitalInputs` (`DigitalInput`),
  KEY `pM_definitions_pM_MailNotify_FK` (`fk_MailID`),
  CONSTRAINT `FK_pM_definitions_pM_DigitalInputs` FOREIGN KEY (`DigitalInput`) REFERENCES `pM_DigitalInputs` (`inputID`),
  CONSTRAINT `pM_definitions_pM_MailNotify_FK` FOREIGN KEY (`fk_MailID`) REFERENCES `pM_MailNotify` (`pk_MailingID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='Definitionstabelle fuer Abteilungen';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pM_definitions`
--

LOCK TABLES `pM_definitions` WRITE;
/*!40000 ALTER TABLE `pM_definitions` DISABLE KEYS */;
INSERT INTO `pM_definitions` VALUES (1,'IT/Controlling',0,NULL),(2,'Betriebsinstandhaltung/ Facility Management',1,NULL),(3,'Werkzeugbau',2,NULL),(4,'Einkauf',3,NULL),(5,'Halle1',4,NULL),(6,'Halle2',5,NULL),(7,'Halle3',6,NULL),(8,'Werkzeuglager',7,NULL),(9,'SCM',0,NULL),(10,'Qualitätswesen',0,NULL),(11,'Personalwesen',0,NULL),(12,'Finanzbuchhaltung',0,NULL),(13,'Vertriebs/ Kundenmanagement, Marketing',0,NULL),(14,'Materiallager',0,NULL);
/*!40000 ALTER TABLE `pM_definitions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-05  6:37:26
