/*
SQLyog Ultimate v11.11 (32 bit)
MySQL - 5.7.16-ndb-7.5.4-cluster-gpl : Database - weibo
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`weibo` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

/*Table structure for table `content_event` */

DROP TABLE IF EXISTS `content_event`;

CREATE TABLE `content_event` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `content_id` varchar(30) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `con_eve_union` (`content_id`,`event_id`),
  KEY `con_eve_idx` (`content_id`),
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*Table structure for table `emotion_multi` */

DROP TABLE IF EXISTS `emotion_multi`;

CREATE TABLE `emotion_multi` (
  `weibo_id` varchar(100) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `emotion_type` varchar(20) DEFAULT NULL,
  `proportion` float DEFAULT NULL,
  `comment1` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment2` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_date` varchar(20) DEFAULT NULL,
  KEY `weibo_id` (`weibo_id`),
  KEY `event_id` (`event_id`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*Table structure for table `emotion_two` */

DROP TABLE IF EXISTS `emotion_two`;

CREATE TABLE `emotion_two` (
  `weibo_id` varchar(100) DEFAULT NULL,
  `event_id` int(11) DEFAULT NULL,
  `emotion_type` varchar(20) DEFAULT NULL,
  `proportion` float DEFAULT NULL,
  `comment1` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment2` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment3` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_date` varchar(20) DEFAULT NULL,
  KEY `weibo_id` (`weibo_id`),
  KEY `event_id` (`event_id`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*Table structure for table `weibo_content` */

DROP TABLE IF EXISTS `weibo_content`;

CREATE TABLE `weibo_content` (
  `_id` varchar(30) NOT NULL,
  `ID` bigint(20) DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `comment` int(11) DEFAULT NULL,
  `transfer` int(11) DEFAULT NULL,
  `praise` int(11) DEFAULT NULL,
  `pubtime` varchar(20) DEFAULT NULL,
  `tools` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*Table structure for table `weibo_event` */

DROP TABLE IF EXISTS `weibo_event`;

CREATE TABLE `weibo_event` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `tag` varchar(45) DEFAULT NULL,
  `start_time` varchar(45) DEFAULT NULL,
  `recent_time` varchar(45) DEFAULT NULL,
  `hot` longtext,
  `keywords` varchar(800) DEFAULT NULL,
  `max_hot` float DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `EVENT_NAME` (`name`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*Table structure for table `weibo_user` */

DROP TABLE IF EXISTS `weibo_user`;

CREATE TABLE `weibo_user` (
  `_id` bigint(20) NOT NULL,
  `city` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num_fans` int(11) DEFAULT NULL,
  `province` varchar(20) DEFAULT NULL,
  `signature` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `url` varchar(50) DEFAULT NULL,
  `num_follows` int(11) DEFAULT NULL,
  `num_tweets` int(11) DEFAULT NULL,
  `influence` float NOT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `keywords` varchar(800) DEFAULT NULL,
  `credentials` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=ndbcluster DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
