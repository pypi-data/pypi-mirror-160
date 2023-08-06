class mf_movement():
    
    def __init__(self):
        import pandas as pd
        import warnings
        warnings.filterwarnings('ignore')
        self.keeper = 'tbd'
        self.num_days = 21 #115 number of days for rolling average; used in line 60
        self.days_back = 900 #number of days to go back from today to collect data. line 152
        self.df_summary_table = pd.DataFrame(columns = ['n', 'Static_Profit', 'Dynamic_Profit', 'Dynamic_Over_Static'])
        self.n = 0
        self.begin_shares = 1
        self.df_3_profits = pd.DataFrame(columns = ['n', 'Static_Profit', 'Unlimited_Dyn_Profit', 'Limited_Dyn_Profit'])
        self.dynamic_profit = 0
        self.df = pd.DataFrame()
        self.Limited_Dyn_Profit = 0.0
        self.Static_Profit = 0.0
        
    def empty_row_rmvl(self, df):
        import pandas as pd
        df.dropna(inplace=True)
        if 'level_0' in df.columns:
            df = df.drop(['level_0'], axis = 1) 
        df.reset_index(inplace = True)
        df['Date'] = pd.to_datetime(df['Date']) #converts Date dtype from object to date dtype
        
        return df
    
    def zero_rmvl(self, df): #drops the entire row if one value in the second to the last columns is 0       
        import pandas as pd

        i = 0
        while i < len(df):
            if df.iloc[i, -2] == 0.0:
                df = df.drop([i])
                df.reset_index(drop = True, inplace = True)
                i -= 1
            else:
                i += 1
                
        df['Date'] = pd.to_datetime(df['Date']) #converts Date dtype from object to date dtype; needs to be done after every reset index
        return df
    
    def obj_to_date(self, df):
        import pandas as pd
        df['Date'] = pd.to_datetime(df['Date'])
        
    def cmf(self, df, num_days):
        df['pre_cmf'] = ((df['close_low'] - df['high_close']) / df['high_low']) * df['Volume']
        self.num_days = num_days #added for multiple runs
        df['cmf'] = df['pre_cmf'].rolling(self.num_days).sum() / df['Volume'].rolling(self.num_days).sum()
        return df
    
    def differences(self, df):
        df['high_low'] = df['High'] - df['Low']
        df['open_close'] = df['Open'] - df['Close']
        df['open_high'] = df['Open'] - df['High']
        df['open_low'] = df['Open'] - df['Low']
        df['high_close'] = df['High'] - df['Close']
        df['close_low'] = df['Close'] - df['Low']
        #display('#57 df', df)
        return df    
    
    def yahoo_api(self):
        import pandas as pd
        import yfinance as yf
        from datetime import datetime, timedelta

        symbol = input('What is the stock symbol? ')
        print('The symbol is: ', symbol)
        which_date = input('What is the most recent date you want to use? Enter [yyyy-mm-dd] or press enter for today. ')

        if which_date:
            end_date = which_date
            end_date = datetime.strptime(end_date,'%Y-%m-%d') #converts the string into the datetime format
        else:
            end_date = datetime.now()
        
        d = timedelta(days = self.days_back) #you are getting self.days_back records (first self.num_days dropped when calculated 20 simple moving average.)
        a = end_date - d # goes back self.days_back
        begin_date = a.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d') #keeps only the date ... removes the time stamp

        df = yf.download(symbol,
        start = begin_date,
        end = end_date,
        progress = False)
        
        print('start date: ', begin_date)
        print('end date: ', end_date)
        
        self.df = df
        
        return df
    
    def buy_sell_signals(self, df1):
        import numpy as np
        import pandas as pd

        # Steps through the dataframe in groups of 206 on record at a time to find the buy sell indicators of the most
        # recent day.
        # dfBuySell is the dataframe that holds the dates when there is a either a buy or sell signal

        mf = mf_movement() #Instantiates the class
        import pandas as pd
        import sys

        dfBuySell = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Buy_Sell'])

        i = 0
        ia = 0

        while i < (len(df1) - self.num_days): #where does the number 206 come from? The length of the df minus the averaging number n

            ia = i
            ib = i + self.num_days #i + the rolling group - averaging number n
            df2Temp = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume',
                   'high_low', 'open_close', 'open_high', 'open_low', 'high_close',
                   'close_low', 'pre_cmf', 'cmf'] )
            while ia < ib: #creates a dataframe that move through the entire dataframe one record at a time
                
                df2Temp = pd.concat([df2Temp, df1.iloc[[ia]]], axis = 0, sort = False, ignore_index = True)
                                
                ia += 1
            
            if (df2Temp.iloc[-5, 14] < df2Temp.iloc[-4, 14] 
                and df2Temp.iloc[-4, 14] < df2Temp.iloc[-3, 14]
                and df2Temp.iloc[-3, 14] > df2Temp.iloc[-2, 14]
                and df2Temp.iloc[-2, 14] > df2Temp.iloc[-1, 14]): #determines if there is a peak in cmf value
                
                dfBuySellTemp = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Buys_Sell'])
                
                dftest = df2Temp.iloc[-1, 0:5] #dftest is a vertical series; iloc converts df to series when iloc 1 row          
                dftest = dftest.to_frame() # need to convert the series back into a dataframe to transpose it
                dfBuySellTemp = np.transpose(dftest) #transposes the dataframe from vertical to horizontal
                
                dfBuySellTemp['Buy_Sell'] = 'Buy'
                dfBuySell = pd.concat([dfBuySell, dfBuySellTemp], axis = 0, sort = False, ignore_index = True)
                dfBuySell = dfBuySell.reindex()
                del dfBuySellTemp

            elif (df2Temp.iloc[-5, 14] > df2Temp.iloc[-4, 14] 
                and df2Temp.iloc[-4, 14] > df2Temp.iloc[-3, 14]
                and df2Temp.iloc[-3, 14] < df2Temp.iloc[-2, 14]
                and df2Temp.iloc[-2, 14] < df2Temp.iloc[-1, 14]):
                
                dfBuySellTemp = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Buys_Sell'])
                
                dftest = df2Temp.iloc[-1, 0:5] #extracting a single row from a dataframe using iloc outputs a series
                dftest = dftest.to_frame() # need to convert the series back into a dataframe to transpose it
                
                dfBuySellTemp = np.transpose(dftest) #transposes the dataframe from vertical to horizontal
                
                dfBuySellTemp['Buy_Sell'] = 'Sell'
                dfBuySell = pd.concat([dfBuySell, dfBuySellTemp], axis = 0, sort = False, ignore_index = True)
                dfBuySell = dfBuySell.reindex()
                del dfBuySellTemp
                  
            else:
                dfBuySellTemp = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Buys_Sell'])
                dftest = df2Temp.iloc[-1, 0:5] #extracting a single row from a dataframe using iloc outputs a series
                dftest = dftest.to_frame() # need to convert the series back into a dataframe to transpose it
                
                dfBuySellTemp = np.transpose(dftest) #transposes the dataframe from vertical to horizontal
    
                dfBuySellTemp['Buy_Sell'] = 'No Action'     
                dfBuySell = pd.concat([dfBuySell, dfBuySellTemp], axis = 0, sort = False, ignore_index = True)
                dfBuySell = dfBuySell.reindex()
                del dfBuySellTemp

            del df2Temp
            i += 1
        return dfBuySell #dfBuySell has the buy and sell signals
    
    def buying_selling(self, df): # performs the actual buying and selling
        import pandas as pd

        dfBuySell1 = df.copy() 
        
        if 'Date' in dfBuySell1.columns:
            dfBuySell1 = dfBuySell1.drop(columns = 'Date') #when df is copied it makes the date into the index and the 

        dfBuySell1[['Open', 'High', 'Low', 'Close']] = dfBuySell1[['Open', 'High', 'Low', 'Close']].astype(float, errors = 'raise')
        
        dfBuySell1['Shares_Transacted'] = 0
        dfBuySell1['Bought'] = 0
        dfBuySell1['Sold'] = 0
        dfBuySell1['Net_Shares'] = self.begin_shares #starting number of shares from __init__

        dfBuySell1 = dfBuySell1.reindex()
        
        '''dfBuySell1:  Index(['Open', 'High', 'Low', 'Close', 'Buy_Sell', 'Shares_Transacted',
       'Bought', 'Sold', 'Net_Shares'''

        i = 0
        t_n = 1 #number of shares per transaction
        t_buy = 1 #multiplier for buy
        t_sell = 1 #multiplier for sell
        
        print()

        while i < len(dfBuySell1): #buys or sells shares as indicator dictates

            if dfBuySell1.iloc[i, 4] == 'Buy': # changed to 4 from 5; decremented all by 1
                dfBuySell1.iloc[i, 6] = int(dfBuySell1.iloc[i, 3] * t_n * t_buy * 100) / 100 #debit of the transaction
                dfBuySell1.iloc[i, 5] = t_n * t_buy #number of shares transacted or bought
                dfBuySell1.iloc[i, 8] += t_n * t_buy #share counter; bought shares added; how many shares remaining                
                
            elif dfBuySell1.iloc[i, 4] == 'Sell':
                dfBuySell1.iloc[i, 7] = int(dfBuySell1.iloc[i, 3] * t_n * t_sell * 100) / 100 #credit of the transaction
                dfBuySell1.iloc[i, 5] = -t_n * t_sell #number of shares transacted sold
                dfBuySell1.iloc[i, 8] += -t_n * t_sell #share counter; sold shares subtracted; how many shares remaining
                                
            elif dfBuySell1.iloc[i, 4] == 'No Action':
                dfBuySell1.iloc[i,8] += 0
            a = i + 1
            while a < len(dfBuySell1):
                dfBuySell1.iloc[a, 8] = dfBuySell1.iloc[i, 8] #carries forward the remaining number of shares
                a += 1

            i += 1

        x = len(dfBuySell1) - 1
        
        total_received_from_shares = dfBuySell1['Sold'].sum()
        initial_invest = round(dfBuySell1.iloc[0, 1] * self.begin_shares)
        net_shares_remaining = dfBuySell1.iloc[len(dfBuySell1) - 1, -1]
        net_shares_tranacted = dfBuySell1['Shares_Transacted'].sum()
        total_spent_on_shares = dfBuySell1['Bought'].sum()
        total_cost = initial_invest + total_spent_on_shares
        remaining_share_value = net_shares_remaining * dfBuySell1.iloc[x, 3]
        total_gain = float(remaining_share_value) + int(total_received_from_shares * 100) / 100 
        profit_dynamic = total_gain - total_cost 
        self.dynamic_profit = profit_dynamic
        dynamic_gain_ratio = profit_dynamic/total_cost
        dynamic_gain_percentage = '{:,.2%}'.format(dynamic_gain_ratio)
        ending_value = self.begin_shares * dfBuySell1.iloc[x, 3]
        profit_static = ending_value - initial_invest 
        static_gain = profit_static/initial_invest
        static_gain_percentage = '{:,.2%}'.format(static_gain)
        
        if static_gain_percentage != 0:
            dyn_ovr_stc_gain = (profit_dynamic - profit_static) / (profit_static)
            dyn_ovr_stc_gain_percentage = '{:,.2%}'.format(dyn_ovr_stc_gain)
        else:
            print('If you did nothing, you made nothing!')
        
        df_summary_table_temp = pd.DataFrame(columns = ['n', 'Static_Profit', 'Dynamic_Profit' , 'Dynamic_Over_Static'])
        
        df_summary_table_temp.loc[0,'n'] = self.num_days 
        df_summary_table_temp['Static_Profit'] = static_gain_percentage
        df_summary_table_temp['Dynamic_Profit'] = dynamic_gain_percentage
        
        dynamic_gain_percentage = dynamic_gain_percentage.replace("%", "") #remove % from string
        dynamic_gain_percentage = dynamic_gain_percentage.replace(",", "") #remove , from string
        
        static_gain_percentage = static_gain_percentage.replace("%", "") #removes % from string
        static_gain_percentage = static_gain_percentage.replace(",", "") #removes , from string

        dynamic_gain_percentage = float(dynamic_gain_percentage) #converts string to float
        static_gain_percentage = float(static_gain_percentage) #converts string to float

        df_summary_table_temp['Dynamic_Over_Static'] = dyn_ovr_stc_gain_percentage
               
        self.df_summary_table = pd.concat([self.df_summary_table, df_summary_table_temp], axis = 0, sort = False, ignore_index = True)
        
        self.df_summary_table = self.df_summary_table.reindex()
        
        del df_summary_table_temp
        
        return self.df_summary_table
        
    def summary_plot(self, summary_table):#plotting
        import matplotlib.pyplot as plt
        import pandas as pd

        df = pd.DataFrame(summary_table) #covert to a dataframe
        df = df.set_index('n') #set the grouping number n as the index
        
        ## Convert string to number ##
        df["Dynamic_Over_Static"] = df["Dynamic_Over_Static"].str.replace("%","") #remove % from string
        df["Dynamic_Over_Static"] = df["Dynamic_Over_Static"].str.replace(",","") #remove , from string
        
        df['Dynamic_Over_Static'] = df['Dynamic_Over_Static'].astype(float)  #converts string to float
        
        df.sort_values('Dynamic_Over_Static', ascending=True, inplace=True)

        plt.scatter(df.index, df['Dynamic_Over_Static'], c='b') #plots the (dynamic - static return) / static return
        plt.show()
        
    def section_defin_inflection_cmf(self, df): #this defines the range and resolution for the AV for evaluation
        import pandas as pd
        #import grouping_sizePkg.grouping_sizePkg
        #mf = grouping_sizePkg.grouping_sizePkg.mf_movement()
        
        begin = int(input('What is the starting Averaging Value Position for the CMF? [Number greater than 10] ')) 
        end = int(input('What is the ending Averaging Value position for the CMF? [Number greater that starting #] ')) 
        resolution = int(input('What is the resolution? [integer value] '))   
        
        begin_index = int(begin) #defines the starting index or position
        end_index = int(end) #defines the ending index or position

        while begin_index <= end_index:
            print('\nWorking ...', begin_index)
            
            if 'index' in df.columns:
                dfA = df.drop(['index'], axis = 1)
            if 'level_0' in df.columns:
                dfA = df.drop(['level_0'], axis = 1)
            
            dfA = self.cmf(df, begin_index) # = num_days is the number of days that are combined together to to produce the indicator
            
            #### Dataframe clean up #####
            if 'index' in dfA.columns:
                dfA = dfA.drop(['index'], axis = 1)
            if 'level_0' in dfA.columns:
                dfA = dfA.drop(['level_0'], axis = 1)
                
            dfA = self.empty_row_rmvl(dfA)
            
            if 'index' in dfA.columns:
                dfA = dfA.drop(['index'], axis = 1)
            
            df1 = self.buy_sell_signals(dfA) #246
            
            if 'Date' in df1.columns:
                df1 = df1.drop(['Date'], axis = 1)
                        
            df1.reset_index(inplace=True)
            if 'index' in df1.columns:
                df1 = df1.drop(['index'], axis = 1)
            
            df1 = df1.rename(columns = {'index':'Date'})
            
            dfC = self.shares_owned(dfA, begin_index) #for pos/neg cmf with limit of 0 to 1 share max
            
            #### Writes the last index information to the summary table              ####
            
            if begin_index == end_index: #
                summary_table = mf.buying_selling(df1) #336
            else:
                self.buying_selling(df1) #336
                
            lst = [dfA, df1, dfC]
            del lst     # memory is released
            
            #### CREATES THE DF TO CAPTURE THE 3 GAINS ####
            net_profit_loss = self.Limited_Dyn_Profit
            BuyHoldProfit = self.Static_Profit

            df2 = {'n': begin_index, 'Limited_Dyn_Profit': net_profit_loss, 'Static_Profit': BuyHoldProfit, 'Unlimited_Dyn_Profit': self.dynamic_profit}
            df2 = pd.DataFrame(df2, index = [0])
            columns=['Numbers']
            self.df_3_profits = pd.concat([self.df_3_profits, df2], axis = 0, sort = False, ignore_index = True)

            begin_index += resolution

        #mf.summary_plot(summary_table) #plots the summary table of all the different grouping values
        
        return df, summary_table
    
    def shares_owned(self, dfB, begin_index): #regulates the number of share owned to no greater than 1 or less than 0
        dfB['shares_movement'] = 0
        dfB['credit_debit'] = 0

        i = 0
        while i < len(dfB):
            if dfB.loc[i, 'cmf'] > 0 and dfB['shares_movement'].sum() < 1: 
                dfB.loc[i, 'shares_movement'] = 1
            elif dfB.loc[i, 'cmf'] > 0 and dfB['shares_movement'].sum() >= 1:
                dfB.loc[i, 'shares_movement'] = 0
            elif dfB.loc[i, 'cmf'] < 0 and dfB['shares_movement'].sum() < 1:
                dfB.loc[i, 'shares_movement'] = 0
            elif dfB.loc[i, 'cmf'] < 0 and dfB['shares_movement'].sum() >= 1:
                dfB.loc[i, 'shares_movement'] = -1

            dfB.loc[i, 'credit_debit'] = dfB.loc[i, 'Close'] * dfB.loc[i, 'shares_movement']

            i += 1

        net_profit_loss = dfB['credit_debit'].sum()
        
        BuyHoldProfit = dfB.loc[(len(dfB) - 1), 'Close'] - dfB.loc[0, 'Close'] #Buy and Hold P/L
        
        #### STORES PROFIT VARIABLES AS GLOBAL VARIABLES ####
        self.Limited_Dyn_Profit = net_profit_loss
        self.Static_Profit = BuyHoldProfit
        
        return dfB
    
    def three_profit_summary_plot(self):#plotting
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        
        self.df_3_profits = self.df_3_profits.set_index('n') #set the grouping number n as the index
        self.df_3_profits.plot()
        
    def Legend_description(self):
        print('Static_profit represents buying one share at the beginning of the time period and just holding')
        print('it to the end of the time period.\n')
        print('Unlimited_Dyn_Profit represents buying one share, one day out of the dip of the cmf and selling one')
        print('share, one day out of the peak of the cmf. This is repeated throught the time period.\n')
        print('Limited_Dyn_Profit prepresents bying one share when the cmf goes from negative to positive and')
        print('selling one share when the cmf goes from positive to negative. This is also repeated. \n')
        print("The y axis is a relative measure of each strategies' performance. The higher the number the better.")
        
        
    def Disclaimer(self):
        import time

        print('WARNING: This is for illustration and entertainment purposes ONLY.')
        print('Do NOT use this information for anything. This includes but is not limited to any financial ')
        print('decisions, and/or stock, option and/or bond purchases or sales, real estate transactions or any other decision.' )
        print('If you disregard this warning you do so at your sole risk and you assume all responsibility for the consequences.')
        print('In using this application you also agree that you will indemnify Kokoro Analytics, its officers,')
        print('employees, volunteers, vendors and contractors from any damages incured from disregarding this warning.\n')
        
        time.sleep(.5)
        agreement = input('Press enter if you have read and will abide by the "Warning" statement above.')
        
        if agreement != '':
            import sys 
            print('\nThank you for your interest but we cannot go any further because you entered something other than enter! \nHave a great day!')
            sys.exit()
            
        print('\nWe use the Chaikin Money Flow indicator. What is the Chaikin Money Flow? See the link below.')
        print('https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/cmf\n')
        