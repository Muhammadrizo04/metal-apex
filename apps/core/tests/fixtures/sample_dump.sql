-- phpMyAdmin SQL Dump (sinov uchun)
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

CREATE TABLE `mx_users` (`ID` int);
INSERT INTO `mx_users` (`ID`, `user_login`, `user_pass`) VALUES
(1, 'admin', 'hash-qiymat');

INSERT INTO `mx_options` (`option_id`, `option_name`, `option_value`) VALUES
(9, 'wpcf7_telegram_tkn', '111:MAXFIY-TOKEN');

INSERT INTO `mx_posts` (`ID`, `post_content`, `post_title`, `post_status`, `post_type`) VALUES
(8, '', 'Asosiy', 'publish', 'page'),
(10, '[:uz]Birinchi xat\\\'boshi.\r\n\r\nIkkinchi, O\'zbek matn.[:ru]Первый абзац.\r\n\r\nВторой абзац.[:]', '[:uz]Mahsulotlar haqida[:ru]О продукции[:]', 'publish', 'page'),
(12, '', 'Aloqa', 'publish', 'page'),
(14, '', 'Ishlar', 'publish', 'page'),
(16, '', 'Mahsulotlar', 'publish', 'page'),
(101, '', 'A1-02', 'inherit', 'attachment'),
(102, '', 'Q3-101', 'inherit', 'attachment'),
(103, '', 'CH5-01', 'inherit', 'attachment'),
(104, '', 'G3-01', 'inherit', 'attachment'),
(105, '', 'G3-01 .', 'inherit', 'attachment'),
(106, '', '[:uz]T4-04[:ru]T4-04[:]', 'inherit', 'attachment'),
(107, '', 'наружный угол', 'inherit', 'attachment'),
(108, '', 'наружный угол ,', 'inherit', 'attachment'),
(109, '', 'Z6-01', 'inherit', 'attachment'),
(201, '', '1', 'inherit', 'attachment'),
(202, '', '11', 'inherit', 'attachment'),
(203, '', '2', 'inherit', 'attachment'),
(205, '', '14', 'inherit', 'attachment'),
(206, '', '2 nusxa', 'inherit', 'attachment'),
(204, 'qavs ), ( ichida', 'Montaj', 'inherit', 'attachment');

INSERT INTO `mx_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES
(1, 101, '_wp_attached_file', '2024/07/a1.png'),
(2, 102, '_wp_attached_file', '2024/09/q3.webp'),
(3, 103, '_wp_attached_file', '2024/07/ch5.png'),
(4, 104, '_wp_attached_file', '2024/07/g3a.png'),
(5, 105, '_wp_attached_file', '2024/07/g3b.png'),
(6, 106, '_wp_attached_file', '2024/09/t4.webp'),
(7, 107, '_wp_attached_file', '2024/07/ug1.png'),
(8, 108, '_wp_attached_file', '2024/07/ug2.png'),
(9, 109, '_wp_attached_file', '2024/07/yoq.png'),
(10, 201, '_wp_attached_file', '2024/07/1.jpg'),
(11, 202, '_wp_attached_file', '2024/07/11.jpg'),
(12, 203, '_wp_attached_file', '2024/07/2.jpg'),
(14, 205, '_wp_attached_file', '2024/07/14.jpg'),
(15, 206, '_wp_attached_file', '2024/07/2.jpg'),
(13, 204, '_wp_attached_file', '2024/07/montage.png'),
(20, 16, 'products', 'a:9:{i:0;s:3:\"101\";i:1;s:3:\"102\";i:2;s:3:\"103\";i:3;s:3:\"104\";i:4;s:3:\"105\";i:5;s:3:\"106\";i:6;s:3:\"107\";i:7;s:3:\"108\";i:8;s:3:\"109\";}'),
(21, 14, 'works', 'a:3:{i:0;s:3:\"201\";i:1;s:3:\"203\";i:2;s:3:\"206\";}'),
(22, 8, 'slider_images', 'a:3:{i:0;s:3:\"205\";i:1;s:3:\"202\";i:2;s:3:\"201\";}'),
(23, 8, 'montage_img', '[:uz]204[:ru]204[:]'),
(24, 12, 'contact_phone_2', '[:uz]+998 94 447 77 17[:ru]+998 94 447 77 17[:]'),
(30, 8, 'what_title', '[:uz]Metal Apex bu nima?[:ru]Что такое Metal Apex?[:]'),
(31, 8, 'what_components_0_text_1', '[:uz]Tashqi qatlam[:ru]Внешний слой[:]'),
(32, 8, 'what_components_0_text_2', '[:uz]Po\'lat plita[:ru]Стальной лист[:]'),
(33, 8, 'offer_offers_0_text_1', '[:uz]Engil vazn[:ru]Лёгкий вес[:]'),
(34, 8, 'offer_offers_0_text_2', '[:uz]3,8 kg[:ru]3,8 кг[:]'),
(35, 8, 'montage_components_0_text_1', '[:uz]devorni tekislash[:ru]выравнивание[:]'),
(36, 8, 'montage_components_0_text_2', '[:uz]Profil[:ru]Профиль[:]'),
(37, 8, 'works_video_0_url', 'https://youtu.be/CAGMRjMMQxI'),
(50, 8, 'works_video_1_url', 'https://www.youtube.com/watch?v=XuN47W_qGYk'),
(38, 8, 'header_instagram', 'https://www.instagram.com/metalapex.uz/'),
(39, 12, 'contact_address', '[:uz]Qo\'qon, Temura Malik ko\'chasi, 79A[:ru]Коканд[:]'),
(40, 12, 'contact_phone_1', '+998 93 503 23 23'),
(41, 12, 'contact_email_1', 'metal-apex@mail.ru');
