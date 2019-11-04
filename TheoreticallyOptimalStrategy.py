"""
Code implementing a TheoreticallyOptimalStrategy object
It should implement testPolicy() which returns a trades data frame
The main part of this code should call marketsimcode as necessary to generate the plots used in the report
"""

"""
Student Name: Jie Lyu 		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676 
"""


"""
[Constrains]
possible actions {-2000, -1000, 0, 1000, 2000}
possible positions {-1000, 0, 1000}

[Policy]
If price goes up tomorrow, I go long.
If price goes down tomorrow, I go short.
"""




from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt


class TheoreticallyOptimalStrategy:

	def testPolicy(self, symbol, sd, ed, sv):

		# setting up
		symbol = symbol[0]
		df = get_data([symbol], pd.date_range(sd, ed))
		price_df = df[[symbol]]
		price_df = price_df.ffill().bfill()

		df_trades = df[['SPY']]
		df_trades = df_trades.rename(
			columns={'SPY': symbol}).astype({symbol: 'int32'})
		df_trades[:] = 0
		dates = df_trades.index

		# current_cash = sv
		current_position = 0

		# making trades
		for i in range(len(dates) - 1):

			if price_df.loc[dates[i+1]].loc[symbol] > price_df.loc[dates[i]].loc[symbol]:
				action = 1000 - current_position
			else:
				action = -1000 - current_position
			df_trades.loc[dates[i]].loc[symbol] = action
			current_position += action

		return df_trades


def author():
	return 'jlyu31'


"""########
Helper functions for report()
"""


def get_benchmark(sd, ed, sv):
	# starting with $100,000 cash, investing in 1000 shares of JPM and holding that position

	df_trades = get_data(['SPY'], pd.date_range(sd, ed))
	df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
	df_trades[:] = 0
	df_trades.loc[df_trades.index[0]] = 1000
	portvals = compute_portvals(df_trades, sv, commission=0.00, impact=0.00)
	return portvals

# takes in pd.df and prints stats
def print_stats(benchmark, theoretical):
	benchmark, theoretical = benchmark['value'], theoretical['value']

	# [Cumulative Return]
	cr_ben = benchmark[-1] / benchmark[0] - 1
	cr_the = theoretical[-1] / theoretical[0] - 1

	# adily return in percentage
	dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
	dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]

	# [Stdev of daily returns]
	sddr_ben = dr_ben.std()
	sddr_the = dr_the.std()

	# [Mean of daily returns]
	adr_ben = dr_ben.mean()
	adr_the = dr_the.mean()

	print("")
	print("[TheoreticallyOptimalStrategy]")
	print("Cumulative return: " + str(cr_the))
	print("Stdev of daily returns: " + str(sddr_the))
	print("Mean of daily returns: " + str(adr_the))
	print("")
	print("[Benchmark]")
	print("Cumulative return: " + str(cr_ben))
	print("Stdev of daily returns: " + str(sddr_ben))
	print("Mean of daily returns: " + str(adr_ben))
	print("")

# takes in pd.df and plots graphs
def plot_graphes(benchmark_portvals, theoretical_portvals):

	# normalize	
	benchmark_portvals['value'] = benchmark_portvals['value'] / benchmark_portvals['value'][0]
	theoretical_portvals['value'] = theoretical_portvals['value'] / theoretical_portvals['value'][0]

	plt.figure(figsize=(14,8))
	plt.title("TheoreticallyOptimalStrategy")
	plt.xlabel("Date")
	plt.ylabel("Cumulative Return")
	plt.xticks(rotation=30)
	plt.grid()
	plt.plot(benchmark_portvals, label="benchmark", color = "green")
	plt.plot(theoretical_portvals, label="theoritical", color = "red")
	plt.legend()
	plt.savefig("report/part2.png", bbox_inches='tight')
	# plt.show()
	plt.clf()


"""########
end of helper functions
"""


def report():

	# testing conditions
	sv = 100000
	sd = dt.datetime(2008, 1, 1)
	# ed = dt.datetime(2008, 1, 15)
	ed = dt.datetime(2009,12,31)

	# get theoretical performance
	ms = TheoreticallyOptimalStrategy()
	df_trades = ms.testPolicy(['JPM'], sd=sd, ed=ed, sv=sv)
	theoretical_portvals = compute_portvals(
		df_trades, sv, commission=0.00, impact=0.00)
	# print(theoretical_portvals)

	# get benchmark performance
	benchmark_portvals = get_benchmark(sd, ed, sv)
	# print(benchmark_portvals)

	# get stats
	print_stats(benchmark_portvals, theoretical_portvals)

	# plot graph
	plot_graphes(benchmark_portvals, theoretical_portvals)


if __name__ == "__main__":
	report()






# # takes in a pd.df and returns a np.array
# def get_listview(portvals, normalized):
# 	val_arr = portvals['value'].values
# 	if normalized:
# 		val_arr = val_arr / val_arr[0]
# 	return val_arr