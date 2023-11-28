import sqlite3
from datetime import datetime

# Criando um SQLite db e tabela de tasks
def create_database():
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            priority_tag TEXT,
            title TEXT,
            description TEXT,
            assignee TEXT,
            status TEXT,
            due_date TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Adicionar nova task
def add_task(priority_tag, title, description, assignee):
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    due_date = input("Entre a data de prazo (formato: DD-MM-YYYY): ")
    cursor.execute('INSERT INTO tasks (priority_tag, title, description, assignee, status, due_date) VALUES (?, ?, ?, ?, ?, ?)',
                   (priority_tag, title, description, assignee, 'Nova', due_date))
    connection.commit()

    # Obtendo o ID da task recém-criada
    cursor.execute('SELECT last_insert_rowid()')
    task_id = cursor.fetchone()[0]
    connection.close()

    print(f"Task criada! ID: {task_id}")

# Atribuir uma task
def assign_task(task_id, new_assignee):
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE tasks SET assignee = ? WHERE id = ?', (new_assignee, task_id))
    connection.commit()
    connection.close()



# Listar todas as tasks por prioridade
def list_tasks():
    connection = sqlite3.connect('taskhub.db')
    cursor = connection.cursor()
    cursor.execute ('SELECT * FROM tasks ORDER BY CASE WHEN priority_tag = "Alta" THEN 1 WHEN priority_tag = "Média" THEN 2 ELSE 3 END')
    tasks = cursor.fetchall()
    connection.close()
    return tasks

if __name__ == "__main__":
    create_database()

    while True:
        print("\nTaskHub Menu:")
        print("1. Criar uma Task")
        print("2. Nomear uma Task")
        print("3. Listar Tasks por Prioridade")
        print("4. Sair")

        choice = input("Selecione uma das opções: ")

        if choice == "1":
            title = input("Entre o título da task aqui: ")
            description = input("Entre a descrição da task aqui: ")
            assignee = input("Adicione o nome de quem terá a task traibuida: ")
            priority_tag = input("Adicione o nível de prioridade (Baixa, Média, Alta): ")
            add_task(priority_tag, title, description, assignee)

        elif choice == "2":
            task_id = int(input("Adicione o ID da task criada: "))
            new_assignee = input("Adicione o nome de quem terá a task atribuída: ")
            assign_task(task_id, new_assignee)
            print("Task atribuída!")

        elif choice == "3":
            tasks = list_tasks()
            if tasks:
                for task in tasks:
                    print(f"Task ID: {task[0]}, Prioridade: {task[1]}, Título: {task[2]}, Descrição: {task[3]}, Atribuído à: {task[4]}, Status: {task[5]}, Prazo: {task[6]}")
            else:
                print("Nenhuma task foi encontrada.")

        elif choice == "4":
            break

        else:
            print("Inválido! Por favor escolha uma opção válida.")
