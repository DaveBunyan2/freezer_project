# Changelog

## [0.0.0-b]

### Added
- pull_data.py
    - Pulls data from CAREL controller.
- insert_data.py 
    - Inserts data into database.
- freezer_program.py
    - Pulls data, processes it and stores it in database.

## [0.0.1-b] - 2023-11-28

### Added
- Calculated and returned time taken to request data from CAREL controller to subtract from wait time so data is pulled every 5 seconds.

## [0.0.2-b] - 2023-11-29

### Added
- extract_data.py
    - Extracts data from database and returns timestamps and values for a given sensor.

## [0.0.3-b] - 2023-11-30

### Changes
- Changed extract_data() to take a start and end date as input.

## [0.0.4-b] - 2023-12-07
- Added extract_last() function to extract_data.py