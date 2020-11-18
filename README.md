# Weather Analysis and API Calls
---
This project is targetted 2 areas to hone the skills:
1. Using sqlalchemy to connect with sqlite and performing some statistics using pandas.
2. Using Flask to create a webpage for having API calls for data from sqlite db.
---
### [climate_starter](climate_starter.ipynb) Notebook 
This notebook houses first piece of the challenge. It connects with sqlite db available in [Resources](Resources) folder and fetches some key data from weather stations table.

### [app.py](app.py) API Connect
This python code utilizes Flask and have following 5 different URL Routes to get the data.
#### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Return the JSON representation of your dictionary with date and precipitation fields.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
