from flask import Flask, abort
from flask.json import jsonify
import requests
from datetime import datetime


app = Flask(__name__)


@app.errorhandler(400)
def not_found(e):
    return jsonify({'Error': 'Bad request. Ensure you use a valid river code, and the number of days must be between 1 and 365.'}), 404


@app.errorhandler(404)
def not_found(e):
    return jsonify({'Error': 'Not found'}), 404


@app.errorhandler(500)
def problem(e):
    return jsonify({'Error': 'There was an error. Please report this to Clara.'}), 500


@app.route('/')
def homepage():
    return 'This is the home page.'


@app.route('/api/river/<site_id>/<days>')
def river_info(site_id, days):

    url = 'https://waterservices.usgs.gov/nwis/iv'

    parameter_code_map = {
        # '00011': 'Water temperature, fahrenheit',
        # '00060': 'Flow, cubic feet per second',
        '00065': 'Gauge height, feet',
    }

    parameter_codes = ','.join(parameter_code_map.keys())   # height, flow, temp

    # is period a positive number between 1 and 365? 
    try:
        days = int(days)
        if days < 1 or days > 365:
            abort(400, 'Days must be an integer between 1 and 365')
    except:
        abort(400, 'Days must be an integer between 1 and 365')


    params = {
        'format': 'json',
        'site': site_id,
        'parameterCd': parameter_codes,
        'siteStatus': 'all',
        'period': f'P{days}D'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 400:  # Bad request, often unrecognized site number
        app.logger.error(f'Bad request for site {site_id} because {response.text}')
        abort(400)

    response.raise_for_status()  

    # get site name, values of parameters, time measurement made 

    river_data = response.json() 

    time_series = river_data['value']['timeSeries']

    if not time_series: 
        # no data or site number not found
        app.logger.error(f'No series of data for site {site_id}')
        abort(404)

    simplified_data = {'data': {} }

    for series in time_series:

        code = series['variable']['variableCode'][0]['value']
        simple_name = parameter_code_map[code]

        values = series['values'][0]['value']

        values_list = []
        times_list = []
        times_human_list = []
        timestamp_list = []

        for value_dict in values:

            data_point = value_dict['value']
            date_str = value_dict['dateTime']
            

            date_time = datetime.fromisoformat(date_str)
            # human_date = datetime.strftime(date_time, '%a %d %b %Y at %I:%M %p')
            timestamp = date_time.timestamp()

            timestamp_list.append(timestamp)
            values_list.append(data_point)
            times_list.append(date_str)
            # times_human_list.append(human_date)

        site_name = series['sourceInfo']['siteName']
        site_name_title = site_name.title()
        
        simplified_data['data'][simple_name] = {
            'values': values_list,
            'times': times_list,
            'timestamps': timestamp_list
            # 'formatted_times': times_human_list,
        }

        simplified_data['location'] = site_name_title


    return jsonify(simplified_data)      