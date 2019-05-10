Author: Scott Butters
Description: Predicting flight cancellations

## Overview

Over 99% of all scheduled domestic flights take off, and the rest are very expensive. Of over 10 million flights scheduled flights each year, hundreds of thousands never leave the tarmac. At an average of $5770 in losses per cancellation this adds up to nearly a billion dollars of opportunity. While a significant chunk of those losses is unavoidable, it stands to reason that if an airline could confidently predict a cancellation far enough in advance, they could start taking measures to reduce those losses by doing things such as rebooking stranded passengers and rescheduling flight crews.

The aim of this project is to build a predictive model that can tell an airline that an upcoming flight will be cancelled at least a day before it actually happens.

The code in this notebook goes through all of the necessary steps to: 
* Download the required datasets
* Build a SQL database containing the data
* Process the data into features usable by machine learning models
* Join the data into a pandas DataFrame  design matrix
* Scrub and prepare the data for modeling
* Build, train, and tune models using cross validation
* Select a final model and predict it's effectiveness with a holdout dataset.