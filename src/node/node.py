from src.node import AgentState

class Node:

    def __init__(self,llm):
        self.llm = llm

    def get_requirement(state:AgentState):
        print('get_requirement')

    def generate_test_scenario(state:AgentState):
        print('generate_test_scenario')

    def review_test_scenario(state:AgentState):
        print('review_test_scenario')
        return {"scenario_review":"Accepted"}

    def generate_test_steps(state:AgentState):
        print('generate_test_steps')

    def review_steps(state:AgentState):
        print('review_steps')
        return {"test_step_review":"Accepted"}

    def finalize_content(state:AgentState):
        print('finalize_content')

    def route_review_test_scenario(state: AgentState):
        """Route back to generate test scenario or genrate go to the test case step based on the review feedback"""
        print(state["scenario_review"])
        return state["scenario_review"]

    def route_review_test_step(state: AgentState):
        """Route back to generate test steps or go to the finalize
        content based on the review feedback"""

        print(state["test_step_review"])
        return state["test_step_review"]