from model.skew.strategy_call import skew_arbitrage_call
from model.skew.strategy_put import skew_arbitrage_put
import matplotlib.pyplot as plt

if __name__ == '__main__':
    start_date = 20190701
    end_date = 20210330
    x1, y1 = skew_arbitrage_call(start_date, end_date)
    x2, y2 = skew_arbitrage_put(start_date, end_date)
    y = [i+j for (i, j) in zip(y1, y2)]
    plt.plot(x1, y1, color='yellow')
    plt.plot(x1, y2, color='blue')
    plt.plot(x1, y, color='green')
    plt.legend(['call','put','call + put'])
    plt.show()
