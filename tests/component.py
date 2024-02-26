import requests
import unittest

ticket_url = 'http://localhost:8000'
statistics_url = 'http://localhost:8001'
add_ticket_url = f'{ticket_url}/add_ticket'
get_ticket_by_id_url = f'{ticket_url}/get_ticket_by_id'
get_tickets_url = f'{ticket_url}/get_tickets'

ticket = {
    "id": 88,
    "passenger_name": "Ormanzhi",
    "passport": "010101.010101",
    "id_ship": 17,
    "direction": "New York"
}


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test1_add_ticket(self):
        res = requests.post(add_ticket_url, json=ticket)
        self.assertEqual(res.status_code, 200)

    def test2_ticket_get(self):
        res = requests.get(f"{get_ticket_by_id_url}?ticket_id=1").json()
        self.assertEqual(res['passenger_name'], "Ormanzhi")
        self.assertEqual(res['passport'], "010101.010101")
        self.assertEqual(res['id_ship'], 0)
        self.assertEqual(res['direction'], "string")

    def test3_fetch_tickets(self):
        res = requests.get(get_tickets_url)
        self.assertTrue(res != "Cant access database!")


if __name__ == '__main__':
    unittest.main()
