#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    // traverse all candidates struct
    for (int i = 0; i < candidate_count; i++)
    {
        // if the name exist in candidates struct, increment his/her votes and return
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    // if the name is not in candidates struct
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    // to store all candidate winner(s)
    string winner_name[candidate_count];
    // to find real number of total winner and indexing for winner_name
    int index = 0;
    // to compare who has the higher vote
    int winner_vote = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        // if the candidate has the same highest number of vote, include his/her name
        if (candidates[i].votes == winner_vote)
        {
            winner_name[index] = candidates[i].name;
            index++;
        }
        // if the candidate has a better number of vote, empty the winner_name array and include his/her name
        else if (candidates[i].votes > winner_vote)
        {
            // include his/her name
            winner_name[0] = candidates[i].name;
            winner_vote = candidates[i].votes;
            // clear other names
            for (int j = 1; j < index; j++)
            {
                winner_name[j] = "";
            }
            // reset index
            index = 1;
        }
    }

    // display winner
    // traverse the winner_name and display each name
    for (int i = 0; i < index; i++)
    {
        printf("%s\n", winner_name[i]);
    }
    return;
}
