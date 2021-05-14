# Assignment2
## Application of machine learning
This project applies the basic machine learning method to option trading.

The 510050.sh option is taken as the research object, and the database option.db contains the historical date data corresponding to the option. The data from July 1, 2016 to July 1, 2019 is taken as the training set, and the data from July 1, 2019 to March 30, 2021 is taken as the test set.

### The first step
First of all, according to the data of the near month contract on each trading day, we calculate the expiration days of the near month contract, and then calculate its skewness. For each expiration day, as long as the backtest interval is long enough, we can calculate enough skewness values for subsequent signal judgment.

For each trading day, we use the difference of implied volatility between the options with delta = 0.5 and the options with delta = 0.25 as skewness. Because there is no option contract with delta equal to 0.5 or 0.25 in the market, we can calculate the Delta and implied volatility of the options corresponding to each exercise price, So we can use the difference method to calculate the corresponding volatility when delta = 0.5 and delta = 0.25. After calculating the skewness, we need to divide it according to the number of days away from the due date, and calculate the corresponding skewness quantile value of each number of days away from the due date.

Finally, we get the following results: the first figure shows the skewness of call options, and the quantile values of the three broken lines are 0.8, 0.5 and 0.2. The first figure shows the skewness of the call option, with three broken lines corresponding to quantiles of 0.9, 0.5 and 0.1. The first figure shows the skewness of the call option, with three broken lines corresponding to quantiles of 0.8, 0.5 and 0.2. The first figure shows the skewness of the call option, with three broken lines corresponding to quantiles of 0.9, 0.5 and 0.1. The points in the figure are the skewness values measured on each trading day.


