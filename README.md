ComputeSimilarity
=================

A program to compute similarity of two documents

#### TODO

- ~~git repo setup~~ 0408
- ~~some initial research and idea search, decide the topic~~ 0408
- ~~setup working environment~~ 0408
- ~~collect some twitter data~~ 0409
- ~~learn some nltk and scikit-learn basics~~ 0410
- ~~my first similarity calculator?~~ 0410
- ~~get more tweets for each tag~~ 0410
- try to explain the results
- try another calculator

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

#### 04092014 9:30-11pm

- tokenization: split texts on non-alphabetic characters
    - token: a set of consecutive words, unigram, bigram...
    - co-occurent: simple phrases
    - stopwords: useless tokens? such as the, a, are
        - for twitter: rt
- lemmatization: Problem of finding the correct dictionary headword form
    - e.g. plural, past tense
    - stemming: change them back to the core words they are made up, chop down affixes from the stem!
- document frequency
    - salient words: high count in the doc + low count across docs

play nltk

- many hashtags are high frequency words

#### 04102014 4-6:30pm, 7:30-9pm, 10-10:30pm

doc similarity

- **salient words**: TF x IDF
- term frequency (TF): `TF(x) = log10(1+c(x)) or c(x)` - high occurrence within doc
- inverse document freq (IDF): `IDF(x) = log10(Ndocs/DF(x))` - low occurrence across docs
- for each doc, `D = [w1, w2, ...]`, where `w` is tfidf score of a token
- cosine similarity: `D1 x D2 / (sqrt(D1^2) x sqrt(D2^2))`

play nltk

- `rt` occurs a lot, and different hashtags have different amount of occurrence of `rt`. itself could be an interesting thing to look at
- is 100 tweets enough for similarity analysis?
- stemming: Porter Stemmer

### first similarity calculator

- given 2 hashtags as input, obtain 100 tweets per tag
- cleaning: lower all characters, remove punctuation, stemming, tokenize
- compute tfidf of 2 docs using scikit-learn
- 6 hashtags are used `#heartbleed #ssl #nba #ncaa #ladygaga #justinbieber`, and I compared each 2 of them

![First similarity calculator 100 tweets](images/hashtag_similarity100.png)

The highest score is `#heartbleed v. #ssl`, 0.538. The second one makes sense too. Then some weird paris such as `#nba v. #ssl` ranked higher than `#ladygaga v. #justinbieber`, which is supposed to be very similar (is that so?). I also computed the same scores for each pair with 2000 tweets per tag.

![First similarity calculator 2000 tweets](images/hashtag_similarity2000.png)

Apparently I have met the cap of twitter API after pulling several times of 2000 tweets. We could see that the first and second ranking did not change. Now `#ladygaga v. #justinbieber` surpasses all other weird pairs, but it does not differ much from `#nba v. #heartbleed`.
