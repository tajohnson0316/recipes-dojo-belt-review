-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema recipes_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema recipes_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `recipes_db` DEFAULT CHARACTER SET utf8 ;
USE `recipes_db` ;

-- -----------------------------------------------------
-- Table `recipes_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recipes_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(144) NOT NULL,
  `password` VARCHAR(72) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recipes_db`.`recipes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recipes_db`.`recipes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(72) NOT NULL,
  `instructions` TEXT(10000) NOT NULL,
  `description` TEXT(10000) NOT NULL,
  `made_on` DATE NOT NULL,
  `under_30` VARCHAR(3) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recipes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_recipes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `recipes_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `recipes_db`.`favorites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `recipes_db`.`favorites` (
  `user_id` INT NOT NULL,
  `recipe_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `recipe_id`),
  INDEX `fk_users_has_recipes_recipes1_idx` (`recipe_id` ASC) VISIBLE,
  INDEX `fk_users_has_recipes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_recipes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `recipes_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_recipes_recipes1`
    FOREIGN KEY (`recipe_id`)
    REFERENCES `recipes_db`.`recipes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
