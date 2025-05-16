CREATE TABLE `fa_ptt` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `createtime` INT UNSIGNED NOT NULL,
    `updatetime` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;