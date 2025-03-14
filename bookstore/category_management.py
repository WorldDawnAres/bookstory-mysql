from bookstore import database

class CategoryManagement:
    def __init__(self):
        self.db = database.Database()
        self.db.connect()

    def add_category(self):
        print("\n--- 添加图书分类 ---")
        category_name = input("请输入分类名称: ")

        query = "INSERT INTO categories (name) VALUES (%s)"
        params = (category_name,)
        self.db.execute_insert(query, params)
        print(f"图书分类 '{category_name}' 添加成功！")

    def query_categories(self):
        print("\n--- 查询所有图书分类 ---")
        query = "SELECT * FROM categories"
        result = self.db.execute_query(query)

        if result:
            print("图书分类列表:")
            for category in result:
                print(f"ID: {category['id']}, 名称: {category['name']}")
        else:
            print("没有图书分类记录。")

    def update_category(self, category_id):
        print("\n--- 更新图书分类 ---")
        category_name = input("请输入新的分类名称: ")

        query = "UPDATE categories SET name = %s WHERE id = %s"
        params = (category_name, category_id)
        self.db.execute_update(query, params)
        print(f"图书分类 '{category_id}' 更新成功！")

    def delete_category(self, category_id):
        print("\n--- 删除图书分类 ---")
        query = "DELETE FROM categories WHERE id = %s"
        params = (category_id,)
        self.db.execute_delete(query, params)
        print(f"图书分类 '{category_id}' 已删除。")

        query = "SELECT MAX(id) FROM categories"
        result = self.db.execute_query(query)
        if result and result[0]['MAX(id)'] is not None:
            max_id = result[0]['MAX(id)']
        else:
            max_id = 0
    
        query = f"ALTER TABLE categories AUTO_INCREMENT = {max_id + 1}"
        self.db.execute_query(query)
        #print(f"成功重置 AUTO_INCREMENT 为 {max_id + 1}。")
    
    def reset_auto_increment(self):
        query_max_id = "SELECT MAX(id) FROM categories"
        result = self.db.execute_query(query_max_id)

        if result and result[0]["MAX(id)"] is not None:
            max_id = result[0]["MAX(id)"]
            next_id = max_id + 1
        else:
            next_id = 1

        self.db.close()
        self.db.connect()

        query_alter = f"ALTER TABLE categories AUTO_INCREMENT = {next_id}"
        self.db.execute_update(query_alter, ())

        print(f"成功重置 AUTO_INCREMENT 为 {next_id}。")


    def manage_categories(self):
        while True:
            print("\n--- 图书分类管理菜单 ---")
            print("1. 添加图书分类")
            print("2. 查询所有图书分类")
            print("3. 更新图书分类")
            print("4. 删除图书分类")
            print("5. 返回")
            choice = input("请输入操作编号: ")

            if choice == "1":
                self.add_category()
            elif choice == "2":
                self.query_categories()
            elif choice == "3":
                category_id = input("请输入要更新的图书分类ID: ")
                self.update_category(category_id)
            elif choice == "4":
                category_id = input("请输入要删除的图书分类ID: ")
                self.delete_category(category_id)
            elif choice == "5":
                break
            else:
                print("无效选择，请重新输入!")

    def __del__(self):
        self.db.close()
