import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='suppliers',
    user='postgres',
    password='21071994',
    port='5432'
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS PhoneBook (
        surname VARCHAR(255),
        name VARCHAR(255),
        number INT
    );
""")
conn.commit()

def search_pattern():
    pattern = input("Введите шаблон для поиска: ").strip()
    cur.execute("SELECT * FROM get_records_by_pattern(%s)", (pattern,))
    results = cur.fetchall()
    for row in results:
        print(row)

def insert_or_update():
    surname = input("Фамилия: ")
    name = input("Имя: ")
    number = input("Номер: ")
    cur.execute("CALL insert_or_update_user(%s, %s, %s)", (surname, name, int(number)))
    conn.commit()
    print("Добавлено/обновлено!")

def insert_many():
    names = input("Введите имена и фамилии через запятую: ").split(",")
    phones = input("Введите номера в том же порядке через запятую: ").split(",")
    names = [x.strip() for x in names]
    phones = [x.strip() for x in phones]
    cur.execute("SELECT insert_many_users(%s, %s)", (names, phones))
    result = cur.fetchone()[0]
    print("Неверные записи:", result)

def paginate():
    limit = int(input("Сколько записей показать: "))
    offset = int(input("С какой позиции начать: "))
    cur.execute("SELECT * FROM get_users_with_pagination(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

def delete_entry():
    mode = input("Удалить по фамилии или номеру? (surname/number): ").strip()
    if mode == "surname":
        val = input("Введите фамилию: ")
        cur.execute("CALL delete_user(%s, NULL)", (val,))
    else:
        val = int(input("Введите номер: "))
        cur.execute("CALL delete_user(NULL, %s)", (val,))
    conn.commit()
    print("Запись удалена!")

def main():
    while True:
        print("""
1. Поиск по шаблону
2. Добавить/Обновить одного пользователя
3. Массовое добавление
4. Показать с пагинацией
5. Удалить пользователя
0. Выйти
""")
        choice = input("Выберите действие: ")
        if choice == "1":
            search_pattern()
        elif choice == "2":
            insert_or_update()
        elif choice == "3":
            insert_many()
        elif choice == "4":
            paginate()
        elif choice == "5":
            delete_entry()
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

    cur.close()
    conn.close()
    print("Соединение закрыто.")

main()
