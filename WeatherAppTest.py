import unittest
import WeatherApp as wa


class WeatherTest(unittest.TestCase):
   def setUp(self) -> None:
        self.rio_list = [-43.2093727, -22.9110137, "Rio", "Brazil"]
        self.israel_list = [35.2257626, 31.7788242, "Jerusalem", "Israel"]
        self.app = wa.app.test_client()

   def test_get_coords_by_name(self):
        name = "3123213#?"
        self.assertEqual(wa.get_coords_by_name(name), None)
        name = "#riomoscow"
        self.assertEqual(wa.get_coords_by_name(name), None)
        name = "rio"
        self.assertEqual(wa.get_coords_by_name(name), self.rio_list)
        name = "israel"
        self.assertEqual(wa.get_coords_by_name(name), self.israel_list)

   def test_get_weather_data(self):
        self.assertIsNotNone(wa.get_weather_data(self.rio_list[0], self.rio_list[1]))
        self.assertIsNotNone(wa.get_weather_data(self.israel_list[0], self.israel_list[1]))

   def test_landing_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
