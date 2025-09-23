# Ultimate Lineup Picker

Ultimate Lineup Picker is a tool that uses Sportsbook player props to determine the ideal fantasy football lineup. By analyzing how Vegas believes players will perform, ULP can infer fantasy points scored. When given a team of players, ULP will use these inferences to generate the ideal lineup for the upcoming week of play.

ULP is primarily written via a combination of Python and Vue. Use of ULP requires a key for [The Odds API](https://the-odds-api.com/), which can be acquired at the link.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Usage](#usage)
- [Initial Steps](#initial-steps)
- [Planned Improvements](#planned-improvements)
- [Completed Improvements](#completed-improvements)
- [Tools Used](#tools-used)

## Prerequisites

- Python is installed
- Vue is installed
- You have an API key for The Odds API
- You have an API key for Sports Data IO

## Development Setup

To set up your development environment for this project, follow these steps:

1. Clone the repository
2. Navigate to ```ultimate-lineup-picker/frontend/```
3. Run ```npm install```
4. Run ```npm run build```
5. Create an environment variable on your machine ```ODDS_API_KEY``` equal to your The Odds API key
6. Create a ```.env.local``` file in your ```frontend/``` folder. Within that file, create a variable named ```VUE_APP_PLAYER_DATA_API_KEY``` and set it equal to your API key for Sports Data IO.

## Usage

1. Open two terminals
2. In one terminal, cd to ```ultimate-lineup-picker/frontend/```
3. In the other terminal, cd to ```ultimate-lineup-picker/backend/```
4. In the frontend terminal, run the development page via ```npm run serve```
5. In the backend terminal, run the development server via ```py main.py```
6. In a web browser, navigate to ```https://localhost:8080/```

## Initial Steps

- [X] Create a frontend prototype that contains a basic splash page, detailing what the project is
- [X] Add a prototype input to the front page that can intake n players and persist the data
- [X] Create a Python script that can intake n players
- [X] Allow input differentiation between players and D/STs
- [X] Correctly grab relevant fantasy stats for D/STs
- [X] Write algorithm to translate estimated player stats into projected fantasy football points
- [X] Improve algorithm to return ideal starting lineup based on predetermined team size and player amount
- [X] Update frontend to send input players to the input of the Python script
- [X] Find a way to inject precreated odds info to avoid using API requests
- [X] Update Python script to return ideal lineup to the frontend
- [X] Update frontend to display the ideal lineup on-screen

## Planned Improvements

- [ ] Investigate why some players show 0 points

- [ ] Add ability to Super Flex (use QB as FLEX)
- [ ] Allow users to pick PPR, half-PPR, and Standard scoring
- [ ] Allow users to adjust point values for player stats (ie, change how many points per yard, value of a TD, etc)

- [ ] Rewrite backend to where players are a class to simplify code
- [ ] Improve backend code - add comments and simplify overly complex behavior
- [ ] Fine-tune estimated fantasy points by including more data points (ie, estimated defensive turnovers, estimated fumbles, etc)

- [ ] Improve formatting of entered players
- [ ] Improve formatting of ideal lineup
- [ ] Enhance UI to make interface prettier

- [ ] Divide components into more modularized pieces
- [ ] Rewrite front end with React, to learn React

## Completed Improvements

- [X] Allow users to adjust player amount (ie, 2 QB, 1 WR, etc)
- [X] Fix minimum position settings to percolate to backend
- [X] Automatically load player data into a JSON variable upon load
- [X] Add ability to automatically check the position, team, and upcoming opponent of each entered player
- [X] Add loading animation while backend calculates
- [X] Add a way to restrict odds for only the immediate next game being played
- [X] Use odds price to improve calculations on over/unders
- [X] Only show "Your Ideal Lineup" component when calculation is complete
- [X] Add button to frontend to signal to backend to use test JSON, or live data
- [X] Add a counter of remaining API calls to front end
- [X] Check all sports books until data is found, instead of only checking the first
- [X] Add error for backend to handle crashes/issues/missing API data during processing

## Tools Used

- [The Odds API](https://the-odds-api.com/)
- [Sports Data IO](https://sportsdata.io/)
- npm
- pip
- Python
- Vue
- Flask
