# Analysis-of-the-crisis-in-the-Gaming-market-using-NLP-and-Graph
This project aims to analyze the current crisis in the gaming industry, focusing on the mass layoffs in 2023 and 2024. We applied various Natural Language Processing (NLP) techniques, including Sentiment Analysis and Named Entity Recognition (NER), combined with graph analysis, to explore user sentiment, feedback, and discussions surrounding the topic on Reddit.

# Table of Contents
1- Project Overview 

Dataset

Methods

Data Collection

Preprocessing

Sentiment Analysis

Named Entity Recognition (NER)

Graph Analysis

Results

Conclusion

# Project Overview

The gaming industry has experienced significant layoffs, with over 10,000 jobs lost in 2023 and an additional 9,500 between January and May 2024. This project seeks to analyze user opinions and sentiment towards these events by gathering data from Reddit and applying various NLP and graph analysis techniques. The primary goals are to:

Understand user sentiment toward the layoffs and the current state of the gaming industry.
Identify the key concerns and criticisms expressed by users.
Investigate patterns of user interaction through graph analysis.

# Dataset

The data was collected from the Reddit community, specifically the r/gaming subreddit, which has over 40 million users. We selected seven posts related to the gaming industry's decline and layoffs, scraping around 3,000 comments.

# Methods:

Data Collection

We used the Apify web scraping platform to gather comments from seven relevant posts in the r/gaming subreddit. The posts included discussions about industry decline, layoffs, and consumer frustrations.

Preprocessing

The preprocessing steps involved:

Removal of deleted comments and missing values.
Cleaning of text by removing HTML tags, mentions, hashtags, numbers, and stopwords (excluding negations for sentiment accuracy).
Text normalization, including conversion to lowercase.

Sentiment Analysis

We employed the cardiffnlp/twitter-roberta-base model, a pre-trained version of RoBERTa fine-tuned on Twitter data, for sentiment classification. The model assigns comments to one of three categories: positive, negative, or neutral. Sentiment scores were also provided, offering a confidence level for each classification.

Named Entity Recognition (NER)

Using a pre-trained BERT model (dbmdz/bert-large-cased-finetuned-conll03-english), we performed NER to identify named entities such as organizations and video games mentioned in the comments. This helped us pinpoint which companies and games were frequently discussed in relation to the layoffs.

Graph Analysis

We applied graph techniques to examine the interaction patterns among users who commented on the selected Reddit posts. Metrics such as node degree, community detection, and message frequency were used to understand the structure of these discussions.

# Results

Sentiment Trends

31% of the comments expressed negative sentiment, indicating strong dissatisfaction with the gaming industry's current state.
The highest number of negative comments occurred in January 2024, correlating with the largest wave of layoffs.

Entity Recognition

Companies: The most frequently mentioned companies were generally perceived negatively, with the exception of Nintendo and Blizzard, which had more positive feedback.
Games: While most games were criticized, titles like Diablo and Overwatch received a relatively higher amount of positive feedback.

Graph Insights

Graph analysis revealed interesting interaction patterns, including:
Prominent discussions between a few highly active users.
Clustering of users into communities based on their interactions, with clear topic distinctions.

Technologies Used:

Python
Hugging Face Transformers
Apify for web scraping
NetworkX for graph analysis
Matplotlib for data visualization

# Conclusion

The project provided valuable insights into how the Reddit gaming community perceives the recent layoffs and broader industry issues. Sentiment analysis showed significant dissatisfaction, especially in early 2024. The NER and graph analyses helped highlight key companies, games, and user interactions.


