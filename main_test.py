import unittest
from main import *


class TestDatabase(unittest.TestCase):
    clean_db


    def test_tables(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Genre'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Shooter',), result_list)
        self.assertIn(('Sport',), result_list)
        self.assertEqual(len(result_list), 20)

        sql = '''
            SELECT Rating
            FROM ESRB

        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)

        self.assertEqual(len(result_list), 7)
        self.assertEqual(result_list[0][0], "RP")

        sql = '''
            SELECT Name, Platform, Genre1
            FROM Games
            Where Name = "Assassin's Creed: Origins"

        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(result_list[0][0], "Assassin's Creed: Origins")
        self.assertEqual(result_list[0][1], "PlayStation 4")
        self.assertEqual(result_list[0][2], "Role-playing (RPG)")

        conn.close()
    # def test_updateANDJoin(self):
    #     init_db()
    #     add_genre_data()
    #     add_games_data()
    #     add_esrb_ratings()
    #     add_platform_data()
    #
    #     conn = sqlite3.connect(DBNAME)
    #     cur = conn.cursor()
    #     sql = '''
    #         SELECT Games.Name, Games.Rating
    #         FROM Games
    #         Join ESRB on Games.Rating = ESRB.ID
    #         Where Name = "For Honor"
    #
    #     '''
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn("For Honor", result_list[0][0])
    #     self.assertIn("6", result_list[0][1])
    #
    #     update_ratings()
    #
    #     cur.execute(sql)
    #
    #     sql = '''
    #         SELECT Games.Rating
    #         FROM Games
    #         Where Name = "For Honor"
    #
    #     '''
    #
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn("M", result_list[0])
    #     conn.close()

class TestPlatformQuery(unittest.TestCase):
    clean_db()

    def test_platformCounts(self):
        test_list = query_platformCounts(2017)

        if isinstance(test_list, list):
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        self.assertIn('Nintendo Switch', test_list[0])
        self.assertIn('iOS', test_list[0])
        self.assertEqual(test_list[1][5], 235)





class TestGenreQuery(unittest.TestCase):
    clean_db()
    def test_genreCounts(self):
        test_list = query_genreCounts(2015)
        if isinstance(test_list, list):
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        self.assertIn('Shooter', test_list[0])

class TestApiCall(unittest.TestCase):
    def test_api_wrapper(self):
        result = igdb.games(1942)

        for game in result.body:
            self.assertEqual(game["id"], 1942)
            self.assertEqual(game["name"], "The Witcher 3: Wild Hunt")

        result = igdb.games(2000)
        if isinstance(result, requests.models.Response): #Tests that API Python wrapper is a Requests call
            self.assertTrue(True)

        else:
            self.assertFalse(False)
            
        for game in result.body:
            self.assertEqual(game["name"], "Postal")
            platform = game["platforms"]
            self.assertEqual(platform[0], 6)





unittest.main()
