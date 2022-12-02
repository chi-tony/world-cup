# Simulate a sports tournament

import csv
import sys
import random
import math

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []

    # Read teams into memory from file
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Assign team name under "team" key
            team = row["team"]

            # Assign team rating under "rating" key as an integer
            rating = int(row["rating"])

            # Add name and rating as a dictionary into the teams list
            teams.append({"team":team, "rating":rating})

    counts = {}

    # Simulate N tournaments and keep track of win counts
    for i in range(N):
        # In each iteration, simulate tournament and check if winner is already in counts list
        current_winner = simulate_tournament(teams)

        # If already in counts, increment win total by 1
        if current_winner in counts:
            counts[current_winner] += 1

        # If not already in counts, add to counts with 1 win
        else:
            counts[current_winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # Calculate the number of rounds necessary based on the number of teams
    rounds = round(math.log(len(teams), 2))
    remaining_teams = teams

    # Iterate through each round and simulate with the remaining teams recursively
    for i in range(rounds):
        remaining_teams = simulate_round(remaining_teams)

    # Determine name of winning team
    winning_team = remaining_teams[0]["team"]

    return winning_team


if __name__ == "__main__":
    main()
