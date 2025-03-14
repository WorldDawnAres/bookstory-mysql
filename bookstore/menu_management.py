def admin_menu(book_mgmt, order_mgmt, inventory_mgmt, category_mgmt, user_mgmt):
    while True:
        print("\n管理员菜单:")
        print("1. 书库管理")
        print("2. 订单管理")
        print("3. 库存管理")
        print("4. 图书分类管理")
        print("5. 用户管理")
        print("6. 退出")
        
        choice = input("请输入操作编号: ")

        if choice == "1":
            print("\n--- 书库管理 ---")
            book_mgmt.manage_books()
        elif choice == "2":
            print("\n--- 订单管理 ---")
            order_mgmt.view_all_orders()
            order_mgmt.manual_create_order()
        elif choice == "3":
            print("\n--- 库存管理 ---")
            inventory_mgmt.manage_inventory()
        elif choice == "4":
            print("\n--- 图书分类管理 ---")
            category_mgmt.manage_categories()
        elif choice == "5":
            print("\n--- 用户管理 ---")
            user_mgmt.manage_user()
        elif choice == "6":
            print("退出系统...")
            break
        else:
            print("无效选择，请重新输入!")


def user_menu(book_mgmt, order_mgmt, username, user_mgmt):
    while True:
        print("\n用户菜单:")
        print("1. 购书功能")
        print("2. 查看订单")
        print("3. 退出系统")

        choice = input("请输入操作编号: ")

        if choice == "1":
            print("\n--- 购书功能 ---")
            book_id = input("请输入要查询的图书ID: ")

            book = book_mgmt.query_books(book_id)

            if book:
                #print(f"找到图书: ID: {book.id}, 标题: {book.title}, 作者: {book.author}, 价格: {book.price}, 库存: {book.stock}")

                quantity = input("请输入购买数量: ")
                if not quantity.isdigit() or int(quantity) <= 0:
                    print("请输入有效的数量。")
                    continue

                books = [{
                    'book_id': book.id,
                    'quantity': int(quantity),
                    'price': book.price,
                    'name': book.title
                }]

                order_mgmt.create_order(username, books)
            else:
                print("未找到该图书，请检查图书ID。")

        elif choice == "2":
            print("\n--- 查看订单 ---")
            order_mgmt.view_user_orders(username)
        elif choice == "3":
            print("退出系统...")
            break
        else:
            print("无效选择，请重新输入!")