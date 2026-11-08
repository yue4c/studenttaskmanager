"""Database-level automated tests; run: python -m unittest test_database.py"""
import tempfile
import unittest
from pathlib import Path
from database import TaskRepository


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.repo = TaskRepository(Path(self.folder.name) / 'test.db')

    def tearDown(self):
        self.folder.cleanup()

    def test_insert_and_list(self):
        self.repo.add('Study GUI', '', 'High', '2026-11-05')
        self.assertEqual(self.repo.all()[0]['title'], 'Study GUI')

    def test_edit(self):
        id_ = self.repo.add('Old', '', 'Low', '2026-11-05')
        self.assertEqual(self.repo.update(id_, 'New', 'Notes', 'High', '2026-11-06', False), 1)
        self.assertEqual(self.repo.all()[0]['title'], 'New')

    def test_delete(self):
        id_ = self.repo.add('Temporary', '', 'Low', '2026-11-05')
        self.repo.delete(id_)
        self.assertEqual(self.repo.totals(), (0, 0))

    def test_completion(self):
        id_ = self.repo.add('Task', '', 'Medium', '2026-11-05')
        self.repo.set_completed(id_, True)
        self.assertEqual(self.repo.totals(), (1, 1))

    def test_search(self):
        self.repo.add('Read notes', '', 'Medium', '2026-11-05')
        self.repo.add('Write code', '', 'High', '2026-11-05')
        self.assertEqual(len(self.repo.all(search='write')), 1)

    def test_filters(self):
        self.repo.add('One', '', 'High', '2026-11-05')
        self.repo.add('Two', '', 'Low', '2026-11-05', True)
        self.assertEqual(len(self.repo.all(priority='High', status='Pending')), 1)
        self.assertEqual(len(self.repo.all(status='Completed')), 1)

    def test_data_survives_new_connection(self):
        self.repo.add('Persistent', '', 'Medium', '2026-11-05')
        another = TaskRepository(self.repo.path)
        self.assertEqual(another.totals()[0], 1)


if __name__ == '__main__':
    unittest.main()
