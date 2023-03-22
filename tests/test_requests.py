import os
import fakeredis
from unittest.mock import patch

os.environ['DATABASE_URL'] = 'sqlite://'
redis_patch = patch('blocklist.BLOCKLIST', fakeredis.FakeStrictRedis())
redis_patch.start()

import unittest
from app import create_app, db
from models import DeveloperModel, InvestmentModel, FlatModel

developer_data = {
    "name": "Birkbud",
    "url": "https://www.birkbud.pl/nieruchomosci/"
}
investments_data = [
    {
        "developer_id": 1,
        "name": "Apartamenty Sienkiewicza",
        "url": "https://www.birkbud.pl/apartamentysienkiewicza/"
    },
    {
        "developer_id": 1,
        "name": "Złote Kaskady",
        "url": "https://www.birkbud.pl/zlotekaskady/"
    }
]
flats_data = [
    {
        "area": 36.3,
        "developer_id": 1,
        "floor_number": 1,
        "invest_name": "Apartamenty Sienkiewicza",
        "investment_id": 1,
        "price": None,
        "rooms_number": 2,
        "status": "sprzedane"
    },
    {
        "area": 47.64,
        "developer_id": 1,
        "floor_number": 2,
        "invest_name": "Apartamenty Sienkiewicza",
        "investment_id": 1,
        "price": None,
        "rooms_number": 3,
        "status": "sprzedane"
    },
    {
        "area": 64.05,
        "developer_id": 1,
        "floor_number": 5,
        "invest_name": "Złote Kaskady",
        "investment_id": 2,
        "price": None,
        "rooms_number": 4,
        "status": "sprzedane"
    },
    {
        "area": 48.39,
        "developer_id": 1,
        "floor_number": 1,
        "invest_name": "Złote Kaskady",
        "investment_id": 2,
        "price": None,
        "rooms_number": 3,
        "status": "sprzedane"
    }
]


class FlaskAppTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app()
        self.app.testing = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.add_data_to_database()
        self.client = self.app.test_client()
        self.create_user()

    def tearDown(self) -> None:
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None
        pass

    def add_data_to_database(self):
        developer = DeveloperModel(**developer_data)
        db.session.add(developer)
        db.session.commit()
        for investment_data in investments_data:
            investment = InvestmentModel(**investment_data)
            db.session.add(investment)
        db.session.commit()
        for flat_data in flats_data:
            flat = FlatModel(**flat_data)
            db.session.add(flat)
        db.session.commit()

    def create_user(self):
        self.client.post("/register", json={
            "username": "Owsiej",
            "password": "Zenek123!"
        })

    def get_fresh_access_token(self):
        response = self.client.post("/login", json={
            "username": "Owsiej",
            "password": "Zenek123!"
        })
        return response.json['access_token']

    def get_refresh_access_token(self):
        response = self.client.post("/login", json={
            "username": "Owsiej",
            "password": "Zenek123!"
        })
        return response.json['refresh_token']

    def test_get_developer_list(self):
        response = self.client.get('/developers')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)
        self.assertIsInstance(response.json, list)

    def test_post_developer_list(self):
        response = self.client.post('/developers', json={
            "name": "Some_developer",
            "url": "some_url"
        })
        developer = DeveloperModel.query.filter_by(id=2).first()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(developer)
        self.assertEqual(developer.name, "Some_developer")
        self.assertIsInstance(response.json, dict)

    def test_get_developer_by_id(self):
        response_good = self.client.get('/developers/1')
        response_bad = self.client.get('/developers/2')
        self.assertIsInstance(response_good.json, dict)
        self.assertEqual(response_good.status_code, 200)
        self.assertEqual(response_good.json['name'], "Birkbud")
        self.assertEqual(response_bad.status_code, 404)

    def test_delete_developer_by_id(self):
        response_first = self.client.delete('/developers/1')
        self.assertEqual(response_first.status_code, 400)
        developer = DeveloperModel.query.filter_by(id=1).first()
        developer_investments = developer.investments.all()
        for developer_investment in developer_investments:
            db.session.delete(developer_investment)
        db.session.commit()
        response_second = self.client.delete('/developers/1')
        self.assertEqual(response_second.status_code, 200)

    def test_put_developer_by_id(self):
        response_first = self.client.put("/developers/1", json={
            "name": "Updated_name",
            "url": "Updated_url"
        })
        self.assertEqual(response_first.status_code, 200)
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertEqual(developer.name, "Updated_name")
        self.assertIsInstance(response_first.json, dict)

        response_second = self.client.put("/developers/1", json={
            "name": "Updated_name",
            "url": 1
        })
        self.assertEqual(response_second.status_code, 422)

    def test_get_investments_list(self):
        response = self.client.get("/investments")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertIsInstance(response.json, list)

    def test_get_investment_by_id(self):
        response_first = self.client.get("/investments/1")
        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(response_first.json["name"], "Apartamenty Sienkiewicza")
        self.assertIsInstance(response_first.json, dict)

        response_second = self.client.get("/investments/3")
        self.assertEqual(response_second.status_code, 404)

    def test_delete_investment_by_id(self):
        response = self.client.delete("/investments/1")
        self.assertEqual(response.status_code, 200)
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertIsInstance(developer, DeveloperModel)
        self.assertEqual(len(developer.investments.all()), 1)
        self.assertEqual(len(developer.flats.all()), 2)

    def test_put_investment_by_id(self):
        response_first = self.client.put("/investments/2", json={
            "name": "Updated_name",
            "url": "Updated_url"
        })
        self.assertEqual(response_first.status_code, 200)
        investment = db.get_or_404(InvestmentModel, 2)
        self.assertEqual(investment.name, "Updated_name")
        self.assertIsInstance(response_first.json, dict)

        response_third = self.client.put("/investments/2", json={
            "name": "Updated_name",
            "url": 1
        })
        self.assertEqual(response_third.status_code, 422)

    def test_get_investment_by_developer_id(self):
        response_first = self.client.get("/developers/1/investments")
        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(len(response_first.json), 2)
        self.assertIsInstance(response_first.json, list)

        response_second = self.client.get("/developers/2/investments/")
        self.assertEqual(response_second.status_code, 404)

    def test_delete_investment_by_developer_id(self):
        response = self.client.delete("/developers/1/investments")
        self.assertEqual(response.status_code, 200)
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertIsInstance(developer, DeveloperModel)
        self.assertEqual(len(developer.investments.all()), 0)
        self.assertEqual(len(developer.flats.all()), 0)

    def test_post_investment_by_developer_id(self):
        response_first = self.client.post("/developers/3/investments", json={
            "name": "Nowa_inwestycja",
            "url": "Updated_name"

        })
        self.assertEqual(response_first.status_code, 404)

        response_second = self.client.post("/developers/1/investments", json={
            "name": "Nowa_inwestycja",
            "url": "Updated_url"
        })
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertEqual(response_second.status_code, 201)
        self.assertEqual(len(developer.investments.all()), 3)
        self.assertIsInstance(response_second.json, dict)

        response_third = self.client.post("/developers/1/investments", json={
            "name": "Złote Kaskady",
            "url": "Updated_url"
        })
        self.assertEqual(response_third.status_code, 400)

        response_forth = self.client.post("/developers/1/investments", json={
            "name": "Updated_name",
            "url": 1
        })
        self.assertEqual(response_forth.status_code, 422)

    def test_get_from_all_flats_by_query_string(self):
        response = self.client.get("/flats", query_string={"area__gt": 60,
                                                           })
        self.assertEqual(len(response.json), 1)
        self.assertIsInstance(response.json, list)

        response_second = self.client.get("/flats", query_string={"rooms_number": 3,
                                                                  "floor_number": 2
                                                                  })
        self.assertEqual(len(response_second.json), 1)
        self.assertIsInstance(response_second.json, list)

        response_third = self.client.get("/flats")
        self.assertEqual(len(response_third.json), 4)

        response_forth = self.client.get("/flats", query_string={"rooms_number": 3,
                                                                 "floor_number": "three",
                                                                 "price": "million"
                                                                 })
        self.assertEqual(response_forth.status_code, 422)

    def test_get_flat_by_id(self):
        response_first = self.client.get("/flats/1")
        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(response_first.json["invest_name"], "Apartamenty Sienkiewicza")
        self.assertIsInstance(response_first.json, dict)

        response_second = self.client.get("/flats/3")
        self.assertEqual(response_second.status_code, 200)
        self.assertEqual(response_second.json["invest_name"], "Złote Kaskady")
        self.assertIsInstance(response_second.json, dict)

        response_third = self.client.get("/flats/5")
        self.assertEqual(response_third.status_code, 404)

    def test_delete_flat_by_id(self):
        response_first = self.client.delete("/flats/1")
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertEqual(len(developer.flats.all()), 3)
        self.assertEqual(response_first.status_code, 200)

        response_first = self.client.delete("/flats/5")
        self.assertEqual(response_first.status_code, 404)

    def test_put_flat_by_id(self):
        response_first = self.client.put("/flats/1", json={
            "floor_number": 10,
            "rooms_number": 5,
            "area": 54.54,
            "price": 42342342344.3,
            "status": "wolne"
        })
        self.assertEqual(response_first.status_code, 200)
        flat = db.get_or_404(FlatModel, 1)
        self.assertEqual(flat.floor_number, 10)
        self.assertIsInstance(response_first.json, dict)

        response_second = self.client.put("/flats/2", json={
            "floor_number": 10,
            "rooms_number": 5,
            "price": 545454.4,
        })
        self.assertEqual(response_second.status_code, 200)
        self.assertIsInstance(response_first.json, dict)

        response_third = self.client.put("/flats/3", json={
            "floor_number": "ten",
            "rooms_number": 3,
            "area": None,
            "price": None,
            "status": "wolne"
        })
        self.assertEqual(response_third.status_code, 422)

        response_forth = self.client.put("/flats/5", json={
            "floor_number": 2,
            "rooms_number": 3,
            "area": 43.43,
            "price": 4342342.34,
            "status": "wolne"
        })
        self.assertEqual(response_forth.status_code, 404)

    def test_get_from_all_flats_from_investment_by_query_string(self):
        response = self.client.get("/investments/flats", query_string={"investment_id": 2,
                                                                       })
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

        response_second = self.client.get("/investments/flats", query_string={"investment_id": 2,
                                                                              "area__lt": 50
                                                                              })
        self.assertEqual(len(response_second.json), 1)
        self.assertEqual(response_second.json[0]["area"], 48.39)

        response_third = self.client.get("/investments/flats", query_string={"area__lt": 50,
                                                                             "floor_number__lt": 5
                                                                             })
        self.assertEqual(response_third.status_code, 422)

        response_forth = self.client.get("/flats", query_string={"investment_id": 1,
                                                                 "rooms_number": 3,
                                                                 "floor_number": "three",
                                                                 "price": "million"
                                                                 })
        self.assertEqual(response_forth.status_code, 422)

    def test_delete_flats_by_investment_id(self):
        response = self.client.delete("/investments/1/flats")
        self.assertEqual(response.status_code, 200)
        investment = db.get_or_404(InvestmentModel, 1)
        self.assertIsInstance(investment, InvestmentModel)
        self.assertEqual(len(investment.flats.all()), 0)
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertEqual(len(developer.flats.all()), 2)

    def test_post_flat_by_investment_id(self):
        response_first = self.client.post("/investments/2/flats", json={
            "floor_number": 2,
            "rooms_number": None,
            "area": 43.43,
            "price": None,
            "status": "wolne"
        })
        self.assertEqual(response_first.status_code, 201)
        investment = db.get_or_404(InvestmentModel, 2)
        self.assertEqual(len(investment.flats.all()), 3)
        self.assertIsInstance(response_first.json, dict)

        response_second = self.client.post("/investments/2/flats", json={})
        self.assertEqual(response_second.status_code, 201)
        self.assertEqual(response_second.json["invest_name"], "Złote Kaskady")
        self.assertIsInstance(response_second.json, dict)

        response_third = self.client.post("/investments/3/flats", json={
            "floor_number": 2,
            "rooms_number": None,
            "area": 43.43,
            "price": None,
            "status": "wolne"
        })
        self.assertEqual(response_third.status_code, 404)

    def test_delete_flats_by_developer_id(self):
        response_first = self.client.delete("/developers/1/flats")
        self.assertEqual(response_first.status_code, 200)
        developer = db.get_or_404(DeveloperModel, 1)
        self.assertIsInstance(developer, DeveloperModel)
        self.assertEqual(len(developer.flats.all()), 0)

        response_second = self.client.delete("/developers/2/flats")
        self.assertEqual(response_second.status_code, 404)

    def test_get_developers_from_scrape(self):
        token = self.get_fresh_access_token()
        refresh_token = self.get_refresh_access_token()
        os.chdir(self.app.root_path)

        response_first = self.client.get("/scrape",
                                         headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_first.status_code, 200)
        self.assertIsInstance(response_first.json, list)

        response_second = self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        response_third = self.client.get("/scrape",
                                         headers={"Authorization": f"Bearer {response_second.json['access_token']}"})
        self.assertEqual(response_third.json['message'], "The token is not fresh.")

    #
    def test_put_developers_from_scrape(self):
        token = self.get_fresh_access_token()
        refresh_token = self.get_refresh_access_token()

        os.chdir(self.app.root_path)
        response_first = self.client.put("/scrape", json={"developer_id": 1},
                                         headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_first.status_code, 201)
        self.assertIsInstance(response_first.json, dict)
        self.assertEqual(len(DeveloperModel.query.all()), 2)

        response_second = self.client.put("/scrape", json={"developer_id": 1},
                                          headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_second.status_code, 201)
        self.assertIsInstance(response_second.json, dict)
        self.assertEqual(len(DeveloperModel.query.all()), 2)

        response_third = self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        response_forth = self.client.get("/scrape",
                                         headers={"Authorization": f"Bearer {response_third.json['access_token']}"})
        self.assertEqual(response_forth.json['message'], "The token is not fresh.")

    def test_get_excel_file(self):
        token = self.get_fresh_access_token()
        response = self.client.get("/flats_to_excel", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.mimetype, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response_first = self.client.post("/register", json={"username": "Owsiej12",
                                                             "password": "Haslo123!"})
        self.assertEqual(response_first.status_code, 201)
        self.assertEqual(response_first.json, {"message": "User created successfully."})

        response_second = self.client.post("/register", json={"username": "Owsiej12",
                                                              "password": "Haslo123!"})
        self.assertEqual(response_second.status_code, 409)
        self.assertEqual(response_second.json['message'], 'An user with that username already exists.')

        response_third = self.client.post("/register", json={"username": "Owsiej1!",
                                                             "password": "Haslo123!"})
        self.assertEqual(response_third.status_code, 422)
        self.assertEqual(response_third.json['errors']['json']['username'][0],
                         'Login can have a maximum 8 chars with no special chars available.')

        response_forth = self.client.post("/register", json={"username": "Owsiej1",
                                                             "password": "haslo123!"})
        self.assertEqual(response_forth.json['errors']['json']['password'][0],
                         "Password must have 6 to 15 characters with at least one capital letter, one small letter, "
                         "one number and one special character.")

        response_fifth = self.client.post("/register", json={"username": "Owsiej12"})
        self.assertEqual(response_fifth.status_code, 422)
        self.assertEqual(response_fifth.json['errors']['json']['password'][0], 'Missing data for required field.')

    def test_get_user_by_id(self):
        response = self.client.get("/user/1")
        self.assertEqual(response.json['username'], "Owsiej")

    def test_delete_user_by_id(self):
        token = self.get_fresh_access_token()
        refresh_token = self.get_refresh_access_token()

        response_first = self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        response_second = self.client.delete("/user/1",
                                             headers={"Authorization": f"Bearer {response_first.json['access_token']}"})
        self.assertEqual(response_second.json['message'], "The token is not fresh.")

        response_third = self.client.delete("/user/1")
        self.assertEqual(response_third.json['message'], "Request must contain an access token")

        response_forth = self.client.delete("/user/1", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_forth.status_code, 200)

        response_fifth = self.client.get("/user/1")
        self.assertEqual(response_fifth.status_code, 404)

    def test_user_login(self):
        response_first = self.client.post("/login", json={
            "username": "Owsiej",
            "password": "Zenek123!"
        })
        self.assertEqual(response_first.status_code, 200)
        self.assertTrue(response_first.json["access_token"])
        self.assertTrue(response_first.json["refresh_token"])

        response_second = self.client.post("/login", json={
            "username": "Owsiej",
            "password": "Zenek12312!"
        })
        self.assertEqual(response_second.json['message'], "Invalid credentials.")

    def test_token_refresh(self):
        token = self.get_fresh_access_token()
        refresh_token = self.get_refresh_access_token()

        response_first = self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        self.assertTrue(response_first.json['access_token'])

        response_second = self.client.post("/refresh", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_second.json['message'], "Invalid token.")

    def test_user_logout(self):
        token = self.get_fresh_access_token()
        response_first = self.client.post("/logout", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_first.json['message'], "Logged out.")

        response_second = self.client.post("/logout", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response_second.json['message'], "The token has been revoked.")

    if __name__ == "__main__":
        unittest.main()
