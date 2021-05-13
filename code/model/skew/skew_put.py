import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from dateutil.parser import parse
from basic_function.calc_Greek import calc_put_delta
from basic_function.calc_implied_volatility import put_implied_vol


def skew_put(option_string='510050.SH', start_date=20190701, end_date=20210330):
    R = 0.02
    # k_all = []
    # s0_all = []

    # 连接数据库，选出所有交易日
    my_db = sqlite3.connect(r'D:\pc\Desktop\Algo_Trading\Assignment2\data\raw\option.db')
    c = my_db.cursor()
    sql = f"SELECT DISTINCT trade_dt\nFROM OPTION_LOCAL ol\nwhere TRADE_DT>={start_date} " \
        f"and TRADE_DT <={end_date}\norder by TRADE_DT"
    c.execute(sql)
    trade_dt_total = c.fetchall()
    trade_dt_total = [i[0] for i in trade_dt_total]

    # 获取etf每天的收盘价
    etf_daily_close_df = pd.read_csv(r'D:\pc\Desktop\Algo_Trading\Assignment2\data\raw\eft_daily_close.csv')
    etf_daily_close_df.set_index(['date'], inplace=True)

    # 定义一个字典储存到期天数及其对应的iv_diff
    iv_diff_all = {}

    # 计算每天的iv(delta=0.5)-iv(delta=0.25)
    for trade_date in trade_dt_total:
        print(trade_date)
        # 根据交易日选出近月到期日
        sql = f"select min(OPTION_ENDTRADE) \nfrom OPTION_LOCAL\nwhere TRADE_DT ={trade_date} and CALL_PUT='put'"
        c.execute(sql)
        result = c.fetchall()
        option_end_date = result[0][0]

        # 根据近月到期日和执行价格选出k,close
        s0 = etf_daily_close_df.loc[trade_date, 'close']
        sql = f"SELECT k,CLOSE\nfrom OPTION_LOCAL ol\nwhere " \
              f"TRADE_DT ={trade_date} and CALL_PUT='put' and OPTION_ENDTRADE={option_end_date} " \
              f"and CONTRACT_MULTIPLIER ='10000'\norder by K ASC"
        c.execute(sql)
        result = c.fetchall()
        k_total = [i[0] for i in result]
        close_total = [i[1] for i in result]
        # k_close = pd.DataFrame(result)
        # k_close.columns = ['K', 'close']
        # k_close.set_index(['K'], inplace=True)

        # 计算T
        days = (parse(str(option_end_date)) - parse(str(trade_date))).days
        if days <= 3:
            continue
        T = days/365
        n = len(close_total)

        # 计算各个k值对应的隐含波动率
        iv_total = [put_implied_vol(s0, k_total[i], T, close_total[i], R) for i in range(n)]

        # 计算各个k对应的delta
        delta_total = [calc_put_delta(s0, k_total[i], T, iv_total[i], R) for i in range(n)]
        # delta_total = delta_total[::-1]
        # iv_total = iv_total[::-1]
        # iv_total = [j for i, j in zip(delta_total, iv_total) if i > 0.02]
        # delta_total = [i for i in delta_total if i > 0.02]
        iv_total = [i[1] for i in sorted(zip(delta_total, iv_total))]
        delta_total = sorted(delta_total)

        # 计算delta等于0.5和0.25时的隐含波动率
        # if len(delta_total) <= 3:
        #     continue
        # fx = spi.splrep(delta_total, iv_total, k=3)
        # iv_delta_025 = spi.splev(0.25, fx)
        # iv_delta_05 = spi.splev(0.5, fx)
        # iv_diff = iv_delta_025 - iv_delta_05
        iv_delta_025 = np.interp(- 0.25, delta_total, iv_total)
        iv_delta_05 = np.interp(- 0.5, delta_total, iv_total)
        iv_diff = iv_delta_025 - iv_delta_05

        # 将这个值储存在字典中
        if days in iv_diff_all.keys():
            iv_diff_all[days].append(iv_diff)
        else:
            iv_diff_all[days] = [iv_diff]
        # x = np.linspace(0.1, 0.6, 1000)
        # y = spi.splev(x, fx)
        # plt.plot(x, y)
        # plt.plot(delta_total, iv_total)
        # plt.legend(['cubic spine', 'true'], loc='upper right')
        # plt.show()
        # k_all.append(k)
        # s0_all.append(s0)
    iv_diff_quantile_up = []
    iv_diff_quantile_middle = []
    iv_diff_quantile_low = []
    iv_diff_up_middle_low = {}
    # 定义两个列表来储存iv_diff的均值和方差
    for key in sorted(iv_diff_all.keys()):
        n = len(iv_diff_all[key])
        plt.scatter([key]*n, iv_diff_all[key], s=5)
        iv_diff_quantile_up.append(np.quantile(iv_diff_all[key], 0.80))
        iv_diff_quantile_middle.append(np.quantile(iv_diff_all[key], 0.5))
        iv_diff_quantile_low.append(np.quantile(iv_diff_all[key], 0.20))
        iv_diff_up_middle_low[key] = [iv_diff_quantile_up[-1], iv_diff_quantile_middle[-1], iv_diff_quantile_low[-1]]
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_up)
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_middle)
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_low)
    plt.xlabel('days to maturity')
    plt.ylabel('iv(delta=-0.25) - iv(delta=-0.5)')
    plt.legend(['quantile=0.8', 'quantile=0.5', 'quantile=0.2'], loc='upper right')
    plt.show()

    iv_diff_quantile_up = []
    iv_diff_quantile_middle = []
    iv_diff_quantile_low = []
    # 定义两个列表来储存iv_diff的均值和方差
    for key in sorted(iv_diff_all.keys()):
        n = len(iv_diff_all[key])
        plt.scatter([key] * n, iv_diff_all[key], s=5)
        iv_diff_quantile_up.append(np.quantile(iv_diff_all[key], 0.9))
        iv_diff_quantile_middle.append(np.quantile(iv_diff_all[key], 0.5))
        iv_diff_quantile_low.append(np.quantile(iv_diff_all[key], 0.1))
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_up)
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_middle)
    plt.plot(sorted(iv_diff_all.keys()), iv_diff_quantile_low)
    plt.xlabel('days to maturity')
    plt.ylabel('iv(delta=-0.25) - iv(delta=-0.5)')
    plt.legend(['quantile=0.9',  'quantile=0.5', 'quantile=0.1'], loc='upper right')
    plt.show()
    return iv_diff_up_middle_low

    # iv_diff_mean = []
    # iv_diff_std = []
    # days_to_maturity = []
    # for key in sorted(iv_diff_all.keys()):
    #     days_to_maturity.append(key)
    #     iv_diff_mean.append(np.mean(iv_diff_all[key]))
    #     iv_diff_std.append(np.std(iv_diff_all[key]))
    #
    # plt.plot(days_to_maturity, [i+2*j for i, j in zip(iv_diff_mean, iv_diff_std)])
    # plt.plot(days_to_maturity, iv_diff_mean)
    # plt.plot(days_to_maturity, [i-2*j for i, j in zip(iv_diff_mean, iv_diff_std)])
    # plt.xlabel('days to maturity')
    # plt.ylabel('iv(delta = 0.25) - iv(delta = 0.5)')
    # plt.show()
    # print(len(days_to_maturity))
    #
    # y = [i-j for i, j in zip(s0_all, k_all)]
    # n = len(k_all)
    # plt.plot(range(n), y)
    # plt.show()


if __name__ == '__main__':
    x = skew_put('510050.SH', 20190701, 20210330)
    iv_diff_up_middle_low_pd = pd.DataFrame(x)
    iv_diff_up_middle_low_pd.to_csv(r"D:\pc\Desktop\Algo_Trading\Assignment2\result\data\mid\csv\put_iv_diff_up_mid_low.csv")