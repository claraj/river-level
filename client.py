from datetime import datetime
import requests 
from bokeh.plotting import figure, show, save
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter


# river_data = requests.get('http://127.0.0.1:5000/api/river/05331000/3').json() # st paul
# river_data = requests.get('http://127.0.0.1:5000/api/river/05288670/10').json() # fridley
# river_data = requests.get('http://127.0.0.1:5000/api/river/05288500/40').json() # brooklyn park
river_data = requests.get('http://127.0.0.1:5000/api/river/05289800/55').json() # minnehaha
# river_data = requests.get('http://127.0.0.1:5000/api/river/05288705/365').json() # shingle


data = river_data['data']['Gauge height, feet']

measurements = data['values'] 
times = data['times']

curdoc().theme = 'dark_minimal'  # caliber, dark_minimal, light_minimal, night_sky, and contrast
p = figure(title=river_data['location'], x_axis_label='Date', x_axis_type="datetime")
p.xaxis.formatter=DatetimeTickFormatter(days=["%m/%d %H:%M"], hours=["%m/%d %H:%M"], minutes=["%m/%d %H:%M"])

dates = [] 
for time in times:
    date = datetime.fromisoformat(time)
    dates.append(date)

p.line(dates, measurements, legend_label='Gauge height, feet', line_width=3, line_color='cyan')
    
show(p)   # display in browser
save(p, filename="example.html")  # and/or save to file


# todo ask use which river location
# ask user how many days. make sure it's between 1 and 365
# ask use if save or show
# use loop to repeat for another river and/or days, or quit