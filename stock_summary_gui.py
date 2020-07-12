import tkinter as tk
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import webbrowser


def tk_window():
    font_style = ('Times', 18)
    output_var = 'Please enter a stock and click button.'
    window = tk.Tk()
    window.minsize(200,200)
    window.title('Quick Stock Summary')

    input_label = tk.Label(
        window, font=font_style, text='Please enter a stock symbol.'
        )
    input_label.grid(row=0, column=0, padx=50, pady=10)

    stock_input = tk.Entry(window, font=font_style, justify='center')
    stock_input.grid(row=1, column=0, padx=50, pady=10)

    results_label = tk.Label(window, font=font_style, text=output_var)
    results_label.grid(row=4, column=0, padx=50, pady=10)

    def button_click():
        try:
            stock_symbol = stock_input.get()
            if stock_symbol.isalpha():
                pas_object = PackAndSend(stock_symbol)
                names_dict, summary_dictionary = pas_object.get_dicts()
                #print('test is alpha ', stock_symbol.isalpha())
                #lazy hack to drop seconds...
                summary_dictionary['Date'] = (
                    str(summary_dictionary['Date'])[:10]
                    )
                ps = ''
                for key in names_dict.keys():
                    ps += str(key) + ': ' + str(names_dict[key]) + '\n' + '\n'
                for key in summary_dictionary.keys():
                    ps += (
                        str(key)
                        + ': '
                        + str(summary_dictionary[key])
                        + '\n'
                        + '\n'
                        )
                results_label.config(text=ps)

                button_frame = tk.Frame()
                button_frame.grid(row=3, column=0)

                webpage_button = tk.Button(
                    button_frame, text='Launch webpage', font=font_style,
                    command=lambda: pas_object.yahoo_finance_summary()
                    )
                webpage_button.grid(row=0, column=0, padx=50, pady=10)

                graph_button = tk.Button(
                    button_frame, text='Graph', font=font_style,
                    command=lambda: pas_object.graph()
                    )
                graph_button.grid(row=0, column=1, padx=50, pady=10)
            else:
                fail_var = 'Please enter a stock symbol as letters only.'
                print(fail_var)
                results_label.config(text=fail_var)
        except Exception as e:
            problem_var = 'I am sorry there was a problem, please try again.'
            results_label.config(text=problem_var)
            print(e, button_click.__name__)

    button = tk.Button(
        window, text='Get Summary!!', font=font_style, command=button_click
        )
    button.grid(row=2, column=0, padx=50, pady=10)
    window.mainloop()


class PackAndSend():

    def __init__(self, ticker):
        self.ticker = ticker
        self.yf_object = GetData(self.ticker)

    #Doesn't really fit here, but I'm lazy.
    def yahoo_finance_summary(self):
        webpage = (
            "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
            .format(self.ticker, self.ticker)
            )
        webbrowser.open(webpage, autoraise=True)

    #Package and return two dictionaries
    def get_dicts(self):
        #yf_object = GetData(ticker)
        df = self.yf_object.df
        info_dict = self.yf_object.info_dict
        summary_dictionary = AnalyzeStock(df).everything_dictionary()
        names_dict = {}
        names_dict['Name'] = info_dict['longName']
        names_dict['Sector'] = info_dict['sector']
        names_dict['Industry'] = info_dict['industry']
        #print(names_dict)
        #print(summary_dictionary)
        return names_dict, summary_dictionary

    def graph(self):
        df = self.yf_object.df
        df = df.loc[:, ['Date', 'Close']]
        x = df.loc[:, 'Date']
        y = df.loc[:, 'Close']
        fig, (ax1) = plt.subplots(
            1, num=self.ticker, sharex=True, figsize=(12,6)
            )
        #Adds space between subplots.
        fig.subplots_adjust(bottom=.2)
        ax1.set_title('Time vs Close')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Close_Price')
        ax1.plot(x,y, color='b', marker="s", label='arguments:x,y')
    #    x = np.asarray(x)
    #    x = x.reshape(-1,1)
        plt.show()


class GetData():

    def __init__(self, ticker):
        self.ticker = ticker
        #yf ticker object
        self.yf_obj = yf.Ticker(str(self.ticker))
        self.df = self.get_df()
        self.info_dict = self.yf_obj.info

    #A function to test if a dataframe is empty, and sort it as well.
    def get_df(self):
        stock = self.yf_obj
        stock = stock.history(period='max')
        stock = stock.reset_index()
        if not stock.empty:
            try:
                stock.sort_values(by=['Date'], ascending=True, inplace=True)
                return stock
            except Exception as e:
                print(
                    'The following exception has occured:', type(e), e,
                    '\n''This was cause by the function {} in the module {}.'
                    .format(self.df_test.__name__, __name__)
                    )
        else:
            #Maybe a little strange, but I want to print this anytime the
            #dataframe is called.
            return print('The dataframe is empty!!')#self.untested_dataframe


class AnalyzeStock():

    def __init__(self, dataframe):
        self.untested_dataframe = dataframe
        #Calls function to test if dataframe and sort it.
        self.df = self.df_test()

    #A function to test if a dataframe is empty, and sort it as well.
    #This seems redundant, but I did this so if you can pass in a dataframe
    #without using the GetData() class and still test it.
    def df_test(self):
        if not self.untested_dataframe.empty:
            try:
                self.untested_dataframe.sort_values(
                    by=['Date'], ascending=True, inplace=True
                    )
                return self.untested_dataframe
            except Exception as e:
                print(
                    'The following exception has occured:', type(e), e,
                    '\n''This was cause by the function {} in the module {}.'
                    .format(self.df_test.__name__, __name__)
                    )
        else:
            #Maybe a little strange, but I want to print this anytime the
            #dataframe is called.
            return print('The dataframe is empty!!')

    #A decorator function for error handling.
    def te_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                #print('started')
                val = func(*args, **kwargs)
                #print('ended')
                return val
            except Exception as e:
                print(
                    'The following exception has occured:', type(e), e,
                    '\n''This was cause by the function {} in the module {}.'
                    .format(func.__name__, __name__)
                    )
        return wrapper

    def everything_dictionary(self):
        stock = self.df
        #Dictionary key constants
        DATE = 'Date'
        CLOSE = 'Close'
        HIGH_5_YEAR = '5_year_high'
        HIGH_1_YEAR = '1_year_high'
        PERCENT_5_YEAR = '5_year_percent_change'
        PERCENT_1_YEAR = '1_year_percent_change'
        PERCENT_30_DAY = '30_day_percent_change'
        MA_200_DAY = '200_day_moving_average'
        MA_30_DAY = '30_day_moving_average'
        STDEV_30_DAY = '30_day_standard_deviation'
        NUMBER_OF_STDEV = 'Number_of_standard_deviations'
        STDEV_PERCENT = 'Standard_deviation_percent'
        keys = (
            DATE, CLOSE, HIGH_5_YEAR, HIGH_1_YEAR, PERCENT_5_YEAR,
            PERCENT_1_YEAR, PERCENT_30_DAY, MA_200_DAY, MA_30_DAY,
            STDEV_30_DAY, NUMBER_OF_STDEV, STDEV_PERCENT,
            )
        summary_dictionary = {key:None for key in keys}
        #from datetime import datetime
        summary_dictionary[DATE] = self.df.loc[stock.index[-1], 'Date']
        summary_dictionary[CLOSE] = round(
            self.df.loc[stock.index[-1], 'Close'], 2
            )
        summary_dictionary[HIGH_5_YEAR] = self.high(5)
        summary_dictionary[HIGH_1_YEAR] = self.high(1)
        summary_dictionary[PERCENT_5_YEAR] = self.percent_gain((365*5))
        summary_dictionary[PERCENT_1_YEAR] = self.percent_gain(365)
        summary_dictionary[PERCENT_30_DAY] = self.percent_gain(30)
        summary_dictionary[MA_200_DAY] = self.moving_average(200)
        summary_dictionary[MA_30_DAY] = self.moving_average(30)
        summary_dictionary[STDEV_30_DAY] = self.standard_deviation(30)[0]
        summary_dictionary[NUMBER_OF_STDEV] = self.standard_deviation(30)[1]
        summary_dictionary[STDEV_PERCENT] = self.standard_deviation(30)[2]
        #print(summary_dictionary)
        return summary_dictionary

    #A function that returns standard deviation amount, the number of standard
    #deviations and what percent of recent close the standard deviation is.
    @te_decorator
    def standard_deviation(self, days):
        stock = self.df
        stock = stock.iloc[-days:,:]
        stdev = round(stock['Close'].std(), 2)
        mean = round(stock['Close'].mean(), 2)
        number_deviations = round((stock.iloc[-1, 1] - mean) / stdev, 2)
        stdev_percent = round((stdev / stock.iloc[-1,1])*100, 2)
        return (stdev, number_deviations, stdev_percent)

    @te_decorator
    def percent_gain(self, days):
        stock = self.df
        stock['Date']= pd.to_datetime(stock['Date'])
        end = stock.loc[stock.index[-1], 'Date']
        start = end - pd.Timedelta(days, 'D')
        filter = stock['Date']>=start
        stock = stock[filter]
        percent = (
            ((stock.loc[stock.index[-1], 'Close']
            - stock.loc[stock.index[0], 'Close'])
            / stock.loc[stock.index[0], 'Close'])
            * 100
            )
        return round(percent,1)

    @te_decorator
    def moving_average(self, days):
        stock = self.df
        ma = stock.loc[stock.index[-days:], 'Close']
        ma = ma.mean()
        return round(ma,2)

    @te_decorator
    def high(self, years):
        stock = self.df
        stock['Date']= pd.to_datetime(stock['Date'])
        end = stock.loc[stock.index[-1], 'Date']
        start = end - pd.Timedelta(365*years, 'D')
        filter = stock['Date']>=start
        stock = stock[filter]
        max = stock['Close'].max()
        return(round(max,2))

if __name__=='__main__':

    tk_window()
