"""Factories for Agents.
"""

from package.simulation.agent.qLearningAgent import QLearningAgent


def getQLearningAgent(config: dict):
    """Creates Q Learning Agent

    Args:
        config (dict): configuration for the agent.

    Returns:
        QLearningAgent.
    """
    return QLearningAgent(config)


def getAgentFromConfig(agent_config: dict):
    """Creates an Agent from the config

    Args:
        agent_config (dict): A config describing an Agent.

    Returns:
        An agent created based on the config.
    """
    if agent_config['agent_type'] == 'q_learning':
        return getQLearningAgent(agent_config)


if __name__ == '__main__':
    pass
