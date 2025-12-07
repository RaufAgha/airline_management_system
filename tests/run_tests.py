#!/usr/bin/env python3
"""
Run test suite from project root.
- Tries to run `pytest` if installed.
- Falls back to `unittest` discovery.

Usage: python run_tests.py
"""
import sys
import os
import subprocess

ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

print(f"Project root: {ROOT}")

# Try pytest first
try:
    import pytest
    print("Running pytest...")
    # Equivalent to `pytest -q`
    ret = pytest.main([os.path.join(ROOT, 'tests'), '-q'])
    sys.exit(ret)
except Exception:
    print("pytest not available or failed to import, falling back to unittest discovery.")

import unittest
# Before running unittest, try to close any open SqliteConnection instances and remove test DB files
try:
    from src.db.sqlite_connection import SqliteConnection
    # close any existing connections
    for inst in list(getattr(SqliteConnection, '_instances', {}).values()):
        try:
            inst.conn.close()
        except Exception:
            pass
    # clear cached instances
    if hasattr(SqliteConnection, '_instances'):
        SqliteConnection._instances.clear()
except Exception:
    # src may not be importable yet; ignore
    pass

# Remove known test DB to start fresh (if not locked)
TEST_DB = os.path.join(ROOT, 'airline_test.db')
try:
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        print(f"Removed existing test DB: {TEST_DB}")
except Exception as e:
    print(f"Warning: could not remove test DB {TEST_DB}: {e}")

loader = unittest.TestLoader()
suite = unittest.TestSuite()
# Discover test modules but skip pytest-only files (filename contains 'pytest')
for fname in os.listdir(os.path.join(ROOT, 'tests')):
    if not fname.startswith('test_') or not fname.endswith('.py'):
        continue
    if 'pytest' in fname:
        print(f"Skipping pytest-only file for unittest run: {fname}")
        continue
    mod_name = fname[:-3]
    try:
        # import module from file path so tests/ is not required to be a package
        import importlib.util
        path = os.path.join(ROOT, 'tests', fname)
        spec = importlib.util.spec_from_file_location(mod_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)
    except Exception as e:
        print(f"Failed to import test module {mod_name}: {e}")

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
if not result.wasSuccessful():
    sys.exit(1)
else:
    sys.exit(0)
