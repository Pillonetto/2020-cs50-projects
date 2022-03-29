// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 115;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //current word
    int index = hash(word);
    node* cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
            cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number with a terrible hash func
unsigned int hash(const char *word)
{
    int index;
    if (strlen(word) > 1)
        index = toupper(word[0]) + toupper(word[1]) - 65;
    else
        index = toupper(word[0]);

    return index;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    int initialized[N];
    for (int i = 0; i < N; i++)
        initialized[i] = 0;
    //create buffer where words will be read to
    char *buffer = malloc(LENGTH + 1);
    if (buffer == NULL)
        return false;
    //open dictionary file
    FILE* dict = fopen(dictionary, "r");
    if (dict == NULL)
        return false;

    //while the eof has not been reached
    while (fscanf(dict, "%s", buffer) != EOF)
    {
        //create new node
        node *n = malloc(sizeof(node));
            if (n == NULL)
                return false;
        n->next = NULL;
        //hash current word
        int index = hash(buffer);
        strcpy(n->word, buffer);
        
        if (initialized[index] == 0)
        {
            table[index] = n;
            initialized[index] = 1;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        

    }
    
    fclose(dict);
    free(buffer);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    //create int to keep track of word
    int counter = 0;

    for (int i = 0; i < N; i++)
    {
        //create traversal pointer to head
        node* cursor = table[i];

        //iterate across whole linked list until end  ----  count how many elements
        while (cursor != NULL)
        {
            cursor = cursor->next;
            counter++;
        }
    }
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    
    for (int i = 0; i < N; i++)
    {
        node* current = table[i];
        
        while (current != NULL)
        {
            node* cursor = current->next;
            free(current);
            current = cursor;
        }
        
        table[i] = NULL;
    }

    return true;

}

