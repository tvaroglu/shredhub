import requests
import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
# from app import app

class Weather:
    @classmethod
    def base_url(cls):
        resources = {
            'domain_name': 'https://tvaroglu-sweater-weather.herokuapp.com',
            'api_version': '/api/v1',
            'endpoint': '/forecast'
        }
        return f"{resources['domain_name']}{resources['api_version']}{resources['endpoint']}"

    @classmethod
    def api_error(cls):
        return {
            'Error': [
                'SweaterWeather API is down, please troubleshoot the effected endpoint directly!'
            ]
        }

    @classmethod
    def sanitize_request_params(cls, city_param, state_param):
        city_param = city_param.replace(',', '')
        return f'{city_param.lower()},{state_param.lower()}'

    @classmethod
    def reformat_input_location(cls, location):
        return location.split(',')[0].capitalize()

    @classmethod
    def list_constructor(cls, list_of_dicts, dict_key):
        output_list = []
        for dict in list_of_dicts:
            output_list.append(dict[dict_key])
        return output_list

    @classmethod
    def mean(cls, data_list):
        return round(np.average(data_list), 2)

    @classmethod
    def median(cls, data_list):
        return round(np.median(data_list), 2)

    @classmethod
    def mode(cls, data_list):
        result = stats.mode(data_list, axis=None)
        # Note, returns min value in list by default if no mode:
        return result[0][0]

    @classmethod
    def state_abbreviations_list(cls):
        states_list = [
            'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
            'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
            'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE',
            'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI',
            'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI',
            'WV', 'WY'
        ]
        return states_list

    def __init__(self):
        self.current_weather = {}
        self.daily_weather = {}
        self.hourly_weather = {}
        self.input_location = ''

    def get_forecast(self, location):
        url = f'{Weather.base_url()}?location={location}'
        response = requests.get(url)
        if response.status_code == 200:
            forecast_data = response.json()['data']['attributes']
            self.current_weather = forecast_data['current_weather']
            self.daily_weather = forecast_data['daily_weather']
            self.hourly_weather = forecast_data['hourly_weather']
            self.input_location = location
            return self
        return Weather.api_error()

    def forecasted_temps(self, data_set, metric=None):
        if data_set == 'hourly':
            return Weather.list_constructor(self.hourly_weather, 'temperature')
        else:
            if metric == 'highs':
                return Weather.list_constructor(self.daily_weather, 'max_temp')
            return Weather.list_constructor(self.daily_weather, 'min_temp')

    def forecasted_conditions(self, data_set):
        if data_set == 'hourly':
            data = Weather.list_constructor(self.hourly_weather, 'conditions')
        data = Weather.list_constructor(self.daily_weather, 'conditions')
        return Weather.mode(data).capitalize()

    # @app.context_processor
    def avg_hourly_temp(self):
        return Weather.mean(self.forecasted_temps('hourly'))

    def median_hourly_temp(self):
        return Weather.median(self.forecasted_temps('hourly'))

    def avg_daily_highs(self):
        return Weather.mean(self.forecasted_temps('daily', 'highs'))

    def avg_daily_lows(self):
        return Weather.mean(self.forecasted_temps('daily', 'lows'))

    def conditions(self):
        return self.current_weather['conditions'].capitalize()

    def current_temp(self):
        return self.current_weather['temperature']

    def feels_like(self):
        return self.current_weather['feels_like']

    def humidity(self):
        return self.current_weather['humidity']

    def uvi(self):
        return round(self.current_weather['uvi'], 1)

    def create_bar_chart(self, input_location=None, x_axis=None, y_axis=None):
        # TODO: figure out args from routes to dynamically render charts
        self.get_forecast(input_location)
        fig = Figure()
        ax = fig.add_axes([0, 0, 1, 1])
        x_axis = Weather.list_constructor(self.hourly_weather, 'time')
        y_axis = Weather.list_constructor(self.hourly_weather, 'temperature')
        bars = ax.bar(x_axis, y_axis)
        ax.bar_label(bars)
        return fig
