"""Initialise agents/."""

from gym_simplifiedtetris_AVELA.agents.dellacherie import DellacherieAgent
from gym_simplifiedtetris_AVELA.agents.q_learning import QLearningAgent
from gym_simplifiedtetris_AVELA.agents.uniform import UniformAgent

__all__ = ["DellacherieAgent", "QLearningAgent", "UniformAgent"]
