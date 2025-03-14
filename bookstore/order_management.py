from bookstore import database

class OrderManagement:
    def __init__(self, db):
        self.db = db

    def view_all_orders(self, status=None, username=None):
        print("\n--- 查看所有订单 ---")
        query = """
            SELECT o.id AS order_id, u.username, o.total_price, o.status
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE 1
        """
        params = []

        if status:
            query += " AND o.status = %s"
            params.append(status)
        
        if username:
            query += " AND u.username = %s"
            params.append(username)

        result = self.db.execute_query(query, params)

        if result:
            for order in result:
                print(f"订单ID: {order['order_id']}, 用户: {order['username']}, 总金额: {order['total_price']}, 状态: {order['status']}")
        else:
            print("没有符合条件的订单记录。")

    def view_user_orders(self, username):
        print("\n--- 查看用户订单 ---")
        query = """
            SELECT o.id AS order_id, o.total_price, o.status
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE u.username = %s
        """
        result = self.db.execute_query(query, (username,))

        if result:
            for order in result:
                print(f"订单ID: {order['order_id']}, 总金额: {order['total_price']}, 状态: {order['status']}")
        else:
            print("没有找到该用户的订单记录。")


    def create_order(self, username, books):
        print("\n--- 创建订单 ---")
        try:
            query = "SELECT id FROM users WHERE username = %s"
            result = self.db.execute_query(query, (username,))

            if not result:
                print("未找到该用户名，请检查用户名是否正确。")
                return

            user_id = result[0]['id']
            total_price = 0

            for book in books:
                query = "SELECT stock, price FROM books WHERE id = %s"
                result = self.db.execute_query(query, (book['book_id'],))

                if not result:
                    print(f"图书ID {book['book_id']} 不存在，跳过该书籍。")
                    return
                stock, price = result[0]['stock'], result[0]['price']
                if stock < book['quantity']:
                    print(f"图书 {book['name']} 库存不足（当前库存: {stock} 本）。")
                    return
                total_price += price * book['quantity']

            self.db.start_transaction()

            query = "INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)"
            order_id = self.db.execute_insert(query, (user_id, total_price, '待处理'))

            if order_id:
                print(f"订单已创建，订单ID: {order_id}，总金额: {total_price} 元")
                for book in books:
                    query = "INSERT INTO order_items (order_id, book_id, quantity) VALUES (%s, %s, %s)"
                    self.db.execute_insert(query, (order_id, book['book_id'], book['quantity']))

                    update_query = "UPDATE books SET stock = stock - %s WHERE id = %s"
                    self.db.execute_update(update_query, (book['quantity'], book['book_id']))
                    print(f"图书 '{book['name']}' 已添加到订单，并减少库存 {book['quantity']} 本。")
            else:
                print("创建订单失败，无法获取订单ID。")

            self.db.commit_transaction()

        except Exception as e:
            self.db.rollback_transaction()
            print(f"创建订单失败: {e}")


    def manual_create_order(self):
        print("\n--- 手动创建订单 ---")
        username = input("请输入用户名: ")

        query = "SELECT id FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,))

        if result:
            user_id = result[0]['id']
            total_price = float(input("请输入总金额: "))
            status = input("请输入订单状态(待处理,处理中,已发货,已完成,已取消):")

            query = "INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)"
            params = (user_id, total_price, status)

            order_id = self.db.execute_insert(query, params)

            if order_id:
                print(f"订单已创建，订单ID: {order_id}，总金额: {total_price}元")

                books = []
                while True:
                    book_id = input("请输入图书ID (输入'结束'完成): ")
                    if book_id.lower() == '结束':
                        break
                    if not book_id.isdigit():
                        print("请输入有效的图书ID。")
                        continue
                    quantity = input("请输入数量: ")
                    if not quantity.isdigit() or int(quantity) <= 0:
                        print("请输入有效的数量。")
                        continue
                    books.append({'book_id': book_id, 'quantity': int(quantity)})

                if books:
                    for book in books:
                        query = "INSERT INTO order_items (order_id, book_id, quantity) VALUES (%s, %s, %s)"
                        params = (order_id, book['book_id'], book['quantity'])
                        self.db.execute_insert(query, params)

                        query = "UPDATE books SET stock = stock - %s WHERE id = %s"
                        self.db.execute_update(query, (book['quantity'], book['book_id']))

                    print(f"订单ID: {order_id} 的图书项已成功添加！")
                else:
                    print("没有添加任何图书项。")
            else:
                print("订单创建失败，请重试。")
        else:
            print("未找到该用户名，请检查用户名是否正确。")



    def close_connection(self):
        if self.db:
            self.db.close()