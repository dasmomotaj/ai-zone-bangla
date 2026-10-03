"""DB persistence tests: DB_DIR override for Render Persistent Disk."""
import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A


class PersistenceTest(unittest.TestCase):
    def test_default_path_unchanged(self):
        self.assertTrue(A.DATABASE.endswith("aizonabangla.db"))
        self.assertEqual(os.path.dirname(A.DATABASE), A._APP_DIR)

    def test_db_dir_env_honored(self):
        with tempfile.TemporaryDirectory() as d:
            path = A.resolve_database_path(d)
            self.assertEqual(path, os.path.join(d, "aizonabangla.db"))
            self.assertTrue(os.path.isdir(d))

    def test_fresh_disk_boots_full_app(self):
        with tempfile.TemporaryDirectory() as d:
            path = A.resolve_database_path(d)
            old = A.DATABASE
            A.DATABASE = path
            try:
                A.init_db()
                A.apply_admin_reset_from_env(path)
                db = sqlite3.connect(path)
                try:
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM admin").fetchone()[0], 1)
                    self.assertGreater(db.execute("SELECT COUNT(*) FROM tools").fetchone()[0], 0)
                    self.assertGreater(db.execute("SELECT COUNT(*) FROM posts").fetchone()[0], 0)
                finally:
                    db.close()
                A.app.testing = True
                c = A.app.test_client()
                self.assertEqual(c.get("/").status_code, 200)
                self.assertEqual(c.get("/login").status_code, 200)
            finally:
                A.DATABASE = old


if __name__ == "__main__":
    unittest.main()
