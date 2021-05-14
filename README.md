# Assignment2
## Application of machine learning
This project applies the basic machine learning method to option trading.

The 510050.sh option is taken as the research object, and the database option.db contains the historical date data corresponding to the option. The data from July 1, 2016 to July 1, 2019 is taken as the training set, and the data from July 1, 2019 to March 30, 2021 is taken as the test set.

### step 1: get skewness quantile
First of all, according to the data of the near month contract on each trading day, we calculate the expiration days of the near month contract, and then calculate its skewness. For each expiration day, as long as the backtest interval is long enough, we can calculate enough skewness values for subsequent signal judgment.

For each trading day, we use the difference of implied volatility between the options with delta = 0.5 and the options with delta = 0.25 as skewness. Because there is no option contract with delta equal to 0.5 or 0.25 in the market, we can calculate the Delta and implied volatility of the options corresponding to each exercise price, So we can use the difference method to calculate the corresponding volatility when delta = 0.5 and delta = 0.25. After calculating the skewness, we need to divide it according to the number of days away from the due date, and calculate the corresponding skewness quantile value of each number of days away from the due date.

Finally, we get the following results: the first figure shows the skewness of call options, and the quantile values of the three broken lines are 0.8, 0.5 and 0.2. The second figure shows the skewness of the call option, with three broken lines corresponding to quantiles of 0.85, 0.5 and 0.15. The third figure shows the skewness of the put option, with three broken lines corresponding to quantiles of 0.8, 0.5 and 0.2. The fourth figure shows the skewness of the put option, with three broken lines corresponding to quantiles of 0.85, 0.5 and 0.15. The points in the figure are the skewness values measured on each trading day.
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/iv_diff_call(quantile%3D0.8and0.2).png)
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/iv_diff_call(quantile%3D0.85and0.15).png)
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/iv_diff_put(quantile%3D0.8and0.1).png)
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/iv_diff_put(quantile%3D0.85and0.15).png)


### step 2： backtesting 

Since we can't directly purchase the options with delta = 0.5 and delta = 0.25 from the market, we need to configure them according to the existing options.

According to the existing options in the market, the delta corresponding to each k value is calculated

let

<p align="center">delta_ 1 = max{ delta | if delta<0.25}</p>
<p align="center">delta_ 2 = min{ delta | if delta>0.25}</p>
<p align="center">delta_ 3 = max{ delta | if delta<0.5}</p>
<p align="center">delta_ 4 = min{ delta | if delta>0.5}</p>

Calculate P1, P2, P3, P4 by the following equation

<p align="center">p1+p2 =1</p>
<p align="center">p3+p4 =1</p>
<p align="center">delta_ 1*p1+delta_ 2*p2 = 0.25</p>
<p align="center">delta_ 3*p2 +delta_ 3*p2 = 0.5</p>

So we can use P1 option 1, P2 option 2 to configure an option with delta = 0.25, and P3 option 1, P4 option 2 to configure an option with delta = 0.5. The next step is to conduct a back test.

We compare the skew calculated with the 0.8-quantile, 0.5-quantile and 0.2-quantile  of skewness from training data to determine whether to open or close the position.

The following two combination diagrams show the back test results of call option trading and put option trading respectively.

<p align="center">**call**</p>
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/skew_arbitrage(call).png)

<p align="center">**put**</p>
![Image text](https://github.com/algo21-220040088/Assignment2/blob/main/result/pictures/skew_arbitrage(put).png)

In the top figure, the broken line represents the quantile value of skewness, and the point represents the skewness value calculated on the trading day. The red dot indicates that skew is at a historical high. On this trading day, you should short the portfolio options with delta = 0.25 and long the portfolio options with delta = 0.5. The blue dot indicates that there is no arbitrage possibility on the trading day, so it does not choose to open a position. The green dot indicates that skew is at a historical low. On this trading day, we should short the portfolio options with delta = 0.5 and long the portfolio options with delta = 0.25.
