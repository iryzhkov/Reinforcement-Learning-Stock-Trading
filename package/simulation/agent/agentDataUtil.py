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

    training_data_dict = {
        'Balance': [],
        'Expected Value': [],
    }
    for stock in agent.stocks:
        training_data_dict[ownedFmt.format(stock)] = []
        training_data_dict[actionFmt.format(stock)] = []
        for days_before in range(agent.input_num_days):
            training_data_dict[highFmt.format(stock, days_before + 1)] = []
            training_data_dict[lowFmt.format(stock, days_before + 1)] = []

    def getStateForIndex(index: int):
        """Gets state for nth date in the session

        Args:
            index: Index of the date

        Returns:
            State dict
        """
        date = available_dates[index]
        return generateStateInputForAgent(data_source, agent, date,
                                          records.loc[date]['Balance'], stocks_owned.loc[date])

    def getActionsForIndex(index: int):
        """Gets actions for nth date in the session

        Args:
            index: Index of the date

        Returns:
            Actions list
        """
        return actions.loc[available_dates[index]]

    next_state = getStateForIndex(0)
    next_actions = getActionsForIndex(0)
    for date_index, date in enumerate(available_dates[:-1]):
        current_state = next_state
        current_actions = next_actions

        next_state = getStateForIndex(date_index + 1)
        next_actions = getActionsForIndex(date_index + 1)
        possible_next_actions = generatePossibleActions(data_source, agent.stocks, date, current_state['Balance'],
                                                        stocks_owned.loc[date])

        current_state['Expected Value'] = agent.expectedModelValue(current_state, current_actions,
                                                                   next_state, next_actions, possible_next_actions,
                                                                   rewards.loc[date]['Reward'])

        for stock in agent.stocks:
            current_state[actionFmt.format(stock)] = actions.loc[date][stock]

        for key in current_state:
            training_data_dict[key].append(current_state[key])

    training_data = pd.DataFrame.from_dict(training_data_dict)
    return training_data
