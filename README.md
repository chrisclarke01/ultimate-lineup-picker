# Ultimate Lineup Picker

Ultimate Lineup Picker is a tool that uses Sportsbook player props to determine the ideal fantasy football lineup. By analyzing how Vegas believes players will perform, ULP can infer fantasy points scored. When given a team of players, ULP will use these inferences to generate the ideal lineup for the upcoming week of play.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Steps](#project-steps)
- [Planned Improvements](#planned-improvements)
- [Housekeeping](#housekeeping)
- [Tools Used](#tools-used)

## Development Setup

To set up your development environment for this project, follow these steps:

1. Clone repository
2. Ensure Python and Vue are installed
3. To install frontend, navigate to frontend/ and enter `npm install -g @vue/cli`
4. Acquire API keys and set them as an environment variable named `ODDS_API_KEY`

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

- [ ] Divide components into more modularized pieces
- [ ] Only show "Your Ideal Lineup" component when calculation is complete
- [ ] Improve formatting of entered players
- [ ] Improve formatting of ideal lineup
- [ ] Enhance UI to make interface prettier
- [ ] Add a counter of remaining API calls to front end
- [ ] Rewrite backend to where players are a class to simplify code
- [ ] Improve backend code - add comments and simplify overly complex behavior
- [ ] Fine-tune estimated fantasy points by including more data points (ie, estimated defensive turnovers, estimated fumbles, etc)
- [ ] Add loading animation while backend calculates
- [ ] Allow users to pick PPR, half-PPR, and Standard scoring
- [ ] Allow users to adjust point values for player stats (ie, change how many points per yard, value of a TD, etc)
- [ ] Allow users to adjust player amount (ie, 2 QB, Super Flex, 1 WR, etc)
- [ ] Add ability to automatically check the position, team, and upcoming opponent of each entered player

## Completed Improvements

- [X] Add a way to restrict odds for only the immediate next game being played
- [X] Use odds price to improve calculations on over/unders

## Housekeeping

- Properly document APIs and used tools in Tools Used
- Add a license
- Improve Development Setup to outline all necessary steps
- Add proper documentation
- Modularize frontend and backend to be better organized and maintainable

## Tools Used

- npm
- Python
- Vue
