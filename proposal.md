# Project McNulty Proposal:

## Aviation is Really Taking Off…Usually

_Scott Butters_

### Overview

In February of 2019, tens of thousands of domestic flights carried passengers around the country—every single day. Tens of thousands of aircraft being carefully tracked, monitored, organized and directed, and hundred of thousands or even millions of passengers count on those planes to get them where they're going. It's an incredible system, and most of the time it actually works. But when it doesn't, it hurts. Flight cancellations are extremely expensive, costing airlines a $1 billion per year. While flight cancellations due to weather may be inevitable, a significant portion of cancellations are due to circumstances under _our_ control. Modern air traffic control is a hundred years in the making and has certainly worked to minimize this issue already, but…can we do better?

### Question

Using data on American commercial flights, can we predict when a cancellation is likely to occur?

As a bonus, can we predict _why_ the cancellation will occur?

### Data Sources

My data set will be primarily based around the "[Marketing Carrier On-Time Performance](https://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=120&DB_URL=)" report released by the Bureau of Transportation Statistics. This database contains information on nearly every flight conducted by a significant U.S. carrier dating back to January 2018, which amounts to approximately 8 million observations. I expect I will supplement this dataset with additional features such as weather forecasts preceding a flight and additional statistics surrounding the model of plane for each flight.

### Features

In order to predict a whether a flight will be canceled, I indend to use at least some of the following features, and potentially more. In order to prevent data leakage and keep the data being used realistic and actionable, no observation will be allowed data that wouldn't have been available 24 hours in advance of the flight's departure. All time-related features are described from the perspective of 24 hours prior to the flight's planned departure time.

| Feature                               | Description                                                  | Type        | Purpose |
| ------------------------------------- | ------------------------------------------------------------ | ----------- | ------- |
| Airline ID                            | ID number to identify unique airline                         | Categorical | Key     |
| AL_C_rate_day                         | Flight cancellation rate by this airline at this airport over past 24 hours | Continuous  | Feature |
| AL_C_rate_7                           | Flight cancellation rate by this airline on this weekday 1 week ago | Continuous  | Feature |
| AL_C_avg_rate_week                    | Flight cancellation rate by this airline at this airport over past 7 days | Continuous  | Feature |
| AL_C_rate_28                          | Flight cancellation rate by this airline on this weekday 4 weeks ago | Continuous  | Feature |
| AL_C_avg_rate_month                   | Flight cancellation rate by this airline at this airport over past 30 days | Continuous  | Feature |
| AL_C_rate_364                         | Flight cancellation rate by this airline on this weekday 52 weeks ago | Continuous  | Feature |
| AL_C_avg_rate_year                    | Flight cancellation rate by this airline at this airport over past 365 days | Continuous  | Feature |
| Tail number                           | Unique airplane identifier ID                                | Categorical | Key     |
| AP_C_rate_day                         | Flight cancellation rate by this airplane over past 24 hours | Continuous  | Feature |
| AP_C_rate_7                           | Flight cancellation rate by this airplane on this weekday 1 week ago | Continuous  | Feature |
| AP_C_avg_rate_week                    | Flight cancellation rate by this airplane at this airport over past 7 days | Continuous  | Feature |
| AP_C_rate_28                          | Flight cancellation rate by this airplane on this weekday 4 weeks ago | Continuous  | Feature |
| AP_C_avg_rate_month                   | Flight cancellation rate by this airplane at this airport over past 30 days | Continuous  | Feature |
| AP_C_rate_364                         | Flight cancellation rate by this airplane on this weekday 52 weeks ago | Continuous  | Feature |
| AP_C_avg_rate_year                    | Flight cancellation rate by this airplane at this airport over past 365 days | Continuous  | Feature |
| Origin Airport ID                     | Unique airport identifier ID for flight origin               | Categorical | Key     |
| orig_C_rate_day                       | Flight cancellation rate for flights departing from origin airport over past 24 hours | Continuous  | Feature |
| repeat same pattern as above          |                                                              |             |         |
| Origin City Market                    | ID for area that may be served by several airlines           | Categorical | Key     |
| OCM_C_rate_day                        | Flight cancellation rate for flights departing from origin city market over past 24 hours | Continuous  | Feature |
| repeat same pattern as above          |                                                              |             |         |
| Dest Airport ID                       | Unique airport identifier ID for destination                 | Categorical | Key     |
| dest_C_rate_day                       | Flight cancellation rate for flights heading to destination airport over past 24 hours | Continuous  | Feature |
| repeat same pattern as above          |                                                              |             |         |
| Dest City Market                      | ID for area that may be served by several airlines           | Categorical | Key     |
| DCM_C_rate_day                        | Flight cancellation rate for flights heading to destination city market over past 24 hours | Continuous  | Feature |
| repeat same pattern as above          |                                                              |             |         |
| Departure time                        | Scheduled departure time                                     | ?           |         |
| Airtime                               | Planned time in air, in minutes                              | Continuous  |         |
| Distance                              | Planned route distance                                       | Continuous  |         |
| On-time incoming arrival percentage   | Percent of flights that arrive at departure airport on-time  | Continuous  |         |
| On-time outgoing departure percentage | Percent of flights that depart from departure airport on-time | Continuous  |         |
| Historical cancellation percentages   | All time average                                             | Continuous  |         |
|                                       | 1 day ago                                                    | Continuous  |         |
|                                       | 7 days ago                                                   | Continuous  |         |
|                                       | 30 days ago                                                  | Continuous  |         |
|                                       | 364 days ago                                                 | Continuous  |         |
|                                       | For this airline                                             | Continuous  |         |
|                                       | From this airport                                            | Continuous  |         |
|                                       | To that airport                                              | Continuous  |         |
|                                       | On this airplane (tail number)                               | Continuous  |         |
|                                       | On this airplane model                                       | Continuous  |         |
| Historical delays (goes back to 2003) | The average number of minutes that a similar incoming flight has been delayed (in minutes) over the avove time periods, for the reasons: carrier delay, weather delay, national air system delay, security delay, and late aircraft delay |             |         |
|                                       |                                                              |             |         |
| Weather Forecast                      | What the weather forecast was ~24 hours ago, in degrees      | Continuous  |         |
| Other airline/craft statistics        |                                                              |             |         |
| Cancelled                             | Boolean for whether or not flight is cancelled, 1=Yes        | Boolean     |         |
| Cancellation Code                     | Reason for cancellation (carrier, weather, national air system, security) | Categorical |         |

I recognize that the continuous features here are a bit of a limited window of predictors. I'll keep searching for additional data that might reasonably augment this dataset, as well as considering whether there are other meaningful continuous predictors I can construct from this dataset.

### Methods

I plan to try a handful of classifier algorithms on this project, including KNN, logistic regression, decision trees and random forest.

### Stretch Goals

If I'm able to predict cancellations with even a moderate level of success, I'd also like to predict additional features, such as the reason for the cancellation. A much more significant change would be also trying to make predictions on the delays of flights.

### Further Insights

By analyzing the results of my most effective model(s), I should be able to extract not only an estimate of which flights will be cancelled, but also probability estimates that each flight will be cancelled. This is a critical number detail to pay attention do, as an airline would want to know how likely a cancellation is to occur if it's to take action in response to the prediction. We can additionally glean insights about what factors contribute most to preventable cancellations in order to focus on what can be changed or improved.

### Known Challenges

Only about 2% of flights are actually cancelled, which means that the dataset is very imbalanced for the target I'm seeking to classify. This will make accuracy not a very meaningful metric and require that I think carefully about which metric to optimize. Additionally, there are a lot of reasons a flight could be cancelled, and I certainly don't know all of them. There are obviously sources of data out there (such as an aircraft's service and maintenance record or the details of how an airline actually makes the decision to cancel a flight) that could greatly help in a prediction setup like this that I simply won't have access to. And then of course there are the cancellations that occur for reasons seemingly emerging from chaos (or weather, which is actually most cancellations). I certainly don't expect to be able to predict all of the cancellations that occur. But predicting any with a reasonably high confidence could be worthwhile.