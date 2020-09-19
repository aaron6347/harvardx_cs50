// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

// to count how many number of words there are
unsigned int count_word = 0;

// boolean of loaded dictionary or not
bool loaded = false;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    // a temporary copy of string to be check from original word
    char toCheck[strlen(word)];
    strcpy(toCheck, word);
    // make the word into all lowercase letters
    for (int i = 0; toCheck[i] != '\0'; i++)
    {
        toCheck[i] = tolower(toCheck[i]);
    }
    // get the hash value of word to be checked
    int index = hash(toCheck);
    // if there is no mispelling and exist in dictionary/hashtable
    if (table[index] != NULL)
    {
        // traverse the node to find the exact word due to possible collision of index in hashtable
        for (node *current = table[index]; current != NULL; current = current->next)
        {
            // compare the word of the current node and if the word is the exact, return true 
            if (strcmp(current->word, toCheck) == 0)
            {
                return true;
            }
        }
    }
    // if the word doesnt exist in dictionary/hashtable or there is mispelling, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int value = 0;
    int single;
    //traverse each character
    for (int i = 0; word[i] != '\0'; i++)
    {
        // if alphabet, -26 and +1 to make a-z as 1-26
        if (isalpha(word[i]))
        {
            single = word[i] - 'a' + 1;    
        }
        // if not alphabet set it as 27
        else
        {
            single = 27;
        }
        // hash function
        value = ((value << 3) + single) % N;
    }
    return value;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary
    FILE *file = fopen(dictionary, "r");
    // if the file doesnt exist, return false
    if (file == NULL)
    {
        return false;
    }
    // if file exist, proceed
    // pre-emptive the hashtable
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    char word[LENGTH + 1];
    node *nodepointer;
    // while there is still nextline
    while (fscanf(file, "%s", word) != EOF)
    {
        // create memory
        nodepointer = malloc(sizeof(node));
        // if no more memory, return false
        if (nodepointer == NULL)
        {           
            printf("Not enough space.");
            return false;
        }
        // if memory exist, proceed
        // copy the word into node struct
        strcpy(nodepointer->word, word);
        // find the hash value
        int index = hash(word);
        // insert this node as the new root of the bucket that points to previous root (if it exist, else NULL)
        nodepointer->next = table[index];
        table[index] = nodepointer;
        count_word++;
    }
    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // if dictionary isnt loaded, return 0
    if (!loaded)
    {
        return 0;   
    }
    // if dictionary is loaded, return the number of words in dictionary
    return count_word;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    // if the dictionary isnt loaded, return false
    if (!loaded)
    {
        return false;
    }
    // if the dictionary is loaded, proceed
    //traverse each hash value
    for (int i = 0; i < N; i++)
    {
        // if the bucket isnt empty
        if (table[i] != NULL)
        {
            node *current = table[i];
            // travere the linked list
            while (current != NULL)
            {
                node *temp = current;
                current = current->next;
                free(temp);
            }
        }
    }
    return true;
}
