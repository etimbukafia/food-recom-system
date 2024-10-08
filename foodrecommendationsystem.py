# -*- coding: utf-8 -*-
"""FoodRecommendationSystem.ipynb

# **Food Recommendation System**
Recommendation of the 5 most similar dishes based on Cosine Similarity with a dish taken as input.
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

df = pd.read_csv('dataset/1662574418893344.csv')
df.head()

# To find number of dishes in the dataset
num_of_dishes = len(list(df['Name'].unique()))
num_of_dishes

# Categories
cat = df['C_Type'].unique()
cat

df.info()

# Cleaning of description
def cleaning(text):
  text = text.lower()
  text  = "".join([char for char in text if char not in string.punctuation])
  return text

df['Describe'] = df['Describe'].apply(cleaning)

# Duplicate Data
df.duplicated().sum()

# Null Data
df.isnull().sum()

"""# **Content Based Filtering**
Recommendation based on the Description of the dishes
"""

vect = TfidfVectorizer(stop_words='english')
X = vect.fit_transform(df['Describe'])

cosine_sim = linear_kernel(X, X)
cosine_sim

food_items = pd.Series(df.index, index=df['Name']).drop_duplicates()
food_items

def food_recommendations(title, cosine_sim = cosine_sim):
    food_index = food_items[title]
    similarity_scores = list(enumerate(cosine_sim[food_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Scores for the five most similar dishes
    # Index 0 is the dish itself
    most_recommended_scores = similarity_scores[1:6]

    most_recommended_dishes = [i[0] for i in most_recommended_scores]
    return df['Name'].iloc[most_recommended_dishes]

print(food_recommendations('tricolour salad'))

"""# **Content Based Filtering: Advanced**
Based on Category, Vegetarian/ Non-Vegetarian, Description
"""

food_features = ['C_Type', 'Veg_Non', 'Describe']

def features_column(x):
    return x['C_Type'] + " " + x['Veg_Non'] + " " + x['Describe']

# Column with all the features to dataframe df
df['features'] = df.apply(features_column, axis=1)

df.head()

vect2 = TfidfVectorizer(stop_words='english')
vect_X = vect2.fit_transform(df['features'])
print(type(vect_X))

# Veg_Non = pd.get_dummies(df['Veg_Non'])
# X2 = vect_X.join(Veg_Non)
cosine_similarity2 = linear_kernel(vect_X, vect_X)

df = df.reset_index()
food_items = pd.Series(df.index, index=df['Name'])

print(food_items)

print(food_recommendations('tricolour salad', cosine_similarity2))