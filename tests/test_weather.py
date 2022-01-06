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
        self.city_format_1 = 'Denver'
        self.city_format_2 = 'denver'
        self.city_format_3 = 'DENVER'
        self.city_formats = [
            self.city_format_1,
            self.city_format_2,
            self.city_format_3
        ]
        for f in self.city_formats:
            assert Weather.sanitize_request_params(f, 'CO') == 'denver,co'

    def test_reformat_input_location(self):
        assert Weather.reformat_input_location('denver,co') == 'Denver'

    def test_hourly_forecast_data(self):
        self.weather = Weather()
        assert self.weather.hourly_weather == {}
        assert self.weather.input_location == ''
        self.weather.get_forecast('denver,co')
        assert self.weather.input_location == 'Denver'
        self.hourly_weather = self.weather.hourly_weather
        assert len(self.hourly_weather) == 8
        for h in self.hourly_weather:
            assert len(h.keys()) == 4
        assert isinstance(self.weather.avg_hourly_temp(), float)
        assert isinstance(self.weather.median_hourly_temp(), float)
        assert isinstance(self.weather.forecasted_conditions('hourly'), str)

    def test_daily_forecast_data(self):
        self.weather = Weather()
        assert self.weather.daily_weather == {}
        self.weather.get_forecast('denver,co')
        self.daily_weather = self.weather.daily_weather
        assert len(self.daily_weather) == 5
        for d in self.daily_weather:
            assert len(d.keys()) == 7
        assert isinstance(self.weather.avg_daily_highs(), float)
        assert isinstance(self.weather.avg_daily_lows(), float)
        assert isinstance(self.weather.forecasted_conditions('daily'), str)

    def test_current_forecast_data(self):
        self.weather = Weather()
        assert self.weather.current_weather == {}
        self.current_forecast = self.weather.get_forecast('denver,co')
        assert str(type(self.current_forecast)) == "<class 'app.weather.Weather'>"
        self.current_weather = self.weather.current_weather
        assert len(self.current_weather.keys()) == 10

    def test_list_constructor(self):
        self.weather = Weather()
        self.weather.get_forecast('denver,co')
        self.daily_max_temp_list = Weather.list_constructor(self.weather.daily_weather, 'max_temp')
        assert len(self.daily_max_temp_list) == 5
        for data_point in self.daily_max_temp_list:
            assert isinstance(data_point, float)

    def test_mean(self):
        self.data_list_1 = [5, 1, 3, 4, 2]
        self.data_list_2 = [5, 1, 3, 4, 2, 2]
        assert Weather.mean(self.data_list_1) == 3.00
        assert Weather.mean(self.data_list_2) == 2.83

    def test_median(self):
        self.data_list_1 = [5, 1, 3, 4, 2]
        self.data_list_2 = [5, 1, 3, 4, 2, 2]
        assert Weather.median(self.data_list_1) == 3.00
        assert Weather.median(self.data_list_2) == 2.50

    def test_mode(self):
        self.data_list_1 = ['snow', 'snow', 'clear sky']
        self.data_list_2 = ['snow', 'clear sky']
        assert Weather.mode(self.data_list_1) == 'snow'
        assert Weather.mode(self.data_list_2) == 'clear sky'

    def test_state_abbreviations_list(self):
        self.state_abbreviations_list = Weather.state_abbreviations_list()
        assert len(self.state_abbreviations_list) == 57
        for state_abbreviation in self.state_abbreviations_list:
            assert isinstance(state_abbreviation, str)
            assert len(state_abbreviation) == 2

    def test_create_plot(self):
        self.weather = Weather()
        self.plot = self.weather.create_plot()
        assert str(type(self.plot)) == "<class 'matplotlib.figure.Figure'>"
