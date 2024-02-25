import asyncio
import unittest
import requests
import psycopg2
from time import sleep
import json
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'statistics_service/app'))
sys.path.append(str(BASE_DIR / 'ticket_service/app'))

from statistics_service.app.main import statistics_alive as doc1
from ticket_service.app.main import ticket_alive as doc2

def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='TicketPort',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except Exception as e:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_roulet_service_connection(self):
        r = asyncio.run(doc1())
        self.assertEqual(r, {'message': 'service alive'})

    def test_user_service_connection(self):
        r = asyncio.run(doc2())
        self.assertEqual(r, {'message': 'service alive'})


if __name__ == '__main__':
    unittest.main()
