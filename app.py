import os
import csv

# Tie Management Strategy
# Plurality: Select first among tied candidates
# Plurality with Runoff: Select first among tied candidates
# Condorcet: Cannot have a tie if there is a winner
# Borda Count: Select first among tied candidates

# Print the ballot summary, showing unique ballots and their counts
def PrintBallotSummary(preferences, n, m):
    print("Ballot Summary:")
    print(f"Number of voters: {n}, Number of candidates: {m}")
    counts = {}
    for row in preferences:
        cells = [str(x).strip().upper() for x in row if x is not None and str(x).strip() != ""]
        key = " > ".join(cells)
        counts[key] = counts.get(key, 0) + 1
    for ballot, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{ballot} : {count} votes")
    print()

# Assume that the CSV file is formatted properly
# There will be no other validation other than checking for the number of voters and candidates
def ReadPreferences(file_path):
    preferences = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            preferences.append(row)

    n = len(preferences)
    if n > 200:
        raise ValueError(f"number of voters n={n} exceeds 200")

    m = len(preferences[0])
    if m > 20:
        raise ValueError(f"number of candidates m={m} exceeds 20")

    return preferences, n, m

def Plurality(preferences):
    vote_count = {}
    for preference in preferences:
        first = preference[0]
        vote_count[first] = vote_count.get(first, 0) + 1

    winner = max(vote_count, key=vote_count.get)
    return winner, vote_count

def PluralityRunoff(preferences, n):
    # First Round
    # if a candidate gets > 50% in first round, then the candidates automatically wins
    first_round_winner, vote_count = Plurality(preferences)
    if vote_count[first_round_winner] > n / 2:
        return first_round_winner

    # Second Round
    # the top two candidates from the first round go to the second round
    top_two = sorted(vote_count.items(), key=lambda x: x[1], reverse=True)[:2]
    candidate1, candidate2 = top_two[0][0], top_two[1][0]
    runoff_count = {}

    # loop through all the candidates and the first among the top two will increment the count
    for preference in preferences:
        for candidate in preference:
            if candidate == candidate1:
                runoff_count[candidate1] = runoff_count.get(candidate1, 0) + 1
                break
            elif candidate == candidate2:
                runoff_count[candidate2] = runoff_count.get(candidate2, 0) + 1
                break

    winner = max(runoff_count, key=runoff_count.get)
    return winner

def Cordocet(preferences, m):
    # the candidate that wins against all other candidates in pairwise comparison is the winner
    # this tracks the number of pairwise wins for each candidate
    # It is possible that there is no Cordocet winner
    cordocet_count = {}
    candidates = preferences[0] 
    for i in range(m):
        for j in range(i+1, m):
            candidate1 = candidates[i]
            candidate2 = candidates[j]
            votes1 = 0
            votes2 = 0

            for preference in preferences:
                if preference.index(candidate1) < preference.index(candidate2):
                    votes1 += 1
                else:
                    votes2 += 1

            if votes1 > votes2:
                cordocet_count[candidate1] = cordocet_count.get(candidate1, 0) + 1
            elif votes2 > votes1:
                cordocet_count[candidate2] = cordocet_count.get(candidate2, 0) + 1

    cordocet_winner = max(cordocet_count, key=cordocet_count.get)
    if cordocet_count[cordocet_winner] == m - 1:
        return cordocet_winner
    else:
        return None

def BordaCount(preferences, m):
    # assign points based on the rank of each candidate in each voter's preference list
    # the one with the lowest total points wins (can be reversed to higher too based on implementation)
    borda_count = {}
    for preference in preferences:
        for i in range(m):
            candidate = preference[i]
            borda_count[candidate] = borda_count.get(candidate, 0) + i

    winner = min(borda_count, key=borda_count.get)
    return winner, borda_count

def run_elections(preferences, n, m):
    PrintBallotSummary(preferences, n, m)

    if (voter_conditions_met(preferences, n)):
        print("Conditions met. Running elections...")
    else:
        print("Conditions not met. Aborting elections.")
        return

    # Plurality Voting
    plurality_winner, _ = Plurality(preferences)
    print("Winner of Plurality:", plurality_winner)

    # Plurality with Runoff Voting
    plurality_runoff_winner = PluralityRunoff(preferences, n)
    print("Winner of Plurality with Runoff:", plurality_runoff_winner)

    # Condorcet Voting
    condorcet_winner = Cordocet(preferences, m)
    print("Winner of Condorcet:", condorcet_winner)

    # Borda Voting
    borda_winner, _ = BordaCount(preferences, m)
    print("Winner of Borda Count:", borda_winner)

def voter_conditions_met(preferences, n):
    best_candidate_count = {}
    worst_candidate_count = {}
    
    for preference in preferences:
        best = preference[0]
        worst = preference[-1]
        best_candidate_count[best] = best_candidate_count.get(best, 0) + 1
        worst_candidate_count[worst] = worst_candidate_count.get(worst, 0) + 1

    # No more than 50% of voters has the same "best candidate"
    if any(count > n * 0.5 for count in best_candidate_count.values()):
        return False

    # No more than 40% of voters has the same "worst candidate" 
    if any(count > n * 0.4 for count in worst_candidate_count.values()):
        return False

    return True

##### RUN THE ELECTIONS #####
print("\nSAMPLE DATASET WITH 27 VOTERS")
preference_data_27 = ReadPreferences('data/27-voters.csv')
run_elections(*preference_data_27)

print("\nSAME WINNER FOR ALL METHODS")
preference_data_same_winner = ReadPreferences('data/same_winner.csv')
run_elections(*preference_data_same_winner)

print("\nDIFFERENT WINNER FOR EACH METHOD")
preference_data_different_winner = ReadPreferences('data/different_winner.csv')
run_elections(*preference_data_different_winner)
