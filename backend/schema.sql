DROP TABLE IF EXISTS `Movie_has_Genre`;
DROP TABLE IF EXISTS `Genre`;
DROP TABLE IF EXISTS `Movie_has_Actor`;
DROP TABLE IF EXISTS `Actor`;
DROP TABLE IF EXISTS `Movie_has_Writer`;
DROP TABLE IF EXISTS `Writer`;
DROP TABLE IF EXISTS `Trailer`;
DROP TABLE IF EXISTS `Movie`;
DROP TABLE IF EXISTS `Director`;

CREATE TABLE `Director` (

  `director_id` int NOT NULL,

  `director_fname` varchar(50) DEFAULT NULL,

  `director_lname` varchar(50) DEFAULT NULL,

  `director_img_url` text,

  `director_popular` float DEFAULT NULL,

  `director_mname` varchar(50) DEFAULT NULL,

  PRIMARY KEY (`director_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Movie` (

  `movie_id` int NOT NULL,

  `movie_title` varchar(255) NOT NULL,

  `movie_overview` text,

  `movie_release_date` date DEFAULT NULL,

  `movie_img_url` text,

  `movie_rating` float DEFAULT NULL,

  `director_id` int NOT NULL,

  `movie_popular` float DEFAULT NULL,

  PRIMARY KEY (`movie_id`),

  KEY `director_id` (`director_id`),

  CONSTRAINT `Movie_ibfk_1` FOREIGN KEY (`director_id`) REFERENCES `Director` (`director_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Actor` (

  `actor_id` int NOT NULL,

  `actor_fname` varchar(50) DEFAULT NULL,

  `actor_lname` varchar(50) DEFAULT NULL,

  `actor_mname` varchar(50) DEFAULT NULL,

  `actor_img_url` text,

  `actor_popular` float DEFAULT NULL,

  PRIMARY KEY (`actor_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Movie_has_Actor` (

  `movie_id` int NOT NULL,

  `actor_id` int NOT NULL,

  PRIMARY KEY (`movie_id`,`actor_id`),

  KEY `actor_id` (`actor_id`),

  CONSTRAINT `Movie_has_Actor_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`),

  CONSTRAINT `Movie_has_Actor_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `Actor` (`actor_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Genre` (

  `genre_id` int NOT NULL,

  `genre_title` varchar(50) NOT NULL,

  PRIMARY KEY (`genre_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Movie_has_Genre` (

  `movie_id` int NOT NULL,

  `genre_id` int NOT NULL,

  PRIMARY KEY (`movie_id`,`genre_id`),

  KEY `genre_id` (`genre_id`),

  CONSTRAINT `Movie_has_Genre_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`),

  CONSTRAINT `Movie_has_Genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `Genre` (`genre_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Writer` (

  `writer_id` int NOT NULL,

  `writer_fname` varchar(50) DEFAULT NULL,

  `writer_mname` varchar(50) DEFAULT NULL,

  `writer_img_url` text,

  `writer_popular` float DEFAULT NULL,

  `writer_lname` varchar(50) DEFAULT NULL,

  PRIMARY KEY (`writer_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Movie_has_Writer` (

  `movie_id` int NOT NULL,

  `writer_id` int NOT NULL,

  PRIMARY KEY (`movie_id`,`writer_id`),

  KEY `writer_id` (`writer_id`),

  CONSTRAINT `Movie_has_Writer_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`),

  CONSTRAINT `Movie_has_Writer_ibfk_2` FOREIGN KEY (`writer_id`) REFERENCES `Writer` (`writer_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Trailer` (

  `trailer_id` VARCHAR(255) NOT NULL,

  `movie_id` INT NOT NULL,

  PRIMARY KEY (`trailer_id`),

  FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (

  `user_id` INT NOT NULL AUTO_INCREMENT,

  `username` VARCHAR(50) NOT NULL,

  `password` VARCHAR(255) NOT NULL,

  `email` VARCHAR(255) NOT NULL,

  PRIMARY KEY (`user_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

