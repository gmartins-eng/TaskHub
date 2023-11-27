import sqlite3

#criando um SQLite db e tabela de tasks
def create_database():
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            assignee TEXT,
            status TEXT
        )
    ''')
    connection.commit()
    connection.close()

#adicionar nova task
def add_task(title, description, assignee):
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (title, description, assignee, status) VALUES (?, ?, ?, ?)', (title, description, assignee, 'Nova'))
    connection.commit()
    connection.close()


def assign_task(task_id, new_assignee):
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE tasks SET assignee = ? WHERE id = ?', (new_assignee, task_id))
    connection.commit()
    connection.close()

# List all tasks
def list_tasks():
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    connection.close()
    return tasks

if __name__ == "__main__":
    create_database()

    while True:
        print("\nTaskHub Menu:")
        print("1. Criar uma Task")
        print("2. Nomear uma Task")
        print("3. Listar Tasks")
        print("4. Sair")

        choice = input("Selecione uma das opções: ")

        if choice == "1":
            title = input("Entre o título da task aqui: ")
            description = input("Entre a descrição da task aqui: ")
            assignee = input("Adicione o nome de quem terá a task traibuida: ")
            add_task(title, description, assignee)
            print("Task criada!")

        elif choice == "2":
            task_id = int(input("Adicione o ID da task criada: "))
            new_assignee = input("Adicione o nome de quem terá a task atribuida: ")
            assign_task(task_id, new_assignee)
            print("Task atribuida!")

        elif choice == "3":
            tasks = list_tasks()
            if tasks:
                for task in tasks:
                    print(f"Task ID: {task[0]}, Título: {task[1]}, Descrição: {task[2]}, Atribuido à: {task[3]}, Status: {task[4]}")
            else:
                print("Nenhuma task foi encontrada.")

        elif choice == "4":
            break

        else:
            print("Inválido! Por favor escolha uma opção válida.")
