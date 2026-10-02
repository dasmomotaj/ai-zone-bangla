"""Tests for the ADMIN_RESET_PASSWORD one-time admin password reset."""
import os
import secrets
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A
from werkzeug.security import check_password_hash, generate_password_hash

# Random per-run values used only against throwaway temp databases.
OLD_PASSWORD = secrets.token_urlsafe(16)
NEW_PASSWORD = secrets.token_urlsafe(16)
SHORT_PASSWORD = secrets.token_urlsafe(6)[:8]
LOG_SENTINEL = secrets.token_urlsafe(16)


class AdminResetTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "test.db")
        self._old_db = A.DATABASE
        A.DATABASE = self.db_path
        self._env = dict(os.environ)
        os.environ.pop("ADMIN_RESET_PASSWORD", None)
        os.environ.pop("ADMIN_INITIAL_PASSWORD", None)
        A.init_db()
        db = sqlite3.connect(self.db_path)
        db.execute("UPDATE admin SET password_hash=? WHERE username='admin'",
                   (generate_password_hash(OLD_PASSWORD),))
        db.commit()
        db.close()

    def tearDown(self):
        A.DATABASE = self._old_db
        os.environ.clear()
        os.environ.update(self._env)
        self.tmp.cleanup()

    def _hash(self):
        db = sqlite3.connect(self.db_path)
        try:
            return db.execute("SELECT password_hash FROM admin WHERE username='admin'").fetchone()[0]
        finally:
            db.close()

    def _count_admins(self):
        db = sqlite3.connect(self.db_path)
        try:
            return db.execute("SELECT COUNT(*) FROM admin").fetchone()[0]
        finally:
            db.close()

    def test_admin_user_exists(self):
        self.assertEqual(self._count_admins(), 1)

    def test_missing_var_changes_nothing(self):
        self.assertEqual(A.apply_admin_reset_from_env(self.db_path), "missing")
        self.assertTrue(check_password_hash(self._hash(), OLD_PASSWORD))

    def test_short_password_rejected(self):
        os.environ["ADMIN_RESET_PASSWORD"] = SHORT_PASSWORD
        self.assertEqual(A.apply_admin_reset_from_env(self.db_path), "rejected:short")
        self.assertTrue(check_password_hash(self._hash(), OLD_PASSWORD))
        self.assertFalse(check_password_hash(self._hash(), SHORT_PASSWORD))

    def test_reset_applies_and_password_hashed(self):
        os.environ["ADMIN_RESET_PASSWORD"] = NEW_PASSWORD
        self.assertEqual(A.apply_admin_reset_from_env(self.db_path), "applied")
        stored = self._hash()
        self.assertNotEqual(stored, NEW_PASSWORD)
        self.assertTrue(check_password_hash(stored, NEW_PASSWORD))

    def test_old_password_fails_new_password_works(self):
        os.environ["ADMIN_RESET_PASSWORD"] = NEW_PASSWORD
        A.apply_admin_reset_from_env(self.db_path)
        stored = self._hash()
        self.assertFalse(check_password_hash(stored, OLD_PASSWORD))
        self.assertTrue(check_password_hash(stored, NEW_PASSWORD))

    def test_no_duplicate_admin_created(self):
        os.environ["ADMIN_RESET_PASSWORD"] = NEW_PASSWORD
        A.apply_admin_reset_from_env(self.db_path)
        self.assertEqual(self._count_admins(), 1)

    def test_second_run_is_idempotent(self):
        os.environ["ADMIN_RESET_PASSWORD"] = NEW_PASSWORD
        self.assertEqual(A.apply_admin_reset_from_env(self.db_path), "applied")
        first_hash = self._hash()
        self.assertEqual(A.apply_admin_reset_from_env(self.db_path), "already-applied")
        self.assertEqual(self._hash(), first_hash)
        self.assertTrue(check_password_hash(self._hash(), NEW_PASSWORD))

    def test_password_never_exposed_in_logs(self):
        sentinel = LOG_SENTINEL
        os.environ["ADMIN_RESET_PASSWORD"] = sentinel
        with self.assertLogs(A.app.logger, level="WARNING") as logs:
            A.apply_admin_reset_from_env(self.db_path)
        combined = "\n".join(logs.output)
        self.assertNotIn(sentinel, combined)

    def test_login_with_reset_password(self):
        os.environ["ADMIN_RESET_PASSWORD"] = NEW_PASSWORD
        A.apply_admin_reset_from_env(self.db_path)
        A.app.testing = True
        client = A.app.test_client()
        resp = client.post("/login", data={"username": "admin", "password": NEW_PASSWORD},
                           follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/admin", resp.headers.get("Location", ""))


if __name__ == "__main__":
    unittest.main()
