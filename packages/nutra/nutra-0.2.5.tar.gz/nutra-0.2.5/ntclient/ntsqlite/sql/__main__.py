"""Call this with python -m sql"""
# pylint: disable=import-error
from sql import build_ntsqlite

if __name__ == "__main__":
    build_ntsqlite(verbose=True)
