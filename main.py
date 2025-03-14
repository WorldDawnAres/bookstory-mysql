from bookstore import database
from bookstore import user_management
from bookstore import book_management
from bookstore import order_management
from bookstore import inventory_management
from bookstore import category_management
from bookstore import menu_management

def main():
    db = database.Database()

    try:
        db.connect()
        #print("数据库连接成功！")
        
        book_mgmt = book_management.BookManagement()
        order_mgmt = order_management.OrderManagement(db)
        inventory_mgmt = inventory_management.InventoryManagement()
        category_mgmt = category_management.CategoryManagement()

        user_mgmt = user_management.UserManagement(db)
        
        print("\n--- 用户登录 ---")
        username, password = user_mgmt.login_prompt()
        user_info = user_mgmt.login(username, password)

        if not user_info:
            print("登录失败！")
            return

        role = user_info['role']

        if role == "root":
            print("\n--- 管理员功能菜单 ---")
            menu_management.admin_menu(book_mgmt, order_mgmt, inventory_mgmt, category_mgmt, user_mgmt)  # 管理员菜单
        else:
            print("\n--- 普通用户功能菜单 ---")
            menu_management.user_menu(book_mgmt, order_mgmt, username, user_mgmt)

    except Exception as e:
        print(f"发生错误: {e}")

    finally:
        db.close()
        #print("数据库连接已关闭。")

if __name__ == "__main__":
    main()