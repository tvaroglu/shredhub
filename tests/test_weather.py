import vcr
import pytest
from app.weather import Weather

@pytest.mark.vcr()
class TestWeather:
    def test_base_url(self):
        assert Weather.base_url() == 'https://tvaroglu-sweater-weather.herokuapp.com/api/v1/forecast'

    def test_api_error(self):
        self.api_error = Weather.api_error()
        assert self.api_error['Error'] == [
            'SweaterWeather API is down, please troubleshoot the effected endpoint directly!'
        ]

    def test_sanitize_request_params(self):
        self.format_1 = 'Denver, CO'
        self.format_2 = 'denver, co'
        self.format_3 = 'DENVER,CO'
        self.formats = [
            self.format_1,
            self.format_2,
            self.format_3
        ]
        for f in self.formats:
            assert Weather.sanitize_request_params(f) == 'denver,co'

    def test_reformat_location(self):
        assert Weather.reformat('denver,co') == 'Denver'

    def test_forecast_data(self):
        self.weather = Weather()
        assert self.weather.current_weather == {}
        assert self.weather.daily_weather == {}
        assert self.weather.hourly_weather == {}
        assert self.weather.input_location == ''
        self.forecast_data = self.weather.get_forecast('denver,co')
        self.current_weather = self.weather.current_weather
        self.daily_weather = self.weather.daily_weather
        self.hourly_weather = self.weather.hourly_weather
        assert len(self.current_weather.keys()) == 10
        assert len(self.daily_weather) == 5
        for d in self.daily_weather:
            assert len(d.keys()) == 7
        assert len(self.hourly_weather) == 8
        for h in self.hourly_weather:
            assert len(h.keys()) == 4
        assert self.weather.input_location == 'Denver'
