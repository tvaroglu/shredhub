import requests
import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
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
            self.input_location = Weather.reformat_input_location(location)
        return Weather.api_error()

    # @app.context_processor
    def avg_hourly_temp(self):
        data = Weather.list_constructor(self.hourly_weather, 'temperature')
        return Weather.mean(data)

    def median_hourly_temp(self):
        data = Weather.list_constructor(self.hourly_weather, 'temperature')
        return Weather.median(data)

    def mode_hourly_temp(self):
        data = Weather.list_constructor(self.hourly_weather, 'temperature')
        return Weather.mode(data)


# # Read in transactions data
# greatest_books = pd.read_csv("top-hundred-books.csv")
#
# # Save transaction times to a separate numpy array
# author_ages = greatest_books['Ages']
#
# # Calculate the average and median value of the author_ages array
# average_age = np.average(author_ages)
# median_age = np.median(author_ages)
# mode_age = 38
#
# # Plot the figure
# plt.hist(author_ages, range=(10, 80), bins=14,  edgecolor='black')
# plt.title("Author Ages at Publication")
# plt.xlabel("Publication Age")
# plt.ylabel("Count")
# plt.axvline(average_age, color='r', linestyle='solid', linewidth=3, label="Mean")
# plt.axvline(median_age, color='y', linestyle='dotted', linewidth=3, label="Median")
# plt.axvline(mode_age, color='orange', linestyle='dashed', linewidth=3, label="Mode")
# plt.legend()
#
# plt.show()
