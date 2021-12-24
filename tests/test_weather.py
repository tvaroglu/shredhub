import vcr
import pytest

@pytest.mark.vcr()
class TestWeather:
    def test_weather_class(self):
        assert True
