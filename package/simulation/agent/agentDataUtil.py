"""Utils for data used by the agents.
"""

from package.simulation.stockData.baseStockDataSource import StockDataSource
from package.simulation.agent.baseAgent import BaseAgent

import pandas as pd

from datetime import datetime

ownedFmt = '{}_owned'
highFmt = '{}_high_{}_days_ago'
lowFmt = '{}_low_{}_days_ago'
actionFmt = '{}_action'


def generateStateInputForAgent(stock_data_source: StockDataSource, agent: BaseAgent,
                               date: datetime, balance: float, stocks_owned: dict):
    """Generates state input to use for the agent.

    Args:
        stock_data_source (StockDataSource): Stock data source used for the session
        agent (BaseAgent): Agent that will get the data
        date (datetime): The date for which to generate the input.
        balance (float): The balance
        stocks_owned (dict): The stock portfolio

    Returns:
        A dict with the state data. Used as an input to the agent.
    """
    state = {
        'Balance': balance,
    }
    stocks_data = stock_data_source.getStockDataForNDaysBefore(date, agent.input_num_days, agent.stocks)
    for stock in agent.stocks:
        state[ownedFmt.format(stock)] = stocks_owned[stock]
        stock_data = stocks_data[stock]
        for days_before in range(agent.input_num_days):
            state[highFmt.format(stock, days_before + 1)] = stock_data.iloc[days_before]['High']
            state[lowFmt.format(stock, days_before + 1)] = stock_data.iloc[days_before]['Low']

    return state


def generateStateInputsForAgent(stock_data_source: StockDataSource, agent: BaseAgent,
                                records: pd.DataFrame, stocks_owned: pd.DataFrame):
    """Generates state input to use for the agent.

    Args:
        stock_data_source (StockDataSource): Stock data source used for the session
        agent (BaseAgent): Agent that will get the data
        records (pd.DataFrame): Session records.
        stocks_owned (dict): Stocks owned during the session.

    Returns:
        A dict with the state data. Used as an input to the agent.
    """
    columns_to_change = {}
    for stock in agent.stocks:
        columns_to_change[stock] = ownedFmt.format(stock)
    states = stocks_owned.rename(columns=columns_to_change)
    states = states.join(records[:]['Balance'])

    last_date = records.index[-1]
    stocks_prices_formatted = {}
    stocks_prices = stock_data_source.getStockDataForNDaysBefore(last_date, agent.input_num_days + len(records) - 1,
                                                                 agent.stocks)

    for num_days_before in range(1, agent.input_num_days + 1):
        for stock in agent.stocks:
            first_index = agent.input_num_days - num_days_before
            last_index = len(stocks_prices[stock]) - num_days_before + 1
            stocks_prices_formatted[highFmt.format(stock, num_days_before)] = stocks_prices[stock]['High'][first_index:last_index]
            stocks_prices_formatted[lowFmt.format(stock, num_days_before)] = stocks_prices[stock]['Low'][first_index:last_index]

    for k in stocks_prices_formatted:
        stocks_prices_formatted[k].index = records.index
    stock_prices_dataframe = pd.DataFrame(stocks_prices_formatted)

    states = states.join(stock_prices_dataframe)
    return states


def generateStateActionInputs(state_dict: dict, possible_actions: list, stocks: list):
    """Generates State-Action inputs used for the model.

    Args:
       state_dict (dict): A dict representing state.
       possible_actions (list): A list representing possible actions.
       stocks (list): A list of stocks.
    """
    state_data_frame = pd.DataFrame(state_dict, index=[0])
    state_data_frame = pd.DataFrame([list(state_data_frame.loc[0])] * (len(possible_actions)),
                                    columns=state_data_frame.columns)

    columns = [actionFmt.format(stock) for stock in stocks]
    actions_data_frame = pd.DataFrame(possible_actions, columns=columns)

    state_action_data_frame = state_data_frame.join(actions_data_frame)
    return state_action_data_frame


def generatePossibleActions(stock_data_source: StockDataSource, stocks: list,
                            date: datetime, balance: float, stocks_owned: dict):
    """generates possible actions given the state.

    Args:
        stock_data_source (StockDataSource): Stock data source used for the session
        stocks (list of str): List of stocks
        date (datetime): The date for which to generate the input.
        balance (float): The balance
        stocks_owned (dict): The stock portfolio

    Returns:
        A dict with the state data. Used as an input to the agent.
    """
    possible_actions = [[0] * len(stocks)]

    for index, stock in enumerate(stocks):
        if stocks_owned[stock] > 0:
            sell_action = [0] * len(stocks)
            sell_action[index] = -1
            possible_actions += [sell_action]

        if stock_data_source.getStockDataForDate(date, stock)['High'] < balance:
            buy_action = [0] * len(stocks)
            buy_action[index] = 1
            possible_actions += [buy_action]

    return possible_actions


def generateTrainingDataFromSession(data_source, stocks_owned, actions, rewards, records, agent):
    """
    """
    # Make sure that we are working with the same dates across all dataframes.
    available_dates = set(stocks_owned.index)
    available_dates = available_dates.intersection(set(actions.index))
    available_dates = available_dates.intersection(set(rewards.index))
    available_dates = sorted(available_dates.intersection(set(records.index)))

    states = generateStateInputsForAgent(data_source, agent, records[available_dates[0]:available_dates[-1]],
                                         stocks_owned[available_dates[0]:available_dates[-1]])
    rewards = rewards[available_dates[0]:available_dates[-1]]
    actions = actions[available_dates[0]:available_dates[-1]]
    action_columns = {}
    for stock in agent.stocks:
        action_columns[stock] = actionFmt.format(stock)
    state_action_values = states.join(actions.rename(columns=action_columns))
    expectations = agent.expectedModelValues(state_action_values, actions, rewards, data_source)

    training_data = state_action_values.join(expectations)
    debug_data = training_data.join(rewards) # includes rewards to see how the attribution works.
    return training_data[:available_dates[-2]]
