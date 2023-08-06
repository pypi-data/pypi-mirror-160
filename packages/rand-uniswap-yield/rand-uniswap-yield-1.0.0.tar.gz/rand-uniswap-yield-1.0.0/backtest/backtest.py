import numpy as np
from .liquidity import *
from .graphql_query import *
from .charts import *

'''
    Bactest method steps:
    1. Fetch data from Graph
    2. Calculate decimals for token0 and token1
    3. Apply decimals for feeGrowthGlobal0X128 and feeGrowthGlobal1X128 as fg0 and fg1
    4. Calculate fees earned by unbounded unit of liquidity in one period
'''


def backtest(address: str, startfrom: int, network: int, range_min: float, range_max: float, target: float, base: int):
    '''
    Backtesting method for calculating returns on a specific strategy.

    :param address (str): Address of the strategy to backtest
    :param startfrom (int): Unix timestamp of the start date
    :param network (int): Network of the strategy
    :param range_min (float): Minimum bound of the range of the strategy
    :param range_max (float): Maximum bound of the range of the strategy
    :param target (float): Target investment amount of the strategy
    :param base (int): Base token to calculate for (token0 or token1)
    :return:     dpd, df_query, df_1, df_2
        - dpd (pd.DataFrame): Returns the dataframe used for calculations
        - df_query (pd.DataFrame): Returns the original dataframe of the query
        - df_1 (pd.DataFrame): Returns the dataframe of Chart 3 and DPD
        - df_2 (pd.DataFrame): Returns the dataframe of Chart 2

    '''

    dpd = graph(network, address, startfrom)
    df_query = dpd.copy()

    # Calculate decimals for pool tokens
    decimal0 = dpd.iloc[0]['pool.token0.decimals']
    decimal1 = dpd.iloc[0]['pool.token1.decimals']
    decimal = decimal1-decimal0
    # Apply decimals for feeGrowthGlobal
    dpd['fg0'] = ((dpd['feeGrowthGlobal0X128'])/(2**128))/(10**decimal0)
    dpd['fg1'] = ((dpd['feeGrowthGlobal1X128'])/(2**128))/(10**decimal1)

    # Calculate fg0 and fg1 (fee earned by an unbounded unit of liquidity in one period)
    # F_Unb = fg(t) — fg(t-1)
    dpd['fg0shift'] = dpd['fg0'].shift(-1)
    dpd['fg1shift'] = dpd['fg1'].shift(-1)
    dpd['fee0token'] = dpd['fg0']-dpd['fg0shift']
    dpd['fee1token'] = dpd['fg1']-dpd['fg1shift']

    # Calculate my liquidity based on supplied range_min and range_max arguments
    SMIN = np.sqrt(range_min * 10 ** (decimal))
    SMAX = np.sqrt(range_max * 10 ** (decimal))

    # Calculate base price and sqrt price of base token
    # If base is zero (using pool0 token)
    if base == 0:
        sqrt0 = np.sqrt(dpd['close'].iloc[-1] * 10 ** (decimal))
        dpd['price0'] = dpd['close']
    # If base is one (using pool1 token)
    elif base == 1:
        sqrt0 = np.sqrt(1/dpd['close'].iloc[-1] * 10 ** (decimal))
        dpd['price0'] = 1/dpd['close']

    # Get amounts for initial investment for both token
    amount0, amount1 = get_initial_amounts(target=target,
                                           sqrt_min=SMIN, sqrt_max=SMAX, sqrt_token0=sqrt0,
                                           initial_price=dpd['price0'].iloc[-1],
                                           decimal_diff=decimal)
    # Get the pct ratio of token0 and token1
    amount0_ratio, amount1_ratio = get_initial_token_ratio(
        amount0=amount0, amount1=amount1,
        initial_price=dpd['price0'].iloc[-1],
        base=base)
    #first_date = dpd['periodStartUnix'].iloc[-1].strftime("%m/%d/%Y, %H:%M:%S")
    #first_close_price = dpd['close'].iloc[-1]
    #print(f"Closing price on {first_date}: {first_close_price}")
    print('Amounts:', amount0, '/', amount1)
    print('Amount ratios:', round(amount0_ratio, 2),
          '% /', round(amount1_ratio, 2), '%')

    # Use get_liquidity function from liquidity module
    myliquidity = get_liquidity(
        dpd['price0'].iloc[-1], range_min, range_max, amount0, amount1, decimal0, decimal1)

    print("My liquidity:", myliquidity)

    # Calculate active liquidity

    dpd['ActiveLiq'] = 0
    dpd['amount0'] = 0
    dpd['amount1'] = 0
    dpd['amount0unb'] = 0
    dpd['amount1unb'] = 0

    # Calculate liquidity for base currency (token1)
    if base == 0:
        for i, row in dpd.iterrows():
            # If both bounds are within high and low prices
            # If high price > range_minmum bound and low price < range_maxmum bound
            if dpd['high'].iloc[i] > range_min and dpd['low'].iloc[i] < range_max:
                dpd.iloc[i, dpd.columns.get_loc('ActiveLiq')] = (min(range_max, dpd['high'].iloc[i]) - max(
                    dpd['low'].iloc[i], range_min)) / (dpd['high'].iloc[i]-dpd['low'].iloc[i]) * 100
            else:
                dpd.iloc[i, dpd.columns.get_loc('ActiveLiq')] = 0

            # Calculate bounded amounts with liquidity module
            amounts = get_amounts(
                dpd['price0'].iloc[i], range_min, range_max, myliquidity, decimal0, decimal1)
            dpd.iloc[i, dpd.columns.get_loc('amount0')] = amounts[1]
            dpd.iloc[i, dpd.columns.get_loc('amount1')] = amounts[0]

            # Calculate unbounded amounts with liquidity module
            amountsunb = get_amounts(
                (dpd['price0'].iloc[i]), 1.0001**(-887220), 1.0001**887220, 1, decimal0, decimal1)
            dpd.iloc[i, dpd.columns.get_loc('amount0unb')] = amountsunb[1]
            dpd.iloc[i, dpd.columns.get_loc('amount1unb')] = amountsunb[0]

    # Calculate liquidity for non-base currency (token1)
    elif base == 1:
        for i, row in dpd.iterrows():
            # If both bounds are within high and low prices
            if (1 / dpd['low'].iloc[i]) > range_min and (1/dpd['high'].iloc[i]) < range_max:
                dpd.iloc[i, dpd.columns.get_loc('ActiveLiq')] = (min(range_max, 1/dpd['low'].iloc[i]) - max(
                    1/dpd['high'].iloc[i], range_min)) / ((1/dpd['low'].iloc[i])-(1/dpd['high'].iloc[i])) * 100
            else:
                dpd.iloc[i, dpd.columns.get_loc('ActiveLiq')] = 0

            # Calculate bounded amounts with liquidity module
            amounts = get_amounts(
                (dpd['price0'].iloc[i]*10**(decimal)), range_min, range_max, myliquidity, decimal0, decimal1)
            dpd.iloc[i, dpd.columns.get_loc('amount0')] = amounts[0]
            dpd.iloc[i, dpd.columns.get_loc('amount1')] = amounts[1]

            # Calculate unbounded amounts with liquidity module
            amountsunb = get_amounts(
                (dpd['price0'].iloc[i]), 1.0001**(-887220), 1.0001**887220, 1, decimal0, decimal1)
            dpd.iloc[i, dpd.columns.get_loc('amount0unb')] = amountsunb[0]
            dpd.iloc[i, dpd.columns.get_loc('amount1unb')] = amountsunb[1]

    # Final fee calculation
    # Total fees * my liquidity * active liquidity / by 100
    dpd['myfee0'] = dpd['fee0token'] * myliquidity * dpd['ActiveLiq'] / 100
    dpd['myfee1'] = dpd['fee1token'] * myliquidity * dpd['ActiveLiq'] / 100

    # Calculate volatility based on price
    window_size = 24  #  Daily volatility
    # Calculate rolling volatility with a daily rolling window and annualize results
    dpd['volatility0_ann'] = dpd['price0'].pct_change().rolling(
        window_size).std()*(252**0.5)

    # Create human readable timestamp indexes
    dpd.index = pd.to_datetime(dpd['periodStartUnix'], unit='s')

    # Get charting for more detailed metrics
    a1, a2, a3 = chart1(dpd, base, myliquidity)

    # Format data for plotting -- Chart 3 and DPD
    # Concat dataframes and drop duplicate columns
    df_1 = pd.concat([dpd, a3], axis=1).T.drop_duplicates().T
    df_1.sort_index(inplace=True)

    # Iterate and drop non-norm columns if normalized exists
    norm_cols = []
    for i in df_1.columns:
        if 'norm' in i:
            norm_cols.append(i)

    for i in df_1.columns:
        for f in norm_cols:
            if f.split('norm')[0] == i:
                df_1.drop(columns=i, axis=1, inplace=True)

    # Drop other columns used for calculations
    df_1.drop(columns=['periodStartUnix',
                       'fg0shift',
                       'fg1shift',
                       'pool.token0.decimals',
                       'pool.token1.decimals',
                       'pool.totalValueLockedToken0',
                       'pool.totalValueLockedToken1',
                       'pool.totalValueLockedUSD',
                       'feeGrowthGlobal0X128',
                       'feeGrowthGlobal1X128',
                       'amountV_shift'], inplace=True)

    # Format data for plotting -- Chart 1 and Chart 2
    # Concat dataframes and drop duplicate columns
    df_2 = pd.concat(
        [a1, a2], axis=1).reset_index().T.drop_duplicates().T
    # Set date as an index
    df_2.set_index('periodStartUnix', inplace=True)
    df_2.sort_index(inplace=True)
    # Iterate and drop non-norm columns if normalized exists
    norm_cols = []
    for i in df_2.columns:
        if 'norm' in i:
            norm_cols.append(i)

    for i in df_2.columns:
        for f in norm_cols:
            if f.split('norm')[0] == i:
                df_2.drop(columns=i, axis=1, inplace=True)

    return dpd, df_query, df_1, df_2
