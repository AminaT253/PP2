import psycopg2
import csv

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

# --- Добавление вручную ---
def insert_manual():
    surname = input("Фамилия: ")
    name = input("Имя: ")
    number = int(input("Номер телефона: "))
    cur.execute("INSERT INTO PhoneBook (surname, name, number) VALUES (%s, %s, %s)",
                (surname, name, number))
    conn.commit()
    print("Данные добавлены!")

def insert_from_csv(filename):
    with open(filename, 'r', encoding='utf-8', errors='replace') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) == 3:
                cur.execute("INSERT INTO PhoneBook (surname, name, number) VALUES (%s, %s, %s)", row)
        conn.commit()
    print("Данные из CSV добавлены!")

def update_user():
    surname = input("Фамилия пользователя для изменения: ")
    field = input("Что изменить? (name/number): ")
    new_value = input("Новое значение: ")
    
    if field == "number":
        new_value = int(new_value)

    cur.execute(f"UPDATE PhoneBook SET {field} = %s WHERE surname = %s", (new_value, surname))
    conn.commit()
    print("Данные обновлены!")

def delete_user():
    choice = input("Удалить по фамилии или номеру? (surname/number): ")
    if choice == "surname":
        value = input("Введите фамилию: ")
        cur.execute("DELETE FROM PhoneBook WHERE surname = %s", (value,))
    elif choice == "number":
        value = int(input("Введите номер телефона: "))
        cur.execute("DELETE FROM PhoneBook WHERE number = %s", (value,))
    conn.commit()
    print("Запись удалена!")

def search_user():
    field = input("Искать по полю (surname/name/number): ")
    value = input("Введите значение для поиска: ")
    if field == "number":
        cur.execute("SELECT * FROM PhoneBook WHERE number = %s", (int(value),))
    else:
        cur.execute(f"SELECT * FROM PhoneBook WHERE {field} = %s", (value,))
    results = cur.fetchall()
    if results:
        print("Найденные записи:")
        for row in results:
            print(row)
    else:
        print("Ничего не найдено.")

def main():
    while True:
        print("\nМеню:")
        print("1. Добавить вручную")
        print("2. Загрузить из CSV")
        print("3. Обновить данные")
        print("4. Удалить пользователя")
        print("5. Показать все записи")
        print("6. Поиск по фильтру")
        print("0. Выйти")
        
        choice = input("Выберите действие: ")

        if choice == "1":
            insert_manual()
        elif choice == "2":
            filename = input("Имя CSV-файла (например, data.csv): ")
            insert_from_csv(filename)
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            cur.execute("SELECT * FROM PhoneBook")
            for row in cur.fetchall():
                print(row)
        elif choice == "6":
            search_user()
        elif choice == "0":
            break
        else:
            print("Неверный выбор, попробуйте снова.")

    cur.close()
    conn.close()
    print("Соединение с базой данных закрыто.")

main()
