## Overview

MKW is an external subscription vendor we work with that provides us daily
snapshots of customer transactions. They do by submitting a TSV of those
uploads to the form in the `/upload` view. A background process asynchronously
loads the data from their submissions into a simply database. From there,
downstream services can query against this database for their own purposes.

## Setup
`pip install -r requirements.txt `

## Run Tests
`python tests/app_test.py`

## Run application
`python app.py`

## Initialize Database
This application uses built in sqlite3. We don't require any setup.
