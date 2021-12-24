import vcr
import pytest
from app.weather import Weather

@pytest.mark.vcr()
class TestWeather:
    def test_weather_class(self):
        self.weather = Weather()
        assert self.weather.base_url() == 'https://tvaroglu-sweater-weather.herokuapp.com/api/v1'
