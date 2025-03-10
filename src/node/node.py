from src.node import AgentState
import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from src.node.node import AgentState, Us

class Node:

    def __init__(self,model):
        self.self.model = self.model
    

def get_requirement(self,state:AgentState):
    prompt ="""Generate a detailed requirement for a Agile user story for a finance application.
        The requirmeent should have business context & multiple Acceptance criteria
        """
    print('get_requirement')
    llm =self.model.with_structured_output(UserStory)
    response =llm.invoke(
        [
            SystemMessage(
                content="You are an expert of creating business user stories for agile."
            ),
            HumanMessage(content=prompt),
        ]
        )
    
    print("==============================================================")
    return {"user_story":response}

def generate_test_scenario(self,state:AgentState):
    print('generate_test_scenario')
    prompt ="""Generate test scenarios from the given user story details.
            Test scenarios should be well thought. 
            should have positive,negative & out of the box test scenarios 
             User story - {user_story}
             Business context - {business_context}
             Acceptance criteria - {acceptance_criteria}
        """
    prompt_formatted = prompt.format(
        user_story=state["user_story"].user_story, 
        business_context=state["user_story"].business_context, 
        acceptance_criteria=state["user_story"].acceptance_critera)
    llm =self.model.with_structured_output(TestScenarios)
    response = llm.invoke(
        [
        SystemMessage(
                content="You are an expert software qualty analyst in "
                "writing functional test cases."
            ),
            HumanMessage(content=prompt_formatted),
        ]
        )
    
    #print(response)
    print("==============================================================")
    return {"test_scenarios":response}


def review_test_scenario(self,state:AgentState):
    print('review_test_scenario')
    prompt ="""Review the test scenarios and provide feedback to 
                Accept or Reject for the given user story details.
                User story - {user_story}
                Business context - {business_context}
                Acceptance criteria - {acceptance_criteria}
            """
    prompt_formatted = prompt.format(
        user_story=state["user_story"].user_story, 
        business_context=state["user_story"].business_context, 
        acceptance_criteria=state["user_story"].acceptance_critera)
    llm =self.model.with_structured_output(Feedback)
    response = llm.invoke(
        [
        SystemMessage(
                content="You are an expert software qualty analyst in "
                "writing functional test cases."
            ),
            HumanMessage(content=prompt_formatted),
        ]
        )
    #print(response)
    print("==============================================================")
    return {"scenario_review":response}


def generate_test_steps(self,state:AgentState):
    print('generate_test_steps')
    prompt ="""Generate test steps for each given scenario. User story details is provided.
                test scenario list- {test_scenario}
                User story - {user_story}
                Business context - {business_context}
                Acceptance criteria - {acceptance_criteria}
            """
    prompt_formatted = prompt.format(
        user_story=state["user_story"].user_story, 
        business_context=state["user_story"].business_context, 
        acceptance_criteria=state["user_story"].acceptance_critera,
        test_scenario = state["test_scenarios"].test_scenarios[0]
        )
    
    #print(prompt_formatted)
    llm =self.model.with_structured_output(TestCases)
    response = llm.invoke(
        [
        SystemMessage(
                content="You are an expert software qualty analyst in "
                "writing functional test cases."
            ),
            HumanMessage(content=prompt_formatted),
        ]
        )
    #print(response)
    print("==============================================================")
    return {"test_case":response}
    

def review_steps(self,state:AgentState):
    print('review_steps')
    print("==============================================================")
    return {"test_step_review":"Accepted"}    

def finalize_content(self,state:AgentState):
    print('finalize_content')
    data = []
    for test_case in state["test_case"].test_cases:
        for step in test_case.test_steps:
            data.append({
                "test_case_id": test_case.test_case_id,
                "work_item_type": test_case.work_item_type,
                "state": test_case.state,
                "test_step": step.test_step,
                "step_action": step.step_action,
                "step_expected": step.step_expected
            })

    df = pd.DataFrame(data)
    print(df)
    print("==============================================================")

def route_review_test_scenario(self,state: AgentState):
    """Route back to generate test scenario or genrate go to the 
    test case step based on the review feedback"""
    print(state["scenario_review"].feedback_decision)
    return state["scenario_review"].feedback_decision
    print("==============================================================")

def route_review_test_step(self,state: AgentState):
    """Route back to generate test steps or go to the finalize
      content based on the review feedback"""

    print(state["test_step_review"])
    return state["test_step_review"]
    print("==============================================================")