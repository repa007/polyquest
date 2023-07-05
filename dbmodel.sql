CREATE TABLE `std_2064_polyquest`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(64) NOT NULL,
  `body` VARCHAR(2048) NOT NULL,
  `course` INT NOT NULL,
  `max` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE TABLE `std_2064_polyquest`.`students` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  `lastname` VARCHAR(64) NOT NULL,
  `group` VARCHAR(64) NOT NULL,
  `course` INT NOT NULL,
  PRIMARY KEY (`id`)),
  `tgname` VARCHAR(256) NOT NULL,
  INDEX (`tgname`)
ENGINE = InnoDB;


CREATE TABLE `std_2064_polyquest`.`taken` (
  `task_id` INT NOT NULL,
  `student_id` INT NOT NULL,
  PRIMARY KEY (`task_id`, `student_id`),
  INDEX `fk_tasks_has_Students_Students1_idx` (`student_id` ASC),
  INDEX `fk_tasks_has_Students_Tasks_idx` (`task_id` ASC),
  CONSTRAINT `fk_tasks_has_Students_Tasks`
    FOREIGN KEY (`task_id`)
    REFERENCES `std_2064_polyquest`.`tasks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tasks_has_Students_students1`
    FOREIGN KEY (`student_id`)
    REFERENCES `std_2064_polyquest`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE `std_2064_polyquest`.`admin` (
  `id` INT NOT NULL AUTO_INCREMENT , 
  `tgname` VARCHAR(256) NOT NULL , 
  PRIMARY KEY (`id`), 
  UNIQUE (`tgname`)) 
ENGINE = InnoDB;
