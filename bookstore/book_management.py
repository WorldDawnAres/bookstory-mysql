from bookstore import database

class Book:
    def __init__(self, book_id, title, author, price, stock):
        self.id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            'book_id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'stock': self.stock
        }
    
    def __str__(self):
        return f"ID: {self.id}, 标题: {self.title}, 作者: {self.author}, 价格: {self.price}, 库存: {self.stock}"


class BookManagement:

    def __init__(self):
        self.db = database.Database()
        self.db.connect()

    def add_book(self):
        print("\n--- 添加新图书 ---")
        title = input("请输入图书标题: ")
        author = input("请输入图书作者: ")
        price = float(input("请输入图书价格: "))
        stock = int(input("请输入图书库存数量: "))

        query = "INSERT INTO books (title, author, price, stock) VALUES (%s, %s, %s, %s)"
        params = (title, author, price, stock)
        self.db.execute_insert(query, params)
        print(f"图书 '{title}' 添加成功！")

    def query_books(self, book_id=None):
        if book_id:
            print("\n--- 查询单本图书 ---")
            query = "SELECT * FROM books WHERE id = %s"
            params = (book_id,)
        else:
            print("\n--- 查询所有图书 ---")
            query = "SELECT * FROM books"
            params = ()

        result = self.db.execute_query(query, params)

        if result:
            if book_id:
                book = result[0]
                book_obj = Book(book['id'], book['title'], book['author'], book['price'], book['stock'])
                print(f"找到图书: ID: {book_obj.id}, 标题: {book_obj.title}, 作者: {book_obj.author}, 价格: {book_obj.price}, 库存: {book_obj.stock}")
                return book_obj
            else:
                print("--- 所有图书 ---")
                for book in result:
                    book_obj = Book(book['id'], book['title'], book['author'], book['price'], book['stock'])
                    print(f"ID: {book_obj.id}, 标题: {book_obj.title}, 作者: {book_obj.author}, 价格: {book_obj.price}, 库存: {book_obj.stock}")
                return result
        else:
            print("没有找到图书。")
            return None



    def update_book(self, book_id):
        if not book_id.isdigit():
            print("请输入有效的图书ID。")
            return

        print("\n--- 更新图书信息 ---")
        title = input("请输入新的图书标题: ")
        author = input("请输入新的图书作者: ")
        price = float(input("请输入新的图书价格: "))
        stock = int(input("请输入新的图书库存数量: "))

        query = "UPDATE books SET title = %s, author = %s, price = %s, stock = %s WHERE id = %s"
        params = (title, author, price, stock, book_id)
        self.db.execute_update(query, params)
        print(f"图书 '{book_id}' 更新成功！")

    def delete_book(self, book_id):
        if not book_id.isdigit():
            print("请输入有效的图书ID。")
            return

        print("\n--- 删除图书 ---")
    
        query = "DELETE FROM books WHERE id = %s"
        params = (book_id,)
        self.db.execute_delete(query, params)
        print(f"图书 '{book_id}' 已删除。")
    
        query = "SELECT MAX(id) FROM books"
        result = self.db.execute_query(query)
        if result and result[0]['MAX(id)'] is not None:
            max_id = result[0]['MAX(id)']
        else:
            max_id = 0
    
        query = f"ALTER TABLE books AUTO_INCREMENT = {max_id + 1}"
        self.db.execute_query(query)
        #print(f"成功重置 AUTO_INCREMENT 为 {max_id + 1}。")


    def reset_auto_increment(self):
        query_max_id = "SELECT MAX(id) FROM books"
        result = self.db.execute_query(query_max_id)
    
        if result and result[0]["MAX(id)"] is not None:
            max_id = result[0]["MAX(id)"]
            next_id = max_id + 1
        else:
            next_id = 1
    
        query_alter = f"ALTER TABLE books AUTO_INCREMENT = {next_id}"
        self.db.execute_update(query_alter, ())
    
        print(f"成功重置 AUTO_INCREMENT 为 {next_id}。")


    def view_all_books(self):
        print("\n--- 所有书籍 ---")
        query = "SELECT * FROM books"
        books = self.db.execute_query(query)

        if books:
            for book in books:
                print(f"ID: {book['id']}, 标题: {book['title']}, 作者: {book['author']}, 价格: {book['price']}, 库存: {book['stock']}")
        else:
            print("没有书籍信息。")

    def manage_books(self):
        while True:
            print("\n--- 图书管理菜单 ---")
            print("1. 添加图书")
            print("2. 查询图书")
            print("3. 更新图书信息")
            print("4. 删除图书")
            print("5. 显示所有书籍")
            print("6. 返回")
            choice = input("请输入操作编号: ")

            if choice == "1":
                self.add_book()
            elif choice == "2":
                book_id = input("请输入要查询的图书ID: ")
                if book_id.isdigit():
                    self.query_books(int(book_id))
                else:
                    print("请输入有效的图书ID。")
            elif choice == "3":
                book_id = input("请输入要更新的图书ID: ")
                self.update_book(book_id)
            elif choice == "4":
                book_id = input("请输入要删除的图书ID: ")
                self.delete_book(book_id)
            elif choice == "5":
                self.view_all_books()
            elif choice == "6":
                break
            else:
                print("无效选择，请重新输入!")


    def __del__(self):
        self.db.close()
