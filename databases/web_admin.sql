CREATE DATABASE `admin` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE `admin`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT null auto_increment,
  `username` varchar(255) unique ,
  `password` varchar(255),
  `token` varchar(255),
  `token_expire` datetime,
  `created` datetime default NOW(),
  `authorization` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

insert into user (id, username, password, authorization) values (0, 'root', 'ecb218586e4d3688c9e742e537eff6f0', 'admin');
