ComputeSimilarity
=================

A program to compute similarity of two documents

#### TODO

- ~~git repo setup~~ 0408
- ~~some initial research and idea search, decide the topic~~ 0408
- ~~setup working environment~~ 0408
- ~~collect some twitter data~~ 0409
- learn some nltk and play with the data
- my first similarity calculator?

#### 04082014 11-12pm

- what is the problem
    - object: document
    - compute similarity of x documents
- what is document similarity?
    - 2 documents have same set of words?
    - 2 documents carry same meaning?
    - document classification?
- what could be document?
    - similarity between 2 linkedIn profiles
    - similarity between a linkedIn profile and a job opening
    - similarity between 2 Twitter hashtags (e.g. comparing tweets containing those 2 tags)

My current take:
How to compute similarity of two Twitter hashtag?

- why  
    - sounds hard: hashtags are short, they contain little information to be compared
    - useful: hashtags are mostly events/entities, by clustering them (hopefully) could eventually bring us some patterns in how events formed in Twitter
        - feel like didnt make this clear enough, need to think about it
- how
    - we could examine tweets containing either hashtag
        - if tweets are similar, it is likely 2 hashtags are similar two (need some validation)
        - let's fix number of tweets to compare to 100 for now
    - other ways?

Tools

- NLTK
- http request lib (for Twitter API)

#### 04092014 5-6pm

the program

- take 2 inputs: 2 strings, representing hashtag
- use Twitter search API to obtain first 100 tweets for each hashtag
    - API secrets store separately
    - search only English and medium-level tweets
- do I remove links and names? leave them there for now.

similarity calculator 1

- combine all 100 tweets into a paragraph
- then count frequency of each word?

miscs

- could only compare entities of 2 hashtags
