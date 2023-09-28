-- Удаление таблиц, если они существуют
-- Удаляем в порядке, обратном созданию, с учетом зависимостей
DROP TABLE IF EXISTS LiveCourses;
DROP TABLE IF EXISTS WebCourses;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Users;
-- Создание таблицы Users
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
-- Создание таблицы Teachers
CREATE TABLE Teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
-- Создание таблицы Students
CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
-- Создание таблицы Categories
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES Categories(id) ON DELETE
    SET NULL ON UPDATE CASCADE
);
-- Создание таблицы Courses
CREATE TABLE Courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    teacher_id INTEGER,
    url TEXT,
    location TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(id) ON DELETE
    SET NULL ON UPDATE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES Teachers(id) ON DELETE
    SET NULL ON UPDATE CASCADE
);