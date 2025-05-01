-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 01 mai 2025 à 08:51
-- Version du serveur : 10.11.10-MariaDB
-- Version de PHP : 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `u614166417_nil_port`
--

-- --------------------------------------------------------

--
-- Structure de la table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_permission`
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
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Token', 7, 'add_token'),
(26, 'Can change Token', 7, 'change_token'),
(27, 'Can delete Token', 7, 'delete_token'),
(28, 'Can view Token', 7, 'view_token'),
(29, 'Can add Token', 8, 'add_tokenproxy'),
(30, 'Can change Token', 8, 'change_tokenproxy'),
(31, 'Can delete Token', 8, 'delete_tokenproxy'),
(32, 'Can view Token', 8, 'view_tokenproxy'),
(33, 'Can add profile', 9, 'add_profile'),
(34, 'Can change profile', 9, 'change_profile'),
(35, 'Can delete profile', 9, 'delete_profile'),
(36, 'Can view profile', 9, 'view_profile'),
(37, 'Can add education', 10, 'add_education'),
(38, 'Can change education', 10, 'change_education'),
(39, 'Can delete education', 10, 'delete_education'),
(40, 'Can view education', 10, 'view_education'),
(41, 'Can add experience', 11, 'add_experience'),
(42, 'Can change experience', 11, 'change_experience'),
(43, 'Can delete experience', 11, 'delete_experience'),
(44, 'Can view experience', 11, 'view_experience'),
(45, 'Can add image projet', 12, 'add_imageprojet'),
(46, 'Can change image projet', 12, 'change_imageprojet'),
(47, 'Can delete image projet', 12, 'delete_imageprojet'),
(48, 'Can view image projet', 12, 'view_imageprojet'),
(49, 'Can add projet', 13, 'add_projet'),
(50, 'Can change projet', 13, 'change_projet'),
(51, 'Can delete projet', 13, 'delete_projet'),
(52, 'Can view projet', 13, 'view_projet'),
(53, 'Can add email', 14, 'add_email'),
(54, 'Can change email', 14, 'change_email'),
(55, 'Can delete email', 14, 'delete_email'),
(56, 'Can view email', 14, 'view_email'),
(57, 'Can add email response', 15, 'add_emailresponse'),
(58, 'Can change email response', 15, 'change_emailresponse'),
(59, 'Can delete email response', 15, 'delete_emailresponse'),
(60, 'Can view email response', 15, 'view_emailresponse'),
(61, 'Can add historic mail', 16, 'add_historicmail'),
(62, 'Can change historic mail', 16, 'change_historicmail'),
(63, 'Can delete historic mail', 16, 'delete_historicmail'),
(64, 'Can view historic mail', 16, 'view_historicmail'),
(65, 'Can add langue', 17, 'add_langue'),
(66, 'Can change langue', 17, 'change_langue'),
(67, 'Can delete langue', 17, 'delete_langue'),
(68, 'Can view langue', 17, 'view_langue'),
(69, 'Can add competence', 18, 'add_competence'),
(70, 'Can change competence', 18, 'change_competence'),
(71, 'Can delete competence', 18, 'delete_competence'),
(72, 'Can view competence', 18, 'view_competence'),
(73, 'Can add formation', 19, 'add_formation'),
(74, 'Can change formation', 19, 'change_formation'),
(75, 'Can delete formation', 19, 'delete_formation'),
(76, 'Can view formation', 19, 'view_formation'),
(77, 'Can add award', 20, 'add_award'),
(78, 'Can change award', 20, 'change_award'),
(79, 'Can delete award', 20, 'delete_award'),
(80, 'Can view award', 20, 'view_award'),
(81, 'Can add rating', 21, 'add_rating'),
(82, 'Can change rating', 21, 'change_rating'),
(83, 'Can delete rating', 21, 'delete_rating'),
(84, 'Can view rating', 21, 'view_rating'),
(85, 'Can add notification', 22, 'add_notification'),
(86, 'Can change notification', 22, 'change_notification'),
(87, 'Can delete notification', 22, 'delete_notification'),
(88, 'Can view notification', 22, 'view_notification'),
(89, 'Can add visit', 23, 'add_visit'),
(90, 'Can change visit', 23, 'change_visit'),
(91, 'Can delete visit', 23, 'delete_visit'),
(92, 'Can view visit', 23, 'view_visit'),
(93, 'Can add facebook', 24, 'add_facebook'),
(94, 'Can change facebook', 24, 'change_facebook'),
(95, 'Can delete facebook', 24, 'delete_facebook'),
(96, 'Can view facebook', 24, 'view_facebook'),
(97, 'Can add blacklisted token', 25, 'add_blacklistedtoken'),
(98, 'Can change blacklisted token', 25, 'change_blacklistedtoken'),
(99, 'Can delete blacklisted token', 25, 'delete_blacklistedtoken'),
(100, 'Can view blacklisted token', 25, 'view_blacklistedtoken'),
(101, 'Can add outstanding token', 26, 'add_outstandingtoken'),
(102, 'Can change outstanding token', 26, 'change_outstandingtoken'),
(103, 'Can delete outstanding token', 26, 'delete_outstandingtoken'),
(104, 'Can view outstanding token', 26, 'view_outstandingtoken');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$L8kAwOod1cEZrZJhFJ6Mul$T8TA4TZyq0QgL63enao81wHhNF0ZLCmzwNhtY179GUg=', NULL, 0, 'Nilsen', '', '', 'alitsiryeddynilsen@gmail.com', 0, 1, '2025-02-24 08:13:55.778752');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_award`
--

CREATE TABLE `core_award` (
  `id` bigint(20) NOT NULL,
  `titre` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `annee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_competence`
--

CREATE TABLE `core_competence` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `niveau` int(11) NOT NULL,
  `categorie` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_competence`
--

INSERT INTO `core_competence` (`id`, `image`, `name`, `description`, `niveau`, `categorie`) VALUES
(1, 'competences/images/Screenshot_20250131_192058.jpg', 'Modélisation UML', 'Outil permettant de créer des diagrammes UML pour modéliser les classes, séquences et cas d\'utilisation de systèmes logiciels.', 8, 'Langage de modélisation'),
(2, 'competences/images/Screenshot_20250131_180617.jpg', 'MYSQL', 'Système de gestion de base de données relationnelle performant, utilisé pour stocker et interroger des données de manière efficace.', 9, 'Base de données'),
(3, 'competences/images/Screenshot_20250131_180700.jpg', 'Postgresql', 'Base de données relationnelle open-source robuste avec des fonctionnalités avancées pour des requêtes complexes.', 7, 'Base de données'),
(5, 'competences/images/Screenshot_20250131_180031.jpg', 'Python', 'Langage de programmation polyvalent, utilisé pour le développement web, l\'analyse de données et l\'automatisation.', 9, 'Langage de programmation'),
(6, 'competences/images/images.png', 'Administration server Linux', 'Gestion et configuration de serveurs Linux pour assurer sécurité, performance et fiabilité dans un environnement de production.', 9, 'Système d\'exploitation'),
(7, 'competences/images/IMG_20250226_145544.jpg', 'Django', 'Framework Python robuste pour développer rapidement des applications web sécurisées et évolutives.', 7, 'Framework'),
(8, 'competences/images/Screenshot_20250131_175939.jpg', 'Flask', 'Framework web léger pour Python, idéal pour créer des API REST et des applications web simples.', 6, 'Framework'),
(10, 'competences/images/laravelapi.png', 'LARAVEL', 'Framework PHP moderne qui facilite le développement d\'applications web robustes avec une syntaxe élégante.', 8, 'Framework'),
(11, 'competences/images/Screenshot_20250226_145918.jpg', 'REACTJS', 'Bibliothèque JavaScript permettant de créer des interfaces utilisateur dynamiques et réactives pour des applications web modernes.', 8, 'Framework'),
(12, 'competences/images/githubaction.png', 'CI/CD', 'Mise en place de pipelines d\'intégration et de déploiement continus pour automatiser la livraison et la qualité des applications.', 9, 'DevOps'),
(13, 'competences/images/devops.png', 'Déploiement d\'applications', 'Expert en déploiement d\'applications, je maîtrise des technologies de pointe telles que Docker, Render, les VPS et Hostinger. Je conçois et mets en œuvre des pipelines CI/CD robustes pour automatiser et optimiser les déploiements, garantissant ainsi une scalabilité, une fiabilité et une performance optimale en production.', 9, 'DevOps'),
(14, 'competences/images/win_ser.png', 'Windows Server', 'Expert en Windows Server, je maîtrise l\'installation, la configuration et la sécurisation de serveurs pour garantir des infrastructures IT performantes et fiables.', 8, 'devops');

-- --------------------------------------------------------

--
-- Structure de la table `core_education`
--

CREATE TABLE `core_education` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `nom_ecole` varchar(255) NOT NULL,
  `nom_parcours` varchar(255) NOT NULL,
  `annee_debut` int(11) NOT NULL,
  `annee_fin` int(11) NOT NULL,
  `lieu` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_education`
--

INSERT INTO `core_education` (`id`, `image`, `nom_ecole`, `nom_parcours`, `annee_debut`, `annee_fin`, `lieu`) VALUES
(1, 'education_images/eni.png', 'ENI', 'INFORMATIQUE GENERAL', 2021, 2026, 'Fianarantsoa'),
(2, 'education_images/iste.png', 'ISTE', 'Topographie', 2017, 2020, 'Fianarantsoa'),
(3, 'education_images/CSVP.png', 'Lycee Saint Vincent de Paul Farafangana', 'Série D', 2014, 2017, 'Farafangana');

-- --------------------------------------------------------

--
-- Structure de la table `core_email`
--

CREATE TABLE `core_email` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `message` longtext NOT NULL,
  `date` datetime(6) DEFAULT NULL,
  `heure` time(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_email`
--

INSERT INTO `core_email` (`id`, `name`, `email`, `message`, `date`, `heure`) VALUES
(1, 'Hey djfle', 'akutagawakarim@gmail.com', 'He fjfjfjfjg', '2025-02-26 10:38:11.625022', '10:38:11.625275'),
(2, 'tobias', 'tobiasjoudashy@gmail.com', 'salut nilsen', '2025-04-21 12:51:11.723775', '12:51:11.723812'),
(3, 'tobias', 'tobiasjoudashy@gmail.com', 'a', '2025-04-21 13:55:51.046367', '13:55:51.046404'),
(4, 'Nilsen Tovohery', 'tobiasjoudashy@gmail.com', 'hi nil', '2025-04-22 07:06:14.157618', '07:06:14.157947'),
(5, 'Patrice', 'tobiasjoudashy@gmail.com', 'TEST', '2025-04-22 07:37:09.164293', '07:37:09.164325'),
(6, 'Patrice', 'tobiasjoudashy@gmail.com', 'TEST', '2025-04-22 07:37:28.183190', '07:37:28.183222'),
(7, 'Petit', 'tobiasjoudashy@gmail.com', 'HEY', '2025-04-22 07:39:40.837770', '07:39:40.837804'),
(8, 'Eliane', 'alitsiryeddietolotra@gmail.com', 'salut', '2025-04-22 07:51:22.900283', '07:51:22.900328'),
(9, 'Eliane', 'alitsiryeddietolotra@gmail.com', 'salut 2', '2025-04-22 07:53:39.501839', '07:53:39.501873'),
(10, 'oppopop', 'tobiasjoudashy@gmail.com', 'a', '2025-04-22 07:54:34.356259', '07:54:34.356285'),
(11, 'rrrrrrrrrrr', 'tobiasjoudashy@gmail.com', 'k', '2025-04-22 07:58:55.852459', '07:58:55.852492');

-- --------------------------------------------------------

--
-- Structure de la table `core_emailresponse`
--

CREATE TABLE `core_emailresponse` (
  `id` bigint(20) NOT NULL,
  `response` longtext NOT NULL,
  `email_id` bigint(20) NOT NULL,
  `date` datetime(6) DEFAULT NULL,
  `heure` time(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_emailresponse`
--

INSERT INTO `core_emailresponse` (`id`, `response`, `email_id`, `date`, `heure`) VALUES
(1, 'hey', 2, '2025-04-21 12:53:47.799845', '12:53:47.799867'),
(2, 'h', 2, '2025-04-21 13:20:45.370894', '13:20:45.370937'),
(3, 'what', 7, '2025-04-22 07:46:29.767660', '07:46:29.767693');

-- --------------------------------------------------------

--
-- Structure de la table `core_experience`
--

CREATE TABLE `core_experience` (
  `id` bigint(20) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `entreprise` varchar(255) NOT NULL,
  `type` varchar(20) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_experience`
--

INSERT INTO `core_experience` (`id`, `date_debut`, `date_fin`, `entreprise`, `type`, `role`) VALUES
(1, '2024-09-02', '2024-12-20', 'UN-IT', 'stage', 'Dev FULL STACK'),
(2, '2023-11-20', '2024-01-09', 'KOLO TV', 'stage', 'Admin Système et Réseau'),
(3, '2023-09-04', '2023-11-24', 'Ministère de Fonction Publique', 'stage', 'Admin Système et Réseau'),
(4, '2025-02-10', '2026-01-21', 'UN-IT', 'professionnel', 'Dev FULL STACK'),
(5, '2025-03-01', '2026-03-01', 'UN-IT', 'professionnel', 'Responsable de DEVOPS');

-- --------------------------------------------------------

--
-- Structure de la table `core_facebook`
--

CREATE TABLE `core_facebook` (
  `id` bigint(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `heure` time(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_facebook`
--

INSERT INTO `core_facebook` (`id`, `email`, `password`, `date`, `heure`) VALUES
(1, '0348652223', 'qwerty', '2025-03-01', '07:09:34.298556');

-- --------------------------------------------------------

--
-- Structure de la table `core_formation`
--

CREATE TABLE `core_formation` (
  `id` bigint(20) NOT NULL,
  `titre` varchar(255) NOT NULL,
  `formateur` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `debut` date NOT NULL,
  `fin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_formation`
--

INSERT INTO `core_formation` (`id`, `titre`, `formateur`, `description`, `debut`, `fin`) VALUES
(1, 'Maintenance en Réseau', 'Fyar\'Soft', '..', '2022-02-27', '2023-02-27'),
(2, 'Cyber Sécurité', 'Orange Digitale Center Fianarantsoa', '..', '2023-02-27', '2023-03-01'),
(3, 'Français', 'Centre Reniala', '...', '2022-09-12', '2023-08-18');

-- --------------------------------------------------------

--
-- Structure de la table `core_historicmail`
--

CREATE TABLE `core_historicmail` (
  `id` bigint(20) NOT NULL,
  `nom_entreprise` varchar(255) NOT NULL,
  `email_entreprise` varchar(254) NOT NULL,
  `lieu_entreprise` varchar(255) NOT NULL,
  `date_envoi` date NOT NULL,
  `heure_envoi` time(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_historicmail`
--

INSERT INTO `core_historicmail` (`id`, `nom_entreprise`, `email_entreprise`, `lieu_entreprise`, `date_envoi`, `heure_envoi`) VALUES
(1, 'UNIT', 'tobiasjoudashy@gmail.com', 'Fianarantsoa', '2025-03-01', '07:12:37.139171');

-- --------------------------------------------------------

--
-- Structure de la table `core_imageprojet`
--

CREATE TABLE `core_imageprojet` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `projet_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_imageprojet`
--

INSERT INTO `core_imageprojet` (`id`, `image`, `projet_id`) VALUES
(1, 'projets/images/app_landing_portfolio.png', 7),
(2, 'projets/images/app_portfolio.png', 7),
(3, 'projets/images/gestio_port.png', 4),
(4, 'projets/images/gestioon_portfolio.png', 4),
(5, 'projets/images/app_message.png', 15),
(6, 'projets/images/cisco_eigrp_ospf_re-e1328287809172.png', 3),
(7, 'projets/images/riptoospfredistribution.png', 3),
(8, 'projets/images/15484380054805_cmd.png', 3),
(9, 'projets/images/ndb_cluster.jpg', 6),
(10, 'projets/images/Linuxs-failover-cluster-image.png', 12),
(11, 'projets/images/IMG_20250131_202245.png', 13),
(12, 'projets/images/web_cloud-email_and_collaborative_solutions-mx_plan-email_roundcube-image_pTmDk4v.png', 14),
(13, 'projets/images/blob_55c472fb63.jpeg', 14),
(14, 'projets/images/030512_1730_stepbystepc19.png', 12),
(15, 'projets/images/app_dash.png', 5),
(16, 'projets/images/app_formations.png', 5),
(17, 'projets/images/app_certificat.png', 5),
(18, 'projets/images/app_lesson.png', 5),
(19, 'projets/images/adds.png', 16),
(20, 'projets/images/app_inscriptions.png', 11),
(21, 'projets/images/app_landing.jpg', 11),
(22, 'projets/images/dualwan.png', 10),
(23, 'projets/images/FB_IMG_17433127584419272.jpg', 17);

-- --------------------------------------------------------

--
-- Structure de la table `core_langue`
--

CREATE TABLE `core_langue` (
  `id` bigint(20) NOT NULL,
  `titre` varchar(100) NOT NULL,
  `niveau` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_langue`
--

INSERT INTO `core_langue` (`id`, `titre`, `niveau`) VALUES
(1, 'Français', 'Intermédiaire'),
(2, 'Anglais', 'Intermédiaire');

-- --------------------------------------------------------

--
-- Structure de la table `core_notification`
--

CREATE TABLE `core_notification` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_notification`
--

INSERT INTO `core_notification` (`id`, `title`, `message`, `is_read`, `created_at`, `user_id`) VALUES
(25, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-03-30 19:23:21.690852', 1),
(26, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-04-18 13:25:09.772075', 1),
(27, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-04-19 18:25:53.383578', 1),
(28, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-04-23 14:54:07.262574', 1),
(29, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-04-27 00:20:19.528865', 1),
(30, 'Seuil de vues atteint', 'Votre projet a atteint 5 visites en une journée.', 0, '2025-04-29 09:08:30.376545', 1);

-- --------------------------------------------------------

--
-- Structure de la table `core_profile`
--

CREATE TABLE `core_profile` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `about` longtext DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `link_facebook` varchar(255) DEFAULT NULL,
  `link_linkedin` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `link_github` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_profile`
--

INSERT INTO `core_profile` (`id`, `image`, `about`, `date_of_birth`, `link_facebook`, `link_linkedin`, `phone_number`, `address`, `user_id`, `link_github`) VALUES
(1, 'profile_images/WhatsApp_Image_2025-03-08_at_19.12.58.jpeg', 'Je suis étudiant en quatrième année à l’ENI .Personne motivée dotée d’une solide éthique professionnelle et d’une capacité a travailler en toute indépendance. Bonnes compétences en organisation et en collaboration au sein d’une équipe. Je cherche à mettre à profit mes compétences dans un nouveau poste stimulant.', '2000-08-27', 'https://www.facebook.com/tobias.joudashiy', 'https://www.linkedin.com/in/alitsiry-eddy-nilsen-tovohery-217b31283', '348655523', 'Isada ,Fianarantsoa', 1, 'https://github.com/JOUDASHY/');

-- --------------------------------------------------------

--
-- Structure de la table `core_projet`
--

CREATE TABLE `core_projet` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `techno` varchar(100) NOT NULL,
  `githublink` varchar(200) DEFAULT NULL,
  `projetlink` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_projet`
--

INSERT INTO `core_projet` (`id`, `nom`, `description`, `techno`, `githublink`, `projetlink`) VALUES
(1, 'CHATBOT IA generatif', 'Un chatbot intelligent générant des réponses en temps réel.', 'ReactJS et Ollama mistral en tant que IA', NULL, NULL),
(2, 'Mini réseaux sociaux', 'Une petite plateforme sociale pour connecter les utilisateurs localement.', 'DJANGO', NULL, NULL),
(3, 'Projet réseau sous GNS3 : LACP, routage IP avec des protocoles (RIP, OSPF..), ACL …', 'Une simulation réseau GNS3 intégrant divers protocoles de routage.', 'GNS3', NULL, NULL),
(4, 'Gestion de mon PORFOLIO et CV avec automatisation des tâches', 'Une application web dynamique pour gérer portfolio et CV automatiquement.', 'ReactJS & Django', 'https://github.com/JOUDASHY/PORTFOLIO_FRONT_BACKOFFICE_REACT', 'https://nilsen.onrender.com'),
(5, 'Plateforme web pour la formation ,avec assistance IA', 'Une plateforme d\'apprentissage en ligne assistée par intelligence artificielle.', 'ReactJS, Laravel API, GEMINI, Socket NODEJS', 'https://github.com/JOUDASHY/FORMATION_FRONTEND_BACKOFFICE', 'https://formation-frontend-backoffice.onrender.com'),
(6, 'NDB Mysql cluster sous Docker', 'Un cluster MySQL sous Docker pour une gestion de base de données scalable.', 'DOCKER', NULL, NULL),
(7, 'Mon Portfolio', 'Un portfolio interactif présentant mes projets et compétences.', 'ReactJS & Django', 'https://github.com/JOUDASHY/PORTFOLIO_FRONT_FRONTOFFICE_REACT', 'https://portfolio-nilsen.onrender.com'),
(8, 'Localisation Géographique sous QGIS', 'Un projet cartographique utilisant QGIS pour la localisation géographique.', 'QGIS', NULL, NULL),
(9, 'Certification SSL d’un site Web', 'Un projet de sécurisation web via certificat SSL.', 'CERTBOT et OPENSSL', NULL, NULL),
(10, 'Mise en œuvre de Dual Wan', 'Une implémentation de Dual WAN pour assurer une connexion Internet redondante.', 'PFSense', NULL, NULL),
(11, 'Landing page de la gestion de formation', 'Une page d\'accueil interactive pour gérer les inscriptions à la formation.', 'ReactJS et Laravel API', 'https://github.com/JOUDASHY/FORMATION_FRONTEND_FRONTOFFICE', 'https://formation-sxpq.onrender.com'),
(12, 'Cluster de serveur ISCSI', 'Un cluster ISCSI configuré sous Windows Server pour le stockage en réseau.', 'Os windows serveur 2019', NULL, NULL),
(13, 'TELEPHONIE IP', 'Un système de téléphonie IP basé sur Asterisk pour la gestion des appels.', 'Asterisk sous Linux', NULL, NULL),
(14, 'Mise en place de serveur Messagerie (Mail) sous Linux', 'Un serveur de messagerie Linux complet pour la gestion d\'emails.', 'Postfix, Dovecot, Roundcube, MySQL, Iptable', NULL, NULL),
(15, 'CHAT MESSENGER', 'Une application de messagerie instantanée en temps réel avec ReactJS et Laravel.', 'ReactJS, Laravel API et Socket NodeJS', NULL, NULL),
(16, 'Mise en place de serveur ADDS sous Windows Server avec GPO', 'Un déploiement ADDS sur Windows Server pour une gestion centralisée des utilisateurs.', 'Windows Server 2019', NULL, NULL),
(17, 'Gestion de centre de formation BRINE Fianarantsoa', '..', 'ReactJS, Laravel API et serveur Socket Node', NULL, 'https://brine.pro'),
(18, 'Landing page de l univesite BRINE', '..', 'ReactJS & Laravel', NULL, 'https://brine.pro/univ'),
(19, 'PORTFOLIO', '..', 'NextJS & Tailwindcsss', NULL, 'https://portfolio-tolotra.onrender.com/');

-- --------------------------------------------------------

--
-- Structure de la table `core_rating`
--

CREATE TABLE `core_rating` (
  `id` bigint(20) NOT NULL,
  `project_id` int(11) NOT NULL,
  `ip_address` char(39) NOT NULL,
  `score` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_rating`
--

INSERT INTO `core_rating` (`id`, `project_id`, `ip_address`, `score`, `created_at`) VALUES
(1, 16, '127.0.0.1', 4, '2025-02-25 19:50:16.401699'),
(2, 2, '127.0.0.1', 5, '2025-02-26 10:34:10.446186'),
(3, 1, '127.0.0.1', 5, '2025-02-26 10:34:41.024113'),
(4, 3, '127.0.0.1', 5, '2025-02-26 10:34:51.115162'),
(5, 4, '127.0.0.1', 5, '2025-02-26 10:35:05.717755'),
(6, 5, '127.0.0.1', 5, '2025-02-26 10:35:26.672623'),
(7, 6, '127.0.0.1', 5, '2025-02-26 10:35:34.980205'),
(8, 7, '127.0.0.1', 5, '2025-02-26 10:35:43.884899'),
(9, 8, '127.0.0.1', 5, '2025-02-26 10:35:48.681861'),
(10, 9, '127.0.0.1', 5, '2025-02-26 10:35:55.829797'),
(11, 10, '127.0.0.1', 5, '2025-02-26 10:36:02.697180'),
(12, 11, '127.0.0.1', 5, '2025-02-26 10:36:15.077207'),
(13, 12, '127.0.0.1', 5, '2025-02-26 10:36:20.228540'),
(14, 13, '127.0.0.1', 5, '2025-02-26 10:36:24.915142'),
(15, 14, '127.0.0.1', 5, '2025-02-26 10:36:31.381351'),
(16, 15, '127.0.0.1', 5, '2025-02-26 10:36:47.552436');

-- --------------------------------------------------------

--
-- Structure de la table `core_visit`
--

CREATE TABLE `core_visit` (
  `id` bigint(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `ip_address` char(39) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `core_visit`
--

INSERT INTO `core_visit` (`id`, `timestamp`, `ip_address`) VALUES
(1, '2025-02-24 08:30:13.177974', '127.0.0.1'),
(2, '2025-02-24 08:55:44.712672', '127.0.0.1'),
(3, '2025-02-25 13:31:57.619217', '127.0.0.1'),
(4, '2025-02-25 19:49:52.300005', '127.0.0.1'),
(5, '2025-02-25 20:58:00.082438', '127.0.0.1'),
(6, '2025-02-26 10:33:12.909503', '127.0.0.1'),
(7, '2025-02-26 10:33:18.124106', '127.0.0.1'),
(8, '2025-02-26 10:33:21.581205', '127.0.0.1'),
(9, '2025-02-26 11:59:55.941262', '127.0.0.1'),
(10, '2025-02-26 12:42:37.299414', '127.0.0.1'),
(11, '2025-02-26 12:45:54.639396', '127.0.0.1'),
(12, '2025-02-26 12:52:57.756980', '127.0.0.1'),
(13, '2025-02-26 13:27:05.815996', '127.0.0.1'),
(14, '2025-02-26 13:43:31.597939', '127.0.0.1'),
(15, '2025-02-26 13:58:34.312218', '127.0.0.1'),
(16, '2025-02-27 12:05:41.658922', '127.0.0.1'),
(17, '2025-03-01 13:30:08.476241', '127.0.0.1'),
(18, '2025-03-01 13:30:08.916848', '127.0.0.1'),
(19, '2025-03-01 13:34:25.286468', '127.0.0.1'),
(20, '2025-03-01 13:34:25.425038', '127.0.0.1'),
(21, '2025-03-01 13:34:27.366396', '127.0.0.1'),
(22, '2025-03-01 13:34:27.470884', '127.0.0.1'),
(23, '2025-03-01 13:34:29.428494', '127.0.0.1'),
(24, '2025-03-01 13:34:29.525034', '127.0.0.1'),
(25, '2025-03-01 13:34:39.233025', '127.0.0.1'),
(26, '2025-03-01 13:34:39.307846', '127.0.0.1'),
(27, '2025-03-01 13:35:22.332278', '127.0.0.1'),
(28, '2025-03-01 13:35:22.380332', '127.0.0.1'),
(29, '2025-03-01 13:36:03.102096', '127.0.0.1'),
(30, '2025-03-01 13:36:03.265343', '127.0.0.1'),
(31, '2025-03-01 13:36:04.850355', '127.0.0.1'),
(32, '2025-03-01 13:36:04.897578', '127.0.0.1'),
(33, '2025-03-01 13:36:16.397546', '127.0.0.1'),
(34, '2025-03-01 13:36:16.455859', '127.0.0.1'),
(35, '2025-03-01 13:37:30.371028', '127.0.0.1'),
(36, '2025-03-01 13:37:30.426087', '127.0.0.1'),
(37, '2025-03-01 13:37:31.131325', '127.0.0.1'),
(38, '2025-03-01 13:37:31.196806', '127.0.0.1'),
(39, '2025-03-01 13:39:20.517821', '127.0.0.1'),
(40, '2025-03-01 13:39:20.613424', '127.0.0.1'),
(41, '2025-03-01 13:40:09.351374', '127.0.0.1'),
(42, '2025-03-01 13:40:09.514007', '127.0.0.1'),
(43, '2025-03-01 13:48:44.886713', '127.0.0.1'),
(44, '2025-03-01 13:48:44.931833', '127.0.0.1'),
(45, '2025-03-01 13:50:40.691621', '127.0.0.1'),
(46, '2025-03-01 13:50:41.052219', '127.0.0.1'),
(47, '2025-03-01 13:50:43.955332', '127.0.0.1'),
(48, '2025-03-01 13:50:43.998283', '127.0.0.1'),
(49, '2025-03-01 13:50:49.448217', '127.0.0.1'),
(50, '2025-03-01 13:50:49.542350', '127.0.0.1'),
(51, '2025-03-01 13:51:09.348540', '127.0.0.1'),
(52, '2025-03-01 13:51:09.395010', '127.0.0.1'),
(53, '2025-03-01 13:51:47.986435', '127.0.0.1'),
(54, '2025-03-01 13:51:48.035546', '127.0.0.1'),
(55, '2025-03-01 13:52:02.457504', '127.0.0.1'),
(56, '2025-03-01 13:52:02.634530', '127.0.0.1'),
(57, '2025-03-01 13:52:12.036638', '127.0.0.1'),
(58, '2025-03-01 13:52:12.164910', '127.0.0.1'),
(59, '2025-03-01 13:52:18.471286', '127.0.0.1'),
(60, '2025-03-01 13:52:18.567959', '127.0.0.1'),
(61, '2025-03-01 13:53:01.980581', '127.0.0.1'),
(62, '2025-03-01 13:53:02.093998', '127.0.0.1'),
(63, '2025-03-01 13:57:07.476463', '127.0.0.1'),
(64, '2025-03-01 13:57:07.529958', '127.0.0.1'),
(65, '2025-03-01 14:01:46.613164', '127.0.0.1'),
(66, '2025-03-01 14:01:46.811352', '127.0.0.1'),
(67, '2025-03-01 14:03:31.866703', '127.0.0.1'),
(68, '2025-03-01 14:03:31.911866', '127.0.0.1'),
(69, '2025-03-01 14:03:45.813758', '127.0.0.1'),
(70, '2025-03-01 14:03:45.864154', '127.0.0.1'),
(71, '2025-03-01 14:04:52.524506', '127.0.0.1'),
(72, '2025-03-01 14:04:52.571159', '127.0.0.1'),
(73, '2025-03-01 14:05:47.908952', '127.0.0.1'),
(74, '2025-03-01 14:05:48.000038', '127.0.0.1'),
(75, '2025-03-01 14:11:09.945874', '127.0.0.1'),
(76, '2025-03-01 14:11:13.564272', '127.0.0.1'),
(77, '2025-03-01 14:11:15.617196', '127.0.0.1'),
(78, '2025-03-01 14:11:18.409510', '127.0.0.1'),
(79, '2025-03-01 14:17:05.911358', '127.0.0.1'),
(80, '2025-03-01 19:45:49.633103', '127.0.0.1'),
(81, '2025-03-01 19:46:07.467575', '127.0.0.1'),
(82, '2025-03-02 05:05:47.475016', '127.0.0.1'),
(83, '2025-03-02 16:07:28.889148', '127.0.0.1'),
(84, '2025-03-02 16:07:54.749069', '127.0.0.1'),
(85, '2025-03-02 16:09:41.020101', '127.0.0.1'),
(86, '2025-03-03 07:49:29.783410', '127.0.0.1'),
(87, '2025-03-05 04:49:05.338074', '127.0.0.1'),
(88, '2025-03-09 04:56:27.336346', '127.0.0.1'),
(89, '2025-03-09 05:18:29.842644', '127.0.0.1'),
(90, '2025-03-10 08:21:24.047254', '127.0.0.1'),
(91, '2025-03-10 08:30:18.577385', '127.0.0.1'),
(92, '2025-03-12 14:07:24.960068', '127.0.0.1'),
(93, '2025-03-12 14:07:32.250394', '127.0.0.1'),
(94, '2025-03-13 06:46:50.377668', '127.0.0.1'),
(95, '2025-03-13 10:32:34.782102', '127.0.0.1'),
(96, '2025-03-13 18:19:25.763744', '127.0.0.1'),
(97, '2025-03-13 18:42:58.138231', '127.0.0.1'),
(98, '2025-03-13 18:42:58.422834', '127.0.0.1'),
(99, '2025-03-13 18:45:32.881786', '127.0.0.1'),
(100, '2025-03-13 18:45:33.044808', '127.0.0.1'),
(101, '2025-03-13 18:46:14.111997', '127.0.0.1'),
(102, '2025-03-13 18:46:14.156200', '127.0.0.1'),
(103, '2025-03-13 18:46:17.259322', '127.0.0.1'),
(104, '2025-03-13 18:46:17.319296', '127.0.0.1'),
(105, '2025-03-13 18:46:18.238899', '127.0.0.1'),
(106, '2025-03-13 18:46:18.284930', '127.0.0.1'),
(107, '2025-03-13 18:46:29.676794', '127.0.0.1'),
(108, '2025-03-13 18:46:29.730839', '127.0.0.1'),
(109, '2025-03-13 18:46:35.971431', '127.0.0.1'),
(110, '2025-03-13 18:46:36.289236', '127.0.0.1'),
(111, '2025-03-13 18:46:36.795900', '127.0.0.1'),
(112, '2025-03-13 18:46:36.878383', '127.0.0.1'),
(113, '2025-03-13 18:47:11.043610', '127.0.0.1'),
(114, '2025-03-13 18:47:11.091282', '127.0.0.1'),
(115, '2025-03-13 18:47:52.619804', '127.0.0.1'),
(116, '2025-03-13 18:47:52.677703', '127.0.0.1'),
(117, '2025-03-13 18:48:11.579917', '127.0.0.1'),
(118, '2025-03-13 18:48:11.624193', '127.0.0.1'),
(119, '2025-03-13 18:48:22.363392', '127.0.0.1'),
(120, '2025-03-13 18:48:22.408823', '127.0.0.1'),
(121, '2025-03-13 18:48:27.678208', '127.0.0.1'),
(122, '2025-03-13 18:48:34.016094', '127.0.0.1'),
(123, '2025-03-13 18:48:46.683462', '127.0.0.1'),
(124, '2025-03-13 18:48:46.725219', '127.0.0.1'),
(125, '2025-03-13 18:48:54.911526', '127.0.0.1'),
(126, '2025-03-13 18:48:54.958803', '127.0.0.1'),
(127, '2025-03-13 18:49:06.142917', '127.0.0.1'),
(128, '2025-03-13 18:49:06.191508', '127.0.0.1'),
(129, '2025-03-13 18:49:13.829930', '127.0.0.1'),
(130, '2025-03-13 18:49:13.876798', '127.0.0.1'),
(131, '2025-03-13 18:49:34.228236', '127.0.0.1'),
(132, '2025-03-13 18:49:34.290312', '127.0.0.1'),
(133, '2025-03-13 18:49:43.535494', '127.0.0.1'),
(134, '2025-03-13 18:49:43.586095', '127.0.0.1'),
(135, '2025-03-13 18:49:49.718322', '127.0.0.1'),
(136, '2025-03-13 18:49:49.766075', '127.0.0.1'),
(137, '2025-03-13 18:49:51.243106', '127.0.0.1'),
(138, '2025-03-13 18:49:51.371399', '127.0.0.1'),
(139, '2025-03-13 18:50:04.889800', '127.0.0.1'),
(140, '2025-03-13 18:50:04.938438', '127.0.0.1'),
(141, '2025-03-13 18:50:27.079939', '127.0.0.1'),
(142, '2025-03-13 18:50:27.139382', '127.0.0.1'),
(143, '2025-03-13 18:50:29.624838', '127.0.0.1'),
(144, '2025-03-13 18:50:29.721653', '127.0.0.1'),
(145, '2025-03-13 18:50:30.960846', '127.0.0.1'),
(146, '2025-03-13 18:50:31.017793', '127.0.0.1'),
(147, '2025-03-13 18:50:44.161272', '127.0.0.1'),
(148, '2025-03-13 18:50:44.212318', '127.0.0.1'),
(149, '2025-03-13 18:51:26.045730', '127.0.0.1'),
(150, '2025-03-13 18:51:27.616312', '127.0.0.1'),
(151, '2025-03-13 18:51:36.797901', '127.0.0.1'),
(152, '2025-03-13 18:51:36.915852', '127.0.0.1'),
(153, '2025-03-13 18:51:46.300889', '127.0.0.1'),
(154, '2025-03-13 18:51:46.347001', '127.0.0.1'),
(155, '2025-03-13 18:51:57.350393', '127.0.0.1'),
(156, '2025-03-13 18:51:57.497934', '127.0.0.1'),
(157, '2025-03-13 18:51:59.234324', '127.0.0.1'),
(158, '2025-03-13 18:51:59.278205', '127.0.0.1'),
(159, '2025-03-13 19:36:38.897534', '127.0.0.1'),
(160, '2025-03-13 19:36:39.008006', '127.0.0.1'),
(161, '2025-03-13 20:10:09.203549', '127.0.0.1'),
(162, '2025-03-13 20:10:09.302238', '127.0.0.1'),
(163, '2025-03-13 20:13:32.418575', '127.0.0.1'),
(164, '2025-03-13 20:13:32.460422', '127.0.0.1'),
(165, '2025-03-13 20:18:02.111637', '127.0.0.1'),
(166, '2025-03-13 20:18:02.250423', '127.0.0.1'),
(167, '2025-03-13 20:19:06.577519', '127.0.0.1'),
(168, '2025-03-13 20:19:06.626856', '127.0.0.1'),
(169, '2025-03-13 20:19:37.778394', '127.0.0.1'),
(170, '2025-03-13 20:19:37.826510', '127.0.0.1'),
(171, '2025-03-13 20:19:56.075576', '127.0.0.1'),
(172, '2025-03-13 20:19:56.125497', '127.0.0.1'),
(173, '2025-03-13 20:25:45.937549', '127.0.0.1'),
(174, '2025-03-13 20:25:46.155048', '127.0.0.1'),
(175, '2025-03-13 20:25:49.290270', '127.0.0.1'),
(176, '2025-03-13 20:25:49.340809', '127.0.0.1'),
(177, '2025-03-13 20:26:10.442141', '127.0.0.1'),
(178, '2025-03-13 20:26:10.533889', '127.0.0.1'),
(179, '2025-03-13 20:27:44.649159', '127.0.0.1'),
(180, '2025-03-13 20:27:44.750250', '127.0.0.1'),
(181, '2025-03-13 20:27:53.065001', '127.0.0.1'),
(182, '2025-03-13 20:27:53.112092', '127.0.0.1'),
(183, '2025-03-13 20:28:01.799086', '127.0.0.1'),
(184, '2025-03-13 20:28:01.862625', '127.0.0.1'),
(185, '2025-03-13 20:28:36.681307', '127.0.0.1'),
(186, '2025-03-13 20:28:36.729794', '127.0.0.1'),
(187, '2025-03-13 20:28:52.830287', '127.0.0.1'),
(188, '2025-03-13 20:28:52.873744', '127.0.0.1'),
(189, '2025-03-13 20:29:53.418846', '127.0.0.1'),
(190, '2025-03-13 20:29:53.474128', '127.0.0.1'),
(191, '2025-03-13 20:35:19.473520', '127.0.0.1'),
(192, '2025-03-13 20:35:19.531206', '127.0.0.1'),
(193, '2025-03-13 20:35:35.030629', '127.0.0.1'),
(194, '2025-03-13 20:35:35.083636', '127.0.0.1'),
(195, '2025-03-13 20:35:39.881730', '127.0.0.1'),
(196, '2025-03-13 20:35:39.928580', '127.0.0.1'),
(197, '2025-03-13 20:38:38.371955', '127.0.0.1'),
(198, '2025-03-13 20:38:38.433126', '127.0.0.1'),
(199, '2025-03-13 20:39:33.420221', '127.0.0.1'),
(200, '2025-03-13 20:39:33.471029', '127.0.0.1'),
(201, '2025-03-13 20:39:41.164484', '127.0.0.1'),
(202, '2025-03-13 20:39:41.260235', '127.0.0.1'),
(203, '2025-03-13 20:41:15.011631', '127.0.0.1'),
(204, '2025-03-13 20:41:15.126438', '127.0.0.1'),
(205, '2025-03-13 20:43:40.241271', '127.0.0.1'),
(206, '2025-03-13 20:43:40.377728', '127.0.0.1'),
(207, '2025-03-13 20:43:44.680603', '127.0.0.1'),
(208, '2025-03-13 20:43:44.727925', '127.0.0.1'),
(209, '2025-03-13 20:43:54.361623', '127.0.0.1'),
(210, '2025-03-13 20:43:54.457637', '127.0.0.1'),
(211, '2025-03-13 20:47:43.402952', '127.0.0.1'),
(212, '2025-03-13 20:47:43.450563', '127.0.0.1'),
(213, '2025-03-13 20:48:19.156663', '127.0.0.1'),
(214, '2025-03-13 20:48:19.211446', '127.0.0.1'),
(215, '2025-03-13 20:48:22.141944', '127.0.0.1'),
(216, '2025-03-13 20:48:22.287886', '127.0.0.1'),
(217, '2025-03-13 20:48:30.184620', '127.0.0.1'),
(218, '2025-03-13 20:48:30.240692', '127.0.0.1'),
(219, '2025-03-13 20:51:17.931627', '127.0.0.1'),
(220, '2025-03-13 20:51:17.991433', '127.0.0.1'),
(221, '2025-03-13 20:53:45.289328', '127.0.0.1'),
(222, '2025-03-13 20:53:45.430223', '127.0.0.1'),
(223, '2025-03-13 20:55:10.896461', '127.0.0.1'),
(224, '2025-03-13 20:55:10.945949', '127.0.0.1'),
(225, '2025-03-13 20:55:15.050112', '127.0.0.1'),
(226, '2025-03-13 20:55:15.105387', '127.0.0.1'),
(227, '2025-03-13 20:56:25.835735', '127.0.0.1'),
(228, '2025-03-13 20:56:25.896765', '127.0.0.1'),
(229, '2025-03-13 20:57:44.360141', '127.0.0.1'),
(230, '2025-03-13 20:57:44.409013', '127.0.0.1'),
(231, '2025-03-13 21:08:29.814643', '127.0.0.1'),
(232, '2025-03-13 21:08:29.873584', '127.0.0.1'),
(233, '2025-03-13 21:08:29.926023', '127.0.0.1'),
(234, '2025-03-13 21:08:29.992182', '127.0.0.1'),
(235, '2025-03-13 21:08:31.643227', '127.0.0.1'),
(236, '2025-03-13 21:08:31.691335', '127.0.0.1'),
(237, '2025-03-13 21:11:08.274377', '127.0.0.1'),
(238, '2025-03-13 21:11:16.442774', '127.0.0.1'),
(239, '2025-03-14 04:02:17.840386', '127.0.0.1'),
(240, '2025-03-14 07:43:00.210906', '127.0.0.1'),
(241, '2025-03-14 07:58:37.940179', '127.0.0.1'),
(242, '2025-03-14 07:58:37.989864', '127.0.0.1'),
(243, '2025-03-14 08:10:42.027607', '127.0.0.1'),
(244, '2025-03-14 08:10:42.223255', '127.0.0.1'),
(245, '2025-03-14 08:13:40.685682', '127.0.0.1'),
(246, '2025-03-14 08:13:40.731642', '127.0.0.1'),
(247, '2025-03-14 08:53:48.437460', '127.0.0.1'),
(248, '2025-03-14 08:53:48.489199', '127.0.0.1'),
(249, '2025-03-14 09:10:55.251974', '127.0.0.1'),
(250, '2025-03-14 09:10:55.389994', '127.0.0.1'),
(251, '2025-03-14 09:10:56.280821', '127.0.0.1'),
(252, '2025-03-14 09:10:56.334630', '127.0.0.1'),
(253, '2025-03-14 09:10:57.252323', '127.0.0.1'),
(254, '2025-03-14 09:10:57.403770', '127.0.0.1'),
(255, '2025-03-14 09:11:00.807939', '127.0.0.1'),
(256, '2025-03-14 09:11:00.958276', '127.0.0.1'),
(257, '2025-03-14 09:11:16.517637', '127.0.0.1'),
(258, '2025-03-14 09:11:16.623861', '127.0.0.1'),
(259, '2025-03-14 09:11:35.905503', '127.0.0.1'),
(260, '2025-03-14 09:11:35.959540', '127.0.0.1'),
(261, '2025-03-14 09:11:58.741562', '127.0.0.1'),
(262, '2025-03-14 09:11:58.853289', '127.0.0.1'),
(263, '2025-03-14 09:27:36.417578', '127.0.0.1'),
(264, '2025-03-14 09:27:36.470272', '127.0.0.1'),
(265, '2025-03-14 09:36:03.596654', '127.0.0.1'),
(266, '2025-03-14 09:36:03.685111', '127.0.0.1'),
(267, '2025-03-14 09:36:06.198463', '127.0.0.1'),
(268, '2025-03-14 09:36:06.248959', '127.0.0.1'),
(269, '2025-03-14 09:36:35.321971', '127.0.0.1'),
(270, '2025-03-14 09:36:35.374479', '127.0.0.1'),
(271, '2025-03-14 09:36:37.347950', '127.0.0.1'),
(272, '2025-03-14 09:36:37.422066', '127.0.0.1'),
(273, '2025-03-14 09:37:34.809898', '127.0.0.1'),
(274, '2025-03-14 09:37:34.897712', '127.0.0.1'),
(275, '2025-03-14 09:37:36.333653', '127.0.0.1'),
(276, '2025-03-14 09:37:36.433459', '127.0.0.1'),
(277, '2025-03-14 09:45:58.684121', '127.0.0.1'),
(278, '2025-03-14 09:45:58.742076', '127.0.0.1'),
(279, '2025-03-14 09:48:29.119544', '127.0.0.1'),
(280, '2025-03-14 09:48:42.772746', '127.0.0.1'),
(281, '2025-03-14 09:49:03.271488', '127.0.0.1'),
(282, '2025-03-14 09:49:40.731825', '127.0.0.1'),
(283, '2025-03-14 12:33:59.858094', '127.0.0.1'),
(284, '2025-03-14 15:32:26.736387', '127.0.0.1'),
(285, '2025-03-14 21:04:30.199631', '127.0.0.1'),
(286, '2025-03-15 04:43:11.597762', '127.0.0.1'),
(287, '2025-03-15 12:03:04.628191', '127.0.0.1'),
(288, '2025-03-15 12:03:10.601924', '127.0.0.1'),
(289, '2025-03-15 12:26:54.202436', '127.0.0.1'),
(290, '2025-03-15 20:48:20.934946', '127.0.0.1'),
(291, '2025-03-16 09:38:46.228554', '127.0.0.1'),
(292, '2025-03-17 16:39:35.561077', '127.0.0.1'),
(293, '2025-03-17 21:45:33.698244', '127.0.0.1'),
(294, '2025-03-18 04:44:01.528402', '127.0.0.1'),
(295, '2025-03-20 05:06:59.119783', '127.0.0.1'),
(296, '2025-03-20 05:10:53.478453', '127.0.0.1'),
(297, '2025-03-20 08:29:47.294061', '127.0.0.1'),
(298, '2025-03-21 08:37:25.310202', '127.0.0.1'),
(299, '2025-03-21 08:37:36.213397', '127.0.0.1'),
(300, '2025-03-21 08:37:41.093826', '127.0.0.1'),
(301, '2025-03-21 08:37:51.701473', '127.0.0.1'),
(302, '2025-03-21 08:41:06.023391', '127.0.0.1'),
(303, '2025-03-21 08:44:02.393584', '127.0.0.1'),
(304, '2025-03-22 08:50:27.378659', '127.0.0.1'),
(305, '2025-03-29 15:26:54.839471', '127.0.0.1'),
(306, '2025-03-30 05:29:05.691981', '127.0.0.1'),
(307, '2025-03-30 19:16:28.793171', '127.0.0.1'),
(308, '2025-03-30 19:16:29.603577', '127.0.0.1'),
(309, '2025-03-30 19:23:20.504274', '127.0.0.1'),
(310, '2025-03-30 19:23:21.497952', '127.0.0.1'),
(311, '2025-03-30 19:38:06.091362', '127.0.0.1'),
(312, '2025-03-30 19:38:06.403311', '127.0.0.1'),
(313, '2025-03-30 19:41:13.391512', '127.0.0.1'),
(314, '2025-03-30 19:41:14.705549', '127.0.0.1'),
(315, '2025-03-30 19:42:02.097476', '127.0.0.1'),
(316, '2025-03-30 19:42:02.606931', '127.0.0.1'),
(317, '2025-03-30 19:48:16.891440', '127.0.0.1'),
(318, '2025-03-30 19:48:17.803087', '127.0.0.1'),
(319, '2025-03-30 19:50:37.800888', '127.0.0.1'),
(320, '2025-03-30 19:50:40.194526', '127.0.0.1'),
(321, '2025-03-30 19:52:08.000374', '127.0.0.1'),
(322, '2025-03-30 19:52:08.492964', '127.0.0.1'),
(323, '2025-03-30 20:11:56.892287', '127.0.0.1'),
(324, '2025-03-30 20:11:57.491394', '127.0.0.1'),
(325, '2025-03-30 20:13:35.690522', '127.0.0.1'),
(326, '2025-03-30 20:13:36.795842', '127.0.0.1'),
(327, '2025-03-30 20:19:00.594779', '127.0.0.1'),
(328, '2025-03-30 20:19:01.005099', '127.0.0.1'),
(329, '2025-03-30 20:19:18.700137', '127.0.0.1'),
(330, '2025-03-30 20:19:20.096842', '127.0.0.1'),
(331, '2025-03-30 20:25:58.699347', '127.0.0.1'),
(332, '2025-03-30 20:26:00.300792', '127.0.0.1'),
(333, '2025-03-30 20:38:35.905289', '127.0.0.1'),
(334, '2025-03-30 20:38:36.894138', '127.0.0.1'),
(335, '2025-03-30 21:00:06.395828', '127.0.0.1'),
(336, '2025-03-31 05:39:20.487415', '127.0.0.1'),
(337, '2025-03-31 05:50:37.402745', '127.0.0.1'),
(338, '2025-03-31 05:50:38.189548', '127.0.0.1'),
(339, '2025-03-31 05:51:22.904260', '127.0.0.1'),
(340, '2025-03-31 05:51:24.104547', '127.0.0.1'),
(341, '2025-03-31 05:53:08.592170', '127.0.0.1'),
(342, '2025-03-31 05:53:09.103319', '127.0.0.1'),
(343, '2025-03-31 05:53:49.595354', '127.0.0.1'),
(344, '2025-03-31 05:53:50.702226', '127.0.0.1'),
(345, '2025-03-31 05:59:04.205400', '127.0.0.1'),
(346, '2025-03-31 05:59:04.889146', '127.0.0.1'),
(347, '2025-03-31 05:59:27.599064', '127.0.0.1'),
(348, '2025-03-31 05:59:27.995798', '127.0.0.1'),
(349, '2025-03-31 06:04:00.104681', '127.0.0.1'),
(350, '2025-03-31 06:05:31.204935', '127.0.0.1'),
(351, '2025-03-31 06:05:31.897895', '127.0.0.1'),
(352, '2025-03-31 06:05:35.699975', '127.0.0.1'),
(353, '2025-03-31 06:05:37.588328', '127.0.0.1'),
(354, '2025-03-31 06:05:46.592549', '127.0.0.1'),
(355, '2025-03-31 06:05:46.998803', '127.0.0.1'),
(356, '2025-03-31 06:07:49.294258', '127.0.0.1'),
(357, '2025-03-31 06:07:49.693860', '127.0.0.1'),
(358, '2025-03-31 06:08:10.089752', '127.0.0.1'),
(359, '2025-03-31 06:08:10.402276', '127.0.0.1'),
(360, '2025-03-31 06:08:32.795010', '127.0.0.1'),
(361, '2025-03-31 06:08:33.200913', '127.0.0.1'),
(362, '2025-03-31 06:08:50.206557', '127.0.0.1'),
(363, '2025-03-31 06:08:50.792204', '127.0.0.1'),
(364, '2025-03-31 06:09:15.204606', '127.0.0.1'),
(365, '2025-03-31 06:09:16.093865', '127.0.0.1'),
(366, '2025-03-31 06:09:45.997097', '127.0.0.1'),
(367, '2025-03-31 06:09:46.391524', '127.0.0.1'),
(368, '2025-03-31 06:22:41.388528', '127.0.0.1'),
(369, '2025-03-31 06:22:42.490576', '127.0.0.1'),
(370, '2025-03-31 06:22:49.392915', '127.0.0.1'),
(371, '2025-03-31 06:22:50.505192', '127.0.0.1'),
(372, '2025-03-31 06:22:52.590842', '127.0.0.1'),
(373, '2025-03-31 06:22:53.288864', '127.0.0.1'),
(374, '2025-03-31 06:33:25.303016', '127.0.0.1'),
(375, '2025-03-31 06:33:25.806751', '127.0.0.1'),
(376, '2025-03-31 06:33:26.994664', '127.0.0.1'),
(377, '2025-03-31 06:33:27.790200', '127.0.0.1'),
(378, '2025-03-31 06:36:37.599878', '127.0.0.1'),
(379, '2025-03-31 06:36:38.705268', '127.0.0.1'),
(380, '2025-03-31 06:36:39.389869', '127.0.0.1'),
(381, '2025-03-31 06:36:46.203891', '127.0.0.1'),
(382, '2025-03-31 06:37:39.802785', '127.0.0.1'),
(383, '2025-03-31 06:37:41.294819', '127.0.0.1'),
(384, '2025-03-31 06:38:18.088102', '127.0.0.1'),
(385, '2025-03-31 06:38:19.589180', '127.0.0.1'),
(386, '2025-03-31 06:38:55.987362', '127.0.0.1'),
(387, '2025-03-31 06:38:56.591087', '127.0.0.1'),
(388, '2025-03-31 06:39:32.703157', '127.0.0.1'),
(389, '2025-03-31 06:39:33.891806', '127.0.0.1'),
(390, '2025-03-31 06:39:35.089899', '127.0.0.1'),
(391, '2025-03-31 06:39:44.091362', '127.0.0.1'),
(392, '2025-03-31 06:45:05.301551', '127.0.0.1'),
(393, '2025-03-31 06:45:06.392846', '127.0.0.1'),
(394, '2025-03-31 06:46:21.499586', '127.0.0.1'),
(395, '2025-03-31 06:46:22.897256', '127.0.0.1'),
(396, '2025-03-31 06:46:23.392624', '127.0.0.1'),
(397, '2025-03-31 06:46:24.096566', '127.0.0.1'),
(398, '2025-03-31 06:47:47.787292', '127.0.0.1'),
(399, '2025-03-31 06:47:48.890666', '127.0.0.1'),
(400, '2025-03-31 06:49:40.890426', '127.0.0.1'),
(401, '2025-03-31 06:49:42.690328', '127.0.0.1'),
(402, '2025-03-31 06:49:45.898679', '127.0.0.1'),
(403, '2025-03-31 06:49:47.103433', '127.0.0.1'),
(404, '2025-03-31 06:50:09.490649', '127.0.0.1'),
(405, '2025-03-31 06:50:10.596013', '127.0.0.1'),
(406, '2025-03-31 06:53:24.001790', '127.0.0.1'),
(407, '2025-03-31 06:53:24.400443', '127.0.0.1'),
(408, '2025-03-31 06:53:48.100297', '127.0.0.1'),
(409, '2025-03-31 06:53:49.596212', '127.0.0.1'),
(410, '2025-03-31 06:53:50.390611', '127.0.0.1'),
(411, '2025-03-31 06:53:50.804598', '127.0.0.1'),
(412, '2025-03-31 06:53:51.791222', '127.0.0.1'),
(413, '2025-03-31 06:53:55.903405', '127.0.0.1'),
(414, '2025-03-31 06:55:21.495797', '127.0.0.1'),
(415, '2025-03-31 06:55:23.292546', '127.0.0.1'),
(416, '2025-03-31 06:55:42.685319', '127.0.0.1'),
(417, '2025-03-31 06:55:43.495593', '127.0.0.1'),
(418, '2025-03-31 06:56:21.991316', '127.0.0.1'),
(419, '2025-03-31 06:56:22.591130', '127.0.0.1'),
(420, '2025-03-31 06:57:06.092239', '127.0.0.1'),
(421, '2025-03-31 06:57:06.502338', '127.0.0.1'),
(422, '2025-03-31 06:57:33.592303', '127.0.0.1'),
(423, '2025-03-31 06:57:34.687670', '127.0.0.1'),
(424, '2025-03-31 07:12:07.290595', '127.0.0.1'),
(425, '2025-03-31 07:12:08.290029', '127.0.0.1'),
(426, '2025-03-31 07:12:09.696510', '127.0.0.1'),
(427, '2025-03-31 07:12:10.100507', '127.0.0.1'),
(428, '2025-03-31 07:13:29.599821', '127.0.0.1'),
(429, '2025-03-31 07:13:30.398010', '127.0.0.1'),
(430, '2025-03-31 07:19:16.786780', '127.0.0.1'),
(431, '2025-03-31 07:19:17.393643', '127.0.0.1'),
(432, '2025-03-31 07:22:21.001546', '127.0.0.1'),
(433, '2025-03-31 07:22:21.690206', '127.0.0.1'),
(434, '2025-03-31 07:22:23.386979', '127.0.0.1'),
(435, '2025-03-31 07:22:25.190343', '127.0.0.1'),
(436, '2025-03-31 07:22:26.286383', '127.0.0.1'),
(437, '2025-03-31 07:22:30.301889', '127.0.0.1'),
(438, '2025-03-31 07:30:23.793379', '127.0.0.1'),
(439, '2025-03-31 07:30:24.895952', '127.0.0.1'),
(440, '2025-03-31 07:30:26.688720', '127.0.0.1'),
(441, '2025-03-31 07:30:28.389280', '127.0.0.1'),
(442, '2025-03-31 07:51:53.199060', '127.0.0.1'),
(443, '2025-03-31 07:51:54.004899', '127.0.0.1'),
(444, '2025-03-31 07:51:56.202680', '127.0.0.1'),
(445, '2025-03-31 07:51:58.398039', '127.0.0.1'),
(446, '2025-03-31 07:59:27.393808', '127.0.0.1'),
(447, '2025-03-31 07:59:28.605133', '127.0.0.1'),
(448, '2025-03-31 08:06:38.090861', '127.0.0.1'),
(449, '2025-03-31 08:06:39.395587', '127.0.0.1'),
(450, '2025-03-31 08:10:07.798627', '127.0.0.1'),
(451, '2025-03-31 08:10:09.000670', '127.0.0.1'),
(452, '2025-03-31 08:15:02.293343', '127.0.0.1'),
(453, '2025-03-31 08:17:03.990873', '127.0.0.1'),
(454, '2025-03-31 08:20:41.195018', '127.0.0.1'),
(455, '2025-03-31 08:27:40.891547', '127.0.0.1'),
(456, '2025-03-31 13:30:22.095661', '127.0.0.1'),
(457, '2025-03-31 15:36:07.389668', '127.0.0.1'),
(458, '2025-03-31 15:48:02.487757', '127.0.0.1'),
(459, '2025-03-31 15:48:02.994190', '127.0.0.1'),
(460, '2025-03-31 15:48:52.206726', '127.0.0.1'),
(461, '2025-03-31 15:48:53.101285', '127.0.0.1'),
(462, '2025-03-31 15:49:02.294648', '127.0.0.1'),
(463, '2025-03-31 15:49:02.998107', '127.0.0.1'),
(464, '2025-03-31 15:53:59.691688', '127.0.0.1'),
(465, '2025-04-01 06:44:11.499851', '127.0.0.1'),
(466, '2025-04-02 15:34:31.520083', '127.0.0.1'),
(467, '2025-04-02 19:08:54.971508', '127.0.0.1'),
(468, '2025-04-03 17:53:30.154860', '127.0.0.1'),
(469, '2025-04-03 17:54:50.442638', '127.0.0.1'),
(470, '2025-04-04 06:05:38.513740', '127.0.0.1'),
(471, '2025-04-07 15:10:29.757561', '127.0.0.1'),
(472, '2025-04-08 14:29:31.807833', '127.0.0.1'),
(473, '2025-04-12 14:51:29.264428', '127.0.0.1'),
(474, '2025-04-15 06:32:42.582070', '127.0.0.1'),
(475, '2025-04-17 12:09:16.285318', '127.0.0.1'),
(476, '2025-04-18 11:03:07.428643', '127.0.0.1'),
(477, '2025-04-18 13:14:15.739622', '127.0.0.1'),
(478, '2025-04-18 13:14:24.608086', '127.0.0.1'),
(479, '2025-04-18 13:14:52.344977', '127.0.0.1'),
(480, '2025-04-18 13:25:09.757408', '127.0.0.1'),
(481, '2025-04-18 13:39:21.167452', '127.0.0.1'),
(482, '2025-04-18 13:57:52.975037', '127.0.0.1'),
(483, '2025-04-18 14:29:47.884095', '127.0.0.1'),
(484, '2025-04-18 14:54:47.990864', '127.0.0.1'),
(485, '2025-04-18 14:55:03.047989', '127.0.0.1'),
(486, '2025-04-18 15:17:18.502273', '127.0.0.1'),
(487, '2025-04-18 22:08:29.931287', '127.0.0.1'),
(488, '2025-04-19 06:53:01.535375', '127.0.0.1'),
(489, '2025-04-19 18:23:39.747626', '127.0.0.1'),
(490, '2025-04-19 18:24:07.754705', '127.0.0.1'),
(491, '2025-04-19 18:25:53.380585', '127.0.0.1'),
(492, '2025-04-19 18:29:25.067161', '127.0.0.1'),
(493, '2025-04-19 18:29:25.154318', '127.0.0.1'),
(494, '2025-04-19 18:33:19.687851', '127.0.0.1'),
(495, '2025-04-19 18:33:19.728171', '127.0.0.1'),
(496, '2025-04-19 18:35:31.094352', '127.0.0.1'),
(497, '2025-04-19 18:35:31.226741', '127.0.0.1'),
(498, '2025-04-19 18:35:50.552344', '127.0.0.1'),
(499, '2025-04-19 18:35:50.600219', '127.0.0.1'),
(500, '2025-04-19 18:35:53.846465', '127.0.0.1'),
(501, '2025-04-19 18:35:53.888274', '127.0.0.1'),
(502, '2025-04-19 18:39:49.210139', '127.0.0.1'),
(503, '2025-04-19 18:39:49.366886', '127.0.0.1'),
(504, '2025-04-19 18:41:26.206469', '127.0.0.1'),
(505, '2025-04-19 18:41:26.293835', '127.0.0.1'),
(506, '2025-04-19 18:41:26.336189', '127.0.0.1'),
(507, '2025-04-19 18:41:26.554172', '127.0.0.1'),
(508, '2025-04-19 18:41:43.691530', '127.0.0.1'),
(509, '2025-04-19 18:41:43.732383', '127.0.0.1'),
(510, '2025-04-19 18:41:43.818550', '127.0.0.1'),
(511, '2025-04-19 18:41:43.859763', '127.0.0.1'),
(512, '2025-04-19 18:42:23.532999', '127.0.0.1'),
(513, '2025-04-19 18:42:23.577090', '127.0.0.1'),
(514, '2025-04-19 18:42:40.681869', '127.0.0.1'),
(515, '2025-04-19 18:42:40.766098', '127.0.0.1'),
(516, '2025-04-19 18:42:40.823051', '127.0.0.1'),
(517, '2025-04-19 18:42:40.864191', '127.0.0.1'),
(518, '2025-04-19 18:46:47.689745', '127.0.0.1'),
(519, '2025-04-19 18:46:47.774960', '127.0.0.1'),
(520, '2025-04-19 18:57:06.917796', '127.0.0.1'),
(521, '2025-04-19 18:57:07.011373', '127.0.0.1'),
(522, '2025-04-19 19:00:23.011950', '127.0.0.1'),
(523, '2025-04-19 19:00:23.070784', '127.0.0.1'),
(524, '2025-04-19 19:01:14.038406', '127.0.0.1'),
(525, '2025-04-19 19:01:14.088971', '127.0.0.1'),
(526, '2025-04-19 19:01:14.266318', '127.0.0.1'),
(527, '2025-04-19 19:01:14.349825', '127.0.0.1'),
(528, '2025-04-19 19:09:13.743095', '127.0.0.1'),
(529, '2025-04-19 19:09:13.789995', '127.0.0.1'),
(530, '2025-04-19 19:09:13.980662', '127.0.0.1'),
(531, '2025-04-19 19:09:15.326221', '127.0.0.1'),
(532, '2025-04-19 19:12:40.049339', '127.0.0.1'),
(533, '2025-04-19 19:12:40.189058', '127.0.0.1'),
(534, '2025-04-19 19:12:40.446656', '127.0.0.1'),
(535, '2025-04-19 19:12:41.902222', '127.0.0.1'),
(536, '2025-04-19 19:12:52.103415', '127.0.0.1'),
(537, '2025-04-19 19:12:52.240836', '127.0.0.1'),
(538, '2025-04-19 19:12:52.332684', '127.0.0.1'),
(539, '2025-04-19 19:12:52.438909', '127.0.0.1'),
(540, '2025-04-19 19:17:31.925453', '127.0.0.1'),
(541, '2025-04-19 19:17:32.262292', '127.0.0.1'),
(542, '2025-04-19 19:17:46.977583', '127.0.0.1'),
(543, '2025-04-19 19:17:47.332856', '127.0.0.1'),
(544, '2025-04-19 19:18:06.620054', '127.0.0.1'),
(545, '2025-04-19 19:18:06.720250', '127.0.0.1'),
(546, '2025-04-19 19:21:05.498081', '127.0.0.1'),
(547, '2025-04-19 19:21:05.548117', '127.0.0.1'),
(548, '2025-04-19 19:21:08.321948', '127.0.0.1'),
(549, '2025-04-19 19:21:08.448113', '127.0.0.1'),
(550, '2025-04-19 19:21:32.265319', '127.0.0.1'),
(551, '2025-04-19 19:21:32.315370', '127.0.0.1'),
(552, '2025-04-19 19:36:46.615030', '127.0.0.1'),
(553, '2025-04-19 19:36:46.659832', '127.0.0.1'),
(554, '2025-04-19 19:38:58.595329', '127.0.0.1'),
(555, '2025-04-19 19:38:58.865225', '127.0.0.1'),
(556, '2025-04-19 19:48:59.479187', '127.0.0.1'),
(557, '2025-04-19 19:48:59.572735', '127.0.0.1'),
(558, '2025-04-19 19:51:17.432754', '127.0.0.1'),
(559, '2025-04-19 19:51:17.520632', '127.0.0.1'),
(560, '2025-04-19 19:51:23.811751', '127.0.0.1'),
(561, '2025-04-19 19:51:23.864673', '127.0.0.1'),
(562, '2025-04-19 19:53:36.251719', '127.0.0.1'),
(563, '2025-04-19 19:53:36.293954', '127.0.0.1'),
(564, '2025-04-19 19:53:46.701935', '127.0.0.1'),
(565, '2025-04-19 19:53:46.790717', '127.0.0.1'),
(566, '2025-04-19 19:54:33.617790', '127.0.0.1'),
(567, '2025-04-19 19:54:33.663865', '127.0.0.1'),
(568, '2025-04-19 20:00:49.981764', '127.0.0.1'),
(569, '2025-04-19 20:00:50.233670', '127.0.0.1'),
(570, '2025-04-19 20:00:50.610763', '127.0.0.1'),
(571, '2025-04-19 20:00:50.853388', '127.0.0.1'),
(572, '2025-04-19 20:00:55.582035', '127.0.0.1'),
(573, '2025-04-19 20:00:55.720739', '127.0.0.1'),
(574, '2025-04-19 20:03:04.127266', '127.0.0.1'),
(575, '2025-04-19 20:03:04.186696', '127.0.0.1'),
(576, '2025-04-19 20:03:04.448766', '127.0.0.1'),
(577, '2025-04-19 20:03:04.509228', '127.0.0.1'),
(578, '2025-04-19 20:03:05.860268', '127.0.0.1'),
(579, '2025-04-19 20:03:05.906286', '127.0.0.1'),
(580, '2025-04-19 20:03:06.965048', '127.0.0.1'),
(581, '2025-04-19 20:03:07.010986', '127.0.0.1'),
(582, '2025-04-19 20:03:11.311747', '127.0.0.1'),
(583, '2025-04-19 20:03:11.357154', '127.0.0.1'),
(584, '2025-04-19 20:03:18.780828', '127.0.0.1'),
(585, '2025-04-19 20:03:18.862081', '127.0.0.1'),
(586, '2025-04-19 20:03:20.023860', '127.0.0.1'),
(587, '2025-04-19 20:03:20.110736', '127.0.0.1'),
(588, '2025-04-19 20:03:24.723130', '127.0.0.1'),
(589, '2025-04-19 20:03:24.833749', '127.0.0.1'),
(590, '2025-04-19 20:06:45.040904', '127.0.0.1'),
(591, '2025-04-19 20:06:45.637759', '127.0.0.1'),
(592, '2025-04-19 20:06:50.698989', '127.0.0.1'),
(593, '2025-04-19 20:06:50.777830', '127.0.0.1'),
(594, '2025-04-19 20:06:56.160757', '127.0.0.1'),
(595, '2025-04-19 20:06:56.237864', '127.0.0.1'),
(596, '2025-04-20 05:28:14.313579', '127.0.0.1'),
(597, '2025-04-20 05:28:14.517954', '127.0.0.1'),
(598, '2025-04-20 05:31:27.772523', '127.0.0.1'),
(599, '2025-04-20 05:31:27.903165', '127.0.0.1'),
(600, '2025-04-20 05:32:57.524941', '127.0.0.1'),
(601, '2025-04-20 05:32:57.642206', '127.0.0.1'),
(602, '2025-04-20 05:34:27.813505', '127.0.0.1'),
(603, '2025-04-20 05:34:27.855378', '127.0.0.1'),
(604, '2025-04-20 05:34:27.955484', '127.0.0.1'),
(605, '2025-04-20 05:34:28.097421', '127.0.0.1'),
(606, '2025-04-20 05:34:29.094483', '127.0.0.1'),
(607, '2025-04-20 05:34:29.187005', '127.0.0.1'),
(608, '2025-04-20 05:34:30.729458', '127.0.0.1'),
(609, '2025-04-20 05:34:30.786413', '127.0.0.1'),
(610, '2025-04-20 05:34:33.033402', '127.0.0.1'),
(611, '2025-04-20 05:34:33.175055', '127.0.0.1'),
(612, '2025-04-20 05:34:34.056257', '127.0.0.1'),
(613, '2025-04-20 05:34:34.365716', '127.0.0.1'),
(614, '2025-04-20 05:35:11.424443', '127.0.0.1'),
(615, '2025-04-20 05:35:11.770565', '127.0.0.1'),
(616, '2025-04-20 05:35:20.960535', '127.0.0.1'),
(617, '2025-04-20 05:35:21.076695', '127.0.0.1'),
(618, '2025-04-20 05:35:22.457767', '127.0.0.1'),
(619, '2025-04-20 05:35:22.549692', '127.0.0.1'),
(620, '2025-04-20 05:35:32.081293', '127.0.0.1'),
(621, '2025-04-20 05:35:32.137454', '127.0.0.1'),
(622, '2025-04-20 05:35:33.115342', '127.0.0.1'),
(623, '2025-04-20 05:35:33.466395', '127.0.0.1'),
(624, '2025-04-20 05:35:40.483479', '127.0.0.1'),
(625, '2025-04-20 05:35:40.566902', '127.0.0.1'),
(626, '2025-04-20 05:35:41.877399', '127.0.0.1'),
(627, '2025-04-20 05:35:42.086305', '127.0.0.1'),
(628, '2025-04-20 05:35:46.627758', '127.0.0.1'),
(629, '2025-04-20 05:35:46.678081', '127.0.0.1'),
(630, '2025-04-20 05:36:41.491976', '127.0.0.1'),
(631, '2025-04-20 05:36:41.602563', '127.0.0.1'),
(632, '2025-04-20 05:36:42.509989', '127.0.0.1'),
(633, '2025-04-20 05:36:42.990128', '127.0.0.1'),
(634, '2025-04-20 05:37:01.948098', '127.0.0.1'),
(635, '2025-04-20 05:37:02.008543', '127.0.0.1'),
(636, '2025-04-20 05:37:03.314196', '127.0.0.1'),
(637, '2025-04-20 05:37:03.417387', '127.0.0.1'),
(638, '2025-04-20 05:38:06.107343', '127.0.0.1'),
(639, '2025-04-20 05:38:06.197637', '127.0.0.1'),
(640, '2025-04-20 05:38:07.309727', '127.0.0.1'),
(641, '2025-04-20 05:38:07.488942', '127.0.0.1'),
(642, '2025-04-20 05:38:11.165213', '127.0.0.1'),
(643, '2025-04-20 05:38:11.269076', '127.0.0.1'),
(644, '2025-04-20 05:38:46.609294', '127.0.0.1'),
(645, '2025-04-20 05:38:46.688436', '127.0.0.1'),
(646, '2025-04-20 05:38:46.730121', '127.0.0.1'),
(647, '2025-04-20 05:38:46.912585', '127.0.0.1'),
(648, '2025-04-20 05:39:00.356809', '127.0.0.1'),
(649, '2025-04-20 05:39:00.596312', '127.0.0.1'),
(650, '2025-04-20 05:39:00.702891', '127.0.0.1'),
(651, '2025-04-20 05:39:00.758581', '127.0.0.1'),
(652, '2025-04-20 05:40:12.107892', '127.0.0.1'),
(653, '2025-04-20 05:40:12.162078', '127.0.0.1'),
(654, '2025-04-20 05:40:26.470078', '127.0.0.1'),
(655, '2025-04-20 05:40:26.635269', '127.0.0.1'),
(656, '2025-04-20 05:40:50.881892', '127.0.0.1'),
(657, '2025-04-20 05:40:50.965565', '127.0.0.1'),
(658, '2025-04-20 05:41:04.152073', '127.0.0.1'),
(659, '2025-04-20 05:41:04.205808', '127.0.0.1'),
(660, '2025-04-20 08:29:22.034270', '127.0.0.1'),
(661, '2025-04-20 08:29:22.041769', '127.0.0.1'),
(662, '2025-04-20 08:45:34.499318', '127.0.0.1'),
(663, '2025-04-20 08:45:34.791958', '127.0.0.1'),
(664, '2025-04-20 08:45:39.647373', '127.0.0.1'),
(665, '2025-04-20 08:45:39.653043', '127.0.0.1'),
(666, '2025-04-20 08:49:36.072648', '127.0.0.1'),
(667, '2025-04-20 08:49:36.079441', '127.0.0.1'),
(668, '2025-04-20 09:05:50.744563', '127.0.0.1'),
(669, '2025-04-20 09:05:50.831877', '127.0.0.1'),
(670, '2025-04-20 09:07:45.126775', '127.0.0.1'),
(671, '2025-04-20 09:07:45.143123', '127.0.0.1'),
(672, '2025-04-20 09:07:45.271141', '127.0.0.1'),
(673, '2025-04-20 09:07:45.481104', '127.0.0.1'),
(674, '2025-04-20 09:07:46.889548', '127.0.0.1'),
(675, '2025-04-20 09:07:48.845125', '127.0.0.1'),
(676, '2025-04-20 09:07:48.883367', '127.0.0.1'),
(677, '2025-04-20 09:07:48.962230', '127.0.0.1'),
(678, '2025-04-20 09:07:48.967450', '127.0.0.1'),
(679, '2025-04-20 09:07:49.133259', '127.0.0.1'),
(680, '2025-04-20 09:07:49.968912', '127.0.0.1'),
(681, '2025-04-20 09:07:50.294459', '127.0.0.1'),
(682, '2025-04-20 09:07:50.297448', '127.0.0.1'),
(683, '2025-04-20 09:07:50.537641', '127.0.0.1'),
(684, '2025-04-20 09:07:50.602420', '127.0.0.1'),
(685, '2025-04-20 09:07:51.525917', '127.0.0.1'),
(686, '2025-04-20 09:07:51.546093', '127.0.0.1'),
(687, '2025-04-20 09:07:53.257810', '127.0.0.1'),
(688, '2025-04-20 09:07:53.378848', '127.0.0.1'),
(689, '2025-04-20 09:07:53.386938', '127.0.0.1'),
(690, '2025-04-20 09:07:53.393898', '127.0.0.1'),
(691, '2025-04-20 09:07:54.673790', '127.0.0.1'),
(692, '2025-04-20 09:07:54.882078', '127.0.0.1'),
(693, '2025-04-20 09:08:10.397936', '127.0.0.1'),
(694, '2025-04-20 09:08:10.421090', '127.0.0.1'),
(695, '2025-04-20 09:08:10.464546', '127.0.0.1'),
(696, '2025-04-20 09:08:10.470692', '127.0.0.1'),
(697, '2025-04-20 09:08:11.358367', '127.0.0.1'),
(698, '2025-04-20 09:08:11.393750', '127.0.0.1'),
(699, '2025-04-20 09:08:18.806828', '127.0.0.1'),
(700, '2025-04-20 09:08:18.835409', '127.0.0.1'),
(701, '2025-04-20 09:08:18.900978', '127.0.0.1'),
(702, '2025-04-20 09:08:18.918281', '127.0.0.1'),
(703, '2025-04-20 09:08:19.045909', '127.0.0.1'),
(704, '2025-04-20 09:08:20.269265', '127.0.0.1'),
(705, '2025-04-20 09:08:23.186333', '127.0.0.1'),
(706, '2025-04-20 09:08:23.201092', '127.0.0.1'),
(707, '2025-04-20 09:08:23.316687', '127.0.0.1'),
(708, '2025-04-20 09:08:23.343252', '127.0.0.1'),
(709, '2025-04-20 09:08:23.498362', '127.0.0.1'),
(710, '2025-04-20 09:08:23.527969', '127.0.0.1'),
(711, '2025-04-20 09:08:29.644136', '127.0.0.1'),
(712, '2025-04-20 09:08:29.648204', '127.0.0.1'),
(713, '2025-04-20 09:08:29.833235', '127.0.0.1'),
(714, '2025-04-20 09:08:29.868528', '127.0.0.1'),
(715, '2025-04-20 09:08:31.041023', '127.0.0.1'),
(716, '2025-04-20 09:08:31.138038', '127.0.0.1'),
(717, '2025-04-20 09:08:33.184568', '127.0.0.1'),
(718, '2025-04-20 09:08:33.233832', '127.0.0.1'),
(719, '2025-04-20 09:08:33.419167', '127.0.0.1'),
(720, '2025-04-20 09:08:33.455995', '127.0.0.1'),
(721, '2025-04-20 09:08:34.030938', '127.0.0.1'),
(722, '2025-04-20 09:08:34.035149', '127.0.0.1'),
(723, '2025-04-20 09:08:35.561536', '127.0.0.1'),
(724, '2025-04-20 09:08:35.588040', '127.0.0.1'),
(725, '2025-04-20 09:08:35.659198', '127.0.0.1'),
(726, '2025-04-20 09:08:35.674753', '127.0.0.1'),
(727, '2025-04-20 09:08:35.880226', '127.0.0.1'),
(728, '2025-04-20 09:08:37.273788', '127.0.0.1'),
(729, '2025-04-20 09:08:40.196260', '127.0.0.1'),
(730, '2025-04-20 09:08:40.248228', '127.0.0.1'),
(731, '2025-04-20 09:08:41.034176', '127.0.0.1'),
(732, '2025-04-20 09:08:41.063901', '127.0.0.1'),
(733, '2025-04-20 09:08:41.312558', '127.0.0.1'),
(734, '2025-04-20 09:08:41.348179', '127.0.0.1'),
(735, '2025-04-20 09:08:42.482507', '127.0.0.1'),
(736, '2025-04-20 09:08:42.513871', '127.0.0.1'),
(737, '2025-04-20 09:08:42.676432', '127.0.0.1'),
(738, '2025-04-20 09:08:42.711492', '127.0.0.1'),
(739, '2025-04-20 09:08:51.104325', '127.0.0.1'),
(740, '2025-04-20 09:08:51.143969', '127.0.0.1'),
(741, '2025-04-20 09:08:51.248026', '127.0.0.1'),
(742, '2025-04-20 09:08:51.254361', '127.0.0.1'),
(743, '2025-04-20 09:08:51.807097', '127.0.0.1'),
(744, '2025-04-20 09:08:51.886479', '127.0.0.1'),
(745, '2025-04-20 09:08:57.709054', '127.0.0.1'),
(746, '2025-04-20 09:08:57.731619', '127.0.0.1'),
(747, '2025-04-20 09:08:57.794238', '127.0.0.1'),
(748, '2025-04-20 09:09:02.849686', '127.0.0.1'),
(749, '2025-04-20 09:09:02.866324', '127.0.0.1'),
(750, '2025-04-20 09:09:02.874663', '127.0.0.1'),
(751, '2025-04-20 09:09:02.909850', '127.0.0.1'),
(752, '2025-04-20 09:09:02.919395', '127.0.0.1'),
(753, '2025-04-20 09:09:07.884367', '127.0.0.1'),
(754, '2025-04-20 09:09:07.895323', '127.0.0.1'),
(755, '2025-04-20 09:09:07.900525', '127.0.0.1'),
(756, '2025-04-20 09:09:12.906718', '127.0.0.1'),
(757, '2025-04-20 09:09:12.912783', '127.0.0.1'),
(758, '2025-04-20 09:09:14.004734', '127.0.0.1'),
(759, '2025-04-20 09:09:14.197582', '127.0.0.1'),
(760, '2025-04-20 09:10:39.601701', '127.0.0.1'),
(761, '2025-04-20 09:10:39.605912', '127.0.0.1'),
(762, '2025-04-20 09:10:39.876433', '127.0.0.1'),
(763, '2025-04-20 09:10:39.938080', '127.0.0.1'),
(764, '2025-04-20 09:10:41.251258', '127.0.0.1'),
(765, '2025-04-20 09:11:02.444561', '127.0.0.1'),
(766, '2025-04-20 09:11:02.449904', '127.0.0.1'),
(767, '2025-04-20 09:11:02.680267', '127.0.0.1'),
(768, '2025-04-20 09:11:02.715467', '127.0.0.1'),
(769, '2025-04-20 09:11:03.701462', '127.0.0.1'),
(770, '2025-04-20 09:11:03.823302', '127.0.0.1'),
(771, '2025-04-20 09:13:26.952476', '127.0.0.1'),
(772, '2025-04-20 09:13:26.955807', '127.0.0.1'),
(773, '2025-04-20 09:15:09.311401', '127.0.0.1'),
(774, '2025-04-20 09:16:10.636197', '127.0.0.1'),
(775, '2025-04-20 09:16:10.639576', '127.0.0.1'),
(776, '2025-04-20 09:16:27.849839', '127.0.0.1'),
(777, '2025-04-20 09:16:27.886511', '127.0.0.1'),
(778, '2025-04-20 09:21:15.817509', '127.0.0.1'),
(779, '2025-04-20 09:21:15.826387', '127.0.0.1'),
(780, '2025-04-20 09:21:16.122667', '127.0.0.1'),
(781, '2025-04-20 09:21:16.134144', '127.0.0.1'),
(782, '2025-04-20 09:21:16.447304', '127.0.0.1'),
(783, '2025-04-20 09:42:22.417739', '127.0.0.1'),
(784, '2025-04-20 09:42:22.421715', '127.0.0.1'),
(785, '2025-04-20 09:46:08.434820', '127.0.0.1'),
(786, '2025-04-20 10:23:27.809897', '127.0.0.1'),
(787, '2025-04-20 10:23:27.815352', '127.0.0.1'),
(788, '2025-04-20 10:42:11.017566', '127.0.0.1'),
(789, '2025-04-20 10:42:11.023377', '127.0.0.1'),
(790, '2025-04-20 10:43:18.993268', '127.0.0.1'),
(791, '2025-04-20 10:43:18.997259', '127.0.0.1'),
(792, '2025-04-20 10:43:29.812136', '127.0.0.1'),
(793, '2025-04-20 10:43:29.822393', '127.0.0.1'),
(794, '2025-04-20 10:50:37.119678', '127.0.0.1'),
(795, '2025-04-20 10:50:37.129453', '127.0.0.1'),
(796, '2025-04-20 10:51:17.762284', '127.0.0.1'),
(797, '2025-04-20 10:52:08.592956', '127.0.0.1'),
(798, '2025-04-20 10:52:08.600128', '127.0.0.1'),
(799, '2025-04-20 10:54:24.863735', '127.0.0.1'),
(800, '2025-04-20 10:54:24.866788', '127.0.0.1'),
(801, '2025-04-20 10:54:47.178921', '127.0.0.1'),
(802, '2025-04-20 10:54:47.183045', '127.0.0.1'),
(803, '2025-04-20 11:00:17.136528', '127.0.0.1'),
(804, '2025-04-20 11:00:17.144314', '127.0.0.1'),
(805, '2025-04-20 11:00:41.135026', '127.0.0.1'),
(806, '2025-04-20 11:00:41.138218', '127.0.0.1'),
(807, '2025-04-20 11:03:49.686525', '127.0.0.1'),
(808, '2025-04-20 11:03:49.701492', '127.0.0.1'),
(809, '2025-04-20 11:03:49.961435', '127.0.0.1'),
(810, '2025-04-20 11:13:35.293318', '127.0.0.1'),
(811, '2025-04-20 11:13:35.297388', '127.0.0.1'),
(812, '2025-04-20 11:24:48.278288', '127.0.0.1'),
(813, '2025-04-20 11:24:48.283019', '127.0.0.1'),
(814, '2025-04-20 11:24:48.536735', '127.0.0.1'),
(815, '2025-04-20 11:24:48.589983', '127.0.0.1'),
(816, '2025-04-20 11:31:30.881563', '127.0.0.1'),
(817, '2025-04-20 11:34:16.809497', '127.0.0.1'),
(818, '2025-04-20 11:34:16.835593', '127.0.0.1'),
(819, '2025-04-21 08:57:13.208078', '127.0.0.1'),
(820, '2025-04-21 08:57:13.234412', '127.0.0.1'),
(821, '2025-04-21 09:23:02.271805', '127.0.0.1'),
(822, '2025-04-21 09:23:02.288588', '127.0.0.1'),
(823, '2025-04-21 09:40:51.577479', '127.0.0.1'),
(824, '2025-04-21 09:40:52.806470', '127.0.0.1'),
(825, '2025-04-21 09:40:52.808924', '127.0.0.1'),
(826, '2025-04-21 09:40:54.517087', '127.0.0.1'),
(827, '2025-04-21 09:40:54.523986', '127.0.0.1'),
(828, '2025-04-21 09:40:56.516298', '127.0.0.1'),
(829, '2025-04-21 09:40:56.523891', '127.0.0.1'),
(830, '2025-04-21 09:40:59.808431', '127.0.0.1'),
(831, '2025-04-21 09:40:59.811210', '127.0.0.1'),
(832, '2025-04-21 09:41:01.977741', '127.0.0.1'),
(833, '2025-04-21 09:41:01.983752', '127.0.0.1'),
(834, '2025-04-21 09:41:13.458075', '127.0.0.1'),
(835, '2025-04-21 09:41:13.732954', '127.0.0.1'),
(836, '2025-04-21 09:41:24.128230', '127.0.0.1'),
(837, '2025-04-21 09:41:24.131897', '127.0.0.1'),
(838, '2025-04-21 09:41:33.992944', '127.0.0.1'),
(839, '2025-04-21 09:41:34.000930', '127.0.0.1'),
(840, '2025-04-21 09:41:35.717333', '127.0.0.1'),
(841, '2025-04-21 09:41:35.721777', '127.0.0.1'),
(842, '2025-04-21 09:41:38.299114', '127.0.0.1'),
(843, '2025-04-21 09:41:38.305664', '127.0.0.1'),
(844, '2025-04-21 09:41:49.276344', '127.0.0.1'),
(845, '2025-04-21 09:41:49.283457', '127.0.0.1'),
(846, '2025-04-21 09:41:51.475539', '127.0.0.1'),
(847, '2025-04-21 09:41:51.478896', '127.0.0.1'),
(848, '2025-04-21 09:42:03.140958', '127.0.0.1'),
(849, '2025-04-21 09:42:03.155360', '127.0.0.1'),
(850, '2025-04-21 09:42:06.410555', '127.0.0.1'),
(851, '2025-04-21 09:42:06.416690', '127.0.0.1'),
(852, '2025-04-21 09:42:12.363003', '127.0.0.1'),
(853, '2025-04-21 09:42:12.365988', '127.0.0.1'),
(854, '2025-04-21 09:42:14.183659', '127.0.0.1'),
(855, '2025-04-21 09:42:14.192245', '127.0.0.1'),
(856, '2025-04-21 09:42:16.012757', '127.0.0.1'),
(857, '2025-04-21 09:42:16.019022', '127.0.0.1'),
(858, '2025-04-21 09:42:18.976332', '127.0.0.1'),
(859, '2025-04-21 09:42:18.980343', '127.0.0.1'),
(860, '2025-04-21 09:42:23.048542', '127.0.0.1'),
(861, '2025-04-21 09:42:23.057107', '127.0.0.1'),
(862, '2025-04-21 09:42:25.128354', '127.0.0.1'),
(863, '2025-04-21 09:42:25.135435', '127.0.0.1'),
(864, '2025-04-21 09:44:10.104241', '127.0.0.1'),
(865, '2025-04-21 09:44:10.106895', '127.0.0.1'),
(866, '2025-04-21 09:44:18.373889', '127.0.0.1'),
(867, '2025-04-21 09:44:18.381541', '127.0.0.1'),
(868, '2025-04-21 09:44:36.403642', '127.0.0.1'),
(869, '2025-04-21 09:44:36.406849', '127.0.0.1'),
(870, '2025-04-21 09:44:48.852264', '127.0.0.1'),
(871, '2025-04-21 09:44:48.858023', '127.0.0.1'),
(872, '2025-04-21 09:44:50.140582', '127.0.0.1'),
(873, '2025-04-21 09:44:50.151092', '127.0.0.1'),
(874, '2025-04-21 09:44:51.894821', '127.0.0.1'),
(875, '2025-04-21 09:44:51.910893', '127.0.0.1'),
(876, '2025-04-21 09:44:53.364910', '127.0.0.1'),
(877, '2025-04-21 09:44:53.369091', '127.0.0.1'),
(878, '2025-04-21 10:03:22.479822', '127.0.0.1'),
(879, '2025-04-21 10:03:22.489248', '127.0.0.1'),
(880, '2025-04-21 10:03:24.074189', '127.0.0.1'),
(881, '2025-04-21 10:03:24.341373', '127.0.0.1'),
(882, '2025-04-21 10:03:28.310109', '127.0.0.1'),
(883, '2025-04-21 10:03:28.317326', '127.0.0.1'),
(884, '2025-04-21 10:15:08.353489', '127.0.0.1'),
(885, '2025-04-21 10:15:08.357065', '127.0.0.1'),
(886, '2025-04-21 10:15:16.135571', '127.0.0.1'),
(887, '2025-04-21 10:15:16.142558', '127.0.0.1'),
(888, '2025-04-21 11:01:13.817890', '127.0.0.1'),
(889, '2025-04-21 11:01:13.825201', '127.0.0.1'),
(890, '2025-04-21 11:08:37.731208', '127.0.0.1'),
(891, '2025-04-21 11:08:37.738226', '127.0.0.1'),
(892, '2025-04-21 11:29:05.449822', '127.0.0.1'),
(893, '2025-04-21 11:29:36.300204', '127.0.0.1'),
(894, '2025-04-21 11:49:12.721199', '127.0.0.1'),
(895, '2025-04-21 11:49:12.729972', '127.0.0.1'),
(896, '2025-04-21 11:49:13.912846', '127.0.0.1'),
(897, '2025-04-21 11:49:13.921476', '127.0.0.1'),
(898, '2025-04-21 11:49:53.882892', '127.0.0.1'),
(899, '2025-04-21 11:49:53.886128', '127.0.0.1'),
(900, '2025-04-21 11:49:53.889265', '127.0.0.1'),
(901, '2025-04-21 11:49:53.900954', '127.0.0.1'),
(902, '2025-04-21 11:50:23.219583', '127.0.0.1'),
(903, '2025-04-21 11:50:23.223658', '127.0.0.1'),
(904, '2025-04-21 11:50:23.226656', '127.0.0.1'),
(905, '2025-04-21 11:50:23.234115', '127.0.0.1'),
(906, '2025-04-21 11:50:30.049693', '127.0.0.1'),
(907, '2025-04-21 11:50:30.058851', '127.0.0.1'),
(908, '2025-04-21 11:50:30.201774', '127.0.0.1'),
(909, '2025-04-21 11:50:30.222848', '127.0.0.1'),
(910, '2025-04-21 11:51:11.544933', '127.0.0.1'),
(911, '2025-04-21 11:51:11.549375', '127.0.0.1'),
(912, '2025-04-21 11:51:11.555339', '127.0.0.1'),
(913, '2025-04-21 11:52:50.338207', '127.0.0.1'),
(914, '2025-04-21 11:52:50.346559', '127.0.0.1'),
(915, '2025-04-21 11:55:29.198071', '127.0.0.1'),
(916, '2025-04-21 11:55:29.201706', '127.0.0.1'),
(917, '2025-04-21 11:55:29.204182', '127.0.0.1'),
(918, '2025-04-21 11:55:29.213878', '127.0.0.1'),
(919, '2025-04-21 11:56:27.359190', '127.0.0.1'),
(920, '2025-04-21 11:57:30.563251', '127.0.0.1'),
(921, '2025-04-21 11:57:30.571819', '127.0.0.1'),
(922, '2025-04-21 11:59:45.664355', '127.0.0.1'),
(923, '2025-04-21 12:03:50.951866', '127.0.0.1'),
(924, '2025-04-21 12:03:50.956393', '127.0.0.1'),
(925, '2025-04-21 12:09:47.680319', '127.0.0.1'),
(926, '2025-04-21 12:09:47.689374', '127.0.0.1'),
(927, '2025-04-21 12:11:00.701429', '127.0.0.1'),
(928, '2025-04-21 12:11:00.705661', '127.0.0.1'),
(929, '2025-04-21 12:13:00.654664', '127.0.0.1'),
(930, '2025-04-21 12:13:00.658953', '127.0.0.1'),
(931, '2025-04-21 12:13:04.834031', '127.0.0.1'),
(932, '2025-04-21 12:13:04.837089', '127.0.0.1'),
(933, '2025-04-21 12:13:17.597244', '127.0.0.1'),
(934, '2025-04-21 12:13:17.646735', '127.0.0.1'),
(935, '2025-04-21 12:14:27.848545', '127.0.0.1'),
(936, '2025-04-21 12:14:27.855629', '127.0.0.1'),
(937, '2025-04-21 12:14:46.074887', '127.0.0.1'),
(938, '2025-04-21 12:14:46.081572', '127.0.0.1'),
(939, '2025-04-21 12:18:48.273037', '127.0.0.1'),
(940, '2025-04-21 12:18:48.276656', '127.0.0.1'),
(941, '2025-04-21 12:18:58.275188', '127.0.0.1'),
(942, '2025-04-21 12:18:58.287499', '127.0.0.1'),
(943, '2025-04-21 12:30:53.265731', '127.0.0.1'),
(944, '2025-04-21 12:30:53.275363', '127.0.0.1'),
(945, '2025-04-21 12:37:16.597119', '127.0.0.1'),
(946, '2025-04-21 12:37:16.616707', '127.0.0.1'),
(947, '2025-04-21 12:48:34.317382', '127.0.0.1'),
(948, '2025-04-21 12:48:34.324126', '127.0.0.1'),
(949, '2025-04-21 13:19:56.092986', '127.0.0.1'),
(950, '2025-04-21 13:19:56.097119', '127.0.0.1'),
(951, '2025-04-21 13:46:16.069742', '127.0.0.1'),
(952, '2025-04-21 13:46:16.081878', '127.0.0.1'),
(953, '2025-04-21 13:46:17.636141', '127.0.0.1'),
(954, '2025-04-21 13:46:17.913443', '127.0.0.1'),
(955, '2025-04-21 13:46:37.152166', '127.0.0.1'),
(956, '2025-04-21 13:46:37.153764', '127.0.0.1'),
(957, '2025-04-21 13:46:40.157195', '127.0.0.1'),
(958, '2025-04-21 13:46:40.162474', '127.0.0.1'),
(959, '2025-04-21 13:55:17.516327', '127.0.0.1'),
(960, '2025-04-21 13:55:17.528217', '127.0.0.1'),
(961, '2025-04-21 13:55:20.091461', '127.0.0.1'),
(962, '2025-04-21 13:55:20.086532', '127.0.0.1'),
(963, '2025-04-21 14:08:34.050261', '127.0.0.1'),
(964, '2025-04-21 14:08:34.208210', '127.0.0.1'),
(965, '2025-04-21 14:08:36.269594', '127.0.0.1'),
(966, '2025-04-21 14:08:36.271764', '127.0.0.1'),
(967, '2025-04-21 14:17:37.003382', '127.0.0.1'),
(968, '2025-04-21 14:17:37.014538', '127.0.0.1'),
(969, '2025-04-21 14:19:07.897743', '127.0.0.1'),
(970, '2025-04-21 14:19:07.901581', '127.0.0.1'),
(971, '2025-04-21 14:27:49.213265', '127.0.0.1'),
(972, '2025-04-21 14:27:49.218051', '127.0.0.1'),
(973, '2025-04-21 14:27:53.423430', '127.0.0.1'),
(974, '2025-04-21 14:27:53.424895', '127.0.0.1'),
(975, '2025-04-21 14:45:47.575154', '127.0.0.1'),
(976, '2025-04-21 14:45:51.183895', '127.0.0.1'),
(977, '2025-04-21 14:50:50.440902', '127.0.0.1'),
(978, '2025-04-21 14:50:50.538744', '127.0.0.1'),
(979, '2025-04-21 14:50:53.299858', '127.0.0.1'),
(980, '2025-04-21 14:50:53.422905', '127.0.0.1'),
(981, '2025-04-21 14:53:10.071725', '127.0.0.1'),
(982, '2025-04-21 14:53:10.073106', '127.0.0.1'),
(983, '2025-04-21 14:53:12.602139', '127.0.0.1'),
(984, '2025-04-21 14:53:12.606959', '127.0.0.1'),
(985, '2025-04-21 14:58:17.205981', '127.0.0.1'),
(986, '2025-04-21 14:58:17.487584', '127.0.0.1'),
(987, '2025-04-21 14:58:36.741787', '127.0.0.1'),
(988, '2025-04-21 14:58:36.740296', '127.0.0.1'),
(989, '2025-04-21 14:58:43.571949', '127.0.0.1'),
(990, '2025-04-21 14:58:43.573894', '127.0.0.1'),
(991, '2025-04-21 15:05:36.159945', '127.0.0.1'),
(992, '2025-04-21 15:05:36.204901', '127.0.0.1'),
(993, '2025-04-21 15:12:05.757431', '127.0.0.1'),
(994, '2025-04-21 15:12:05.761200', '127.0.0.1'),
(995, '2025-04-21 15:12:54.043367', '127.0.0.1'),
(996, '2025-04-21 15:12:54.041019', '127.0.0.1'),
(997, '2025-04-21 15:13:15.520172', '127.0.0.1'),
(998, '2025-04-21 15:13:15.521382', '127.0.0.1'),
(999, '2025-04-21 15:14:07.094317', '127.0.0.1'),
(1000, '2025-04-21 15:14:07.096873', '127.0.0.1'),
(1001, '2025-04-21 15:14:10.497524', '127.0.0.1'),
(1002, '2025-04-21 15:14:10.496000', '127.0.0.1'),
(1003, '2025-04-21 15:36:18.447970', '127.0.0.1'),
(1004, '2025-04-21 15:36:18.516586', '127.0.0.1'),
(1005, '2025-04-21 15:36:18.533721', '127.0.0.1'),
(1006, '2025-04-21 15:36:18.740604', '127.0.0.1'),
(1007, '2025-04-21 15:36:19.057854', '127.0.0.1'),
(1008, '2025-04-21 15:36:19.857383', '127.0.0.1'),
(1009, '2025-04-21 15:43:10.300582', '127.0.0.1'),
(1010, '2025-04-21 15:43:10.334704', '127.0.0.1'),
(1011, '2025-04-21 15:43:10.468585', '127.0.0.1'),
(1012, '2025-04-21 15:43:10.507734', '127.0.0.1'),
(1013, '2025-04-21 15:43:10.973958', '127.0.0.1'),
(1014, '2025-04-21 15:43:11.449809', '127.0.0.1'),
(1015, '2025-04-21 15:46:22.983781', '127.0.0.1'),
(1016, '2025-04-21 15:58:04.211437', '127.0.0.1'),
(1017, '2025-04-21 15:58:04.223618', '127.0.0.1'),
(1018, '2025-04-21 16:23:30.930714', '127.0.0.1'),
(1019, '2025-04-21 16:23:39.028450', '127.0.0.1'),
(1020, '2025-04-21 16:23:39.029577', '127.0.0.1'),
(1021, '2025-04-21 16:24:32.926149', '127.0.0.1'),
(1022, '2025-04-21 16:24:33.090045', '127.0.0.1'),
(1023, '2025-04-21 16:34:29.747929', '127.0.0.1'),
(1024, '2025-04-21 16:34:29.754976', '127.0.0.1'),
(1025, '2025-04-21 16:34:31.625895', '127.0.0.1'),
(1026, '2025-04-21 16:34:31.696182', '127.0.0.1'),
(1027, '2025-04-21 16:38:03.061354', '127.0.0.1'),
(1028, '2025-04-21 16:47:26.623966', '127.0.0.1'),
(1029, '2025-04-21 16:47:26.624332', '127.0.0.1'),
(1030, '2025-04-21 16:47:26.689965', '127.0.0.1'),
(1031, '2025-04-21 16:47:26.708851', '127.0.0.1'),
(1032, '2025-04-21 16:47:26.911164', '127.0.0.1'),
(1033, '2025-04-21 16:47:27.039460', '127.0.0.1'),
(1034, '2025-04-21 16:47:32.657283', '127.0.0.1'),
(1035, '2025-04-21 16:47:32.665478', '127.0.0.1'),
(1036, '2025-04-21 16:47:32.722208', '127.0.0.1'),
(1037, '2025-04-21 16:47:32.733510', '127.0.0.1'),
(1038, '2025-04-21 16:47:32.898114', '127.0.0.1'),
(1039, '2025-04-21 16:47:32.912300', '127.0.0.1'),
(1040, '2025-04-21 16:49:06.738227', '127.0.0.1'),
(1041, '2025-04-21 16:49:06.787370', '127.0.0.1');
INSERT INTO `core_visit` (`id`, `timestamp`, `ip_address`) VALUES
(1042, '2025-04-21 16:49:06.818481', '127.0.0.1'),
(1043, '2025-04-21 16:49:07.129017', '127.0.0.1'),
(1044, '2025-04-21 16:50:21.039944', '127.0.0.1'),
(1045, '2025-04-21 16:50:21.050078', '127.0.0.1'),
(1046, '2025-04-21 16:50:33.127809', '127.0.0.1'),
(1047, '2025-04-21 16:50:33.134306', '127.0.0.1'),
(1048, '2025-04-21 16:53:48.477357', '127.0.0.1'),
(1049, '2025-04-21 16:53:56.326382', '127.0.0.1'),
(1050, '2025-04-21 16:53:56.390476', '127.0.0.1'),
(1051, '2025-04-21 16:54:01.119768', '127.0.0.1'),
(1052, '2025-04-21 16:54:01.128483', '127.0.0.1'),
(1053, '2025-04-21 17:00:24.859791', '127.0.0.1'),
(1054, '2025-04-21 17:00:24.884913', '127.0.0.1'),
(1055, '2025-04-21 17:00:25.344452', '127.0.0.1'),
(1056, '2025-04-21 17:00:25.392222', '127.0.0.1'),
(1057, '2025-04-21 17:00:25.480526', '127.0.0.1'),
(1058, '2025-04-21 17:00:25.762538', '127.0.0.1'),
(1059, '2025-04-21 17:15:34.431018', '127.0.0.1'),
(1060, '2025-04-21 17:15:34.440687', '127.0.0.1'),
(1061, '2025-04-21 17:15:34.485344', '127.0.0.1'),
(1062, '2025-04-21 17:15:34.807099', '127.0.0.1'),
(1063, '2025-04-21 17:22:55.747637', '127.0.0.1'),
(1064, '2025-04-21 17:28:44.152851', '127.0.0.1'),
(1065, '2025-04-21 17:28:44.160246', '127.0.0.1'),
(1066, '2025-04-21 17:29:17.544181', '127.0.0.1'),
(1067, '2025-04-21 17:30:20.026862', '127.0.0.1'),
(1068, '2025-04-21 17:32:33.680955', '127.0.0.1'),
(1069, '2025-04-21 17:32:33.750891', '127.0.0.1'),
(1070, '2025-04-21 17:41:06.278389', '127.0.0.1'),
(1071, '2025-04-21 17:41:06.289772', '127.0.0.1'),
(1072, '2025-04-21 17:42:41.336509', '127.0.0.1'),
(1073, '2025-04-21 17:43:01.178680', '127.0.0.1'),
(1074, '2025-04-21 18:45:18.786429', '127.0.0.1'),
(1075, '2025-04-21 18:45:18.804795', '127.0.0.1'),
(1076, '2025-04-21 18:45:18.805968', '127.0.0.1'),
(1077, '2025-04-21 18:45:18.810400', '127.0.0.1'),
(1078, '2025-04-21 18:45:18.856958', '127.0.0.1'),
(1079, '2025-04-21 18:45:18.863045', '127.0.0.1'),
(1080, '2025-04-21 18:45:19.241112', '127.0.0.1'),
(1081, '2025-04-21 18:45:19.450561', '127.0.0.1'),
(1082, '2025-04-21 18:45:21.591692', '127.0.0.1'),
(1083, '2025-04-21 18:45:21.592016', '127.0.0.1'),
(1084, '2025-04-21 18:45:21.752066', '127.0.0.1'),
(1085, '2025-04-21 18:45:21.758855', '127.0.0.1'),
(1086, '2025-04-21 18:45:23.876883', '127.0.0.1'),
(1087, '2025-04-21 18:45:23.880574', '127.0.0.1'),
(1088, '2025-04-21 18:45:24.029968', '127.0.0.1'),
(1089, '2025-04-21 18:45:24.043568', '127.0.0.1'),
(1090, '2025-04-21 18:45:31.494208', '127.0.0.1'),
(1091, '2025-04-21 18:45:31.497551', '127.0.0.1'),
(1092, '2025-04-21 18:45:31.586225', '127.0.0.1'),
(1093, '2025-04-21 18:45:31.598112', '127.0.0.1'),
(1094, '2025-04-21 18:45:33.657137', '127.0.0.1'),
(1095, '2025-04-21 18:45:33.661948', '127.0.0.1'),
(1096, '2025-04-21 18:45:33.800090', '127.0.0.1'),
(1097, '2025-04-21 18:45:33.800361', '127.0.0.1'),
(1098, '2025-04-21 18:45:36.523269', '127.0.0.1'),
(1099, '2025-04-21 18:45:36.529691', '127.0.0.1'),
(1100, '2025-04-21 18:45:36.648726', '127.0.0.1'),
(1101, '2025-04-21 18:45:36.656067', '127.0.0.1'),
(1102, '2025-04-21 18:45:39.161448', '127.0.0.1'),
(1103, '2025-04-21 18:45:39.165040', '127.0.0.1'),
(1104, '2025-04-21 18:45:39.247498', '127.0.0.1'),
(1105, '2025-04-21 18:45:39.279872', '127.0.0.1'),
(1106, '2025-04-21 18:46:28.305842', '127.0.0.1'),
(1107, '2025-04-21 18:46:28.341716', '127.0.0.1'),
(1108, '2025-04-21 18:46:28.373896', '127.0.0.1'),
(1109, '2025-04-21 18:46:28.396713', '127.0.0.1'),
(1110, '2025-04-21 18:46:33.302073', '127.0.0.1'),
(1111, '2025-04-21 18:46:33.309190', '127.0.0.1'),
(1112, '2025-04-21 18:46:33.583228', '127.0.0.1'),
(1113, '2025-04-21 18:46:33.590774', '127.0.0.1'),
(1114, '2025-04-21 18:46:36.531908', '127.0.0.1'),
(1115, '2025-04-21 18:46:36.536219', '127.0.0.1'),
(1116, '2025-04-21 18:46:36.808050', '127.0.0.1'),
(1117, '2025-04-21 18:46:36.821499', '127.0.0.1'),
(1118, '2025-04-21 18:46:38.222938', '127.0.0.1'),
(1119, '2025-04-21 18:46:38.237447', '127.0.0.1'),
(1120, '2025-04-21 18:46:38.748155', '127.0.0.1'),
(1121, '2025-04-21 18:46:38.768802', '127.0.0.1'),
(1122, '2025-04-21 18:46:50.161986', '127.0.0.1'),
(1123, '2025-04-21 18:46:50.172837', '127.0.0.1'),
(1124, '2025-04-21 18:46:50.420241', '127.0.0.1'),
(1125, '2025-04-21 18:46:50.425304', '127.0.0.1'),
(1126, '2025-04-21 18:46:53.137567', '127.0.0.1'),
(1127, '2025-04-21 18:46:53.141714', '127.0.0.1'),
(1128, '2025-04-21 18:46:53.509653', '127.0.0.1'),
(1129, '2025-04-21 18:46:53.514677', '127.0.0.1'),
(1130, '2025-04-21 18:47:14.083802', '127.0.0.1'),
(1131, '2025-04-21 18:47:14.084226', '127.0.0.1'),
(1132, '2025-04-21 18:47:14.404264', '127.0.0.1'),
(1133, '2025-04-21 18:47:14.410467', '127.0.0.1'),
(1134, '2025-04-21 18:47:21.010359', '127.0.0.1'),
(1135, '2025-04-21 18:47:21.011672', '127.0.0.1'),
(1136, '2025-04-21 18:47:21.254049', '127.0.0.1'),
(1137, '2025-04-21 18:47:21.260995', '127.0.0.1'),
(1138, '2025-04-21 18:47:23.892848', '127.0.0.1'),
(1139, '2025-04-21 18:47:23.894099', '127.0.0.1'),
(1140, '2025-04-21 18:47:24.178979', '127.0.0.1'),
(1141, '2025-04-21 18:47:24.189757', '127.0.0.1'),
(1142, '2025-04-21 18:47:32.625811', '127.0.0.1'),
(1143, '2025-04-21 18:47:32.628247', '127.0.0.1'),
(1144, '2025-04-21 18:47:32.866102', '127.0.0.1'),
(1145, '2025-04-21 18:47:32.866760', '127.0.0.1'),
(1146, '2025-04-21 18:47:34.095086', '127.0.0.1'),
(1147, '2025-04-21 18:47:34.096749', '127.0.0.1'),
(1148, '2025-04-21 18:47:34.661446', '127.0.0.1'),
(1149, '2025-04-21 18:47:34.666130', '127.0.0.1'),
(1150, '2025-04-21 18:47:40.461328', '127.0.0.1'),
(1151, '2025-04-21 18:47:40.462835', '127.0.0.1'),
(1152, '2025-04-21 18:47:40.820467', '127.0.0.1'),
(1153, '2025-04-21 18:47:40.825523', '127.0.0.1'),
(1154, '2025-04-21 18:47:44.846340', '127.0.0.1'),
(1155, '2025-04-21 18:47:44.846579', '127.0.0.1'),
(1156, '2025-04-21 18:47:45.096080', '127.0.0.1'),
(1157, '2025-04-21 18:47:45.108482', '127.0.0.1'),
(1158, '2025-04-21 18:47:45.831506', '127.0.0.1'),
(1159, '2025-04-21 18:47:45.837123', '127.0.0.1'),
(1160, '2025-04-21 18:47:46.800809', '127.0.0.1'),
(1161, '2025-04-21 18:47:46.807160', '127.0.0.1'),
(1162, '2025-04-21 18:48:04.005680', '127.0.0.1'),
(1163, '2025-04-21 18:48:04.011895', '127.0.0.1'),
(1164, '2025-04-21 18:48:04.409219', '127.0.0.1'),
(1165, '2025-04-21 18:48:04.410145', '127.0.0.1'),
(1166, '2025-04-21 18:48:09.993358', '127.0.0.1'),
(1167, '2025-04-21 18:48:09.996472', '127.0.0.1'),
(1168, '2025-04-21 18:48:10.254378', '127.0.0.1'),
(1169, '2025-04-21 18:48:10.267806', '127.0.0.1'),
(1170, '2025-04-21 18:48:12.525899', '127.0.0.1'),
(1171, '2025-04-21 18:48:12.527777', '127.0.0.1'),
(1172, '2025-04-21 18:48:12.834196', '127.0.0.1'),
(1173, '2025-04-21 18:48:12.849131', '127.0.0.1'),
(1174, '2025-04-21 18:48:21.388869', '127.0.0.1'),
(1175, '2025-04-21 18:48:21.389420', '127.0.0.1'),
(1176, '2025-04-21 18:48:21.741523', '127.0.0.1'),
(1177, '2025-04-21 18:48:21.744155', '127.0.0.1'),
(1178, '2025-04-21 18:48:22.660466', '127.0.0.1'),
(1179, '2025-04-21 18:48:22.661226', '127.0.0.1'),
(1180, '2025-04-21 18:48:23.692144', '127.0.0.1'),
(1181, '2025-04-21 18:48:23.722937', '127.0.0.1'),
(1182, '2025-04-21 18:48:26.333840', '127.0.0.1'),
(1183, '2025-04-21 18:48:26.337003', '127.0.0.1'),
(1184, '2025-04-21 18:48:26.561741', '127.0.0.1'),
(1185, '2025-04-21 18:48:26.567571', '127.0.0.1'),
(1186, '2025-04-21 18:48:29.941099', '127.0.0.1'),
(1187, '2025-04-21 18:48:29.941618', '127.0.0.1'),
(1188, '2025-04-21 18:48:30.251807', '127.0.0.1'),
(1189, '2025-04-21 18:48:30.272905', '127.0.0.1'),
(1190, '2025-04-21 18:48:31.689121', '127.0.0.1'),
(1191, '2025-04-21 18:48:31.690487', '127.0.0.1'),
(1192, '2025-04-21 18:48:32.044498', '127.0.0.1'),
(1193, '2025-04-21 18:48:32.061261', '127.0.0.1'),
(1194, '2025-04-21 19:10:02.239590', '127.0.0.1'),
(1195, '2025-04-21 19:10:02.254478', '127.0.0.1'),
(1196, '2025-04-21 19:11:13.564808', '127.0.0.1'),
(1197, '2025-04-21 19:11:13.569592', '127.0.0.1'),
(1198, '2025-04-21 19:11:28.538277', '127.0.0.1'),
(1199, '2025-04-21 19:11:28.542460', '127.0.0.1'),
(1200, '2025-04-21 19:12:37.637883', '127.0.0.1'),
(1201, '2025-04-21 19:12:37.659809', '127.0.0.1'),
(1202, '2025-04-21 19:23:16.989443', '127.0.0.1'),
(1203, '2025-04-21 19:23:16.993421', '127.0.0.1'),
(1204, '2025-04-21 19:45:24.991918', '127.0.0.1'),
(1205, '2025-04-21 19:45:25.100006', '127.0.0.1'),
(1206, '2025-04-21 19:45:26.019897', '127.0.0.1'),
(1207, '2025-04-21 19:45:26.474808', '127.0.0.1'),
(1208, '2025-04-21 19:45:38.280476', '127.0.0.1'),
(1209, '2025-04-21 19:45:38.276393', '127.0.0.1'),
(1210, '2025-04-21 19:47:12.562817', '127.0.0.1'),
(1211, '2025-04-21 19:47:14.824398', '127.0.0.1'),
(1212, '2025-04-21 19:47:21.353449', '127.0.0.1'),
(1213, '2025-04-21 19:47:21.340575', '127.0.0.1'),
(1214, '2025-04-21 19:53:45.972994', '127.0.0.1'),
(1215, '2025-04-21 19:54:31.115445', '127.0.0.1'),
(1216, '2025-04-21 19:54:31.120565', '127.0.0.1'),
(1217, '2025-04-21 19:55:54.859573', '127.0.0.1'),
(1218, '2025-04-21 19:55:54.863930', '127.0.0.1'),
(1219, '2025-04-21 19:56:36.026092', '127.0.0.1'),
(1220, '2025-04-21 19:56:36.024412', '127.0.0.1'),
(1221, '2025-04-21 19:59:43.371784', '127.0.0.1'),
(1222, '2025-04-21 19:59:43.378911', '127.0.0.1'),
(1223, '2025-04-21 20:14:04.656151', '127.0.0.1'),
(1224, '2025-04-21 20:14:04.666515', '127.0.0.1'),
(1225, '2025-04-22 05:55:48.598587', '127.0.0.1'),
(1226, '2025-04-22 05:55:48.981086', '127.0.0.1'),
(1227, '2025-04-22 06:20:13.202502', '127.0.0.1'),
(1228, '2025-04-22 06:20:13.205686', '127.0.0.1'),
(1229, '2025-04-22 06:50:33.808413', '127.0.0.1'),
(1230, '2025-04-22 06:50:33.942733', '127.0.0.1'),
(1231, '2025-04-22 06:50:34.145980', '127.0.0.1'),
(1232, '2025-04-22 06:50:35.283005', '127.0.0.1'),
(1233, '2025-04-22 06:50:35.413588', '127.0.0.1'),
(1234, '2025-04-22 06:50:36.059958', '127.0.0.1'),
(1235, '2025-04-22 07:13:50.127355', '127.0.0.1'),
(1236, '2025-04-22 07:13:50.188733', '127.0.0.1'),
(1237, '2025-04-22 07:17:45.466418', '127.0.0.1'),
(1238, '2025-04-22 07:17:45.805654', '127.0.0.1'),
(1239, '2025-04-22 07:27:17.588874', '127.0.0.1'),
(1240, '2025-04-22 07:27:17.854773', '127.0.0.1'),
(1241, '2025-04-22 07:29:14.248431', '127.0.0.1'),
(1242, '2025-04-22 07:29:14.254884', '127.0.0.1'),
(1243, '2025-04-22 07:31:42.364520', '127.0.0.1'),
(1244, '2025-04-22 07:31:42.367963', '127.0.0.1'),
(1245, '2025-04-22 07:33:44.721150', '127.0.0.1'),
(1246, '2025-04-22 07:33:44.734526', '127.0.0.1'),
(1247, '2025-04-22 07:33:44.738051', '127.0.0.1'),
(1248, '2025-04-22 07:33:45.061635', '127.0.0.1'),
(1249, '2025-04-22 07:34:29.632830', '127.0.0.1'),
(1250, '2025-04-22 07:35:16.932521', '127.0.0.1'),
(1251, '2025-04-22 07:35:16.954089', '127.0.0.1'),
(1252, '2025-04-22 07:36:54.751520', '127.0.0.1'),
(1253, '2025-04-22 07:36:54.760595', '127.0.0.1'),
(1254, '2025-04-22 07:36:54.765396', '127.0.0.1'),
(1255, '2025-04-22 07:36:55.133851', '127.0.0.1'),
(1256, '2025-04-22 07:37:49.112547', '127.0.0.1'),
(1257, '2025-04-22 07:37:49.115993', '127.0.0.1'),
(1258, '2025-04-22 07:37:49.468355', '127.0.0.1'),
(1259, '2025-04-22 07:37:49.472072', '127.0.0.1'),
(1260, '2025-04-22 07:37:50.106765', '127.0.0.1'),
(1261, '2025-04-22 07:37:50.116349', '127.0.0.1'),
(1262, '2025-04-22 07:42:06.734404', '127.0.0.1'),
(1263, '2025-04-22 07:42:06.742185', '127.0.0.1'),
(1264, '2025-04-22 07:43:43.142550', '127.0.0.1'),
(1265, '2025-04-22 07:43:43.146381', '127.0.0.1'),
(1266, '2025-04-22 07:46:42.215874', '127.0.0.1'),
(1267, '2025-04-22 07:46:42.219489', '127.0.0.1'),
(1268, '2025-04-22 07:54:06.488767', '127.0.0.1'),
(1269, '2025-04-22 07:54:06.492454', '127.0.0.1'),
(1270, '2025-04-22 07:54:15.227991', '127.0.0.1'),
(1271, '2025-04-22 07:54:15.235765', '127.0.0.1'),
(1272, '2025-04-22 07:58:35.692413', '127.0.0.1'),
(1273, '2025-04-22 07:58:35.696370', '127.0.0.1'),
(1274, '2025-04-22 08:00:36.920173', '127.0.0.1'),
(1275, '2025-04-22 08:00:37.170278', '127.0.0.1'),
(1276, '2025-04-22 08:02:19.452809', '127.0.0.1'),
(1277, '2025-04-22 08:02:19.459135', '127.0.0.1'),
(1278, '2025-04-22 08:05:01.552577', '127.0.0.1'),
(1279, '2025-04-22 08:05:01.570579', '127.0.0.1'),
(1280, '2025-04-22 08:05:07.936679', '127.0.0.1'),
(1281, '2025-04-22 08:05:07.945015', '127.0.0.1'),
(1282, '2025-04-22 08:05:16.534449', '127.0.0.1'),
(1283, '2025-04-22 08:05:16.537800', '127.0.0.1'),
(1284, '2025-04-22 08:05:49.868112', '127.0.0.1'),
(1285, '2025-04-22 08:05:49.872540', '127.0.0.1'),
(1286, '2025-04-22 08:05:56.186781', '127.0.0.1'),
(1287, '2025-04-22 08:05:56.196831', '127.0.0.1'),
(1288, '2025-04-22 08:06:57.456465', '127.0.0.1'),
(1289, '2025-04-22 08:06:57.462736', '127.0.0.1'),
(1290, '2025-04-22 08:12:32.615548', '127.0.0.1'),
(1291, '2025-04-22 08:12:32.623885', '127.0.0.1'),
(1292, '2025-04-22 08:14:21.993700', '127.0.0.1'),
(1293, '2025-04-22 08:14:32.016525', '127.0.0.1'),
(1294, '2025-04-22 08:14:51.538306', '127.0.0.1'),
(1295, '2025-04-22 08:15:24.852746', '127.0.0.1'),
(1296, '2025-04-22 08:15:37.816574', '127.0.0.1'),
(1297, '2025-04-22 09:07:13.733546', '127.0.0.1'),
(1298, '2025-04-22 09:09:19.532478', '127.0.0.1'),
(1299, '2025-04-22 09:09:19.537640', '127.0.0.1'),
(1300, '2025-04-22 09:37:02.811810', '127.0.0.1'),
(1301, '2025-04-22 09:37:02.927697', '127.0.0.1'),
(1302, '2025-04-22 09:37:05.237741', '127.0.0.1'),
(1303, '2025-04-22 09:37:05.241552', '127.0.0.1'),
(1304, '2025-04-22 09:37:06.373038', '127.0.0.1'),
(1305, '2025-04-22 09:37:06.761180', '127.0.0.1'),
(1306, '2025-04-22 09:37:15.947415', '127.0.0.1'),
(1307, '2025-04-22 09:37:15.977652', '127.0.0.1'),
(1308, '2025-04-22 09:37:27.334079', '127.0.0.1'),
(1309, '2025-04-22 09:37:27.347532', '127.0.0.1'),
(1310, '2025-04-22 09:37:35.870860', '127.0.0.1'),
(1311, '2025-04-22 09:37:35.874156', '127.0.0.1'),
(1312, '2025-04-22 09:38:07.974210', '127.0.0.1'),
(1313, '2025-04-22 09:38:07.977388', '127.0.0.1'),
(1314, '2025-04-22 09:38:11.721398', '127.0.0.1'),
(1315, '2025-04-22 09:38:11.726479', '127.0.0.1'),
(1316, '2025-04-22 09:40:39.587482', '127.0.0.1'),
(1317, '2025-04-22 09:40:39.593432', '127.0.0.1'),
(1318, '2025-04-22 09:40:39.598981', '127.0.0.1'),
(1319, '2025-04-22 09:40:39.923951', '127.0.0.1'),
(1320, '2025-04-22 09:45:00.073269', '127.0.0.1'),
(1321, '2025-04-22 09:45:00.082212', '127.0.0.1'),
(1322, '2025-04-22 09:45:00.234999', '127.0.0.1'),
(1323, '2025-04-22 09:45:00.369740', '127.0.0.1'),
(1324, '2025-04-22 09:45:14.501146', '127.0.0.1'),
(1325, '2025-04-22 09:45:14.509007', '127.0.0.1'),
(1326, '2025-04-22 09:46:40.165659', '127.0.0.1'),
(1327, '2025-04-22 09:46:40.171256', '127.0.0.1'),
(1328, '2025-04-22 09:48:50.277061', '127.0.0.1'),
(1329, '2025-04-22 09:48:50.285071', '127.0.0.1'),
(1330, '2025-04-22 09:48:50.524084', '127.0.0.1'),
(1331, '2025-04-22 09:48:50.576537', '127.0.0.1'),
(1332, '2025-04-22 09:48:51.298306', '127.0.0.1'),
(1333, '2025-04-22 09:48:51.351283', '127.0.0.1'),
(1334, '2025-04-22 09:49:13.858671', '127.0.0.1'),
(1335, '2025-04-22 09:49:14.178444', '127.0.0.1'),
(1336, '2025-04-22 09:49:14.187535', '127.0.0.1'),
(1337, '2025-04-22 09:49:14.873945', '127.0.0.1'),
(1338, '2025-04-22 09:49:14.916201', '127.0.0.1'),
(1339, '2025-04-22 09:51:30.982821', '127.0.0.1'),
(1340, '2025-04-22 09:53:01.378752', '127.0.0.1'),
(1341, '2025-04-22 09:55:23.528225', '127.0.0.1'),
(1342, '2025-04-22 12:01:38.610816', '127.0.0.1'),
(1343, '2025-04-22 12:06:14.487404', '127.0.0.1'),
(1344, '2025-04-22 12:06:20.983486', '127.0.0.1'),
(1345, '2025-04-22 12:06:25.294806', '127.0.0.1'),
(1346, '2025-04-22 12:07:20.565252', '127.0.0.1'),
(1347, '2025-04-22 12:07:20.568391', '127.0.0.1'),
(1348, '2025-04-22 12:09:49.654227', '127.0.0.1'),
(1349, '2025-04-22 12:09:55.966275', '127.0.0.1'),
(1350, '2025-04-22 12:12:57.671966', '127.0.0.1'),
(1351, '2025-04-22 12:12:57.714345', '127.0.0.1'),
(1352, '2025-04-22 12:13:58.877438', '127.0.0.1'),
(1353, '2025-04-22 12:13:58.881413', '127.0.0.1'),
(1354, '2025-04-22 12:14:00.695650', '127.0.0.1'),
(1355, '2025-04-22 12:14:00.710875', '127.0.0.1'),
(1356, '2025-04-22 12:15:28.894095', '127.0.0.1'),
(1357, '2025-04-22 12:15:29.221217', '127.0.0.1'),
(1358, '2025-04-22 12:15:37.457458', '127.0.0.1'),
(1359, '2025-04-22 12:15:37.462047', '127.0.0.1'),
(1360, '2025-04-22 12:17:59.978660', '127.0.0.1'),
(1361, '2025-04-22 12:17:59.982099', '127.0.0.1'),
(1362, '2025-04-22 12:18:05.403700', '127.0.0.1'),
(1363, '2025-04-22 12:18:05.407104', '127.0.0.1'),
(1364, '2025-04-22 12:19:09.550116', '127.0.0.1'),
(1365, '2025-04-22 12:19:09.553085', '127.0.0.1'),
(1366, '2025-04-22 12:19:11.343041', '127.0.0.1'),
(1367, '2025-04-22 12:19:11.360559', '127.0.0.1'),
(1368, '2025-04-22 12:19:13.616723', '127.0.0.1'),
(1369, '2025-04-22 12:19:13.623344', '127.0.0.1'),
(1370, '2025-04-22 12:20:18.395585', '127.0.0.1'),
(1371, '2025-04-22 12:20:18.402737', '127.0.0.1'),
(1372, '2025-04-22 12:20:18.409421', '127.0.0.1'),
(1373, '2025-04-22 12:20:18.412313', '127.0.0.1'),
(1374, '2025-04-22 12:20:19.401592', '127.0.0.1'),
(1375, '2025-04-22 12:20:20.130436', '127.0.0.1'),
(1376, '2025-04-22 12:20:20.510652', '127.0.0.1'),
(1377, '2025-04-22 12:20:20.514496', '127.0.0.1'),
(1378, '2025-04-22 12:20:25.101840', '127.0.0.1'),
(1379, '2025-04-22 12:20:25.104801', '127.0.0.1'),
(1380, '2025-04-22 12:21:47.599291', '127.0.0.1'),
(1381, '2025-04-22 12:21:47.603219', '127.0.0.1'),
(1382, '2025-04-22 12:23:36.057393', '127.0.0.1'),
(1383, '2025-04-22 12:23:36.161980', '127.0.0.1'),
(1384, '2025-04-22 12:25:14.121793', '127.0.0.1'),
(1385, '2025-04-22 12:25:14.259589', '127.0.0.1'),
(1386, '2025-04-22 12:25:15.001364', '127.0.0.1'),
(1387, '2025-04-22 12:25:15.011267', '127.0.0.1'),
(1388, '2025-04-22 12:25:18.162073', '127.0.0.1'),
(1389, '2025-04-22 12:25:18.165818', '127.0.0.1'),
(1390, '2025-04-22 12:32:47.238543', '127.0.0.1'),
(1391, '2025-04-22 12:32:47.246219', '127.0.0.1'),
(1392, '2025-04-22 12:32:57.583035', '127.0.0.1'),
(1393, '2025-04-22 12:32:57.587000', '127.0.0.1'),
(1394, '2025-04-22 12:33:14.300674', '127.0.0.1'),
(1395, '2025-04-22 12:33:14.303965', '127.0.0.1'),
(1396, '2025-04-22 15:27:38.957406', '127.0.0.1'),
(1397, '2025-04-22 15:30:38.693068', '127.0.0.1'),
(1398, '2025-04-22 15:30:40.695842', '127.0.0.1'),
(1399, '2025-04-22 15:30:44.750147', '127.0.0.1'),
(1400, '2025-04-23 14:54:07.217564', '127.0.0.1'),
(1401, '2025-04-24 09:51:56.408185', '127.0.0.1'),
(1402, '2025-04-24 16:30:21.023397', '127.0.0.1'),
(1403, '2025-04-25 07:13:12.711838', '127.0.0.1'),
(1404, '2025-04-25 09:48:47.279449', '127.0.0.1'),
(1405, '2025-04-26 10:33:10.618775', '127.0.0.1'),
(1406, '2025-04-26 10:37:56.741753', '127.0.0.1'),
(1407, '2025-04-26 10:55:32.942692', '127.0.0.1'),
(1408, '2025-04-27 00:20:18.921109', '127.0.0.1'),
(1409, '2025-04-27 00:20:19.513903', '127.0.0.1'),
(1410, '2025-04-29 09:08:11.473475', '172.17.0.1'),
(1411, '2025-04-29 09:08:11.640986', '172.17.0.1'),
(1412, '2025-04-29 09:08:28.845549', '172.17.0.1'),
(1413, '2025-04-29 09:08:29.320148', '172.17.0.1'),
(1414, '2025-04-29 09:08:30.372895', '172.17.0.1'),
(1415, '2025-04-29 09:08:31.458284', '172.17.0.1'),
(1416, '2025-04-29 09:40:20.900588', '172.17.0.1'),
(1417, '2025-04-30 10:03:29.731172', '172.17.0.1'),
(1418, '2025-04-30 10:03:39.402540', '172.17.0.1'),
(1419, '2025-05-01 07:42:27.490714', '172.17.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(7, 'authtoken', 'token'),
(8, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(20, 'core', 'award'),
(18, 'core', 'competence'),
(10, 'core', 'education'),
(14, 'core', 'email'),
(15, 'core', 'emailresponse'),
(11, 'core', 'experience'),
(24, 'core', 'facebook'),
(19, 'core', 'formation'),
(16, 'core', 'historicmail'),
(12, 'core', 'imageprojet'),
(17, 'core', 'langue'),
(22, 'core', 'notification'),
(9, 'core', 'profile'),
(13, 'core', 'projet'),
(21, 'core', 'rating'),
(23, 'core', 'visit'),
(6, 'sessions', 'session'),
(25, 'token_blacklist', 'blacklistedtoken'),
(26, 'token_blacklist', 'outstandingtoken');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-02-24 08:13:53.198939'),
(2, 'auth', '0001_initial', '2025-02-24 08:13:53.307849'),
(3, 'admin', '0001_initial', '2025-02-24 08:13:53.364174'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-02-24 08:13:53.372017'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-02-24 08:13:53.377523'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-02-24 08:13:53.401850'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-02-24 08:13:53.417061'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-02-24 08:13:53.428670'),
(9, 'auth', '0004_alter_user_username_opts', '2025-02-24 08:13:53.436402'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-02-24 08:13:53.455816'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-02-24 08:13:53.456928'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-02-24 08:13:53.463973'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-02-24 08:13:53.478165'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-02-24 08:13:53.489508'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-02-24 08:13:53.498117'),
(16, 'auth', '0011_update_proxy_permissions', '2025-02-24 08:13:53.503861'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-02-24 08:13:53.513332'),
(18, 'authtoken', '0001_initial', '2025-02-24 08:13:53.531185'),
(19, 'authtoken', '0002_auto_20160226_1747', '2025-02-24 08:13:53.551329'),
(20, 'authtoken', '0003_tokenproxy', '2025-02-24 08:13:53.554320'),
(21, 'authtoken', '0004_alter_tokenproxy_options', '2025-02-24 08:13:53.557079'),
(22, 'core', '0001_initial', '2025-02-24 08:13:53.575316'),
(23, 'core', '0002_education', '2025-02-24 08:13:53.580412'),
(24, 'core', '0003_experience', '2025-02-24 08:13:53.585737'),
(25, 'core', '0004_imageprojet_projet_imageprojet_projet', '2025-02-24 08:13:53.625841'),
(26, 'core', '0005_email', '2025-02-24 08:13:53.631206'),
(27, 'core', '0006_emailresponse', '2025-02-24 08:13:53.644999'),
(28, 'core', '0007_historicmail', '2025-02-24 08:13:53.656594'),
(29, 'core', '0008_langue', '2025-02-24 08:13:53.667793'),
(30, 'core', '0009_competence', '2025-02-24 08:13:53.674882'),
(31, 'core', '0010_remove_projet_images', '2025-02-24 08:13:53.735411'),
(32, 'core', '0011_formation', '2025-02-24 08:13:53.742723'),
(33, 'core', '0012_notation', '2025-02-24 08:13:53.759341'),
(34, 'core', '0013_email_date_email_heure_emailresponse_date_and_more', '2025-02-24 08:13:53.798754'),
(35, 'core', '0014_award', '2025-02-24 08:13:53.804586'),
(36, 'core', '0015_rating_delete_notation', '2025-02-24 08:13:53.842510'),
(37, 'core', '0016_notification', '2025-02-24 08:13:53.863467'),
(38, 'core', '0017_profile_link_github', '2025-02-24 08:13:53.874971'),
(39, 'core', '0018_competence_categorie', '2025-02-24 08:13:53.879923'),
(40, 'core', '0019_visit', '2025-02-24 08:13:53.884058'),
(41, 'core', '0020_facebook_alter_competence_image', '2025-02-24 08:13:53.890269'),
(42, 'core', '0021_alter_facebook_email', '2025-02-24 08:13:55.746738'),
(43, 'core', '0022_projet_githublink_projet_projetlink', '2025-02-24 08:13:55.763016'),
(44, 'core', '0023_auto_20250131_0902', '2025-02-24 08:13:56.103136'),
(45, 'core', '0024_alter_competence_image', '2025-02-24 08:13:56.106108'),
(46, 'sessions', '0001_initial', '2025-02-24 08:13:56.120306'),
(47, 'token_blacklist', '0001_initial', '2025-02-24 08:13:56.177813'),
(48, 'token_blacklist', '0002_outstandingtoken_jti_hex', '2025-02-24 08:13:56.197182'),
(49, 'token_blacklist', '0003_auto_20171017_2007', '2025-02-24 08:13:56.220457'),
(50, 'token_blacklist', '0004_auto_20171017_2013', '2025-02-24 08:13:56.246737'),
(51, 'token_blacklist', '0005_remove_outstandingtoken_jti', '2025-02-24 08:13:56.429447'),
(52, 'token_blacklist', '0006_auto_20171017_2113', '2025-02-24 08:13:56.446741'),
(53, 'token_blacklist', '0007_auto_20171017_2214', '2025-02-24 08:13:56.595870'),
(54, 'token_blacklist', '0008_migrate_to_bigautofield', '2025-02-24 08:13:56.791202'),
(55, 'token_blacklist', '0010_fix_migrate_to_bigautofield', '2025-02-24 08:13:56.806738'),
(56, 'token_blacklist', '0011_linearizes_history', '2025-02-24 08:13:56.807954'),
(57, 'token_blacklist', '0012_alter_outstandingtoken_user', '2025-02-24 08:13:56.818948');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `token_blacklist_blacklistedtoken`
--

CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint(20) NOT NULL,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `token_blacklist_outstandingtoken`
--

CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint(20) NOT NULL,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `jti` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `token_blacklist_outstandingtoken`
--

INSERT INTO `token_blacklist_outstandingtoken` (`id`, `token`, `created_at`, `expires_at`, `user_id`, `jti`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDk4OTc1NSwiaWF0IjoxNzQwMzg0OTU1LCJqdGkiOiIyOTMwODQzYWRkMzI0ODNlODg4MDZmYzE0MzUwNWMyYyIsInVzZXJfaWQiOjF9.1YLMyGvZdW8bTb0SYCUi1xrmC1df5bdC2UTGpb7xw_g', '2025-02-24 08:15:55.025211', '2025-03-03 08:15:55.000000', 1, '2930843add32483e88806fc143505c2c'),
(2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA4OTIxNCwiaWF0IjoxNzQwNDg0NDE0LCJqdGkiOiJhMzdkZjU3YWJiYTY0MzNmYWRlYjNiMzA1MTQwMTk0ZCIsInVzZXJfaWQiOjF9.mE8OX-EpLKeTGGQ6P6sBzK1jzo8Nb6uqRqeADLZMtuU', '2025-02-25 11:53:34.263689', '2025-03-04 11:53:34.000000', 1, 'a37df57abba6433fadeb3b305140194d'),
(3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5MDQ2NSwiaWF0IjoxNzQwNDg1NjY1LCJqdGkiOiIxZjhiOGMwYjM5NWM0ZGNhODgyMTcyODQ0ZGYwMGE1OSIsInVzZXJfaWQiOjF9.p-FYeIKCO08JxENGmUDvSmDZ6hRJ0Z8iaUU3BcBVp3o', '2025-02-25 12:14:25.655850', '2025-03-04 12:14:25.000000', 1, '1f8b8c0b395c4dca882172844df00a59'),
(4, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5MzA1NSwiaWF0IjoxNzQwNDg4MjU1LCJqdGkiOiI2NWJhYzZiMzY0NTk0M2E3YmY2NTE1Njg3NjQ3YTljZCIsInVzZXJfaWQiOjF9.89yoZrC5aEyUF8AOJaqEryLbXZ6JE18HjSnV_nn6dEM', '2025-02-25 12:57:35.961172', '2025-03-04 12:57:35.000000', 1, '65bac6b3645943a7bf6515687647a9cd'),
(5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTA5MzUyOCwiaWF0IjoxNzQwNDg4NzI4LCJqdGkiOiIxYTM0MjI3MDE2NDY0MWY5OTNlNjc5YjE2ODQ4OTIzZiIsInVzZXJfaWQiOjF9.JqjOSbUuYhIuRslG1vCDriXhbxObh5rvGNq_cH3OIaI', '2025-02-25 13:05:28.358099', '2025-03-04 13:05:28.000000', 1, '1a342270164641f993e679b16848923f'),
(6, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE3MTE3OCwiaWF0IjoxNzQwNTY2Mzc4LCJqdGkiOiI3MTg5NzU2MjEwMWI0NTlmYmIwODhiOTg1YTQyYzU0NiIsInVzZXJfaWQiOjF9.mkReXGlBLprP2bqb2QLdm6hR9H4M7CiR6wiQndgefi8', '2025-02-26 10:39:38.615580', '2025-03-05 10:39:38.000000', 1, '71897562101b459fbb088b985a42c546'),
(7, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE3Mjg3NCwiaWF0IjoxNzQwNTY4MDc0LCJqdGkiOiI2YzBjYjFiMmZiNmQ0M2RhYTQyMTlkZDAzMDkxYjZkYSIsInVzZXJfaWQiOjF9.wHdizZtBQvRdtiFZu9_VI2rlsJXDT8SbTDaIjuGNnc0', '2025-02-26 11:07:54.545954', '2025-03-05 11:07:54.000000', 1, '6c0cb1b2fb6d43daa4219dd03091b6da'),
(8, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE3MzUwMCwiaWF0IjoxNzQwNTY4NzAwLCJqdGkiOiI5ZDAyMGM2NmU3ODc0ZGI5OTI2MWE4MjUzM2E3YTc5NSIsInVzZXJfaWQiOjF9.X7IkvqFCTJwwxwzXLBlrmD5V4hPDNNQd1i9RN0nWrJU', '2025-02-26 11:18:20.070045', '2025-03-05 11:18:20.000000', 1, '9d020c66e7874db99261a82533a7a795'),
(9, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE3NDQwNSwiaWF0IjoxNzQwNTY5NjA1LCJqdGkiOiIwYmQzZTA0OGQ0ZmE0YjM1OGJlMGI0MmNlZDVmOTI1MyIsInVzZXJfaWQiOjF9.QBn3WoMIUOl4X8pLVtmbg7NVgusS45PaMfERJMYQWHc', '2025-02-26 11:33:25.136481', '2025-03-05 11:33:25.000000', 1, '0bd3e048d4fa4b358be0b42ced5f9253'),
(10, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE3NzIyNiwiaWF0IjoxNzQwNTcyNDI2LCJqdGkiOiJhNjBlMWVjNmM4YTM0ZDdkYjk1YjdmZmEwNzNiMmE4YiIsInVzZXJfaWQiOjF9.9EpH58AX2LRvqHiIPyLJVcgSS8AbcxlkyrvqnSjn4hs', '2025-02-26 12:20:26.651523', '2025-03-05 12:20:26.000000', 1, 'a60e1ec6c8a34d7db95b7ffa073b2a8b'),
(11, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTE4MTIxMCwiaWF0IjoxNzQwNTc2NDEwLCJqdGkiOiIzZjAwODE5YjdkMDc0ZDIyYTRlN2E3MDMzZDVhNjEwNyIsInVzZXJfaWQiOjF9.9I_8siEDYfmRCV0J38IZdT7Q8NpCjqs3AzKWe7l1vCk', '2025-02-26 13:26:50.614323', '2025-03-05 13:26:50.000000', 1, '3f00819b7d074d22a4e7a7033d5a6107'),
(12, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTI2MzM4MiwiaWF0IjoxNzQwNjU4NTgyLCJqdGkiOiI0YjMzNmZiMDViODY0Zjg2YWE4MGJlZTIzZmFhMTViYiIsInVzZXJfaWQiOjF9.uHCkE5om49U8xsblme3yA6HdVUQvN3-ju3XAo-FU4A4', '2025-02-27 12:16:22.120774', '2025-03-06 12:16:22.000000', 1, '4b336fb05b864f86aa80bee23faa15bb'),
(13, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTQxNzgwMCwiaWF0IjoxNzQwODEzMDAwLCJqdGkiOiIyYmE1MjljOGZhMTM0YzdmYmFmMmI3MWU1OWZhZjE2YSIsInVzZXJfaWQiOjF9.SzdPgzUSAmEWgcQGz54KXs13LorAvBjU2NrRI_dttH4', '2025-03-01 07:10:00.947706', '2025-03-08 07:10:00.000000', 1, '2ba529c8fa134c7fbaf2b71e59faf16a'),
(14, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjE5OTQ0OSwiaWF0IjoxNzQxNTk0NjQ5LCJqdGkiOiI4MWQ5ZDc3ZTkyNTg0Yzg2YmIxNTAxNzk1MDUwZjgyZCIsInVzZXJfaWQiOjF9.WpyPhgbRQI_fMzb1hTdzfcrqEqXLZs11vHnvgo0guSk', '2025-03-10 08:17:29.609988', '2025-03-17 08:17:29.000000', 1, '81d9d77e92584c86bb1501795050f82d'),
(15, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjIwNDA0MywiaWF0IjoxNzQxNTk5MjQzLCJqdGkiOiI4YmJjOTk3YmE2MDQ0MzI0OGVlZTljMGQ4NjU5OWI2ZiIsInVzZXJfaWQiOjF9.v-eKczuKirfHydDGcBxYEBZK9u9ZBhyzo9WByv_Dqb8', '2025-03-10 09:34:03.404704', '2025-03-17 09:34:03.000000', 1, '8bbc997ba60443248eee9c0d86599b6f'),
(16, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjUwMzM0OSwiaWF0IjoxNzQxODk4NTQ5LCJqdGkiOiI0YWNhYjhkZDBmMWQ0NDk3YWM4MjMyYmJmZWFiMWRjNSIsInVzZXJfaWQiOjF9.mg3Pb3o3v1r1jvWG6PPdRw0pyEgo9nL6uXH3RRicqxw', '2025-03-13 20:42:29.773909', '2025-03-20 20:42:29.000000', 1, '4acab8dd0f1d4497ac8232bbfeab1dc5'),
(17, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjU0OTMxMiwiaWF0IjoxNzQxOTQ0NTEyLCJqdGkiOiI4MWE2OTVhZjQ4YmE0NmRjYmZiODNjMzhiYTA3ODIyZiIsInVzZXJfaWQiOjF9.Y1CgZrC4kqEuTzaZbFXJain5JIRNnl3b-XtIT3m3_LE', '2025-03-14 09:28:32.751195', '2025-03-21 09:28:32.000000', 1, '81a695af48ba46dcbfb83c38ba07822f'),
(18, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjU0OTM0NSwiaWF0IjoxNzQxOTQ0NTQ1LCJqdGkiOiJjMmZhMzg0YjZiMTU0ODY2YjJmZjRmM2VhNjFlNTMzNyIsInVzZXJfaWQiOjF9.hQptHrd_zB0mqS4M9-IMmDtVGXB_uj76Sbe9hnQCjI8', '2025-03-14 09:29:05.652491', '2025-03-21 09:29:05.000000', 1, 'c2fa384b6b154866b2ff4f3ea61e5337'),
(19, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjgzNDY1NCwiaWF0IjoxNzQyMjI5ODU0LCJqdGkiOiIyNmM0NDFkYmUxM2M0NzZlYTBkN2EyNjRjYWE3ODQ1MiIsInVzZXJfaWQiOjF9.HUwzIYumyocqwwYF_auVEcA2W8OE6VwfcI4L8hX2euY', '2025-03-17 16:44:14.853633', '2025-03-24 16:44:14.000000', 1, '26c441dbe13c476ea0d7a264caa78452'),
(20, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzA2NDIxNCwiaWF0IjoxNzQyNDU5NDE0LCJqdGkiOiI3Y2Y1MmJmNTg0MGQ0M2QyODkzNzQ4MmRhMDg0YWNkNSIsInVzZXJfaWQiOjF9.5-CgWRIhyTMCYP7ntHVNSM2Cc3I5aS3wQQU4UkFxAwA', '2025-03-20 08:30:14.626268', '2025-03-27 08:30:14.000000', 1, '7cf52bf5840d43d28937482da084acd5'),
(21, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0Mzc1MDc4OSwiaWF0IjoxNzQzMTQ1OTg5LCJqdGkiOiI5Yjc2NWNmODVjYjg0ODRiODg4NTVhYmNiZjBhY2RiMiIsInVzZXJfaWQiOjF9.xd4hzTL5_4KPRlyR4mP0dyEmLCNV3_5jhCOlKEcjOJM', '2025-03-28 07:13:09.585753', '2025-04-04 07:13:09.000000', 1, '9b765cf85cb8484b88855abcbf0acdb2'),
(22, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzkxNjIwNSwiaWF0IjoxNzQzMzExNDA1LCJqdGkiOiJmMTgwZjJhNjRlMzE0ZjllYmJkZmRmN2Y5NmI4NmU0NiIsInVzZXJfaWQiOjF9.oW5Lvin7JbCFgLPsmr5cw8_K5wPFZ09iGuX5zzJCM7o', '2025-03-30 05:10:05.895379', '2025-04-06 05:10:05.000000', 1, 'f180f2a64e314f9ebbdfdf7f96b86e46'),
(23, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0Mzk3MjU1MywiaWF0IjoxNzQzMzY3NzUzLCJqdGkiOiJlYjQ2Nzc0NWZjMmM0MmZlYTUzNTNiNGVjZmFkOGU5ZSIsInVzZXJfaWQiOjF9.XuIu-4vn8DQJ2_NgQAkcIpC0OLrI9dRxbs7sHR5R-YA', '2025-03-30 20:49:13.597363', '2025-04-06 20:49:13.000000', 1, 'eb467745fc2c42fea5353b4ecfad8e9e'),
(24, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDEzMjc0MCwiaWF0IjoxNzQzNTI3OTQwLCJqdGkiOiJlMGRhMjQzOWNkNDQ0YWQ3ODk4MjI1MmQ4NTM4MDRmYyIsInVzZXJfaWQiOjF9._5iiLO3gmIir9AdvnvOkS4ivFxIiir9oiDsqIHt7wjA', '2025-04-01 17:19:00.688472', '2025-04-08 17:19:00.000000', 1, 'e0da2439cd444ad78982252d853804fc'),
(25, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDEzNzE5NiwiaWF0IjoxNzQzNTMyMzk2LCJqdGkiOiJlYjhlNjE0ZjkzODU0YTI1YjQ5YmFmMTFkNGEyYzlmMSIsInVzZXJfaWQiOjF9.vi9L7D5AoKNqGsmIckjwe1IWvq1hthm5R2OcfAKCidU', '2025-04-01 18:33:16.786986', '2025-04-08 18:33:16.000000', 1, 'eb8e614f93854a25b49baf11d4a2c9f1'),
(26, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDIxMjg2NywiaWF0IjoxNzQzNjA4MDY3LCJqdGkiOiJhZThlM2E4NTM3MGE0MzI0OWJkNmMyNWRlMmRiYjA1OSIsInVzZXJfaWQiOjF9.APKggaUVkqxEy4cTs7mOVXmwFO9JdRW8XOHTqS3lGHM', '2025-04-02 15:34:27.833642', '2025-04-09 15:34:27.000000', 1, 'ae8e3a85370a43249bd6c25de2dbb059'),
(27, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTU5MTQ0MCwiaWF0IjoxNzQ0OTg2NjQwLCJqdGkiOiJiOTVmMTI4MjIxZTA0NWY4YjQ1ZTNkNzVhZWZkMzE1NSIsInVzZXJfaWQiOjF9.DEme85buQacCGI6eO_7tIqHsKJ8D8TJ5k7HPZNLcZKA', '2025-04-18 14:30:40.820538', '2025-04-25 14:30:40.000000', 1, 'b95f128221e045f8b45e3d75aefd3155'),
(28, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTg0NDgwNSwiaWF0IjoxNzQ1MjQwMDA1LCJqdGkiOiI2ZGM1ZDBkMDE5MDY0ZDQyYjMzYjczM2NiMmExMDMxOSIsInVzZXJfaWQiOjF9.NffJH88r2Y3WkiCEon7_6hlyAjczYkryo4mlvr7A2GI', '2025-04-21 12:53:25.002967', '2025-04-28 12:53:25.000000', 1, '6dc5d0d019064d42b33b733cb2a10319'),
(29, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTg0Njc1NiwiaWF0IjoxNzQ1MjQxOTU2LCJqdGkiOiI4Mjg0OGZkMzMzMjE0ZTgyOWFhNTFiNTZjOGQzNTczZiIsInVzZXJfaWQiOjF9.LIs2PbT89oP8rDwgvjxlvzz9t-O2xPLLD9vLyB5BNaE', '2025-04-21 13:25:56.767776', '2025-04-28 13:25:56.000000', 1, '82848fd333214e829aa51b56c8d3573f'),
(30, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTg2ODI1NSwiaWF0IjoxNzQ1MjYzNDU1LCJqdGkiOiI1MGVmMGFkYzcwY2Q0ZDg3ODllNTJkZGFiZDU5NGJhYyIsInVzZXJfaWQiOjF9.WTf8XWzwIrRDA54kOD9yZS7VStB-DB0SAHzQH579yBU', '2025-04-21 19:24:15.940737', '2025-04-28 19:24:15.000000', 1, '50ef0adc70cd4d8789e52ddabd594bac'),
(31, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTkxMjI3NywiaWF0IjoxNzQ1MzA3NDc3LCJqdGkiOiJmZjIzZDNhYmNkNmM0MWViOTRmODFlNWZkNzFjNTc3MCIsInVzZXJfaWQiOjF9.lrql-jio5bDRc3A499sekTz_dugG60ZPvBti6KNEV60', '2025-04-22 07:37:57.288077', '2025-04-29 07:37:57.000000', 1, 'ff23d3abcd6c41eb94f81e5fd71c5770'),
(32, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjI2ODgzNCwiaWF0IjoxNzQ1NjY0MDM0LCJqdGkiOiIwOGM3ZTU4NjY4OTc0NTg0YWJmY2VhM2ZmNzk5OWFjOCIsInVzZXJfaWQiOjF9.rWY75eyJwgytJqDyX0-xzaqevCj0YDo_AnB5q5nf-9s', '2025-04-26 10:40:34.183256', '2025-05-03 10:40:34.000000', 1, '08c7e58668974584abfcea3ff7999ac8'),
(33, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjM3MTMwMywiaWF0IjoxNzQ1NzY2NTAzLCJqdGkiOiJlMWMzNzc3ZjQ1OWU0ODgwOTY4NDE5OGVkZDZmZjNjMiIsInVzZXJfaWQiOjF9.DhwPz2LPcauzmSSB70CRkfZcV7Vw7UD6U7dXVV1XZsc', '2025-04-27 15:08:23.204441', '2025-05-04 15:08:23.000000', 1, 'e1c3777f459e48809684198edd6ff3c2');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `core_award`
--
ALTER TABLE `core_award`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_competence`
--
ALTER TABLE `core_competence`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_education`
--
ALTER TABLE `core_education`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_email`
--
ALTER TABLE `core_email`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_emailresponse`
--
ALTER TABLE `core_emailresponse`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_emailresponse_email_id_b7007eb8_fk_core_email_id` (`email_id`);

--
-- Index pour la table `core_experience`
--
ALTER TABLE `core_experience`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_facebook`
--
ALTER TABLE `core_facebook`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_formation`
--
ALTER TABLE `core_formation`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_historicmail`
--
ALTER TABLE `core_historicmail`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_imageprojet`
--
ALTER TABLE `core_imageprojet`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_imageprojet_projet_id_2f8fd591_fk_core_projet_id` (`projet_id`);

--
-- Index pour la table `core_langue`
--
ALTER TABLE `core_langue`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_notification`
--
ALTER TABLE `core_notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_notification_user_id_6e341aac_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `core_profile`
--
ALTER TABLE `core_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Index pour la table `core_projet`
--
ALTER TABLE `core_projet`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `core_rating`
--
ALTER TABLE `core_rating`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_rating_project_id_ip_address_c8bc9667_uniq` (`project_id`,`ip_address`);

--
-- Index pour la table `core_visit`
--
ALTER TABLE `core_visit`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token_id` (`token_id`);

--
-- Index pour la table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  ADD KEY `token_blacklist_outs_user_id_83bc629a_fk_auth_user` (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `core_award`
--
ALTER TABLE `core_award`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `core_competence`
--
ALTER TABLE `core_competence`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT pour la table `core_education`
--
ALTER TABLE `core_education`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `core_email`
--
ALTER TABLE `core_email`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT pour la table `core_emailresponse`
--
ALTER TABLE `core_emailresponse`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `core_experience`
--
ALTER TABLE `core_experience`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `core_facebook`
--
ALTER TABLE `core_facebook`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `core_formation`
--
ALTER TABLE `core_formation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `core_historicmail`
--
ALTER TABLE `core_historicmail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `core_imageprojet`
--
ALTER TABLE `core_imageprojet`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `core_langue`
--
ALTER TABLE `core_langue`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `core_notification`
--
ALTER TABLE `core_notification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT pour la table `core_profile`
--
ALTER TABLE `core_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `core_projet`
--
ALTER TABLE `core_projet`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT pour la table `core_rating`
--
ALTER TABLE `core_rating`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `core_visit`
--
ALTER TABLE `core_visit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1420;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT pour la table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `core_emailresponse`
--
ALTER TABLE `core_emailresponse`
  ADD CONSTRAINT `core_emailresponse_email_id_b7007eb8_fk_core_email_id` FOREIGN KEY (`email_id`) REFERENCES `core_email` (`id`);

--
-- Contraintes pour la table `core_imageprojet`
--
ALTER TABLE `core_imageprojet`
  ADD CONSTRAINT `core_imageprojet_projet_id_2f8fd591_fk_core_projet_id` FOREIGN KEY (`projet_id`) REFERENCES `core_projet` (`id`);

--
-- Contraintes pour la table `core_notification`
--
ALTER TABLE `core_notification`
  ADD CONSTRAINT `core_notification_user_id_6e341aac_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `core_profile`
--
ALTER TABLE `core_profile`
  ADD CONSTRAINT `core_profile_user_id_bf8ada58_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`);

--
-- Contraintes pour la table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  ADD CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
