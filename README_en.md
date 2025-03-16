# Catalogue

- [Catalogue](#catalogue)
  - [Download link](#download-link)
  - [Function](#function)
  - [Program Structure](#program-structure)
  - [Introduction](#introduction)
  - [Installation and operation mode](#installation-and-operation-mode)
    - [Install Python library](#install-python-library)
    - [Run the program](#run-the-program)
      - [Method 1](#method-1)
      - [Method 2](#method-2)
  - [Precautions](#precautions)

**[English](README_en.md) | [简体中文](README.md)**

## Download link

[Click here to download](https://github.com/WorldDawnAres/bookstory-mysql/releases)

>This program is a simple book management program using MySQL. It is recommended to use MySQL-V8.0.36 version when using it
>
>Welcome to download and experience if you are interested

## Function

- [x] User management, user permission management
- [x] Library management: Add, delete, modify, and query functions
- [x] Book classification management
- [x] Inventory management and handling methods when inventory is insufficient
- [x] Book purchase process settings
- [x] Order Management

## Program Structure

```bash
bookstory-mysql
├── /bookstore
│   ├── icon.jpg
│   ├── __init__.py 
│   ├── config.py
│   ├── book_management.py
│   ├── category_management.py
│   ├── database.py
│   ├── inventory_management.py
│   ├── menu_management.py
│   ├── user_management.py
│   └── order_management.py
├── main.py
└── /README.md
```

## Introduction

>This program implements the basic functions of a book management system through the cmd command-line interface, including user management, book management, book classification management, inventory management, book purchase process settings, and order management.
>
>The program is written in Python and uses MySQL database to store data.
>
>The following is the interface usage diagram of the program:

! [Screenshot 1] (./Pictures/1.png "optional title")

! [Screenshot 1] (./Pictures/2.png "optional title")

## Installation and operation mode

### Install Python library

>Use the following command to install the required Python libraries:

```bash
pip install mysql-connector-python
Pip install PyInstaller (optional)
```

### Run the program

>You can use any of the following methods to run the program:

#### Method 1

>Using PyInstaller to package programs:

```bash
PyInstaller -F --add-data "bookstore/*;bookstore" -i bookstore\icon.jpg main.py
```

>Then find the executable file in the dist directory.

#### Method 2

>Directly run Python script:

```bash
python main.py
```

## Precautions

>This program uses MySQL database, so it is necessary to first install MySQL database and create corresponding databases and tables.
>
>After installing the database, create corresponding tables in the database using SQL statements in the mysql-config.txt file.

[Click here to view the MySQL installation tutorial](https://blog.csdn.net/m0_71422677/article/details/136007088)
