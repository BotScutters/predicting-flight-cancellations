Predicting Flight Cancellations
==============

***Using machine earning to predict whether or not an upcoming flight will be canceled***

**Author:** *Scott Butters*

# Data Dictionary

The data for this project is derived from several sources. For information on the data as it comes in from these sources, consult the links below. The table beneath that describes the features I've constructed from those to use in modeling.

## Flight Records

My data set is primarily derived from the "[Marketing Carrier On-Time Performance](https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time#)" report released by the Bureau of Transportation Statistics. This database contains information on nearly every flight conducted by a significant U.S. carrier dating back to January 1987.

As that amount of data is pretty unwieldy for a prototype, for the purposes of this project I've narrowed the scope to only making predictions on flights departing from the start of 2007 to the end of 2018.

## Weather Records

To supplement the flight data, the model also makes use of historical weather data for the same time duration. This weather data is acquired via the Dark Sky API, and gives hourly records of precipitation, temperature, wind, visibility, and more. 

## Design Matrix

| Feature                     | Description                                                  | Type       | Purpose |
| --------------------------- | ------------------------------------------------------------ | ---------- | ------- |
| cancelled                   | Whether or not the scheduled flight was cancelled            | Boolean    | Label   |
| est_time                    | Planned time in air, in minutes                              | Continuous | Feature |
| distance                    | Planned distance of flight                                   | Continuous | Feature |
| cr_1d_ago                   | Cancellation rate on the day 1 day prior to flight           | Continuous | Feature |
| cr_1w_ago                   | Cancellation rate on the day 1 week prior to flight          | Continuous | Feature |
| cr_4w_ago                   | Cancellation rate on the day 4 weeks prior to flight         | Continuous | Feature |
| cr_52w_ago                  | Cancellation rate on the day 52 weeks prior to flight        | Continuous | Feature |
| {feature}\_cr\_{time}_ago   | Cancellation rate by this {feature} on the day {time} prior to flight<br />Features as per above include<br />* Reporting airline<br />* Destination<br />* Departure time block<br />* Arrival time block<br />* Aircraft tail number<br />Time spans include<br />* 1 day<br />* 1 week<br />* 4 weeks<br />* 52 weeks | Continuous | Feature |
| 7_day_CR_avg                | Cancellation rate over the 7 days prior to flight            | Continuous | Feature |
| 30_day_CR_avg               | Cancellation rate over the 30 days prior to flight           | Continuous | Feature |
| 365_day_CR_avg              | Cancellation rate over the 365 days prior to flight          | Continuous | Feature |
| {time}\_CR_avg_by_{feature} | Cancellation rate by this {feature} over the {time} prior to flight<br />Features as per above include<br />* Reporting airline<br />* Destination<br />* Destination city market<br />* Departure time block<br />* Arrival time block<br />* Time spans include<br />* 7 days<br />* 30 days<br />* 365 days | Continuous | Feature |

In addition to the above features, the data also constructs two sets of weather features. The first set is taken directly from the Dark Sky API, and provides observations of weather statistics from 24 hours prior to the scheduled flight departure. I additionally constructed a proxy features to simulate a weather forecast for the actual time of departure, since this data was not readily available. All of these features are prefixed by the "forecast_" designator and simply take the actual observed measurements and apply a small amount of noise to the observations to induce error.

