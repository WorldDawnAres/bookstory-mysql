import mysql.connector
from mysql.connector import Error
from bookstore import config

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=config.DATABASE_CONFIG['host'],
                port=config.DATABASE_CONFIG['port'],
                user=config.DATABASE_CONFIG['user'],
                password=config.DATABASE_CONFIG['password'],
                database=config.DATABASE_CONFIG['database'],
                charset=config.DATABASE_CONFIG['charset']
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                #print("成功连接到数据库")
        except Error as err:
            print(f"数据库连接失败: {err}")
            self.connection = None
            self.cursor = None

    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            #print("数据库连接已关闭")

    def start_transaction(self):
        if self.is_connected():
            if self.connection.in_transaction:
                print("事务已存在，无法开始新的事务")
                self.rollback_transaction()
            self.connection.start_transaction()
            print("事务已开始")
        else:
            print("数据库未连接，无法开始事务")

    def commit_transaction(self):
        if self.is_connected():
            self.connection.commit()
            print("事务已提交")
        else:
            print("数据库未连接，无法提交事务")

    def rollback_transaction(self):
        if self.is_connected():
            self.connection.rollback()
            print("事务已回滚")
        else:
            print("数据库未连接，无法回滚事务")

    def execute_query(self, query, params=None):
        try:
            if not self.is_connected():
                print("数据库未连接，无法执行查询操作")
                return None
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchall()  # 获取所有查询结果
            return result
        except Error as err:
            print(f"查询失败: {err}")
            return None

    def execute_update(self, query, params=None):
        try:
            if not self.is_connected():
                print("数据库未连接，无法执行更新操作")
                return
            self.cursor.execute(query, params or ())
            self.connection.commit()  # 提交事务
            #print(f"成功执行更新操作：{query}")
        except Error as err:
            print(f"执行失败: {err}")
            self.connection.rollback()  # 回滚事务

    def execute_insert(self, query, params=None):
        try:
            if not self.is_connected():
                print("数据库未连接，无法执行插入操作")
                return None
            self.cursor.execute(query, params or ())
            self.connection.commit()  # 提交事务
            last_insert_id = self.cursor.lastrowid  # 获取最后插入的ID
            print(f"成功插入记录，ID: {last_insert_id}")
            return last_insert_id
        except Error as err:
            print(f"插入失败: {err}")
            self.connection.rollback()  # 回滚事务
            return None

    def execute_delete(self, query, params=None):
        try:
            if not self.is_connected():
                print("数据库未连接，无法执行删除操作")
                return
            self.cursor.execute(query, params or ())
            self.connection.commit()  # 提交事务
            print(f"成功删除记录：{query}")
        except Error as err:
            print(f"删除失败: {err}")
            self.connection.rollback()  # 回滚事务

    def reset_auto_increment(self):
        try:
            # 查询最小的可用 ID
            query_min_id = """
            SELECT MIN(t1.id + 1) AS next_id
            FROM books t1
            LEFT JOIN books t2 ON t1.id + 1 = t2.id
            WHERE t2.id IS NULL;
            """
            result = self.execute_query(query_min_id)
            
            if result and result[0]["next_id"] is not None:
                next_id = result[0]["next_id"]
            else:
                next_id = 1  # 如果没有记录，设置为 1
            
            # 重新连接数据库，以确保查询顺序正确
            self.close()  # 先关闭数据库连接
            self.connect()  # 重新连接数据库

            # 设置新的 AUTO_INCREMENT 值
            query_alter = f"ALTER TABLE books AUTO_INCREMENT = {next_id}"
            self.execute_update(query_alter, ())
            #print(f"成功重置 AUTO_INCREMENT 为 {next_id}。")
        except Error as err:
            print(f"重置 AUTO_INCREMENT 失败: {err}")

    def create_order(self, book_id, quantity):
        try:
            if not self.is_connected():
                print("数据库未连接，无法创建订单")
                return False

            self.start_transaction()

            query = "SELECT stock FROM books WHERE id = %s"
            stock_result = self.execute_query(query, (book_id,))
            if not stock_result or stock_result[0]['stock'] < quantity:
                print("库存不足，无法购买")
                self.rollback_transaction()
                return False

            new_stock = stock_result[0]['stock'] - quantity
            update_query = "UPDATE books SET stock = %s WHERE id = %s"
            self.execute_update(update_query, (new_stock, book_id))

            insert_query = "INSERT INTO orders (book_id, quantity) VALUES (%s, %s)"
            self.execute_insert(insert_query, (book_id, quantity))

            self.commit_transaction()
            print("订单创建成功")
            return True
        except Error as err:
            print(f"创建订单失败: {err}")
            self.rollback_transaction()
            return False
