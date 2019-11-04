To run manual strategy, run python3 ManualStrategy.py. 
Change the function report() to generate specific performance printout and charts.
A ManualStrategy instance can be created like this
    ms = ManualStrategy()
    df_trades = ms.testPolicy(symbol, sd=sd, ed=ed, sv=sv)

To run TheoreticallyOptimalStrategy, run python3 TheoreticallyOptimalStrategy.py. 
Change the function report() to generate specific performance printout and charts.
A TheoreticallyOptimalStrategy instance can be created like this
	ms = TheoreticallyOptimalStrategy()
	df_trades = ms.testPolicy(symbol, sd=sd, ed=ed, sv=sv)
