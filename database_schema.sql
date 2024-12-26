-- Adminer 4.8.4 MySQL 11.6.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

CREATE DATABASE `comictracker` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `comictracker`;

CREATE TABLE `series` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `publisher` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `series_fk` int(11) NOT NULL,
  `issue` int(11) NOT NULL,
  `box` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `series_fk` (`series_fk`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`series_fk`) REFERENCES `series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2024-12-26 18:46:43
