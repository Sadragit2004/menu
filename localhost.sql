-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 27, 2026 at 01:06 PM
-- Server version: 11.4.5-MariaDB-cll-lve
-- PHP Version: 8.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jldgbolx_web`
--
CREATE DATABASE IF NOT EXISTS `jldgbolx_web` DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;
USE `jldgbolx_web`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Category', 6, 'add_category'),
(22, 'Can change Category', 6, 'change_category'),
(23, 'Can delete Category', 6, 'delete_category'),
(24, 'Can view Category', 6, 'view_category'),
(25, 'Can add نرخ ارز', 7, 'add_exchangerate'),
(26, 'Can change نرخ ارز', 7, 'change_exchangerate'),
(27, 'Can delete نرخ ارز', 7, 'delete_exchangerate'),
(28, 'Can view نرخ ارز', 7, 'view_exchangerate'),
(29, 'Can add food', 8, 'add_food'),
(30, 'Can change food', 8, 'change_food'),
(31, 'Can delete food', 8, 'delete_food'),
(32, 'Can view food', 8, 'view_food'),
(33, 'Can add غذای کاستوم رستوران', 9, 'add_foodrestaurant'),
(34, 'Can change غذای کاستوم رستوران', 9, 'change_foodrestaurant'),
(35, 'Can delete غذای کاستوم رستوران', 9, 'delete_foodrestaurant'),
(36, 'Can view غذای کاستوم رستوران', 9, 'view_foodrestaurant'),
(37, 'Can add Menu Category', 10, 'add_menucategory'),
(38, 'Can change Menu Category', 10, 'change_menucategory'),
(39, 'Can delete Menu Category', 10, 'delete_menucategory'),
(40, 'Can view Menu Category', 10, 'view_menucategory'),
(41, 'Can add بازدید منو', 11, 'add_menuview'),
(42, 'Can change بازدید منو', 11, 'change_menuview'),
(43, 'Can delete بازدید منو', 11, 'delete_menuview'),
(44, 'Can view بازدید منو', 11, 'view_menuview'),
(45, 'Can add restaurant', 12, 'add_restaurant'),
(46, 'Can change restaurant', 12, 'change_restaurant'),
(47, 'Can delete restaurant', 12, 'delete_restaurant'),
(48, 'Can view restaurant', 12, 'view_restaurant'),
(49, 'Can add menu paper desien', 13, 'add_menupaperdesien'),
(50, 'Can change menu paper desien', 13, 'change_menupaperdesien'),
(51, 'Can delete menu paper desien', 13, 'delete_menupaperdesien'),
(52, 'Can view menu paper desien', 13, 'view_menupaperdesien'),
(53, 'Can add درخواست ایجاد منو کاغذی', 14, 'add_requesttocreatepapermenu'),
(54, 'Can change درخواست ایجاد منو کاغذی', 14, 'change_requesttocreatepapermenu'),
(55, 'Can delete درخواست ایجاد منو کاغذی', 14, 'delete_requesttocreatepapermenu'),
(56, 'Can view درخواست ایجاد منو کاغذی', 14, 'view_requesttocreatepapermenu'),
(57, 'Can add نویسنده', 15, 'add_author'),
(58, 'Can change نویسنده', 15, 'change_author'),
(59, 'Can delete نویسنده', 15, 'delete_author'),
(60, 'Can view نویسنده', 15, 'view_author'),
(61, 'Can add مقاله', 16, 'add_blog'),
(62, 'Can change مقاله', 16, 'change_blog'),
(63, 'Can delete مقاله', 16, 'delete_blog'),
(64, 'Can view مقاله', 16, 'view_blog'),
(65, 'Can add  گروه مقاله', 17, 'add_group_blog'),
(66, 'Can change  گروه مقاله', 17, 'change_group_blog'),
(67, 'Can delete  گروه مقاله', 17, 'delete_group_blog'),
(68, 'Can view  گروه مقاله', 17, 'view_group_blog'),
(69, 'Can add more_question', 18, 'add_more_question'),
(70, 'Can change more_question', 18, 'change_more_question'),
(71, 'Can delete more_question', 18, 'delete_more_question'),
(72, 'Can view more_question', 18, 'view_more_question'),
(73, 'Can add meta_tag', 19, 'add_meta_tag'),
(74, 'Can change meta_tag', 19, 'change_meta_tag'),
(75, 'Can delete meta_tag', 19, 'delete_meta_tag'),
(76, 'Can view meta_tag', 19, 'view_meta_tag'),
(77, 'Can add پلن', 20, 'add_plan'),
(78, 'Can change پلن', 20, 'change_plan'),
(79, 'Can delete پلن', 20, 'delete_plan'),
(80, 'Can view پلن', 20, 'view_plan'),
(81, 'Can add ویژگی پلن', 21, 'add_planfeature'),
(82, 'Can change ویژگی پلن', 21, 'change_planfeature'),
(83, 'Can delete ویژگی پلن', 21, 'delete_planfeature'),
(84, 'Can view ویژگی پلن', 21, 'view_planfeature'),
(85, 'Can add سفارش پلن', 22, 'add_planorder'),
(86, 'Can change سفارش پلن', 22, 'change_planorder'),
(87, 'Can delete سفارش پلن', 22, 'delete_planorder'),
(88, 'Can view سفارش پلن', 22, 'view_planorder'),
(89, 'Can add اطلاعات تکمیلی سفارش', 23, 'add_orderdetailinfo'),
(90, 'Can change اطلاعات تکمیلی سفارش', 23, 'change_orderdetailinfo'),
(91, 'Can delete اطلاعات تکمیلی سفارش', 23, 'delete_orderdetailinfo'),
(92, 'Can view اطلاعات تکمیلی سفارش', 23, 'view_orderdetailinfo'),
(93, 'Can add محصول', 24, 'add_product'),
(94, 'Can change محصول', 24, 'change_product'),
(95, 'Can delete محصول', 24, 'delete_product'),
(96, 'Can view محصول', 24, 'view_product'),
(97, 'Can add ویژگی محصول', 25, 'add_productfeature'),
(98, 'Can change ویژگی محصول', 25, 'change_productfeature'),
(99, 'Can delete ویژگی محصول', 25, 'delete_productfeature'),
(100, 'Can view ویژگی محصول', 25, 'view_productfeature'),
(101, 'Can add عکس گالری', 26, 'add_productgallery'),
(102, 'Can change عکس گالری', 26, 'change_productgallery'),
(103, 'Can delete عکس گالری', 26, 'delete_productgallery'),
(104, 'Can view عکس گالری', 26, 'view_productgallery'),
(105, 'Can add سفارش محصول', 27, 'add_productorder'),
(106, 'Can change سفارش محصول', 27, 'change_productorder'),
(107, 'Can delete سفارش محصول', 27, 'delete_productorder'),
(108, 'Can view سفارش محصول', 27, 'view_productorder'),
(109, 'Can add جزئیات سفارش محصول', 28, 'add_productorderdetail'),
(110, 'Can change جزئیات سفارش محصول', 28, 'change_productorderdetail'),
(111, 'Can delete جزئیات سفارش محصول', 28, 'delete_productorderdetail'),
(112, 'Can view جزئیات سفارش محصول', 28, 'view_productorderdetail'),
(113, 'Can add سفارش منو', 29, 'add_ordermenu'),
(114, 'Can change سفارش منو', 29, 'change_ordermenu'),
(115, 'Can delete سفارش منو', 29, 'delete_ordermenu'),
(116, 'Can view سفارش منو', 29, 'view_ordermenu'),
(117, 'Can add عکس منو', 30, 'add_menuimage'),
(118, 'Can change عکس منو', 30, 'change_menuimage'),
(119, 'Can delete عکس منو', 30, 'delete_menuimage'),
(120, 'Can view عکس منو', 30, 'view_menuimage'),
(121, 'Can add پرداخت', 31, 'add_peyment'),
(122, 'Can change پرداخت', 31, 'change_peyment'),
(123, 'Can delete پرداخت', 31, 'delete_peyment'),
(124, 'Can view پرداخت', 31, 'view_peyment'),
(125, 'Can add محتوا', 32, 'add_content'),
(126, 'Can change محتوا', 32, 'change_content'),
(127, 'Can delete محتوا', 32, 'delete_content'),
(128, 'Can view محتوا', 32, 'view_content'),
(129, 'Can add باکس متن و تصویر', 33, 'add_textimageblock'),
(130, 'Can change باکس متن و تصویر', 33, 'change_textimageblock'),
(131, 'Can delete باکس متن و تصویر', 33, 'delete_textimageblock'),
(132, 'Can view باکس متن و تصویر', 33, 'view_textimageblock'),
(133, 'Can add دوره', 34, 'add_course'),
(134, 'Can change دوره', 34, 'change_course'),
(135, 'Can delete دوره', 34, 'delete_course'),
(136, 'Can view دوره', 34, 'view_course'),
(137, 'Can add task result', 35, 'add_taskresult'),
(138, 'Can change task result', 35, 'change_taskresult'),
(139, 'Can delete task result', 35, 'delete_taskresult'),
(140, 'Can view task result', 35, 'view_taskresult'),
(141, 'Can add chord counter', 36, 'add_chordcounter'),
(142, 'Can change chord counter', 36, 'change_chordcounter'),
(143, 'Can delete chord counter', 36, 'delete_chordcounter'),
(144, 'Can view chord counter', 36, 'view_chordcounter'),
(145, 'Can add group result', 37, 'add_groupresult'),
(146, 'Can change group result', 37, 'change_groupresult'),
(147, 'Can delete group result', 37, 'delete_groupresult'),
(148, 'Can view group result', 37, 'view_groupresult'),
(149, 'Can add crontab', 38, 'add_crontabschedule'),
(150, 'Can change crontab', 38, 'change_crontabschedule'),
(151, 'Can delete crontab', 38, 'delete_crontabschedule'),
(152, 'Can view crontab', 38, 'view_crontabschedule'),
(153, 'Can add interval', 39, 'add_intervalschedule'),
(154, 'Can change interval', 39, 'change_intervalschedule'),
(155, 'Can delete interval', 39, 'delete_intervalschedule'),
(156, 'Can view interval', 39, 'view_intervalschedule'),
(157, 'Can add periodic task', 40, 'add_periodictask'),
(158, 'Can change periodic task', 40, 'change_periodictask'),
(159, 'Can delete periodic task', 40, 'delete_periodictask'),
(160, 'Can view periodic task', 40, 'view_periodictask'),
(161, 'Can add periodic task track', 41, 'add_periodictasks'),
(162, 'Can change periodic task track', 41, 'change_periodictasks'),
(163, 'Can delete periodic task track', 41, 'delete_periodictasks'),
(164, 'Can view periodic task track', 41, 'view_periodictasks'),
(165, 'Can add solar event', 42, 'add_solarschedule'),
(166, 'Can change solar event', 42, 'change_solarschedule'),
(167, 'Can delete solar event', 42, 'delete_solarschedule'),
(168, 'Can view solar event', 42, 'view_solarschedule'),
(169, 'Can add clocked', 43, 'add_clockedschedule'),
(170, 'Can change clocked', 43, 'change_clockedschedule'),
(171, 'Can delete clocked', 43, 'delete_clockedschedule'),
(172, 'Can view clocked', 43, 'view_clockedschedule'),
(173, 'Can add مشتری', 44, 'add_customer'),
(174, 'Can change مشتری', 44, 'change_customer'),
(175, 'Can delete مشتری', 44, 'delete_customer'),
(176, 'Can view مشتری', 44, 'view_customer'),
(177, 'Can add روز کاری', 45, 'add_workingday'),
(178, 'Can change روز کاری', 45, 'change_workingday'),
(179, 'Can delete روز کاری', 45, 'delete_workingday'),
(180, 'Can view روز کاری', 45, 'view_workingday'),
(181, 'Can add زمان کاری', 46, 'add_workingtime'),
(182, 'Can change زمان کاری', 46, 'change_workingtime'),
(183, 'Can delete زمان کاری', 46, 'delete_workingtime'),
(184, 'Can view زمان کاری', 46, 'view_workingtime'),
(185, 'Can add میز', 47, 'add_table'),
(186, 'Can change میز', 47, 'change_table'),
(187, 'Can delete میز', 47, 'delete_table'),
(188, 'Can view میز', 47, 'view_table'),
(189, 'Can add تنظیمات رزرو', 48, 'add_reservationsettings'),
(190, 'Can change تنظیمات رزرو', 48, 'change_reservationsettings'),
(191, 'Can delete تنظیمات رزرو', 48, 'delete_reservationsettings'),
(192, 'Can view تنظیمات رزرو', 48, 'view_reservationsettings'),
(193, 'Can add رزرو', 49, 'add_reservation'),
(194, 'Can change رزرو', 49, 'change_reservation'),
(195, 'Can delete رزرو', 49, 'delete_reservation'),
(196, 'Can view رزرو', 49, 'view_reservation');

-- --------------------------------------------------------

--
-- Table structure for table `blog_author`
--

CREATE TABLE `blog_author` (
  `id` bigint(20) NOT NULL,
  `Author_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_blog`
--

CREATE TABLE `blog_blog` (
  `id` bigint(20) NOT NULL,
  `name_blog` varchar(100) NOT NULL,
  `subject` varchar(30) NOT NULL,
  `image_name` varchar(100) NOT NULL,
  `view` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `time_read` varchar(30) NOT NULL,
  `register_data` datetime(6) NOT NULL,
  `update_data` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `description2` longtext NOT NULL,
  `key_words` varchar(1000) DEFAULT NULL,
  `slug` varchar(40) NOT NULL,
  `grop_blog_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_blog_Auther_blog`
--

CREATE TABLE `blog_blog_Auther_blog` (
  `id` bigint(20) NOT NULL,
  `blog_id` bigint(20) NOT NULL,
  `author_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_group_blog`
--

CREATE TABLE `blog_group_blog` (
  `id` bigint(20) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `slug` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_meta_tag`
--

CREATE TABLE `blog_meta_tag` (
  `id` bigint(20) NOT NULL,
  `title_header` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `keyword_list` longtext DEFAULT NULL,
  `og_title` varchar(100) NOT NULL,
  `blog_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_more_question`
--

CREATE TABLE `blog_more_question` (
  `id` bigint(20) NOT NULL,
  `qus` varchar(300) NOT NULL,
  `answer` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `register_date` datetime(6) NOT NULL,
  `update_date` date DEFAULT NULL,
  `blog_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-01-07 08:34:17.479508', '1', 'پلن پایه', 1, '[{\"added\": {}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(2, '2026-01-07 08:45:47.698665', '1', 'پلن پایه', 2, '[{\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u067e\\u0644\\u062a\\u0641\\u0631\\u0645 \\u0645\\u0646\\u0648 \\u062f\\u06cc\\u062c\\u06cc\\u062a\\u0627\\u0644\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u067e\\u0646\\u0644 \\u06a9\\u0646\\u062a\\u0631\\u0644 \\u063a\\u0630\\u0627 \\u0647\\u0627\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062a\\u0639\\u062f\\u0627\\u062f \\u0646\\u0627\\u0645\\u062d\\u062f\\u0648\\u062f \\u063a\\u0630\\u0627\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062a\\u0639\\u062f\\u0627\\u062f \\u0646\\u0627\\u0645\\u062d\\u062f\\u0648\\u062f \\u062f\\u0633\\u062a\\u0647 \\u0628\\u0646\\u062f\\u06cc\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u0634\\u062e\\u0635\\u06cc \\u0633\\u0627\\u0632\\u06cc \\u062a\\u0635\\u0627\\u0648\\u06cc\\u0631\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062f\\u0633\\u062a\\u0631\\u0633\\u06cc \\u0628\\u0647 \\u0645\\u0646\\u0648 \\u06a9\\u0627\\u063a\\u0630\\u06cc\"}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(3, '2026-01-07 08:46:24.474252', '1', 'پلن پایه', 2, '[{\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u067e\\u0644\\u062a\\u0641\\u0631\\u0645 \\u0645\\u0646\\u0648 \\u062f\\u06cc\\u062c\\u06cc\\u062a\\u0627\\u0644\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}, {\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u067e\\u0646\\u0644 \\u06a9\\u0646\\u062a\\u0631\\u0644 \\u063a\\u0630\\u0627 \\u0647\\u0627\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}, {\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062a\\u0639\\u062f\\u0627\\u062f \\u0646\\u0627\\u0645\\u062d\\u062f\\u0648\\u062f \\u063a\\u0630\\u0627\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}, {\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062a\\u0639\\u062f\\u0627\\u062f \\u0646\\u0627\\u0645\\u062d\\u062f\\u0648\\u062f \\u062f\\u0633\\u062a\\u0647 \\u0628\\u0646\\u062f\\u06cc\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}, {\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u0634\\u062e\\u0635\\u06cc \\u0633\\u0627\\u0632\\u06cc \\u062a\\u0635\\u0627\\u0648\\u06cc\\u0631\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}, {\"changed\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 - \\u062f\\u0633\\u062a\\u0631\\u0633\\u06cc \\u0628\\u0647 \\u0645\\u0646\\u0648 \\u06a9\\u0627\\u063a\\u0630\\u06cc\", \"fields\": [\"\\u0641\\u0639\\u0627\\u0644\"]}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(4, '2026-01-07 08:50:25.992444', '2', 'پلن حرفه ای', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - \\u0627\\u0645\\u06a9\\u0627\\u0646\\u0627\\u062a \\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - \\u062f\\u0633\\u062a\\u0631\\u0633\\u06cc \\u0628\\u0647 \\u067e\\u0646\\u0644 \\u0631\\u0632\\u0631 \\u0645\\u06cc\\u0632\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - 2 \\u0639\\u062f\\u062f \\u0627\\u0633\\u062a\\u0646\\u062f \\u0631\\u0627\\u06cc\\u06af\\u0627\\u0646\"}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(5, '2026-01-07 08:51:11.853082', '2', 'پلن حرفه ای', 2, '[{\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - 1 \\u0633\\u0627\\u0644 \\u067e\\u0634\\u062a\\u06cc\\u0628\\u0627\\u0646\\u06cc \\u0631\\u0627\\u06cc\\u06af\\u0627\\u0646\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - \\u0627\\u0641\\u0632\\u0648\\u062f\\u0646 \\u063a\\u0630\\u0627 \\u062a\\u0648\\u0633\\u0637 \\u0634\\u0631\\u06a9\\u062a\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc - \\u0633\\u0626\\u0648 \\u0648 \\u0646\\u0645\\u0627\\u06cc\\u0634 \\u062f\\u0631 \\u0646\\u062a\\u0627\\u06cc\\u062c \\u062c\\u0633\\u062a\\u062c\\u0648 \\u06af\\u0648\\u06af\\u0644\"}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(6, '2026-01-07 09:12:35.734157', '2', 'پلن حرفه ای', 2, '[]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(7, '2026-01-07 09:15:22.240564', '3', 'پلن VIP', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - \\u0627\\u0645\\u06a9\\u0627\\u0646\\u0627\\u062a \\u067e\\u0644\\u0646 \\u067e\\u0627\\u06cc\\u0647 \\u0648 \\u062d\\u0631\\u0641\\u0647 \\u0627\\u06cc\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - \\u062f\\u0627\\u0645\\u0646\\u0647 \\u0627\\u062e\\u062a\\u0635\\u0627\\u0635\\u06cc\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - \\u062e\\u0631\\u06cc\\u062f \\u0648 \\u0641\\u0631\\u0648\\u0634 \\u0627\\u0646\\u0644\\u0627\\u06cc\\u0646 \\u063a\\u0630\\u0627\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - \\u0637\\u0631\\u0627\\u062d\\u06cc \\u0638\\u0627\\u0647\\u0631 \\u0627\\u062e\\u062a\\u0635\\u0627\\u0635\\u06cc\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - \\u0637\\u0631\\u0627\\u062d\\u06cc \\u06a9\\u062f \\u0646\\u0648\\u06cc\\u0633\\u06cc \\u0627\\u062e\\u062a\\u0635\\u0627\\u0635\\u06cc\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u067e\\u0644\\u0646\", \"object\": \"\\u067e\\u0644\\u0646 VIP - 1 \\u0633\\u0627\\u0644 \\u067e\\u0634\\u062a\\u06cc\\u0628\\u0627\\u0646\\u06cc \\u0631\\u0627\\u06cc\\u06af\\u0627\\u0646\"}}]', 20, '6f0bbf15b0c145ed8745949f18187651'),
(8, '2026-01-07 09:26:51.651015', '1', 'پلاک رومیزی فلزی ( استند رومیزی کافه )', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u0645\\u062d\\u0635\\u0648\\u0644\", \"object\": \"\\u062c\\u0646\\u0633: \\u0648\\u0631\\u0642 \\u0622\\u0644\\u0648\\u0645\\u06cc\\u0646\\u06cc\\u0648\\u0645\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u0645\\u062d\\u0635\\u0648\\u0644\", \"object\": \"\\u0627\\u0628\\u0639\\u0627\\u062f \\u0645\\u062d\\u0635\\u0648\\u0644: \\u062a\\u0627 \\u0634\\u062f\\u0647  8.5*7 \\u0633\\u0627\\u0646\\u062a\\u06cc\\u0645\\u062a\\u0631\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u0645\\u062d\\u0635\\u0648\\u0644\", \"object\": \"\\u0627\\u0628\\u0639\\u0627\\u062f \\u0686\\u0627\\u067e: 7*5 \\u0633\\u0627\\u0646\\u062a\\u06cc\\u0645\\u062a\\u0631\"}}, {\"added\": {\"name\": \"\\u0648\\u06cc\\u0698\\u06af\\u06cc \\u0645\\u062d\\u0635\\u0648\\u0644\", \"object\": \"\\u06af\\u0627\\u0631\\u0627\\u0646\\u062a\\u06cc / \\u0636\\u0645\\u0627\\u0646: \\u062f\\u0627\\u0631\\u062f\"}}, {\"added\": {\"name\": \"\\u0639\\u06a9\\u0633 \\u06af\\u0627\\u0644\\u0631\\u06cc\", \"object\": \"\\u06af\\u0627\\u0644\\u0631\\u06cc \\u067e\\u0644\\u0627\\u06a9 \\u0631\\u0648\\u0645\\u06cc\\u0632\\u06cc \\u0641\\u0644\\u0632\\u06cc ( \\u0627\\u0633\\u062a\\u0646\\u062f \\u0631\\u0648\\u0645\\u06cc\\u0632\\u06cc \\u06a9\\u0627\\u0641\\u0647 )\"}}]', 24, '6f0bbf15b0c145ed8745949f18187651'),
(9, '2026-01-07 09:27:53.923115', '1', 'سازه باو', 2, '[{\"changed\": {\"fields\": [\"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '6f0bbf15b0c145ed8745949f18187651'),
(10, '2026-01-07 14:44:05.624361', '1', 'نوشیدنی', 1, '[{\"added\": {}}]', 6, '6f0bbf15b0c145ed8745949f18187651'),
(11, '2026-01-07 14:44:52.442831', '2', 'نوشیدنی سرد', 1, '[{\"added\": {}}]', 6, '6f0bbf15b0c145ed8745949f18187651'),
(12, '2026-01-07 14:45:11.588792', '3', 'نوشیدنی گرم', 1, '[{\"added\": {}}]', 6, '6f0bbf15b0c145ed8745949f18187651'),
(13, '2026-01-07 14:45:34.620213', '4', 'دسر و کیک', 1, '[{\"added\": {}}]', 6, '6f0bbf15b0c145ed8745949f18187651'),
(14, '2026-01-07 14:48:28.566833', '1dcda7a3-c14d-4710-89eb-d281ebe2b491', '09149663136', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 50, '6f0bbf15b0c145ed8745949f18187651'),
(15, '2026-01-07 14:48:46.808943', '1dcda7a3-c14d-4710-89eb-d281ebe2b491', '09149663136', 2, '[{\"changed\": {\"fields\": [\"Is staff\", \"Superuser status\"]}}]', 50, '6f0bbf15b0c145ed8745949f18187651'),
(16, '2026-01-07 15:30:55.075156', '1', 'لاته', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(17, '2026-01-07 15:33:00.837533', '2', 'اسپرسو', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(18, '2026-01-07 15:34:57.817995', '3', 'ماکیاتو', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(19, '2026-01-07 15:36:11.946735', '2', 'اسپرسو', 2, '[{\"changed\": {\"fields\": [\"Sound\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(20, '2026-01-07 15:36:55.533803', '2', 'اسپرسو', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(21, '2026-01-07 15:39:45.176228', '2', 'اسپرسو', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(22, '2026-01-07 15:41:46.782276', '4', 'ماسالا', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(23, '2026-01-07 15:43:36.348032', '5', 'هات چاکلت', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(24, '2026-01-07 15:43:39.819525', '5', 'هات چاکلت', 2, '[]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(25, '2026-01-07 15:48:39.889764', '6', 'چای', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(26, '2026-01-07 15:50:29.747801', '7', 'دمنوش', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(27, '2026-01-07 15:52:17.770054', '8', 'قهوه ترک', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(28, '2026-01-07 15:54:20.083082', '9', 'آیس آمریکانو', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(29, '2026-01-07 15:57:11.928412', '10', 'آیس لاته', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(30, '2026-01-07 15:59:13.316447', '11', 'ایس کارامل', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(31, '2026-01-07 16:01:53.418117', '12', 'کوک اسپرسو', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(32, '2026-01-07 16:04:07.723262', '13', 'ابمیوه', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(33, '2026-01-07 16:05:30.569134', '14', 'لوسی', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(34, '2026-01-07 16:07:33.750657', '15', 'کیک شکلاتی', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(35, '2026-01-07 16:08:56.249564', '16', 'خاگینه', 1, '[{\"added\": {}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(36, '2026-01-07 16:23:31.975784', '2', 'TIB', 2, '[{\"changed\": {\"fields\": [\"\\u0645\\u062a\\u0646\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(37, '2026-01-08 07:23:30.998576', '3', 'vilo', 2, '[{\"changed\": {\"fields\": [\"\\u0645\\u062a\\u0646\", \"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(38, '2026-01-08 07:47:33.224085', '1', 'پلن پایه', 2, '[{\"changed\": {\"fields\": [\"\\u0642\\u06cc\\u0645\\u062a \\u067e\\u0644\\u0646\"]}}]', 20, '1dcda7a3c14d471089ebd281ebe2b491'),
(39, '2026-01-08 07:47:58.426333', '3', '09146597108 - پلن VIP - 16500000', 3, '', 22, '1dcda7a3c14d471089ebd281ebe2b491'),
(40, '2026-01-08 07:47:58.427036', '2', '09146597108 - پلن پایه - 1200000', 3, '', 22, '1dcda7a3c14d471089ebd281ebe2b491'),
(41, '2026-01-08 07:47:58.427650', '1', '09309087909 - پلن پایه - 1200000', 3, '', 22, '1dcda7a3c14d471089ebd281ebe2b491'),
(42, '2026-01-08 07:54:52.139467', '4', '09146597108 - پلن پایه - 10000', 3, '', 22, '1dcda7a3c14d471089ebd281ebe2b491'),
(43, '2026-01-08 07:55:30.880059', '1', 'پلن پایه', 2, '[{\"changed\": {\"fields\": [\"\\u0642\\u06cc\\u0645\\u062a \\u067e\\u0644\\u0646\"]}}]', 20, '1dcda7a3c14d471089ebd281ebe2b491'),
(44, '2026-01-08 08:55:00.280411', '2', 'TIB', 2, '[{\"changed\": {\"fields\": [\"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(45, '2026-01-08 08:55:17.833797', '2', 'TIB', 2, '[{\"changed\": {\"fields\": [\"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(46, '2026-01-08 08:55:29.117454', '2', 'TIB', 2, '[{\"changed\": {\"fields\": [\"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(47, '2026-01-08 08:55:54.427363', '3', 'vilo', 3, '', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(48, '2026-01-08 08:55:54.428039', '1', 'سازه باو', 3, '', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(49, '2026-01-08 08:58:16.231680', '1', 'پلن پایه', 2, '[{\"changed\": {\"fields\": [\"\\u0642\\u06cc\\u0645\\u062a \\u067e\\u0644\\u0646\"]}}]', 20, '1dcda7a3c14d471089ebd281ebe2b491'),
(50, '2026-01-08 08:58:35.760127', '2', 'پلن حرفه ای', 2, '[{\"changed\": {\"fields\": [\"\\u0642\\u06cc\\u0645\\u062a \\u067e\\u0644\\u0646\"]}}]', 20, '1dcda7a3c14d471089ebd281ebe2b491'),
(51, '2026-01-08 08:58:55.933108', '3', 'پلن VIP', 2, '[{\"changed\": {\"fields\": [\"\\u0642\\u06cc\\u0645\\u062a \\u067e\\u0644\\u0646\"]}}]', 20, '1dcda7a3c14d471089ebd281ebe2b491'),
(52, '2026-01-08 09:00:28.426174', '4', 'یسی', 2, '[{\"changed\": {\"fields\": [\"\\u0645\\u062a\\u0646\", \"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(53, '2026-01-08 09:00:38.672698', '4', 'یسی', 2, '[{\"changed\": {\"fields\": [\"\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u0642\\u0636\\u0627\"]}}]', 12, '1dcda7a3c14d471089ebd281ebe2b491'),
(54, '2026-01-08 09:03:59.069730', '6', '09146597108 - پلن پایه - 2900000', 3, '', 22, '1dcda7a3c14d471089ebd281ebe2b491'),
(55, '2026-01-08 09:39:39.116003', '5', 'اسپرسو بار', 1, '[{\"added\": {}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(56, '2026-01-08 09:42:08.454573', '5', 'اسپرسو بار', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(57, '2026-01-08 09:47:43.479539', '6', 'قهوه دمی', 1, '[{\"added\": {}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(58, '2026-01-08 09:49:18.753709', '5', 'اسپرسو بار', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(59, '2026-01-08 09:49:51.261172', '5', 'اسپرسو بار', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(60, '2026-01-08 09:51:40.375935', '6', 'قهوه دمی', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 6, '1dcda7a3c14d471089ebd281ebe2b491'),
(61, '2026-01-08 10:37:07.783761', '28', 'موکا', 2, '[{\"changed\": {\"fields\": [\"\\u0639\\u0646\\u0648\\u0627\\u0646 \\u0641\\u0627\\u0631\\u0633\\u06cc\", \"Image\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(62, '2026-01-08 10:38:21.567922', '30', 'کن پانا', 2, '[{\"changed\": {\"fields\": [\"\\u0639\\u0646\\u0648\\u0627\\u0646 \\u0641\\u0627\\u0631\\u0633\\u06cc\", \"Image\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491'),
(63, '2026-01-08 11:36:49.672394', '43', 'ایس لاته طعم دار', 2, '[{\"changed\": {\"fields\": [\"\\u0639\\u0646\\u0648\\u0627\\u0646 \\u0641\\u0627\\u0631\\u0633\\u06cc\", \"Image\"]}}]', 8, '1dcda7a3c14d471089ebd281ebe2b491');

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int(11) NOT NULL,
  `clocked_time` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_periodictask`
--

CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) UNSIGNED NOT NULL CHECK (`total_run_count` >= 0),
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int(10) UNSIGNED DEFAULT NULL CHECK (`priority` >= 0),
  `headers` longtext NOT NULL DEFAULT '{}',
  `clocked_id` int(11) DEFAULT NULL,
  `expire_seconds` int(10) UNSIGNED DEFAULT NULL CHECK (`expire_seconds` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_periodictasks`
--

CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_beat_solarschedule`
--

CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_results_chordcounter`
--

CREATE TABLE `django_celery_results_chordcounter` (
  `id` int(11) NOT NULL,
  `group_id` varchar(255) NOT NULL,
  `sub_tasks` longtext NOT NULL,
  `count` int(10) UNSIGNED NOT NULL CHECK (`count` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_results_groupresult`
--

CREATE TABLE `django_celery_results_groupresult` (
  `id` int(11) NOT NULL,
  `group_id` varchar(255) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_celery_results_taskresult`
--

CREATE TABLE `django_celery_results_taskresult` (
  `id` int(11) NOT NULL,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext DEFAULT NULL,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext DEFAULT NULL,
  `meta` longtext DEFAULT NULL,
  `task_args` longtext DEFAULT NULL,
  `task_kwargs` longtext DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  `periodic_task_name` varchar(255) DEFAULT NULL,
  `date_started` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(15, 'blog', 'author'),
(16, 'blog', 'blog'),
(17, 'blog', 'group_blog'),
(19, 'blog', 'meta_tag'),
(18, 'blog', 'more_question'),
(4, 'contenttypes', 'contenttype'),
(43, 'django_celery_beat', 'clockedschedule'),
(38, 'django_celery_beat', 'crontabschedule'),
(39, 'django_celery_beat', 'intervalschedule'),
(40, 'django_celery_beat', 'periodictask'),
(41, 'django_celery_beat', 'periodictasks'),
(42, 'django_celery_beat', 'solarschedule'),
(36, 'django_celery_results', 'chordcounter'),
(37, 'django_celery_results', 'groupresult'),
(35, 'django_celery_results', 'taskresult'),
(32, 'main', 'content'),
(34, 'main', 'course'),
(33, 'main', 'textimageblock'),
(6, 'menu', 'category'),
(7, 'menu', 'exchangerate'),
(8, 'menu', 'food'),
(9, 'menu', 'foodrestaurant'),
(10, 'menu', 'menucategory'),
(13, 'menu', 'menupaperdesien'),
(11, 'menu', 'menuview'),
(14, 'menu', 'requesttocreatepapermenu'),
(12, 'menu', 'restaurant'),
(30, 'order', 'menuimage'),
(29, 'order', 'ordermenu'),
(31, 'peyment', 'peyment'),
(20, 'plan', 'plan'),
(21, 'plan', 'planfeature'),
(22, 'plan', 'planorder'),
(23, 'product', 'orderdetailinfo'),
(24, 'product', 'product'),
(25, 'product', 'productfeature'),
(26, 'product', 'productgallery'),
(27, 'product', 'productorder'),
(28, 'product', 'productorderdetail'),
(5, 'sessions', 'session'),
(44, 'table', 'customer'),
(49, 'table', 'reservation'),
(48, 'table', 'reservationsettings'),
(47, 'table', 'table'),
(45, 'table', 'workingday'),
(46, 'table', 'workingtime'),
(50, 'user', 'customuser');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-01-07 08:08:34.474758'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-01-07 08:08:34.499526'),
(3, 'auth', '0001_initial', '2026-01-07 08:08:34.576755'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-01-07 08:08:34.591295'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-01-07 08:08:34.595374'),
(6, 'auth', '0004_alter_user_username_opts', '2026-01-07 08:08:34.598714'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-01-07 08:08:34.622801'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-01-07 08:08:34.624297'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-01-07 08:08:34.627770'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-01-07 08:08:34.631215'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-01-07 08:08:34.634747'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-01-07 08:08:34.649208'),
(13, 'auth', '0011_update_proxy_permissions', '2026-01-07 08:08:34.653535'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-01-07 08:08:34.657103'),
(15, 'user', '0001_initial', '2026-01-07 08:08:34.789223'),
(16, 'admin', '0001_initial', '2026-01-07 08:08:34.824991'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-01-07 08:08:34.830645'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-07 08:08:34.836253'),
(19, 'blog', '0001_initial', '2026-01-07 08:08:34.947394'),
(20, 'blog', '0002_alter_blog_image_name', '2026-01-07 08:08:34.951906'),
(21, 'blog', '0003_alter_blog_image_name', '2026-01-07 08:08:34.957236'),
(22, 'blog', '0004_alter_blog_image_name', '2026-01-07 08:08:34.961561'),
(23, 'blog', '0005_alter_blog_image_name', '2026-01-07 08:08:34.965838'),
(24, 'blog', '0006_alter_blog_image_name', '2026-01-07 08:08:34.970216'),
(25, 'blog', '0007_alter_blog_image_name', '2026-01-07 08:08:34.974656'),
(26, 'blog', '0008_alter_blog_image_name', '2026-01-07 08:08:34.978939'),
(27, 'blog', '0009_alter_blog_image_name', '2026-01-07 08:08:34.983634'),
(28, 'django_celery_beat', '0001_initial', '2026-01-07 08:08:35.038597'),
(29, 'django_celery_beat', '0002_auto_20161118_0346', '2026-01-07 08:08:35.066755'),
(30, 'django_celery_beat', '0003_auto_20161209_0049', '2026-01-07 08:08:35.079386'),
(31, 'django_celery_beat', '0004_auto_20170221_0000', '2026-01-07 08:08:35.082653'),
(32, 'django_celery_beat', '0005_add_solarschedule_events_choices', '2026-01-07 08:08:35.086703'),
(33, 'django_celery_beat', '0006_auto_20180322_0932', '2026-01-07 08:08:35.144327'),
(34, 'django_celery_beat', '0007_auto_20180521_0826', '2026-01-07 08:08:35.173252'),
(35, 'django_celery_beat', '0008_auto_20180914_1922', '2026-01-07 08:08:35.193334'),
(36, 'django_celery_beat', '0006_auto_20180210_1226', '2026-01-07 08:08:35.205575'),
(37, 'django_celery_beat', '0006_periodictask_priority', '2026-01-07 08:08:35.217889'),
(38, 'django_celery_beat', '0009_periodictask_headers', '2026-01-07 08:08:35.230101'),
(39, 'django_celery_beat', '0010_auto_20190429_0326', '2026-01-07 08:08:35.350146'),
(40, 'django_celery_beat', '0011_auto_20190508_0153', '2026-01-07 08:08:35.380291'),
(41, 'django_celery_beat', '0012_periodictask_expire_seconds', '2026-01-07 08:08:35.393396'),
(42, 'django_celery_beat', '0013_auto_20200609_0727', '2026-01-07 08:08:35.400179'),
(43, 'django_celery_beat', '0014_remove_clockedschedule_enabled', '2026-01-07 08:08:35.410467'),
(44, 'django_celery_beat', '0015_edit_solarschedule_events_choices', '2026-01-07 08:08:35.413914'),
(45, 'django_celery_beat', '0016_alter_crontabschedule_timezone', '2026-01-07 08:08:35.420575'),
(46, 'django_celery_beat', '0017_alter_crontabschedule_month_of_year', '2026-01-07 08:08:35.426028'),
(47, 'django_celery_beat', '0018_improve_crontab_helptext', '2026-01-07 08:08:35.431207'),
(48, 'django_celery_beat', '0019_alter_periodictasks_options', '2026-01-07 08:08:35.433605'),
(49, 'django_celery_results', '0001_initial', '2026-01-07 08:08:35.451296'),
(50, 'django_celery_results', '0002_add_task_name_args_kwargs', '2026-01-07 08:08:35.474884'),
(51, 'django_celery_results', '0003_auto_20181106_1101', '2026-01-07 08:08:35.477491'),
(52, 'django_celery_results', '0004_auto_20190516_0412', '2026-01-07 08:08:35.519150'),
(53, 'django_celery_results', '0005_taskresult_worker', '2026-01-07 08:08:35.537435'),
(54, 'django_celery_results', '0006_taskresult_date_created', '2026-01-07 08:08:35.574850'),
(55, 'django_celery_results', '0007_remove_taskresult_hidden', '2026-01-07 08:08:35.586925'),
(56, 'django_celery_results', '0008_chordcounter', '2026-01-07 08:08:35.595212'),
(57, 'django_celery_results', '0009_groupresult', '2026-01-07 08:08:35.751255'),
(58, 'django_celery_results', '0010_remove_duplicate_indices', '2026-01-07 08:08:35.757957'),
(59, 'django_celery_results', '0011_taskresult_periodic_task_name', '2026-01-07 08:08:35.767842'),
(60, 'django_celery_results', '0012_taskresult_date_started', '2026-01-07 08:08:35.778253'),
(61, 'django_celery_results', '0013_taskresult_django_cele_periodi_1993cf_idx', '2026-01-07 08:08:35.787582'),
(62, 'django_celery_results', '0014_alter_taskresult_status', '2026-01-07 08:08:35.790709'),
(63, 'main', '0001_initial', '2026-01-07 08:08:35.803370'),
(64, 'main', '0002_alter_textimageblock_image', '2026-01-07 08:08:35.806035'),
(65, 'main', '0003_alter_textimageblock_image', '2026-01-07 08:08:35.808727'),
(66, 'main', '0004_alter_textimageblock_image', '2026-01-07 08:08:35.811237'),
(67, 'main', '0005_alter_textimageblock_image', '2026-01-07 08:08:35.813727'),
(68, 'main', '0006_alter_textimageblock_image', '2026-01-07 08:08:35.816583'),
(69, 'main', '0007_alter_textimageblock_image', '2026-01-07 08:08:35.819183'),
(70, 'main', '0008_alter_textimageblock_image', '2026-01-07 08:08:35.821622'),
(71, 'main', '0009_course_alter_textimageblock_image', '2026-01-07 08:08:35.830170'),
(72, 'menu', '0001_initial', '2026-01-07 08:08:35.890090'),
(73, 'menu', '0002_initial', '2026-01-07 08:08:36.245302'),
(74, 'menu', '0003_design_remove_restaurant_background_color_and_more', '2026-01-07 08:08:36.356947'),
(75, 'menu', '0004_restaurant_design', '2026-01-07 08:08:36.390029'),
(76, 'menu', '0005_remove_restaurant_design_delete_design', '2026-01-07 08:08:36.433941'),
(77, 'menu', '0006_menupaperdesien_requesttocreatepapermenu', '2026-01-07 08:08:36.487589'),
(78, 'menu', '0007_menupaperdesien_image', '2026-01-07 08:08:36.498271'),
(79, 'menu', '0008_alter_menupaperdesien_image', '2026-01-07 08:08:36.502106'),
(80, 'menu', '0009_alter_menupaperdesien_image', '2026-01-07 08:08:36.505608'),
(81, 'menu', '0010_alter_menupaperdesien_image', '2026-01-07 08:08:36.510658'),
(82, 'order', '0001_initial', '2026-01-07 08:08:36.570430'),
(83, 'order', '0002_alter_ordermenu_image', '2026-01-07 08:08:36.580353'),
(84, 'order', '0003_alter_ordermenu_image', '2026-01-07 08:08:36.589344'),
(85, 'order', '0004_alter_ordermenu_image', '2026-01-07 08:08:36.598296'),
(86, 'order', '0005_alter_ordermenu_image', '2026-01-07 08:08:36.607806'),
(87, 'order', '0006_alter_ordermenu_image', '2026-01-07 08:08:36.617871'),
(88, 'order', '0007_alter_ordermenu_image', '2026-01-07 08:08:36.626846'),
(89, 'order', '0008_alter_ordermenu_image', '2026-01-07 08:08:36.635815'),
(90, 'order', '0009_alter_ordermenu_image', '2026-01-07 08:08:36.645169'),
(91, 'peyment', '0001_initial', '2026-01-07 08:08:36.653909'),
(92, 'peyment', '0002_initial', '2026-01-07 08:08:36.710014'),
(93, 'plan', '0001_initial', '2026-01-07 08:08:36.775223'),
(94, 'plan', '0002_initial', '2026-01-07 08:08:36.877083'),
(95, 'product', '0001_initial', '2026-01-07 08:08:36.998570'),
(96, 'product', '0002_initial', '2026-01-07 08:08:37.200293'),
(97, 'product', '0003_remove_productorder_total_price_and_more', '2026-01-07 08:08:37.271428'),
(98, 'product', '0004_remove_productorder_plan_price_and_more', '2026-01-07 08:08:37.336673'),
(99, 'sessions', '0001_initial', '2026-01-07 08:08:37.356245'),
(100, 'table', '0001_initial', '2026-01-07 08:08:37.689683');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('svf7g2ckmetfb0ga682sji2rphn2zong', '.eJxVjjsOgzAQBe_iOrb8A--mpM8Z0Nq7BJIIJD5VlLsHJIqkfjOj91YtbWvfbovM7cDqqhwXpkRBFxdZx-SsBpSs2YOTLD5HdOryq2UqTxkPlx803idTpnGdh2wOxJzrYm4Ty6s52b9AT0u_2x4LSlUXZqAgTBYidYQMYmOoLZMXyRUUEsH9BCCkELzUCUJlO4zq8wVUa0G6:1vdUqI:DBq2hgHUlvvf1K4AJbXpWS_-vhcT-RXR_xTLfaxUEkU', '2026-01-21 14:48:58.081329'),
('u6xmhiqxybywbrubvth32samq2nnn6gl', '.eJxVjEtOxDAQBe_iNcn403Hbs2QPV4ja7jYJZByUj4SEuDseaTazfVX1ftVtTfMi7-ctyaauSkcXfYjoAdSLqvJzjOe2NHD5pirLpY0jncc0nrts48yNWA02g5gOuPgORHJHIKHLqLl9oXgoz1mi_CX13vIn1Y-1z2s9tjn1d6V_0L1_W1mW14f7dDDRPrUagymDMdkPloJoj1EPwllbzI5CGTigY-1jKM5J5CKWBEzEZhOGZNTfP5UrT_Q:1vdmPr:uUJI2EvPKFbzkDa2TMMTrwNqQRSrSleBeTbTgd0F9y8', '2026-01-22 09:34:51.125193'),
('z6evkdi34vwjbh0f0p2017vgirbd1s5r', '.eJxVjktuwzAMBe-idW3rZ5nMsvvkCgYlMrVaWy78AQoUvXsVIJusZ-bh_apljXmW27lE2dRFaTQeQ3DGBfWmivwc47nNFXTfVGTujhw74iWXruKRzmMaz122MXN1DCemgVyTjOfGD0Y3gBIbtmAkio0ezWsWKX1JebT8SeVjbdNaji3H9qG0T7q315Vlfn-6LwMT7VOtLSaUPiRmICdMGjzdCRlEexc0kxWJPSQSwXoCEAbnrIQBXK_v6NXfP3beVDw:1vdlQn:12z2nHsD16R8fvu1ld2N8WYG43sc6iWDRFMhnoopeow', '2026-01-22 08:31:45.425680');

-- --------------------------------------------------------

--
-- Table structure for table `main_content`
--

CREATE TABLE `main_content` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `image` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_course`
--

CREATE TABLE `main_course` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `video_link` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `thumbnail` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_textimageblock`
--

CREATE TABLE `main_textimageblock` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `text` longtext NOT NULL,
  `image` varchar(100) NOT NULL,
  `image_position` varchar(5) NOT NULL,
  `order` int(10) UNSIGNED NOT NULL CHECK (`order` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_category`
--

CREATE TABLE `menu_category` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_en` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `displayOrder` int(11) DEFAULT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `parent_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `menu_category`
--

INSERT INTO `menu_category` (`id`, `title`, `title_en`, `slug`, `isActive`, `displayOrder`, `createdAt`, `updatedAt`, `image`, `parent_id`) VALUES
(1, 'نوشیدنی', 'drink', 'noshdn', 1, 0, '2026-01-07 14:44:05.622564', '2026-01-07 14:44:05.622588', 'categories/images/509f51eb-cb8f-4967-b5af-10622fca990f.png', NULL),
(2, 'نوشیدنی سرد', 'Cold drink', 'noshdn-srd', 1, 0, '2026-01-07 14:44:52.441620', '2026-01-07 14:44:52.441638', 'categories/images/15fd22ad-5aec-4af4-b37a-621601be41fa.png', 1),
(3, 'نوشیدنی گرم', 'hot drink', 'noshdn-rm', 1, 0, '2026-01-07 14:45:11.587251', '2026-01-07 14:45:11.587270', 'categories/images/189eaa33-c53f-464c-bf57-243ac8047fc4.png', 1),
(4, 'دسر و کیک', 'Desserts and cakes', 'dsr-o', 1, 0, '2026-01-07 14:45:34.619022', '2026-01-07 14:45:34.619056', 'categories/images/f0468a97-6bc1-41c4-994d-0a7b79b5e067.png', 1),
(5, 'اسپرسو بار', 'Espresso bar', 'srso-br', 1, 0, '2026-01-08 09:39:39.114225', '2026-01-08 09:49:51.259718', 'categories/images/c75cd52e-6dc9-467b-87f4-bf008cad6a6b.png', 1),
(6, 'قهوه دمی', 'Brewed coffee', 'khoh-dm', 1, 0, '2026-01-08 09:47:43.476675', '2026-01-08 09:51:40.374406', 'categories/images/af2ebfc0-79e8-4c8f-8f42-d975f52f6a47.png', 1);

-- --------------------------------------------------------

--
-- Table structure for table `menu_exchangerate`
--

CREATE TABLE `menu_exchangerate` (
  `id` bigint(20) NOT NULL,
  `rate` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_food`
--

CREATE TABLE `menu_food` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_en` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `displayOrder` int(11) DEFAULT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `description_en` longtext DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `sound` varchar(100) DEFAULT NULL,
  `price` int(10) UNSIGNED DEFAULT NULL CHECK (`price` >= 0),
  `price_usd_cents` int(10) UNSIGNED DEFAULT NULL CHECK (`price_usd_cents` >= 0),
  `preparationTime` int(11) DEFAULT NULL,
  `created_by` varchar(20) NOT NULL,
  `menuCategory_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `menu_food`
--

INSERT INTO `menu_food` (`id`, `title`, `title_en`, `slug`, `isActive`, `displayOrder`, `createdAt`, `updatedAt`, `description`, `description_en`, `image`, `sound`, `price`, `price_usd_cents`, `preparationTime`, `created_by`, `menuCategory_id`) VALUES
(1, 'لاته', 'Latte', 'lth', 1, 0, '2026-01-07 15:30:55.070537', '2026-01-07 15:30:55.070556', 'شیر داغ + قهوه اسپرسو + کف شیر.', 'Hot milk + espresso coffee + milk foam.', 'foods/images/4f8952ec-e5a2-4a07-9088-3ffc0cf9f244.jpg', '', 86000, 143, 5, 'restaurant', 2),
(2, 'اسپرسو', 'Espresso', 'srso', 1, 0, '2026-01-07 15:33:00.833486', '2026-01-07 15:39:45.173504', 'آب داغ+ فشار بالا+ قهوه ریز', 'Hot water + high pressure + ground coffee', 'foods/images/19f5cdf7-e0a7-4304-80ef-8cb41212a64f.jpg', 'sound/menu/396fb995-8eb1-42e5-bea0-072a944e1eef.jpg', 60000, 100, 4, 'restaurant', 2),
(3, 'ماکیاتو', 'Macchiato', 'mto', 1, 0, '2026-01-07 15:34:57.815003', '2026-01-07 15:34:57.815022', 'اسپرسو + لکه‌ای از شیر (یا کف شیر).', 'Espresso + a splash of milk (or milk foam).', 'foods/images/266b0bf1-9161-49b7-aa6f-fe5348db47c1.webp', '', 89000, 148, 8, 'restaurant', 2),
(4, 'ماسالا', 'Masala', 'msl', 1, 0, '2026-01-07 15:41:46.779464', '2026-01-07 15:41:46.779481', 'مخلوط ادویه گرم هندی.', 'Hot Indian spice mix.', 'foods/images/c7902059-2043-4a2c-9a30-096fa9189d19.jpg', '', NULL, NULL, 6, 'restaurant', 2),
(5, 'هات چاکلت', 'Hot chocolate', 'ht-lt', 1, 0, '2026-01-07 15:43:36.344433', '2026-01-07 15:43:39.817516', 'شکلات ذوب‌شده + شیر داغ + خامه/شکر.', 'Melted chocolate + hot milk + cream/sugar.', 'foods/images/a73e39b2-eadc-41bd-95e9-0be9d926127b.jpg', '', NULL, NULL, 95000, 'restaurant', 2),
(6, 'چای', 'tea', 'tea', 1, 0, '2026-01-07 15:48:39.886367', '2026-01-07 15:48:39.886387', 'چای: برگ‌های خشک‌شده گیاه کاملیا سیننسیس.', 'Tea: Dried leaves of the Camellia sinensis plant.', 'foods/images/c2cd945f-8227-4ed7-9fb0-b4f5bd894cef.jpeg', '', 40000, 66, 6, 'restaurant', 2),
(7, 'دمنوش', 'Herbal tea', 'dmnosh', 1, 0, '2026-01-07 15:50:29.743878', '2026-01-07 15:50:29.743897', 'گل، برگ، یا ریشه گیاهان دارویی که در آب داغ خیسانده می‌شوند', 'Flowers, leaves, or roots of medicinal plants steeped in hot water', 'foods/images/cb55ed21-0ab4-44e2-be18-025002e7d284.jpg', '', 50000, 83, 6, 'restaurant', 2),
(8, 'قهوه ترک', 'Turkish coffee', 'khoh-tr', 1, 0, '2026-01-07 15:52:17.766927', '2026-01-07 15:52:17.766947', 'پودر قهوه بسیار نرم + آب + شکر (در فنجان کوچک روی حرارت).', 'Very fine coffee powder + water + sugar (in a small cup over heat).', 'foods/images/0db36c4a-f5eb-4b1d-8c73-3bd385a903d0.jpg', '', 85000, 141, 5, 'restaurant', 2),
(9, '                                                                                                                                                                    آیس آمریکانو                            ', 'Ice Americano', 's-mrno', 0, 0, '2026-01-07 15:54:20.080268', '2026-01-08 08:32:36.259792', 'اسپرسو + یخ + آب سرد.', 'Espresso + ice + cold water.', 'foods/images/d9e7a050-2659-4c03-ad20-45475b291226.webp', '', 100, 133, 7, 'restaurant', 1),
(10, 'آیس لاته', 'Iced latte', 's-lth', 1, 0, '2026-01-07 15:57:11.924332', '2026-01-07 15:57:11.924353', 'اسپرسو + شیر سرد + یخ.', 'Espresso + cold milk + ice.', 'foods/images/5912878f-9520-439d-83ed-05fd9967a3c3.jpg', '', 86000, 143, 7, 'restaurant', 1),
(11, '                                                                                                                                                                    ایس کارامل                            ', 'Caramel ice', 's-rml', 0, 0, '2026-01-07 15:59:13.313001', '2026-01-08 08:33:14.617748', 'اسپرسو + شیر + یخ + سس کارامل.', 'Espresso + milk + ice + caramel sauce.', 'foods/images/e9bf5cbf-adb5-46e7-b766-92393b18dd4b.jpg', '', 100000, 166, 8, 'restaurant', 1),
(12, 'کوک اسپرسو', 'Espresso maker', 'o-srso', 1, 0, '2026-01-07 16:01:53.412765', '2026-01-07 16:01:53.412791', 'شات اسپرسو خنک + آب گازدار + یخ + لیمو (اختیاری).', 'Cool espresso shot + sparkling water + ice + lemon (optional).', 'foods/images/e86b40db-68cc-4f03-b4f7-1d06d22c44d1.jpg', '', 90000, 150, 9, 'restaurant', 1),
(13, 'ابمیوه', NULL, 'bmoh', 1, 0, '2026-01-07 16:04:07.719110', '2026-01-07 16:04:07.719130', 'آب طبیعی فشرده‌شده میوه‌ها یا سبزی‌ها (مانند پرتقال، سیب، هویج).', 'Natural, pressed juice from fruits or vegetables (such as oranges, apples, carrots).', 'foods/images/39823fff-df4e-4f0e-a57e-d8feaee112d7.webp', '', 140000, 233, 12, 'restaurant', 1),
(14, 'لوسی', 'lucy', 'los', 1, 0, '2026-01-07 16:05:30.566253', '2026-01-07 16:05:30.566273', 'قهوه سرد آماده (آیسد کافی) است که توسط استارباکس', 'It is a cold brew coffee (iced coffee) made by Starbucks.', 'foods/images/8bdc25ce-4bb6-496e-98e7-9d4658ed9276.jpg', '', 160000, 266, 7, 'restaurant', 1),
(15, 'کیک شکلاتی', 'Chocolate cake', 'shlt', 1, 0, '2026-01-07 16:07:33.747014', '2026-01-07 16:07:33.747033', 'آرد + شکر + تخم‌مرغ + کره + پودر کاکائو.', 'Flour + sugar + eggs + butter + cocoa powder.', 'foods/images/5c5ec527-7028-4e81-8478-6552a9549a00.jpg', '', 80000, 133, 3, 'restaurant', 3),
(16, 'خاگینه', 'Khagineh', 'khnh', 1, 0, '2026-01-07 16:08:56.245709', '2026-01-07 16:08:56.245728', 'تخم‌مرغ همزده + شیر + آرد (در تابه).', 'Scrambled eggs + milk + flour (in a pan).', 'foods/images/e6fa0939-637a-457d-aa1e-7670b688b5f8.jpg', '', 45000, 75, 4, 'restaurant', 3),
(17, '                                                                                                                                                                    سینگل                            ', NULL, '', 1, 0, '2026-01-08 09:55:23.702198', '2026-01-08 09:56:19.146247', '(ترکیب 70/30 روبستا )', NULL, 'foods/images/f5baf866-12a3-4555-979b-a471721209e5.jpg', '', 80000, 133, 10, 'restaurant', 6),
(18, 'دبل', NULL, '-1', 1, 0, '2026-01-08 09:57:39.122426', '2026-01-08 09:57:42.986323', 'ترکیب 70/30 روبستا )', NULL, 'foods/images/d17191d0-cf0c-4f00-a2e7-7009ec92c0c9.webp', '', 90000, 150, 10, 'restaurant', 6),
(19, 'آمریکانو', NULL, '-2', 1, 0, '2026-01-08 09:59:39.611584', '2026-01-08 09:59:45.290492', '(ترکیب 70/30 روبستا)', NULL, 'foods/images/ea09b565-1eed-4f8c-bc6b-ec2f8d4aa39b.jpg', '', 95000, 158, 10, 'restaurant', 6),
(20, 'عربیکا (تک خاستگاه)', NULL, '-3', 1, 0, '2026-01-08 10:05:33.729234', '2026-01-08 10:05:40.360417', '(سینگل - دبل - امریکانو )', NULL, 'foods/images/129b25b1-dd3d-48c8-ac75-a13f61150554.jpg', '', 105000, 175, 10, 'restaurant', 6),
(21, 'روبستا ( تک خاستگاه )', NULL, '-4', 1, 0, '2026-01-08 10:09:47.827350', '2026-01-08 10:17:53.192112', '( سینگل - دبل - امریکانو )', NULL, 'foods/images/2b860a32-417c-4f52-b4a1-824a8b65a5c1.webp', '', 100000, 166, 10, 'restaurant', 6),
(22, 'قهوه برند..', NULL, '-5', 1, 0, '2026-01-08 10:13:42.209114', '2026-01-08 10:13:46.192171', '(قهوه آمیکو و...', NULL, 'foods/images/b2e6108e-b65f-48d7-9601-3688488a7bc2.webp', '', 0, 0, 10, 'restaurant', 6),
(23, '                                                                                                                                                                    کاپوچینو                            ', NULL, '-6', 1, 0, '2026-01-08 10:16:26.250369', '2026-01-08 10:17:49.878922', 'با شیر گرم و کفِ غلیظِ رقصان.', NULL, 'foods/images/5445f92a-a027-43bd-a7e5-6b36316ed58a.jpg', '', 115000, 191, 10, 'restaurant', 6),
(24, 'لاته', NULL, '-7', 1, 0, '2026-01-08 10:18:59.918250', '2026-01-08 10:21:15.033009', 'عطری از قهوه‌ای شیرین و شیری ملایم.', NULL, 'foods/images/7cc80fb1-386e-441a-a4fa-9b3c4a202f72.jpg', '', 125000, 208, 10, 'restaurant', 6),
(25, 'بلک لاته', NULL, '-8', 1, 0, '2026-01-08 10:21:07.017585', '2026-01-08 10:21:11.059509', 'بلک‌لاته‌ای تلخ و شیرین', NULL, 'foods/images/f9d435be-b773-4c33-b67b-5d45a2e7f3c5.jpg', '', 135000, 225, 12, 'restaurant', 6),
(26, 'کاپوچینو طعم دار', NULL, '-9', 1, 0, '2026-01-08 10:24:23.171115', '2026-01-08 10:24:29.877788', '( فندق - کارامل - وانیل - نارگیل )', NULL, 'foods/images/221a0de2-5f40-49c1-8f83-dba707929543.jpg', '', 130000, 216, 15, 'restaurant', 6),
(27, 'لاته طعم دار', NULL, '-10', 1, 0, '2026-01-08 10:27:33.502996', '2026-01-08 10:27:57.474413', '(فندق - کارامل - وانیل - نارگیل )', NULL, 'foods/images/8e6f4bd5-8a6b-4c64-a646-8ca6d166ce1d.jpg', '', 140000, 233, 15, 'restaurant', 6),
(28, 'موکا', NULL, '-11', 1, 0, '2026-01-08 10:30:21.345615', '2026-01-08 10:37:07.780773', '( سس شکلات + شیر + فوم شیر + اسپرسو )', '', 'foods/images/a9b2acfc-173d-4385-8f81-794ff29bb7bc.webp', '', 140000, 233, 15, 'restaurant', 6),
(29, 'کارامل ماکیاتو', NULL, '-12', 1, 0, '2026-01-08 10:33:12.186414', '2026-01-08 10:33:16.006229', '( سس کارامل + فوم شیر + شیر + اسپرسو', NULL, 'foods/images/116a804b-26b6-4562-8974-7e3d96c8c23b.jpg', '', 140000, 233, 15, 'restaurant', 6),
(30, 'کن پانا', NULL, '-13', 1, 0, '2026-01-08 10:35:25.089135', '2026-01-08 10:38:21.565242', '(اسپرسو + خامه )', '', 'foods/images/4d1fd554-f768-4a42-b078-f6a1138ed348.webp', '', 125000, 208, 15, 'restaurant', 6),
(31, 'بووم بن', NULL, '-14', 1, 0, '2026-01-08 10:40:33.454950', '2026-01-08 10:40:38.529330', '( اسپرسو +  شیر عسل + فوم شیر )', NULL, 'foods/images/4a1d9dfc-4068-423d-9fa9-13aa58eb00ec.jpg', '', 140000, 233, 16, 'restaurant', 6),
(32, 'افوگاتو', NULL, '-15', 1, 0, '2026-01-08 10:42:15.704802', '2026-01-08 11:35:42.904868', ' (بستنی + اسپرسو )', NULL, 'foods/images/8d0980b9-6c84-4ecc-a03d-d837dccb923d.jpg', '', 145000, 241, 16, 'restaurant', 6),
(33, 'ترک', NULL, '-16', 1, 0, '2026-01-08 11:07:33.040097', '2026-01-08 11:12:53.790076', 'با طعمِ کهنِ شرقی و رایحه‌ای پایدار.', NULL, 'foods/images/e3b7d4e9-3290-4f9d-b215-8538cf473e64.jpg', '', 90000, 150, 12, 'restaurant', 7),
(34, 'قهوه طعم دار', NULL, '-17', 1, 0, '2026-01-08 11:09:17.132918', '2026-01-08 11:12:59.840517', '( هل + دارچین )', NULL, 'foods/images/ad775762-4aa6-4760-ad35-95e977c32c73.jpg', '', 110000, 183, 12, 'restaurant', 7),
(35, 'فرانسه', NULL, '-18', 1, 0, '2026-01-08 11:10:24.068113', '2026-01-08 11:13:00.669939', '.', NULL, 'foods/images/46589593-b018-43cd-a103-4ea6190be46c.jpg', '', 130000, 216, 13, 'restaurant', 7),
(36, 'یونانی', NULL, '-19', 1, 0, '2026-01-08 11:12:48.514293', '2026-01-08 11:12:53.026899', 'ترک به شهر', NULL, 'foods/images/137db6d1-8caf-4d0b-9703-bdf54dba5f20.webp', '', 115000, 191, 13, 'restaurant', 7),
(37, 'کلد برو', NULL, '-20', 1, 0, '2026-01-08 11:17:33.380681', '2026-01-08 11:24:09.663249', '(دم آوری با قهوه عربیکا تک خاستگاه کلمبیا )', NULL, 'foods/images/7a05f62e-9007-426b-8890-fc4a29a9f3aa.webp', '', 130000, 216, 15, 'restaurant', 4),
(38, 'کلد برو طعم دار', NULL, '-21', 1, 0, '2026-01-08 11:19:30.893290', '2026-01-08 11:24:13.353266', 'ترویکال + نارگیل + انگور قرمز ', NULL, 'foods/images/a055df32-d6de-4cf8-b5bb-1f5aad9da40a.jpg', '', 140000, 233, 12, 'restaurant', 4),
(39, 'آیس امریکانو', NULL, '-22', 1, 0, '2026-01-08 11:22:00.690279', '2026-01-08 11:24:14.064970', 'آمریکنوی خنک و تلخ،', NULL, 'foods/images/7b241f2f-9f28-4859-be2e-cf6f1a4535ed.webp', '', 100000, 166, 12, 'restaurant', 4),
(40, 'ایس لاته', NULL, '-23', 1, 0, '2026-01-08 11:23:58.993010', '2026-01-08 11:24:08.966403', 'با شیر سرد و طعمی ملایم از قهوه.', NULL, 'foods/images/519608c4-ae6d-4a60-9a48-1d8061322ebf.jpg', '', 130000, 216, 15, 'restaurant', 4),
(41, 'ایس نوع لیمو سیب', NULL, '-24', 1, 0, '2026-01-08 11:26:45.466387', '2026-01-08 11:28:31.656905', 'ترش و شیرین با تکه‌های یخ.', NULL, 'foods/images/f5fafdea-9229-44d4-9c37-68c571b4e764.webp', '', 110000, 183, 12, 'restaurant', 4),
(42, 'ایس نوع هلو', NULL, '-25', 1, 0, '2026-01-08 11:28:23.136075', '2026-01-08 11:28:32.322572', 'معطر و خنک، با طعم تابستانی میوه‌ها.', NULL, 'foods/images/6153c75a-f4ef-48f2-af28-12afecf346ae.webp', '', 110000, 183, 12, 'restaurant', 4),
(43, '                                                                                                                                                                    ایس لاته طعم دار                            ', NULL, '-26', 1, 0, '2026-01-08 11:31:15.397350', '2026-01-08 11:37:12.023989', 'فندق + کارامل + وانیل + نارگیل', '', 'foods/images/f3d8ff19-5362-40b4-8150-f5403e641834.webp', '', 125000, 208, 12, 'restaurant', 4),
(44, 'کوک اسپرسو', NULL, '-27', 1, 0, '2026-01-08 11:32:25.188195', '2026-01-08 11:34:45.471049', 'اسپرسو + کولا', NULL, 'foods/images/2286764b-240b-4b7b-9f35-8716e67a6281.jpg', '', 140000, 233, 13, 'restaurant', 4),
(45, 'هایپ اسپرسو', NULL, '-28', 1, 0, '2026-01-08 11:34:39.610668', '2026-01-08 11:34:47.671930', 'اسپرسو + انرژی زا', NULL, 'foods/images/edeb8314-1cd1-41e1-88fa-02b7992b5c7a.jpg', '', 150000, 250, 14, 'restaurant', 4),
(46, 'هات چاکلت', NULL, '-29', 1, 0, '2026-01-08 11:39:18.410230', '2026-01-08 11:41:53.273742', 'شیرین و دلگرم‌کننده، با رایحهٔ کاکائو.', NULL, 'foods/images/720d60e5-11a5-46ea-a9c1-65559df41c74.webp', '', 135000, 225, 13, 'restaurant', 5),
(47, 'وایت چاکلت', NULL, '-30', 1, 0, '2026-01-08 11:41:47.341420', '2026-01-08 11:41:52.427253', 'شکلات سفید + شیر', NULL, 'foods/images/3a732f00-6d16-4f28-901e-0047cbab64d0.webp', '', 125000, 208, 14, 'restaurant', 5),
(48, 'پینک چاکلت', NULL, '-31', 1, 0, '2026-01-08 11:43:57.452228', '2026-01-08 11:45:26.423568', 'شکلات صورتی + شیر', NULL, 'foods/images/28138645-9c0f-45ee-980a-6cd2d3a96b87.jpg', '', 125000, 208, 125000, 'restaurant', 5),
(49, 'کافی میکس', NULL, '-32', 1, 0, '2026-01-08 11:47:34.255640', '2026-01-08 11:51:39.942635', 'قهوه فوری + کافی پیت + شیر', NULL, 'foods/images/665cc2ed-4e9e-4135-a9c5-825dd753e153.jpg', '', 115000, 191, 13, 'restaurant', 5),
(50, 'ثعلب دارچین', NULL, '-33', 1, 0, '2026-01-08 11:49:12.609580', '2026-01-08 11:51:40.555050', 'ثعلب + دارچین + شهر', NULL, 'foods/images/37ce8c89-ded2-484d-a722-4c9ce1ded8c6.jpg', '', 120000, 200, 12, 'restaurant', 5),
(51, 'شیر نسکافه', NULL, '-34', 1, 0, '2026-01-08 11:51:31.305441', '2026-01-08 11:51:51.483480', 'قهوه فوری گلد + شیر', NULL, 'foods/images/b61c48b3-0e09-48c1-9390-2a7d838028e8.jpg', '', 120000, 200, 15, 'restaurant', 5),
(52, 'چای کرک', NULL, '-35', 1, 0, '2026-01-08 11:53:31.079978', '2026-01-08 11:54:38.543905', 'ترکیبی از انوع ادویه ها + شیر', NULL, 'foods/images/58d3a756-f1fd-4650-bfab-c3bf219009a1.jpg', '', 125000, 208, 13, 'restaurant', 5),
(53, 'چای ماسالا', NULL, '-36', 1, 0, '2026-01-08 11:55:58.680999', '2026-01-08 11:56:04.445039', 'ترکیبی از انوع ادویه ها + شیر', NULL, 'foods/images/1c2425ab-88d0-47b9-9a9b-da134191bcb0.jpeg', '', 130000, 216, 14, 'restaurant', 5),
(54, 'نوتلا چاکلت', NULL, '-37', 0, 0, '2026-01-08 11:59:19.880091', '2026-01-08 11:59:19.880112', 'نوتلا + شکلات + شیر', NULL, 'foods/images/108e0fa9-b2e1-4bd9-babb-a328c57b92c8.jpeg', '', 165000, 275, 18, 'restaurant', 5),
(55, 'لوتوس چاکلت', NULL, '-38', 1, 0, '2026-01-08 12:01:10.666944', '2026-01-08 12:03:11.016198', 'کرم بیسکویئت + شکلات + شیر', NULL, 'foods/images/4bbcf324-713c-4060-956a-31b9f19ef264.webp', '', 155000, 258, 19, 'restaurant', 5),
(56, 'هات پسته زعفران', NULL, '-39', 1, 0, '2026-01-08 12:03:04.689642', '2026-01-08 12:03:10.226956', 'پسته + زعفران + شیر', NULL, 'foods/images/d8a70711-2dea-4444-93a2-115cd8ae86ab.jpg', '', 175000, 291, 19, 'restaurant', 5);

-- --------------------------------------------------------

--
-- Table structure for table `menu_food_restaurants`
--

CREATE TABLE `menu_food_restaurants` (
  `id` bigint(20) NOT NULL,
  `food_id` bigint(20) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `menu_food_restaurants`
--

INSERT INTO `menu_food_restaurants` (`id`, `food_id`, `restaurant_id`) VALUES
(1, 1, 2),
(2, 2, 2),
(3, 3, 2),
(4, 4, 2),
(5, 5, 2),
(6, 6, 2),
(7, 7, 2),
(8, 8, 2),
(9, 9, 2),
(10, 10, 2),
(11, 11, 2),
(12, 12, 2),
(13, 13, 2),
(14, 14, 2),
(15, 15, 2),
(16, 16, 2),
(17, 17, 5),
(18, 18, 5),
(19, 19, 5),
(20, 20, 5),
(21, 21, 5),
(22, 22, 5),
(23, 23, 5),
(24, 24, 5),
(25, 25, 5),
(26, 26, 5),
(27, 27, 5),
(28, 28, 5),
(29, 29, 5),
(30, 30, 5),
(31, 31, 5),
(32, 32, 5),
(33, 33, 5),
(34, 34, 5),
(35, 35, 5),
(36, 36, 5),
(37, 37, 5),
(38, 38, 5),
(39, 39, 5),
(40, 40, 5),
(41, 41, 5),
(42, 42, 5),
(43, 43, 5),
(44, 44, 5),
(45, 45, 5),
(46, 46, 5),
(47, 47, 5),
(48, 48, 5),
(49, 49, 5),
(50, 50, 5),
(51, 51, 5),
(52, 52, 5),
(53, 53, 5),
(54, 54, 5),
(55, 55, 5),
(56, 56, 5);

-- --------------------------------------------------------

--
-- Table structure for table `menu_menucategory`
--

CREATE TABLE `menu_menucategory` (
  `id` bigint(20) NOT NULL,
  `customTitle` varchar(255) DEFAULT NULL,
  `customTitle_en` varchar(255) DEFAULT NULL,
  `customImage` varchar(100) DEFAULT NULL,
  `displayOrder` int(11) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `restaurant_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `menu_menucategory`
--

INSERT INTO `menu_menucategory` (`id`, `customTitle`, `customTitle_en`, `customImage`, `displayOrder`, `isActive`, `createdAt`, `updatedAt`, `category_id`, `restaurant_id`) VALUES
(1, NULL, NULL, '', 0, 1, '2026-01-07 14:45:50.234775', '2026-01-07 14:45:50.234794', 2, 2),
(2, NULL, NULL, '', 0, 1, '2026-01-07 14:45:50.236611', '2026-01-07 14:45:50.236627', 3, 2),
(3, NULL, NULL, '', 0, 1, '2026-01-07 14:45:50.238148', '2026-01-07 14:45:50.238165', 4, 2),
(4, NULL, NULL, '', 0, 1, '2026-01-08 09:52:03.138980', '2026-01-08 09:52:03.139002', 2, 5),
(5, NULL, NULL, '', 0, 1, '2026-01-08 09:52:03.140772', '2026-01-08 09:52:03.140788', 3, 5),
(6, NULL, NULL, '', 0, 1, '2026-01-08 09:52:03.142353', '2026-01-08 09:52:03.142370', 5, 5),
(7, NULL, NULL, '', 0, 1, '2026-01-08 09:52:03.143800', '2026-01-08 09:52:03.143816', 6, 5);

-- --------------------------------------------------------

--
-- Table structure for table `menu_menupaperdesien`
--

CREATE TABLE `menu_menupaperdesien` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `createAt` datetime(6) NOT NULL,
  `image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_menuview`
--

CREATE TABLE `menu_menuview` (
  `id` bigint(20) NOT NULL,
  `session_key` varchar(40) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_requesttocreatepapermenu`
--

CREATE TABLE `menu_requesttocreatepapermenu` (
  `id` bigint(20) NOT NULL,
  `text_content` longtext DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `background_image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `paper_id` bigint(20) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu_restaurant`
--

CREATE TABLE `menu_restaurant` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_en` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `displayOrder` int(11) DEFAULT NULL,
  `createdAt` datetime(6) DEFAULT NULL,
  `updatedAt` datetime(6) DEFAULT NULL,
  `english_name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `description_en` longtext DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `coverImage` varchar(100) DEFAULT NULL,
  `text` longtext NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `address_en` longtext DEFAULT NULL,
  `openingTime` time(6) DEFAULT NULL,
  `closingTime` time(6) DEFAULT NULL,
  `minimumOrder` decimal(10,2) DEFAULT NULL,
  `deliveryFee` decimal(10,2) DEFAULT NULL,
  `taxRate` decimal(5,2) DEFAULT NULL,
  `isSeo` tinyint(1) DEFAULT NULL,
  `expireDate` datetime(6) DEFAULT NULL,
  `show_usd_price` tinyint(1) NOT NULL,
  `show_preparation_time` tinyint(1) NOT NULL,
  `menu_active` tinyint(1) NOT NULL,
  `owner_id` char(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `menu_restaurant`
--

INSERT INTO `menu_restaurant` (`id`, `title`, `title_en`, `slug`, `isActive`, `displayOrder`, `createdAt`, `updatedAt`, `english_name`, `description`, `description_en`, `logo`, `coverImage`, `text`, `phone`, `address`, `address_en`, `openingTime`, `closingTime`, `minimumOrder`, `deliveryFee`, `taxRate`, `isSeo`, `expireDate`, `show_usd_price`, `show_preparation_time`, `menu_active`, `owner_id`) VALUES
(2, 'TIB', NULL, 'tib', 1, 0, '2026-01-07 14:31:28.068534', '2026-01-08 08:55:29.116046', 'tib', '', '', '', '', '<p>مینی&zwnj;بار TIB تبریز | پذیرایی فوق&zwnj;حرفه&zwnj;ای در قلب شهر اولین&zwnj;ها</p>\r\n\r\n<p><strong>آدرس:</strong> چهارراه منصور، همکف مجتمع تجاری اطلس، تبریز<br />\r\n<strong>کلمه کلیدی اصلی:</strong> مینی بار tib تبریز</p>\r\n\r\n<p>تجربه&zwnj;ای بی&zwnj;نظیر از پذیرایی مدرن در شهر تاریخی تبریز</p>\r\n\r\n<p>تبریز، شهر فرهنگ، تاریخ و هنر، اکنون میزبان یک تجربه&zwnj;ی مدرن و منحصربه&zwnj;فرد در زمینه&zwnj;ی پذیرایی و بار است. <strong>مینی&zwnj;بار TIB تبریز</strong> با تلفیقی از هنر شیرین&zwnj;کاری سنتی و مدرنیته&zwnj;ی خدمات حرفه&zwnj;ای، فضایی منحصربه&zwnj;فرد را برای مشتریان خوش&zwnj;سلیقه&zwnj;ی آذربایجانی ایجاد کرده است.</p>\r\n\r\n<p>طراحی داخلی و فضاسازی: ترکیب هنر و مدرنیته</p>\r\n\r\n<p>همان&zwnj;طور که تبریز در عین حفظ بناهای تاریخی، چهره&zwnj;ای مدرن به خود گرفته است، طراحی داخلی <strong>مینی&zwnj;بار TIB</strong> نیز با الهام از همین دوگانگی زیبا شکل گرفته است. فضای همکف مجتمع تجاری اطلس در چهارراه منصور، با دکوراسیونی مدرن، نورپردازی حساب&zwnj;شده و مبلمان راحت، محیطی ایده&zwnj;آل را برای یک دورهمی کاری، جشن کوچک یا صرفاً یک عصرانه&zwnj;ی متفاوت فراهم می&zwnj;آورد.</p>\r\n\r\n<p>منوی فوق&zwnj;حرفه&zwnj;ای: ترکیبی از نوشیدنی&zwnj;های ویژه و غذاهای لذیذ</p>\r\n\r\n<p><strong>مینی&zwnj;بار TIB</strong> با افتخار منویی دوست&zwnj;داشتنی ارائه می&zwnj;دهد که هم نیاز نوشیدنی&zwnj;های ویژه را پاسخ می&zwnj;گوید و هم با غذاهای سبک و خوشمزه از مهمانان پذیرایی می&zwnj;کند.</p>\r\n\r\n<p><strong>منوی نوشیدنی&zwnj;های ویژه</strong></p>\r\n\r\n<p><strong>نوشیدنی&zwnj;های گرم</strong></p>\r\n\r\n<ul>\r\n	<li>\r\n	<p><strong>لاته</strong> &mdash; 86 تومان | ترکیبی نرم از اسپرسو و شیر بخارپز</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>اسپرسو</strong> &mdash; 60 تومان | شات خالص و قوی قهوه</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>ماکیاتو</strong> &mdash; 89 تومان | اسپرسو با لکه&zwnj;ای از کف شیر</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>ماسالا</strong> &mdash; 90 تومان | چای هندی با ادویه&zwnj;های گرم</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>هات چاکلت</strong> &mdash; 95 تومان | شکلات داغ غنی و لذیذ</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>چای</strong> &mdash; 40 تومان | انواع چای مرغوب</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>دمنوش</strong> &mdash; 50 تومان | گیاهان دارویی آرامش&zwnj;بخش</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>ترک</strong> &mdash; 85 تومان | قهوه&zwnj;ای اصیل به روش سنتی</p>\r\n	</li>\r\n</ul>\r\n\r\n<p><strong>نوشیدنی&zwnj;های سرد</strong></p>\r\n\r\n<ul>\r\n	<li>\r\n	<p><strong>آیس آمریکانو</strong> &mdash; 80 تومان | اسپرسو خنک با آب سرد</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>آیس لاته</strong> &mdash; 86 تومان | اسپرسو با شیر سرد و یخ</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>آیس کارامل</strong> &mdash; 89 تومان | ترکیب شیرین اسپرسو، شیر و سس کارامل</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>کوک اسپرسو</strong> &mdash; 90 تومان | انرژیزایی با اسپرسو و آب گازدار</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>پاور</strong> &mdash; 130 تومان | نوشیدنی انرژی&zwnj;بخش ویژه</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>آبمیوه</strong> &mdash; 140 تومان | تازه و طبیعی</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>لوسی</strong> &mdash; 160 تومان | قهوه سرد با طعم بلوبری</p>\r\n	</li>\r\n</ul>\r\n\r\n<p><strong>منوی کیک و دسر</strong></p>\r\n\r\n<ul>\r\n	<li>\r\n	<p><strong>کیک شکلاتی</strong> &mdash; 80 تومان | غنی و لطیف</p>\r\n	</li>\r\n	<li>\r\n	<p><strong>خاگینه</strong> &mdash; 45 تومان | سبک و خوشمزه</p>\r\n	</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>', NULL, '', '', NULL, NULL, NULL, NULL, 9.00, 1, '2026-12-29 14:31:28.000000', 0, 1, 1, '1dcda7a3c14d471089ebd281ebe2b491'),
(4, 'یسی', NULL, 'ee', 1, 0, '2026-01-08 08:59:59.950243', '2026-01-08 09:00:38.671444', 'ee', '', '', '', '', '<p>خالی</p>', NULL, '', '', NULL, NULL, NULL, NULL, 9.00, 1, '2026-01-10 08:59:59.000000', 0, 1, 1, '2be599b28fa846caa13851a49de2bff8'),
(5, 'کافه ونگوگ', NULL, 'vangog', 1, 0, '2026-01-08 09:36:59.846295', '2026-01-08 10:06:28.097679', 'vangog', NULL, NULL, 'restaurants/logos/55a5c168-d451-4254-953b-46314bdb59c8.jpg', '', 'خالی', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 9.00, 1, '2026-02-06 09:36:59.844615', 0, 1, 1, '2042c4e14df64eeca4e8c70d9687e64f');

-- --------------------------------------------------------

--
-- Table structure for table `order_menuimage`
--

CREATE TABLE `order_menuimage` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_ordermenu`
--

CREATE TABLE `order_ordermenu` (
  `id` bigint(20) NOT NULL,
  `isfinaly` tinyint(1) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` smallint(5) UNSIGNED NOT NULL CHECK (`status` >= 0),
  `is_seo_enabled` tinyint(1) NOT NULL,
  `base_price` int(10) UNSIGNED NOT NULL CHECK (`base_price` >= 0),
  `seo_extra_price` int(10) UNSIGNED NOT NULL CHECK (`seo_extra_price` >= 0),
  `final_price` int(10) UNSIGNED NOT NULL CHECK (`final_price` >= 0),
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `peyment_peyment`
--

CREATE TABLE `peyment_peyment` (
  `id` bigint(20) NOT NULL,
  `createAt` datetime(6) NOT NULL,
  `updateAt` datetime(6) NOT NULL,
  `amount` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `isFinaly` tinyint(1) NOT NULL,
  `statusCode` int(11) DEFAULT NULL,
  `refId` varchar(50) DEFAULT NULL,
  `payment_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `plan_order_id` int(11) DEFAULT NULL,
  `product_order_id` int(11) DEFAULT NULL,
  `customer_id` char(32) NOT NULL,
  `order_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `peyment_peyment`
--

INSERT INTO `peyment_peyment` (`id`, `createAt`, `updateAt`, `amount`, `description`, `isFinaly`, `statusCode`, `refId`, `payment_type`, `status`, `plan_order_id`, `product_order_id`, `customer_id`, `order_id`) VALUES
(1, '2026-01-07 10:46:43.015366', '2026-01-07 10:46:43.015698', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 1, '6f0bbf15b0c145ed8745949f18187651', NULL),
(2, '2026-01-07 10:58:57.329933', '2026-01-07 10:58:57.330290', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 2, '6f0bbf15b0c145ed8745949f18187651', NULL),
(3, '2026-01-07 11:09:50.951791', '2026-01-07 11:09:50.952141', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 3, '6f0bbf15b0c145ed8745949f18187651', NULL),
(4, '2026-01-07 13:44:44.326279', '2026-01-07 13:44:44.326600', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 4, '6f0bbf15b0c145ed8745949f18187651', NULL),
(5, '2026-01-08 07:24:02.837469', '2026-01-08 07:24:02.837819', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 5, '2be599b28fa846caa13851a49de2bff8', NULL),
(6, '2026-01-08 07:43:58.012865', '2026-01-08 07:43:58.013209', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 6, '2be599b28fa846caa13851a49de2bff8', NULL),
(7, '2026-01-08 07:46:54.291151', '2026-01-08 07:47:05.146108', 12000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'canceled', NULL, 7, '2be599b28fa846caa13851a49de2bff8', NULL),
(8, '2026-01-08 07:48:13.840569', '2026-01-08 07:48:13.840902', 100000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 8, '2be599b28fa846caa13851a49de2bff8', NULL),
(9, '2026-01-08 07:51:27.588235', '2026-01-08 07:51:27.588530', 100000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 9, '2be599b28fa846caa13851a49de2bff8', NULL),
(10, '2026-01-08 07:55:46.627041', '2026-01-08 07:55:46.627363', 20000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'pending', NULL, 10, '2be599b28fa846caa13851a49de2bff8', NULL),
(11, '2026-01-08 08:05:51.545778', '2026-01-08 08:06:30.872001', 20000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 1, 100, '81400813601', 'product', 'success', NULL, 11, '2be599b28fa846caa13851a49de2bff8', NULL),
(12, '2026-01-08 08:42:07.502928', '2026-01-08 08:42:51.332282', 20000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 1, 100, '81402238601', 'product', 'success', NULL, 12, '2be599b28fa846caa13851a49de2bff8', NULL),
(13, '2026-01-08 08:46:38.752691', '2026-01-08 08:47:23.489847', 20000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 1, 100, '81402416401', 'product', 'success', NULL, 13, '2be599b28fa846caa13851a49de2bff8', NULL),
(14, '2026-01-08 09:00:54.378503', '2026-01-08 09:00:57.036892', 29000000, 'پرداخت محصولات (شامل 0 تومان مالیات)', 0, NULL, NULL, 'product', 'canceled', NULL, 14, '2be599b28fa846caa13851a49de2bff8', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `plan_plan`
--

CREATE TABLE `plan_plan` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `price` int(10) UNSIGNED DEFAULT NULL CHECK (`price` >= 0),
  `expiryDays` int(11) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `isFavorit` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `plan_plan`
--

INSERT INTO `plan_plan` (`id`, `name`, `slug`, `description`, `price`, `expiryDays`, `isActive`, `createdAt`, `updatedAt`, `isFavorit`) VALUES
(1, 'پلن پایه', 'basic-plan', 'این پلن مخصوص کافه های کوچیک و با تعداد غذا و مشتریان متوسط', 2900000, 365, 1, '2026-01-07 08:34:17.478602', '2026-01-08 08:58:16.229674', 0),
(2, 'پلن حرفه ای', 'ln-hrfh', 'این پلن مخصوص رستوران ها با تعداد غذای و مشتریان بالا و رزرویاسون میز', 3900000, 365, 1, '2026-01-07 08:50:25.989542', '2026-01-08 08:58:35.759038', 1),
(3, 'پلن VIP', 'ln-vip', 'مخصوص رستوران های بزرگ و برتر با غذا و مشتریان زیاد و خاص', 40000000, 365, 1, '2026-01-07 09:15:22.235520', '2026-01-08 08:58:55.931014', 0);

-- --------------------------------------------------------

--
-- Table structure for table `plan_planfeature`
--

CREATE TABLE `plan_planfeature` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  `order` int(11) NOT NULL,
  `isAvailable` tinyint(1) NOT NULL,
  `plan_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `plan_planfeature`
--

INSERT INTO `plan_planfeature` (`id`, `title`, `value`, `order`, `isAvailable`, `plan_id`) VALUES
(1, 'پلتفرم منو دیجیتال', NULL, 0, 0, 1),
(2, 'پنل کنترل غذا ها', NULL, 0, 0, 1),
(3, 'تعداد نامحدود غذا', NULL, 0, 0, 1),
(4, 'تعداد نامحدود دسته بندی', NULL, 0, 0, 1),
(5, 'شخصی سازی تصاویر', NULL, 0, 0, 1),
(6, 'دسترسی به منو کاغذی', NULL, 0, 0, 1),
(7, 'امکانات پلن پایه', NULL, 0, 1, 2),
(8, 'دسترسی به پنل رزر میز', NULL, 0, 1, 2),
(9, '2 عدد استند رایگان', NULL, 0, 1, 2),
(10, '1 سال پشتیبانی رایگان', NULL, 0, 1, 2),
(11, 'افزودن غذا توسط شرکت', NULL, 0, 1, 2),
(12, 'سئو و نمایش در نتایج جستجو گوگل', NULL, 0, 1, 2),
(13, 'امکانات پلن پایه و حرفه ای', NULL, 0, 1, 3),
(14, 'دامنه اختصاصی', NULL, 0, 1, 3),
(15, 'خرید و فروش انلاین غذا', NULL, 0, 1, 3),
(16, 'طراحی ظاهر اختصاصی', NULL, 0, 1, 3),
(17, 'طراحی کد نویسی اختصاصی', NULL, 0, 1, 3),
(18, '1 سال پشتیبانی رایگان', NULL, 0, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `plan_planorder`
--

CREATE TABLE `plan_planorder` (
  `id` bigint(20) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `finalPrice` int(10) UNSIGNED NOT NULL CHECK (`finalPrice` >= 0),
  `isActive` tinyint(1) NOT NULL,
  `isPaid` tinyint(1) NOT NULL,
  `paidAt` datetime(6) DEFAULT NULL,
  `expiryDate` datetime(6) DEFAULT NULL,
  `trackingCode` varchar(100) DEFAULT NULL,
  `plan_id` bigint(20) NOT NULL,
  `restaurant_id` bigint(20) DEFAULT NULL,
  `user_id` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_orderdetailinfo`
--

CREATE TABLE `product_orderdetailinfo` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `province` varchar(100) NOT NULL,
  `codePost` varchar(10) NOT NULL,
  `description` longtext DEFAULT NULL,
  `discount_code` varchar(50) DEFAULT NULL,
  `discount_amount` int(10) UNSIGNED NOT NULL CHECK (`discount_amount` >= 0),
  `created_at` datetime(6) NOT NULL,
  `product_order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_product`
--

CREATE TABLE `product_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `price` int(10) UNSIGNED NOT NULL CHECK (`price` >= 0),
  `description` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `publish_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `product_product`
--

INSERT INTO `product_product` (`id`, `name`, `price`, `description`, `is_active`, `publish_date`) VALUES
(1, 'پلاک رومیزی فلزی ( استند رومیزی کافه )', 105000, 'استند رومیزی کافه', 1, '2026-01-07 09:26:51.615511');

-- --------------------------------------------------------

--
-- Table structure for table `product_productfeature`
--

CREATE TABLE `product_productfeature` (
  `id` bigint(20) NOT NULL,
  `key` varchar(100) NOT NULL,
  `value` varchar(200) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `product_productfeature`
--

INSERT INTO `product_productfeature` (`id`, `key`, `value`, `slug`, `product_id`) VALUES
(1, 'جنس', 'ورق آلومینیوم', 'S', 1),
(2, 'ابعاد محصول', 'تا شده  8.5*7 سانتیمتر', 'DSDS', 1),
(3, 'ابعاد چاپ', '7*5 سانتیمتر', 'SDSD', 1),
(4, 'گارانتی / ضمان', 'دارد', 'SDS', 1);

-- --------------------------------------------------------

--
-- Table structure for table `product_productgallery`
--

CREATE TABLE `product_productgallery` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `alt_text` varchar(200) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `product_productgallery`
--

INSERT INTO `product_productgallery` (`id`, `image`, `alt_text`, `is_active`, `product_id`) VALUES
(1, 'products/gallery/desktop-plate-1-768x768.jpg', 'س', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `product_productorder`
--

CREATE TABLE `product_productorder` (
  `id` bigint(20) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `tax_amount` int(10) UNSIGNED NOT NULL CHECK (`tax_amount` >= 0),
  `final_price` int(10) UNSIGNED NOT NULL CHECK (`final_price` >= 0),
  `isPaid` tinyint(1) NOT NULL,
  `paidAt` datetime(6) DEFAULT NULL,
  `trackingCode` varchar(100) DEFAULT NULL,
  `expiryDate` datetime(6) DEFAULT NULL,
  `plan_id` bigint(20) NOT NULL,
  `user_id` char(32) NOT NULL,
  `total_price` int(10) UNSIGNED NOT NULL CHECK (`total_price` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `product_productorder`
--

INSERT INTO `product_productorder` (`id`, `createdAt`, `status`, `tax_amount`, `final_price`, `isPaid`, `paidAt`, `trackingCode`, `expiryDate`, `plan_id`, `user_id`, `total_price`) VALUES
(1, '2026-01-07 09:28:08.912796', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '6f0bbf15b0c145ed8745949f18187651', 0),
(2, '2026-01-07 10:58:49.346141', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '6f0bbf15b0c145ed8745949f18187651', 0),
(3, '2026-01-07 11:09:49.643600', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '6f0bbf15b0c145ed8745949f18187651', 0),
(4, '2026-01-07 13:44:41.936095', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '6f0bbf15b0c145ed8745949f18187651', 0),
(5, '2026-01-08 07:23:59.838626', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(6, '2026-01-08 07:43:56.082493', 'pending', 0, 1200000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(7, '2026-01-08 07:46:52.413190', 'failed', 0, 1200000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(8, '2026-01-08 07:48:12.199539', 'pending', 0, 10000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(9, '2026-01-08 07:51:26.262515', 'pending', 0, 10000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(10, '2026-01-08 07:55:44.999987', 'pending', 0, 2000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0),
(11, '2026-01-08 08:05:50.178226', 'paid', 0, 2000, 1, '2026-01-08 08:06:30.875130', NULL, '2027-01-08 08:06:30.877680', 1, '2be599b28fa846caa13851a49de2bff8', 0),
(12, '2026-01-08 08:42:05.703599', 'paid', 0, 2000, 1, '2026-01-08 08:42:51.334699', NULL, '2027-01-08 08:42:51.336797', 1, '2be599b28fa846caa13851a49de2bff8', 0),
(13, '2026-01-08 08:46:36.837889', 'paid', 0, 2000, 1, '2026-01-08 08:47:23.492542', NULL, '2027-01-08 08:47:23.494746', 1, '2be599b28fa846caa13851a49de2bff8', 0),
(14, '2026-01-08 09:00:52.003756', 'failed', 0, 2900000, 0, NULL, NULL, NULL, 1, '2be599b28fa846caa13851a49de2bff8', 0);

-- --------------------------------------------------------

--
-- Table structure for table `product_productorderdetail`
--

CREATE TABLE `product_productorderdetail` (
  `id` bigint(20) NOT NULL,
  `price` int(10) UNSIGNED NOT NULL CHECK (`price` >= 0),
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `product_name` varchar(200) NOT NULL,
  `product_description` longtext NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `product_order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `restaurant_food_restaurant`
--

CREATE TABLE `restaurant_food_restaurant` (
  `id` bigint(20) NOT NULL,
  `custom_price` int(10) UNSIGNED DEFAULT NULL CHECK (`custom_price` >= 0),
  `custom_image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `display_order` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `food_id` bigint(20) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_customer`
--

CREATE TABLE `table_customer` (
  `id` bigint(20) NOT NULL,
  `national_code` varchar(10) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `birth_date` varchar(10) DEFAULT NULL,
  `is_vip` tinyint(1) NOT NULL,
  `special_notes` longtext DEFAULT NULL,
  `total_reservations` int(10) UNSIGNED NOT NULL CHECK (`total_reservations` >= 0),
  `successful_reservations` int(10) UNSIGNED NOT NULL CHECK (`successful_reservations` >= 0),
  `cancellation_count` int(10) UNSIGNED NOT NULL CHECK (`cancellation_count` >= 0),
  `is_active` tinyint(1) DEFAULT NULL,
  `created_jalali` varchar(10) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_reservation`
--

CREATE TABLE `table_reservation` (
  `id` bigint(20) NOT NULL,
  `reservation_code` varchar(10) NOT NULL,
  `reservation_jalali_date` varchar(10) DEFAULT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `duration_minutes` int(10) UNSIGNED NOT NULL CHECK (`duration_minutes` >= 0),
  `guest_count` int(10) UNSIGNED NOT NULL CHECK (`guest_count` >= 0),
  `special_requests` longtext DEFAULT NULL,
  `reservation_status` varchar(20) NOT NULL,
  `is_confirmed` tinyint(1) NOT NULL,
  `confirmation_code` varchar(6) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `customer_arrived` tinyint(1) NOT NULL,
  `arrival_jalali_time` varchar(16) DEFAULT NULL,
  `created_jalali` varchar(10) DEFAULT NULL,
  `created_jalali_time` varchar(8) DEFAULT NULL,
  `updated_jalali` varchar(16) DEFAULT NULL,
  `customer_id` bigint(20) DEFAULT NULL,
  `table_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_reservationsettings`
--

CREATE TABLE `table_reservationsettings` (
  `id` bigint(20) NOT NULL,
  `max_advance_days` int(10) UNSIGNED NOT NULL CHECK (`max_advance_days` >= 0),
  `min_advance_hours` int(10) UNSIGNED NOT NULL CHECK (`min_advance_hours` >= 0),
  `max_guests_per_reservation` int(10) UNSIGNED NOT NULL CHECK (`max_guests_per_reservation` >= 0),
  `default_reservation_duration` int(10) UNSIGNED NOT NULL CHECK (`default_reservation_duration` >= 0),
  `slot_duration` int(10) UNSIGNED NOT NULL CHECK (`slot_duration` >= 0),
  `auto_confirm_reservations` tinyint(1) NOT NULL,
  `require_phone_verification` tinyint(1) NOT NULL,
  `max_reservations_per_time_slot` int(10) UNSIGNED NOT NULL CHECK (`max_reservations_per_time_slot` >= 0),
  `allow_same_day_reservations` tinyint(1) NOT NULL,
  `friday_off` tinyint(1) NOT NULL,
  `thursday_evening_off` tinyint(1) NOT NULL,
  `special_holidays` longtext NOT NULL,
  `created_jalali` varchar(10) DEFAULT NULL,
  `updated_jalali` varchar(16) DEFAULT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_table`
--

CREATE TABLE `table_table` (
  `id` bigint(20) NOT NULL,
  `table_number` varchar(50) NOT NULL,
  `table_type` varchar(20) NOT NULL,
  `capacity` int(10) UNSIGNED NOT NULL CHECK (`capacity` >= 0),
  `description` longtext DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `min_reservation_duration` int(10) UNSIGNED NOT NULL CHECK (`min_reservation_duration` >= 0),
  `max_reservation_duration` int(10) UNSIGNED NOT NULL CHECK (`max_reservation_duration` >= 0),
  `has_view` tinyint(1) NOT NULL,
  `is_smoking` tinyint(1) NOT NULL,
  `is_vip` tinyint(1) NOT NULL,
  `floor` int(10) UNSIGNED NOT NULL CHECK (`floor` >= 0),
  `section` varchar(100) NOT NULL,
  `created_jalali` varchar(10) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_workingday`
--

CREATE TABLE `table_workingday` (
  `id` bigint(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `display_order` int(11) NOT NULL,
  `is_weekend` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `table_workingtime`
--

CREATE TABLE `table_workingtime` (
  `id` bigint(20) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `break_start` time(6) DEFAULT NULL,
  `break_end` time(6) DEFAULT NULL,
  `day_id` bigint(20) NOT NULL,
  `restaurant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_customuser`
--

CREATE TABLE `user_customuser` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` char(32) NOT NULL,
  `mobileNumber` varchar(11) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `family` varchar(60) DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `user_customuser`
--

INSERT INTO `user_customuser` (`password`, `last_login`, `is_superuser`, `id`, `mobileNumber`, `email`, `name`, `family`, `gender`, `birth_date`, `is_active`, `is_staff`) VALUES
('pbkdf2_sha256$320000$4wRcvZ5qrlY4c4kaoGw4R0$LKx8SmD14pVsKhG8+oI8inFP5roWAPdEDS0olhGmYZg=', '2026-01-08 08:31:45.423825', 1, '1dcda7a3c14d471089ebd281ebe2b491', '09149663136', NULL, 'احسان', 'تیب', 'M', NULL, 1, 1),
('', '2026-01-08 09:34:51.088865', 0, '2042c4e14df64eeca4e8c70d9687e64f', '09396897644', NULL, 'اقای', 'ونگوگ', 'M', NULL, 1, 0),
('', '2026-01-08 07:21:35.906007', 0, '2be599b28fa846caa13851a49de2bff8', '09146597108', NULL, 'abbas', 'd', 'M', NULL, 1, 0),
('pbkdf2_sha256$320000$8H9ebib5gVpAjYQfufNuU9$cHj6Y9284AK5m1Oqo+T34VsvcfrfPsNsPbbhpHwfUdc=', '2026-01-07 09:27:20.643650', 1, '6f0bbf15b0c145ed8745949f18187651', '09309087909', 's@gmail.com', 'sa', 'abadkar', '', '2026-01-07', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_customuser_groups`
--

CREATE TABLE `user_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` char(32) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_customuser_user_permissions`
--

CREATE TABLE `user_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` char(32) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_userdevice`
--

CREATE TABLE `user_userdevice` (
  `id` bigint(20) NOT NULL,
  `deviceInfo` varchar(255) NOT NULL,
  `ipAddress` char(39) DEFAULT NULL,
  `createdAt` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_usersecurity`
--

CREATE TABLE `user_usersecurity` (
  `id` bigint(20) NOT NULL,
  `activeCode` varchar(16) DEFAULT NULL,
  `expireCode` datetime(6) DEFAULT NULL,
  `isBan` tinyint(1) NOT NULL,
  `isInfoFiled` tinyint(1) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `user_usersecurity`
--

INSERT INTO `user_usersecurity` (`id`, `activeCode`, `expireCode`, `isBan`, `isInfoFiled`, `createdAt`, `user_id`) VALUES
(1, '76892', '2026-01-08 07:22:36.305370', 0, 0, '2026-01-07 08:32:34.140449', '6f0bbf15b0c145ed8745949f18187651'),
(2, NULL, NULL, 0, 0, '2026-01-07 14:30:13.168412', '1dcda7a3c14d471089ebd281ebe2b491'),
(3, NULL, NULL, 0, 0, '2026-01-08 07:21:04.003603', '2be599b28fa846caa13851a49de2bff8'),
(4, NULL, NULL, 0, 0, '2026-01-08 09:34:36.100837', '2042c4e14df64eeca4e8c70d9687e64f');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `blog_author`
--
ALTER TABLE `blog_author`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blog_blog`
--
ALTER TABLE `blog_blog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blog_blog_grop_blog_id_3d70f028_fk_blog_group_blog_id` (`grop_blog_id`);

--
-- Indexes for table `blog_blog_Auther_blog`
--
ALTER TABLE `blog_blog_Auther_blog`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `blog_blog_Auther_blog_blog_id_author_id_d2800935_uniq` (`blog_id`,`author_id`),
  ADD KEY `blog_blog_Auther_blog_author_id_d348a5aa_fk_blog_author_id` (`author_id`);

--
-- Indexes for table `blog_group_blog`
--
ALTER TABLE `blog_group_blog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `blog_meta_tag`
--
ALTER TABLE `blog_meta_tag`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blog_meta_tag_blog_id_e82227b9_fk_blog_blog_id` (`blog_id`);

--
-- Indexes for table `blog_more_question`
--
ALTER TABLE `blog_more_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blog_more_question_blog_id_7ba8a432_fk_blog_blog_id` (`blog_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_user_customuser_id` (`user_id`);

--
-- Indexes for table `django_celery_beat_clockedschedule`
--
ALTER TABLE `django_celery_beat_clockedschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_crontabschedule`
--
ALTER TABLE `django_celery_beat_crontabschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_intervalschedule`
--
ALTER TABLE `django_celery_beat_intervalschedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  ADD KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  ADD KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  ADD KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`);

--
-- Indexes for table `django_celery_beat_periodictasks`
--
ALTER TABLE `django_celery_beat_periodictasks`
  ADD PRIMARY KEY (`ident`);

--
-- Indexes for table `django_celery_beat_solarschedule`
--
ALTER TABLE `django_celery_beat_solarschedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`);

--
-- Indexes for table `django_celery_results_chordcounter`
--
ALTER TABLE `django_celery_results_chordcounter`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `group_id` (`group_id`);

--
-- Indexes for table `django_celery_results_groupresult`
--
ALTER TABLE `django_celery_results_groupresult`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `group_id` (`group_id`),
  ADD KEY `django_cele_date_cr_bd6c1d_idx` (`date_created`),
  ADD KEY `django_cele_date_do_caae0e_idx` (`date_done`);

--
-- Indexes for table `django_celery_results_taskresult`
--
ALTER TABLE `django_celery_results_taskresult`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `task_id` (`task_id`),
  ADD KEY `django_cele_task_na_08aec9_idx` (`task_name`),
  ADD KEY `django_cele_status_9b6201_idx` (`status`),
  ADD KEY `django_cele_worker_d54dd8_idx` (`worker`),
  ADD KEY `django_cele_date_cr_f04a50_idx` (`date_created`),
  ADD KEY `django_cele_date_do_f59aad_idx` (`date_done`),
  ADD KEY `django_cele_periodi_1993cf_idx` (`periodic_task_name`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `main_content`
--
ALTER TABLE `main_content`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_course`
--
ALTER TABLE `main_course`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_textimageblock`
--
ALTER TABLE `main_textimageblock`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_category`
--
ALTER TABLE `menu_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `menu_category_parent_id_82b84bf3_fk_menu_category_id` (`parent_id`);

--
-- Indexes for table `menu_exchangerate`
--
ALTER TABLE `menu_exchangerate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_food`
--
ALTER TABLE `menu_food`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `menu_food_menuCategory_id_39355987_fk_menu_menucategory_id` (`menuCategory_id`);

--
-- Indexes for table `menu_food_restaurants`
--
ALTER TABLE `menu_food_restaurants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `menu_food_restaurants_food_id_restaurant_id_9d40e4a4_uniq` (`food_id`,`restaurant_id`),
  ADD KEY `menu_food_restaurant_restaurant_id_0c79144b_fk_menu_rest` (`restaurant_id`);

--
-- Indexes for table `menu_menucategory`
--
ALTER TABLE `menu_menucategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `menu_menucategory_restaurant_id_category_id_939e1bee_uniq` (`restaurant_id`,`category_id`),
  ADD KEY `menu_menucategory_category_id_1e285993_fk_menu_category_id` (`category_id`);

--
-- Indexes for table `menu_menupaperdesien`
--
ALTER TABLE `menu_menupaperdesien`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_menuview`
--
ALTER TABLE `menu_menuview`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `menu_menuview_restaurant_id_session_key_b0442eae_uniq` (`restaurant_id`,`session_key`),
  ADD KEY `menu_menuview_session_key_7ddcef05` (`session_key`),
  ADD KEY `menu_menuvi_restaur_726959_idx` (`restaurant_id`,`created_at`),
  ADD KEY `menu_menuvi_session_b194fb_idx` (`session_key`,`restaurant_id`),
  ADD KEY `menu_menuvi_ip_addr_e3fd47_idx` (`ip_address`,`restaurant_id`);

--
-- Indexes for table `menu_requesttocreatepapermenu`
--
ALTER TABLE `menu_requesttocreatepapermenu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `menu_requesttocreate_paper_id_9317bf01_fk_menu_menu` (`paper_id`),
  ADD KEY `menu_requesttocreate_restaurant_id_1e580cd3_fk_menu_rest` (`restaurant_id`);

--
-- Indexes for table `menu_restaurant`
--
ALTER TABLE `menu_restaurant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD UNIQUE KEY `english_name` (`english_name`),
  ADD KEY `menu_restaurant_owner_id_e34fb125_fk_user_customuser_id` (`owner_id`);

--
-- Indexes for table `order_menuimage`
--
ALTER TABLE `order_menuimage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_menuimage_order_id_1c3adc60_fk_order_ordermenu_id` (`order_id`);

--
-- Indexes for table `order_ordermenu`
--
ALTER TABLE `order_ordermenu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_ordermenu_restaurant_id_48018483_fk_menu_restaurant_id` (`restaurant_id`);

--
-- Indexes for table `peyment_peyment`
--
ALTER TABLE `peyment_peyment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `peyment_peyment_customer_id_e6ea7ec5_fk_user_customuser_id` (`customer_id`),
  ADD KEY `peyment_peyment_order_id_dcb25998_fk_order_ordermenu_id` (`order_id`);

--
-- Indexes for table `plan_plan`
--
ALTER TABLE `plan_plan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `plan_planfeature`
--
ALTER TABLE `plan_planfeature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plan_planfeature_plan_id_0a6669ad_fk_plan_plan_id` (`plan_id`);

--
-- Indexes for table `plan_planorder`
--
ALTER TABLE `plan_planorder`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plan_planorder_plan_id_e1d4bc18_fk_plan_plan_id` (`plan_id`),
  ADD KEY `plan_planorder_restaurant_id_2080f1e7_fk_menu_restaurant_id` (`restaurant_id`),
  ADD KEY `plan_planor_user_id_432a8a_idx` (`user_id`,`createdAt`),
  ADD KEY `plan_planor_isPaid_eb5f72_idx` (`isPaid`,`createdAt`);

--
-- Indexes for table `product_orderdetailinfo`
--
ALTER TABLE `product_orderdetailinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_order_id` (`product_order_id`);

--
-- Indexes for table `product_product`
--
ALTER TABLE `product_product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_productfeature`
--
ALTER TABLE `product_productfeature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_productfeature_slug_9565910b` (`slug`),
  ADD KEY `product_productfeature_product_id_e984accf_fk_product_product_id` (`product_id`);

--
-- Indexes for table `product_productgallery`
--
ALTER TABLE `product_productgallery`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_productgallery_product_id_4680161b_fk_product_product_id` (`product_id`);

--
-- Indexes for table `product_productorder`
--
ALTER TABLE `product_productorder`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_productorder_plan_id_908d60e7_fk_plan_plan_id` (`plan_id`),
  ADD KEY `product_productorder_user_id_3f59f6bb_fk_user_customuser_id` (`user_id`);

--
-- Indexes for table `product_productorderdetail`
--
ALTER TABLE `product_productorderdetail`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_productorderdeta_product_order_id_product_4a825000_uniq` (`product_order_id`,`product_id`),
  ADD KEY `product_productorder_product_id_7f88cfe1_fk_product_p` (`product_id`);

--
-- Indexes for table `restaurant_food_restaurant`
--
ALTER TABLE `restaurant_food_restaurant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `restaurant_food_restaurant_restaurant_id_food_id_52724cff_uniq` (`restaurant_id`,`food_id`),
  ADD KEY `restaurant_food_restaurant_food_id_6aa7ff29_fk_menu_food_id` (`food_id`);

--
-- Indexes for table `table_customer`
--
ALTER TABLE `table_customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `national_code` (`national_code`),
  ADD KEY `table_custo_nationa_323dde_idx` (`national_code`),
  ADD KEY `table_custo_phone_n_5d3440_idx` (`phone_number`),
  ADD KEY `table_custo_is_vip_e19c55_idx` (`is_vip`);

--
-- Indexes for table `table_reservation`
--
ALTER TABLE `table_reservation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reservation_code` (`reservation_code`),
  ADD KEY `table_reser_reserva_301429_idx` (`reservation_code`),
  ADD KEY `table_reser_reserva_afa9b6_idx` (`reservation_jalali_date`),
  ADD KEY `table_reser_custome_40b2da_idx` (`customer_id`),
  ADD KEY `table_reser_reserva_673207_idx` (`reservation_status`),
  ADD KEY `table_reservation_table_id_0d35355c_fk_table_table_id` (`table_id`);

--
-- Indexes for table `table_reservationsettings`
--
ALTER TABLE `table_reservationsettings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `restaurant_id` (`restaurant_id`);

--
-- Indexes for table `table_table`
--
ALTER TABLE `table_table`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `table_table_restaurant_id_table_number_583e47cc_uniq` (`restaurant_id`,`table_number`);

--
-- Indexes for table `table_workingday`
--
ALTER TABLE `table_workingday`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `table_workingtime`
--
ALTER TABLE `table_workingtime`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `table_workingtime_restaurant_id_day_id_13f039c1_uniq` (`restaurant_id`,`day_id`),
  ADD KEY `table_workingtime_day_id_77584f23_fk_table_workingday_id` (`day_id`);

--
-- Indexes for table `user_customuser`
--
ALTER TABLE `user_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mobileNumber` (`mobileNumber`);

--
-- Indexes for table `user_customuser_groups`
--
ALTER TABLE `user_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_customuser_groups_customuser_id_group_id_e0a2f621_uniq` (`customuser_id`,`group_id`),
  ADD KEY `user_customuser_groups_group_id_bcbc9e48_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `user_customuser_user_permissions`
--
ALTER TABLE `user_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_customuser_user_per_customuser_id_permission_a5da865d_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `user_customuser_user_permission_id_e57e8b9a_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `user_userdevice`
--
ALTER TABLE `user_userdevice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_userdevice_user_id_3b07676b_fk_user_customuser_id` (`user_id`);

--
-- Indexes for table `user_usersecurity`
--
ALTER TABLE `user_usersecurity`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=197;

--
-- AUTO_INCREMENT for table `blog_author`
--
ALTER TABLE `blog_author`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blog_blog`
--
ALTER TABLE `blog_blog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blog_blog_Auther_blog`
--
ALTER TABLE `blog_blog_Auther_blog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blog_group_blog`
--
ALTER TABLE `blog_group_blog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blog_meta_tag`
--
ALTER TABLE `blog_meta_tag`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blog_more_question`
--
ALTER TABLE `blog_more_question`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `django_celery_beat_clockedschedule`
--
ALTER TABLE `django_celery_beat_clockedschedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_crontabschedule`
--
ALTER TABLE `django_celery_beat_crontabschedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_intervalschedule`
--
ALTER TABLE `django_celery_beat_intervalschedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_beat_solarschedule`
--
ALTER TABLE `django_celery_beat_solarschedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_results_chordcounter`
--
ALTER TABLE `django_celery_results_chordcounter`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_results_groupresult`
--
ALTER TABLE `django_celery_results_groupresult`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_celery_results_taskresult`
--
ALTER TABLE `django_celery_results_taskresult`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `main_content`
--
ALTER TABLE `main_content`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_course`
--
ALTER TABLE `main_course`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_textimageblock`
--
ALTER TABLE `main_textimageblock`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_category`
--
ALTER TABLE `menu_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `menu_exchangerate`
--
ALTER TABLE `menu_exchangerate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_food`
--
ALTER TABLE `menu_food`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `menu_food_restaurants`
--
ALTER TABLE `menu_food_restaurants`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `menu_menucategory`
--
ALTER TABLE `menu_menucategory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `menu_menupaperdesien`
--
ALTER TABLE `menu_menupaperdesien`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_menuview`
--
ALTER TABLE `menu_menuview`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_requesttocreatepapermenu`
--
ALTER TABLE `menu_requesttocreatepapermenu`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu_restaurant`
--
ALTER TABLE `menu_restaurant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order_menuimage`
--
ALTER TABLE `order_menuimage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_ordermenu`
--
ALTER TABLE `order_ordermenu`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `peyment_peyment`
--
ALTER TABLE `peyment_peyment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `plan_plan`
--
ALTER TABLE `plan_plan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `plan_planfeature`
--
ALTER TABLE `plan_planfeature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `plan_planorder`
--
ALTER TABLE `plan_planorder`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `product_orderdetailinfo`
--
ALTER TABLE `product_orderdetailinfo`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_product`
--
ALTER TABLE `product_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `product_productfeature`
--
ALTER TABLE `product_productfeature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `product_productgallery`
--
ALTER TABLE `product_productgallery`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `product_productorder`
--
ALTER TABLE `product_productorder`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `product_productorderdetail`
--
ALTER TABLE `product_productorderdetail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `restaurant_food_restaurant`
--
ALTER TABLE `restaurant_food_restaurant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_customer`
--
ALTER TABLE `table_customer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_reservation`
--
ALTER TABLE `table_reservation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_reservationsettings`
--
ALTER TABLE `table_reservationsettings`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_table`
--
ALTER TABLE `table_table`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_workingday`
--
ALTER TABLE `table_workingday`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `table_workingtime`
--
ALTER TABLE `table_workingtime`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_customuser_groups`
--
ALTER TABLE `user_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_customuser_user_permissions`
--
ALTER TABLE `user_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_userdevice`
--
ALTER TABLE `user_userdevice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_usersecurity`
--
ALTER TABLE `user_usersecurity`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `blog_blog`
--
ALTER TABLE `blog_blog`
  ADD CONSTRAINT `blog_blog_grop_blog_id_3d70f028_fk_blog_group_blog_id` FOREIGN KEY (`grop_blog_id`) REFERENCES `blog_group_blog` (`id`);

--
-- Constraints for table `blog_blog_Auther_blog`
--
ALTER TABLE `blog_blog_Auther_blog`
  ADD CONSTRAINT `blog_blog_Auther_blog_author_id_d348a5aa_fk_blog_author_id` FOREIGN KEY (`author_id`) REFERENCES `blog_author` (`id`),
  ADD CONSTRAINT `blog_blog_Auther_blog_blog_id_4ce15739_fk_blog_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_blog` (`id`);

--
-- Constraints for table `blog_meta_tag`
--
ALTER TABLE `blog_meta_tag`
  ADD CONSTRAINT `blog_meta_tag_blog_id_e82227b9_fk_blog_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_blog` (`id`);

--
-- Constraints for table `blog_more_question`
--
ALTER TABLE `blog_more_question`
  ADD CONSTRAINT `blog_more_question_blog_id_7ba8a432_fk_blog_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_blog` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`);

--
-- Constraints for table `django_celery_beat_periodictask`
--
ALTER TABLE `django_celery_beat_periodictask`
  ADD CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  ADD CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`);

--
-- Constraints for table `menu_category`
--
ALTER TABLE `menu_category`
  ADD CONSTRAINT `menu_category_parent_id_82b84bf3_fk_menu_category_id` FOREIGN KEY (`parent_id`) REFERENCES `menu_category` (`id`);

--
-- Constraints for table `menu_food`
--
ALTER TABLE `menu_food`
  ADD CONSTRAINT `menu_food_menuCategory_id_39355987_fk_menu_menucategory_id` FOREIGN KEY (`menuCategory_id`) REFERENCES `menu_menucategory` (`id`);

--
-- Constraints for table `menu_food_restaurants`
--
ALTER TABLE `menu_food_restaurants`
  ADD CONSTRAINT `menu_food_restaurant_restaurant_id_0c79144b_fk_menu_rest` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`),
  ADD CONSTRAINT `menu_food_restaurants_food_id_869fa0f3_fk_menu_food_id` FOREIGN KEY (`food_id`) REFERENCES `menu_food` (`id`);

--
-- Constraints for table `menu_menucategory`
--
ALTER TABLE `menu_menucategory`
  ADD CONSTRAINT `menu_menucategory_category_id_1e285993_fk_menu_category_id` FOREIGN KEY (`category_id`) REFERENCES `menu_category` (`id`),
  ADD CONSTRAINT `menu_menucategory_restaurant_id_4cdb2a55_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `menu_menuview`
--
ALTER TABLE `menu_menuview`
  ADD CONSTRAINT `menu_menuview_restaurant_id_71992620_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `menu_requesttocreatepapermenu`
--
ALTER TABLE `menu_requesttocreatepapermenu`
  ADD CONSTRAINT `menu_requesttocreate_paper_id_9317bf01_fk_menu_menu` FOREIGN KEY (`paper_id`) REFERENCES `menu_menupaperdesien` (`id`),
  ADD CONSTRAINT `menu_requesttocreate_restaurant_id_1e580cd3_fk_menu_rest` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `menu_restaurant`
--
ALTER TABLE `menu_restaurant`
  ADD CONSTRAINT `menu_restaurant_owner_id_e34fb125_fk_user_customuser_id` FOREIGN KEY (`owner_id`) REFERENCES `user_customuser` (`id`);

--
-- Constraints for table `order_menuimage`
--
ALTER TABLE `order_menuimage`
  ADD CONSTRAINT `order_menuimage_order_id_1c3adc60_fk_order_ordermenu_id` FOREIGN KEY (`order_id`) REFERENCES `order_ordermenu` (`id`);

--
-- Constraints for table `order_ordermenu`
--
ALTER TABLE `order_ordermenu`
  ADD CONSTRAINT `order_ordermenu_restaurant_id_48018483_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `peyment_peyment`
--
ALTER TABLE `peyment_peyment`
  ADD CONSTRAINT `peyment_peyment_customer_id_e6ea7ec5_fk_user_customuser_id` FOREIGN KEY (`customer_id`) REFERENCES `user_customuser` (`id`),
  ADD CONSTRAINT `peyment_peyment_order_id_dcb25998_fk_order_ordermenu_id` FOREIGN KEY (`order_id`) REFERENCES `order_ordermenu` (`id`);

--
-- Constraints for table `plan_planfeature`
--
ALTER TABLE `plan_planfeature`
  ADD CONSTRAINT `plan_planfeature_plan_id_0a6669ad_fk_plan_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plan_plan` (`id`);

--
-- Constraints for table `plan_planorder`
--
ALTER TABLE `plan_planorder`
  ADD CONSTRAINT `plan_planorder_plan_id_e1d4bc18_fk_plan_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plan_plan` (`id`),
  ADD CONSTRAINT `plan_planorder_restaurant_id_2080f1e7_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`),
  ADD CONSTRAINT `plan_planorder_user_id_d743189d_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`);

--
-- Constraints for table `product_orderdetailinfo`
--
ALTER TABLE `product_orderdetailinfo`
  ADD CONSTRAINT `product_orderdetaili_product_order_id_5fcb3bf9_fk_product_p` FOREIGN KEY (`product_order_id`) REFERENCES `product_productorder` (`id`);

--
-- Constraints for table `product_productfeature`
--
ALTER TABLE `product_productfeature`
  ADD CONSTRAINT `product_productfeature_product_id_e984accf_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`);

--
-- Constraints for table `product_productgallery`
--
ALTER TABLE `product_productgallery`
  ADD CONSTRAINT `product_productgallery_product_id_4680161b_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`);

--
-- Constraints for table `product_productorder`
--
ALTER TABLE `product_productorder`
  ADD CONSTRAINT `product_productorder_plan_id_908d60e7_fk_plan_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plan_plan` (`id`),
  ADD CONSTRAINT `product_productorder_user_id_3f59f6bb_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`);

--
-- Constraints for table `product_productorderdetail`
--
ALTER TABLE `product_productorderdetail`
  ADD CONSTRAINT `product_productorder_product_id_7f88cfe1_fk_product_p` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  ADD CONSTRAINT `product_productorder_product_order_id_fb27e0c4_fk_product_p` FOREIGN KEY (`product_order_id`) REFERENCES `product_productorder` (`id`);

--
-- Constraints for table `restaurant_food_restaurant`
--
ALTER TABLE `restaurant_food_restaurant`
  ADD CONSTRAINT `restaurant_food_rest_restaurant_id_c264b3be_fk_menu_rest` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`),
  ADD CONSTRAINT `restaurant_food_restaurant_food_id_6aa7ff29_fk_menu_food_id` FOREIGN KEY (`food_id`) REFERENCES `menu_food` (`id`);

--
-- Constraints for table `table_reservation`
--
ALTER TABLE `table_reservation`
  ADD CONSTRAINT `table_reservation_customer_id_690e78a5_fk_table_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `table_customer` (`id`),
  ADD CONSTRAINT `table_reservation_table_id_0d35355c_fk_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `table_table` (`id`);

--
-- Constraints for table `table_reservationsettings`
--
ALTER TABLE `table_reservationsettings`
  ADD CONSTRAINT `table_reservationset_restaurant_id_ab68f019_fk_menu_rest` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `table_table`
--
ALTER TABLE `table_table`
  ADD CONSTRAINT `table_table_restaurant_id_6b9284ec_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `table_workingtime`
--
ALTER TABLE `table_workingtime`
  ADD CONSTRAINT `table_workingtime_day_id_77584f23_fk_table_workingday_id` FOREIGN KEY (`day_id`) REFERENCES `table_workingday` (`id`),
  ADD CONSTRAINT `table_workingtime_restaurant_id_4649d94e_fk_menu_restaurant_id` FOREIGN KEY (`restaurant_id`) REFERENCES `menu_restaurant` (`id`);

--
-- Constraints for table `user_customuser_groups`
--
ALTER TABLE `user_customuser_groups`
  ADD CONSTRAINT `user_customuser_grou_customuser_id_192632a7_fk_user_cust` FOREIGN KEY (`customuser_id`) REFERENCES `user_customuser` (`id`),
  ADD CONSTRAINT `user_customuser_groups_group_id_bcbc9e48_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `user_customuser_user_permissions`
--
ALTER TABLE `user_customuser_user_permissions`
  ADD CONSTRAINT `user_customuser_user_customuser_id_4552d9cc_fk_user_cust` FOREIGN KEY (`customuser_id`) REFERENCES `user_customuser` (`id`),
  ADD CONSTRAINT `user_customuser_user_permission_id_e57e8b9a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `user_userdevice`
--
ALTER TABLE `user_userdevice`
  ADD CONSTRAINT `user_userdevice_user_id_3b07676b_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`);

--
-- Constraints for table `user_usersecurity`
--
ALTER TABLE `user_usersecurity`
  ADD CONSTRAINT `user_usersecurity_user_id_51d5adcf_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
