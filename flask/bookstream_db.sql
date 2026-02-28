-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2026 at 09:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookstream_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `price`, `image_url`, `description`) VALUES
(5, 'The Great Gatsby', 'F. Scott Fitzgerald', 15.97, '/static/images/GreatGatsby.webp', 'A classic tale of obsession, wealth, and the elusive American Dream in the Roaring Twenties.'),
(6, 'Atomic Habits', 'James Clear', 22.50, '/static/images/AtomicHabits.jpg', 'An easy and proven way to build good habits and break bad ones with tiny daily changes.'),
(7, 'The Alchemist', 'James Clear', 22.50, '/static/images/TheAlchemist.jpg', 'A magical story about Santiago, a shepherd boy who travels to Egypt in search of treasure.'),
(8, '1984', 'George Orwell', 12.99, '/static/images/1984.jpg', 'A chilling dystopian novel about government surveillance, totalitarianism, and thought control.'),
(9, 'Meditations', 'Marcus Aurelius', 18.00, '/static/images/Meditations.webp', 'Timeless stoic wisdom from the Roman Emperor on how to live a virtuous and peaceful life.'),
(10, 'The Silent Patient', 'Alex Michaelides', 19.99, '/static/images/Thesilentpatient.png', 'A shocking psychological thriller about a woman who shoots her husband and never speaks again.'),
(11, 'Sapiens', 'Yuval Noah Harari', 25.00, '/static/images/Sapiens.jpg', 'A brief history of humankind, exploring how biology and history have defined us.'),
(12, 'Deep Work', 'Cal Newport', 20.00, '/static/images/Deepwork.jpg', 'Rules for focused success in a distracted world, teaching you how to master difficult skills.'),
(13, 'Dune', 'Frank Herbert', 21.50, '/static/images/Dune.jpg', 'The epic sci-fi masterpiece about politics, religion, and power on the desert planet Arrakis.'),
(14, 'The Psychology of Money', 'Morgan Housel', 17.50, '/static/images/money.jpg', 'Timeless lessons on wealth, greed, and happiness, focusing on the human side of finance.'),
(15, 'Ikigai', 'Hector Garcia', 16.00, '/static/images/ikigai.jpg', 'The Japanese secret to a long and happy life by finding your true purpose every single day.');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `book_id`, `total_price`, `created_at`) VALUES
(9, 2, 6, 22.50, '2026-02-27 17:05:59'),
(10, 2, 7, 22.50, '2026-02-27 17:05:59'),
(11, 2, 12, 20.00, '2026-02-27 17:05:59'),
(12, 2, 14, 17.50, '2026-02-27 17:05:59'),
(13, 2, 15, 16.00, '2026-02-27 17:05:59');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `full_name`, `email`, `password`, `role`) VALUES
(1, 'merit baidya', 'mbhollowman@gmail.com', 'asasas', 'admin'),
(2, 'yugal', 'yugal@gmail.com', 'yugal1', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user` (`user_id`),
  ADD KEY `idx_book` (`book_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
