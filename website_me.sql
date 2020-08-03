-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2020 at 09:35 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `website_me`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `subject` text NOT NULL,
  `msg` text NOT NULL,
  `dt_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`id`, `name`, `email`, `subject`, `msg`, `dt_time`) VALUES
(21, 'Sample Name', 'dhruvashaw@gmail.com', 'Sample Subject!', 'Sample Message', '2020-04-17 11:51:29'),
(23, 'Sample Name', 'cuberseastindiaopen@gmail.com', 'Sample Subject!', 'Sample Message', '2020-04-17 13:49:50'),
(26, 'Sample Name', 'swapnashaw.ss@gmail.com', 'Sample Subject!', 'Sample Message', '2020-04-17 13:49:53'),
(27, 'Dhruva Shaw', 'dhruvashaw@gmail.com', 'thjrfhdh', 'dhdhdhds', '2020-04-21 12:39:38');

-- --------------------------------------------------------

--
-- Table structure for table `cover`
--

CREATE TABLE `cover` (
  `id` int(11) NOT NULL,
  `header` varchar(250) NOT NULL DEFAULT 'Dhruva Shaw',
  `body` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cover`
--

INSERT INTO `cover` (`id`, `header`, `body`) VALUES
(1, 'Welcome', 'I am Dhruva Shaw, a cuber, student from Kolkata, India. and I love cubing.');

-- --------------------------------------------------------

--
-- Table structure for table `passwordtracker`
--

CREATE TABLE `passwordtracker` (
  `id` int(11) NOT NULL,
  `website` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `dt_time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `passwordtracker`
--

INSERT INTO `passwordtracker` (`id`, `website`, `username`, `password`, `dt_time`) VALUES
(1, 'Google', 'dhruvashaw@gmail.com', 'cube12345?', '2020-04-20 10:39:51'),
(5, 'GitHub', 'dhruvashaw@gmail.com (Dhruvacube)', 'cube12345?', '2020-04-20 11:08:54'),
(7, 'Yahoo', 'dhruvashaw@yahoo.com', 'cube12345', '2020-04-20 11:13:13'),
(8, 'WCA', '2016SHAW01', 'cube12345?', '2020-04-21 12:37:57');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cover`
--
ALTER TABLE `cover`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `passwordtracker`
--
ALTER TABLE `passwordtracker`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `cover`
--
ALTER TABLE `cover`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `passwordtracker`
--
ALTER TABLE `passwordtracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
