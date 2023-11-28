import unittest
import sqlite3
from unittest.mock import patch
from io import StringIO
import app

class TestTaskHubFunctions(unittest.TestCase):

    def setUp(self):
        self.module_name = 'taskhub.db'
        app.create_database()

    def tearDown(self):
        connection = sqlite3.connect(f'{self.module_name}.db')
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS tasks')
        connection.commit()
        connection.close()

    @patch('builtins.input', side_effect=['20-12-2023'])
    def test_add_task(self, mock_input):
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.add_task(priority_tag, title, description, assignee)

        output = mock_stdout.getvalue().strip()
        self.assertIn("Task criada!", output)
        self.assertIn("ID:", output)

    def test_assign_task(self):
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'
        app.add_task(priority_tag, title, description, assignee)

        connection = sqlite3.connect('taskhub.db')
        cursor = connection.cursor()
        cursor.execute('SELECT MAX(id) FROM tasks')
        task_id = cursor.fetchone()[0]
        connection.close()

        new_assignee = 'Jane Doe'

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.assign_task(task_id, new_assignee)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Task atribuída!")
        
    def test_list_tasks(self):
        priority_tag = 'Alta'
        title = 'Test Task'
        description = 'Test Description'
        assignee = 'John Doe'
        app.add_task(priority_tag, title, description, assignee)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            app.list_tasks()

        output = mock_stdout.getvalue().strip()
        print("DEBUG - Test Output:", output)


if __name__ == '__main__':
    unittest.main()