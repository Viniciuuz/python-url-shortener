# URL Shortener

Url shortener built with flask and pandas

## Backend

* [Flask](https://github.com/pallets/flask)
* [Pandas](https://github.com/pandas-dev/pandas)

## Frontend

* [Halfmoon](https://github.com/halfmoonui/halfmoon)

## Endpoints

### records

This endpoint returns all the entrys (JSON formatted)

### put

This endpoint accepts only POST requests. Get the all the parameters in the url (alias, url, comment) and saves them in the csv file

### del

This endpoint accepts only POST requests. Get the alias from the url and deletes the entry registered as that alias