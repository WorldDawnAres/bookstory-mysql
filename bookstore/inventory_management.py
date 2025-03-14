from bookstore import database

class InventoryManagement:
    def __init__(self):
        self.db = database.Database()
        self.db.connect()

    def add_book_to_inventory(self, book_title, quantity):
        if quantity <= 0:
            print("请输入一个有效的数量（大于0）。")
            return
        
        if not self.db.is_connected():
            print("数据库未连接，无法操作。")
            return
        
        try:
            self.db.start_transaction()

            query = "SELECT stock FROM books WHERE title = %s"
            result = self.db.execute_query(query, (book_title,))

            if result:
                current_stock = result[0]['stock']
                new_stock = current_stock + quantity
                update_query = "UPDATE books SET stock = %s WHERE title = %s"
                self.db.execute_update(update_query, (new_stock, book_title))
                print(f"{book_title} 已添加 {quantity} 本到库存，当前库存: {new_stock} 本。")
            else:
                print(f"库存中没有找到书籍 '{book_title}'。")

            self.db.commit_transaction()

        except Exception as e:
            self.db.rollback_transaction()
            print(f"操作失败，错误: {e}")

    def remove_book_from_inventory(self, book_title, quantity):
        if quantity <= 0:
            print("请输入一个有效的数量（大于0）。")
            return

        if not self.db.is_connected():
            print("数据库未连接，无法操作。")
            return

        try:
            self.db.start_transaction()

            query = "SELECT stock FROM books WHERE title = %s"
            result = self.db.execute_query(query, (book_title,))

            if result:
                current_stock = result[0]['stock']
                if current_stock >= quantity:
                    new_stock = current_stock - quantity
                    update_query = "UPDATE books SET stock = %s WHERE title = %s"
                    self.db.execute_update(update_query, (new_stock, book_title))
                    print(f"{book_title} 已移除 {quantity} 本，当前库存: {new_stock} 本。")
                else:
                    print(f"库存中没有足够的 {book_title}，当前库存: {current_stock} 本。")
            else:
                print(f"库存中没有找到书籍 '{book_title}'。")

            self.db.commit_transaction()

            self.db.reset_auto_increment()

        except Exception as e:
            self.db.rollback_transaction()
            print(f"操作失败，错误: {e}")

    def update_inventory(self, book_title, new_quantity):
        if new_quantity < 0:
            print("请输入一个有效的库存数量（大于等于0）。")
            return

        if not self.db.is_connected():
            print("数据库未连接，无法操作。")
            return

        try:
            self.db.start_transaction()

            query = "SELECT stock FROM books WHERE title = %s"
            result = self.db.execute_query(query, (book_title,))

            if result:
                current_stock = result[0].get('stock', 0)
                update_query = "UPDATE books SET stock = %s WHERE title = %s"
                self.db.execute_update(update_query, (new_quantity, book_title))
                print(f"{book_title} 的库存已更新为 {new_quantity} 本。")
            else:
                print(f"库存中没有找到书籍 '{book_title}'。")

            self.db.commit_transaction()

        except Exception as e:
            self.db.rollback_transaction()
            print(f"操作失败，错误: {e}")

    def view_inventory(self):
        query = "SELECT title, stock FROM books"
        result = self.db.execute_query(query)
        if result:
            print("--- 当前库存 ---")
            for row in result:
                print(f"书名: {row['title']}, 库存: {row['stock']} 本")
        else:
            print("没有找到库存信息。")

    def manage_inventory(self):
        while True:
            print("--- 库存管理菜单 ---")
            print("1. 添加书籍到库存")
            print("2. 移除书籍")
            print("3. 更新库存数量")
            print("4. 查看当前库存")
            print("5. 返回上级菜单")
            choice = input("请输入操作编号: ")

            if choice == '1':
                book_title = input("请输入书名: ")
                quantity = int(input("请输入添加的数量: "))
                self.add_book_to_inventory(book_title, quantity)
            elif choice == '2':
                book_title = input("请输入书名: ")
                quantity = int(input("请输入移除的数量: "))
                self.remove_book_from_inventory(book_title, quantity)
            elif choice == '3':
                book_title = input("请输入书名: ")
                new_quantity = int(input("请输入新的库存数量: "))
                self.update_inventory(book_title, new_quantity)
            elif choice == '4':
                self.view_inventory()
            elif choice == '5':
                print("返回上级菜单")
                break
            else:
                print("无效的操作编号，请重新输入。")
