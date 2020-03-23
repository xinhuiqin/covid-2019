-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: covid_2019
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `china_day_list`
--

DROP TABLE IF EXISTS `china_day_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `china_day_list` (
  `ds` date NOT NULL COMMENT '日期',
  `confirm` int(11) NOT NULL COMMENT '累计确诊',
  `suspect` int(11) NOT NULL COMMENT '现有疑似',
  `dead` int(11) NOT NULL COMMENT '累计死亡',
  `heal` int(11) NOT NULL COMMENT '累计治愈',
  `now_confirm` int(11) NOT NULL COMMENT '当前确诊',
  `now_severe` int(11) NOT NULL COMMENT '当前重症',
  `imported_case` int(11) NOT NULL COMMENT '累计输入病例',
  `dead_rate` float NOT NULL COMMENT '死亡率',
  `heal_rate` float NOT NULL COMMENT '治愈率',
  `add_confirm` int(11) NOT NULL COMMENT '新增确诊',
  `add_suspect` int(11) NOT NULL COMMENT '新增疑似',
  `add_dead` int(11) NOT NULL COMMENT '新增死亡',
  `add_heal` int(11) NOT NULL COMMENT '新增治愈',
  `add_imported_case` int(11) NOT NULL COMMENT '新增输入病例',
  PRIMARY KEY (`ds`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `china_day_list`
--

LOCK TABLES `china_day_list` WRITE;
/*!40000 ALTER TABLE `china_day_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `china_day_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provience_day_list`
--

DROP TABLE IF EXISTS `provience_day_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provience_day_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provience` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '省',
  `city` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '市',
  `confirm` int(11) NOT NULL COMMENT '累计确诊',
  `confirm_add` int(11) NOT NULL COMMENT '新增确诊',
  `heal` int(11) NOT NULL COMMENT '累计治愈',
  `dead` int(11) NOT NULL COMMENT '累计死亡',
  `update_time` datetime NOT NULL COMMENT '数据最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provience_day_list`
--

LOCK TABLES `provience_day_list` WRITE;
/*!40000 ALTER TABLE `provience_day_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `provience_day_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-23 15:27:43
