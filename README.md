# Voting Methods Practical

This repository includes a Python script implementing four voting methods for ranked voting data stored in CSV files.

## Requirements

- Python 3.x  

## Usage

### 1. Voting Methods Script

**File:**  
`app.py`

**Description:**  
Reads ranked-choice ballots from CSV files and determines the winner according to several electoral systems: Plurality, Plurality with Runoff, Condorcet, and Borda Count. Includes validation for input size and distribution of best/worst votes.

**How to run:**  python voting_methods.py

**Output:**  
For each test dataset, the script prints:
- Ballot summary (number of voters/candidates, distinct ballot types, vote counts)
- Validation check results
- Winner under each of:
  - Plurality  
  - Plurality with Runoff  
  - Condorcet  
  - Borda Count

**Sample datasets referenced:**  
- `data/27-voters.csv`  
- `data/same_winner.csv`  
- `data/different_winner.csv`

## CSV Format

Ballot files must be in CSV format, with each line representing a voter's preferences **from most preferred to least preferred**. Each value is a candidate’s letter identifier (e.g., `A`, `B`, `C`, etc.), and every row must contain the same number and order of unique candidates.

**Example:**

A,C,E,F,G,H,D,B
A,C,E,F,G,H,D,B
B,D,E,F,G,H,C,A
D,B,E,F,G,H,A,C
E,D,B,C,F,G,H,A
C,D,E,F,G,H,A,B
F,G,H,A,B,C,D,E

The above example represents seven voters, each specifying their complete ranking of eight candidates.

## Notes

- Input files must be in CSV format and contain no more than **200 voters** (rows) and **20 candidates** (columns).
- Each row should represent a full ranking for a voter; it is assumed that there are no missing entries or extra whitespace.
- The script enforces that no more than **50% of voters** can rank the same candidate best, and no more than **40%** can rank the same candidate worst, or the election is aborted.

