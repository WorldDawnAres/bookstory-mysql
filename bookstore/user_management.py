from bookstore import database

class UserManagement:
    def __init__(self, db: database.Database):
        self.db = db
        self.db.connect()  # 初始化数据库连接

    def login_prompt(self):
        print("\n请输入用户名和密码进行登录")
        username = input("用户名: ")
        password = input("密码: ")
        return username, password

    def add_user(self):
        print("\n--- 添加用户 ---")
        username = input("请输入新用户名: ")
        password = input("请输入密码: ")
        role = input("请输入用户角色（customer/root）: ")

        query = "SELECT * FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,))
        
        if result:
            print(f"用户名 '{username}' 已经存在！")
        else:
            insert_query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            self.db.execute_insert(insert_query, (username, password, role))
            print(f"用户 {username} 添加成功！")

    def view_users(self):
        print("\n--- 查看所有用户 ---")
        query = "SELECT username, password, role FROM users"
        users = self.db.execute_query(query)

        if users:
            for user in users:
                print(f"用户名: {user['username']}, 密码: {user['password']}, 角色: {user['role']}")
        else:
            print("没有用户信息。")

    def delete_user(self):
        print("\n--- 删除用户 ---")
        username = input("请输入要删除的用户名: ")

        query = "SELECT * FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,))

        if not result:
            print(f"用户名 '{username}' 不存在！")
        else:
            delete_query = "DELETE FROM users WHERE username = %s"
            self.db.execute_delete(delete_query, (username,))
        
            query_max_id = "SELECT MAX(id) FROM users"
            result = self.db.execute_query(query_max_id)
        
            if result and result[0]["MAX(id)"] is not None:
                max_id = result[0]["MAX(id)"]
                next_id = max_id + 1
            else:
                next_id = 1

            query_alter = f"ALTER TABLE users AUTO_INCREMENT = {next_id}"
            self.db.execute_update(query_alter, ())

            result_after_delete = self.db.execute_query("SELECT * FROM users WHERE username = %s", (username,))
            if not result_after_delete:
                print(f"用户 {username} 删除成功！")
            else:
                print(f"删除用户 {username} 失败。")


    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, password))

        if result:
            return result[0]
        return None

    def manage_user(self):
        while True:
            print("\n--- 用户管理菜单 ---")
            print("1. 添加用户")
            print("2. 查看所有用户")
            print("3. 删除用户")
            print("4. 返回")
            choice = input("请输入操作编号: ")

            if choice == "1":
                self.add_user()
            elif choice == "2":
                self.view_users()
            elif choice == "3":
                self.delete_user()
            elif choice == "4":
                break
            else:
                print("无效选择，请重新输入!")

    def __del__(self):
        self.db.close()
