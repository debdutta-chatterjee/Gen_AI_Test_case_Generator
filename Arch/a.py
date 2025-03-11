from typing import Annotated, Sequence
from typing_extensions import TypedDict,Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq 
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd

class UserStory(BaseModel):
    user_story: str  = Field(
        description="user story title",
    )
    business_context:str  = Field(
        description="business context",
    )
    acceptance_critera : str = Field(
        description="acceptance criteria",
    )

from typing import List
class TestScenario(BaseModel):
    test_scenario: str  = Field(
        description="test scenario",
    )
class TestScenarios(BaseModel):
    test_scenarios: List[TestScenario]  = Field(
        description="list of test scenarios",
    )

class Feedback(BaseModel):
    feedback_text: str  = Field(
        default='',
        description="feedback in written words",
    )
    feedback_decision:  Literal["Accepted", "Rejected"]  = Field(
        default='Accepted',
        description="feedback in boolean accpeted or rejected",
    )

class TestStep(BaseModel):
    test_step: str  = Field(
        description="test steps",
    )
    step_action: str  = Field(
        description="action",
    )
    step_expected: str  = Field(
        description="expected step",
    )
class TestCase(BaseModel):
    test_case_id: str  = Field(
        description="test case id",
    )
    work_item_type: str  = Field(
        description="work item type",
    )
    state: str  = Field(
        description="state",
    )
    test_steps: List[TestStep]  = Field(
        description="list of test cases",
    )
class TestCases(BaseModel):
    test_cases: List[TestCase]  = Field(
        description="list of test cases",
    )

class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    #messages: Annotated[Sequence[BaseMessage], add_messages]
   
    user_story : UserStory
    test_scenarios: TestScenarios
    scenario_review: Feedback
    test_step_review: Feedback
    test_case: Literal["Accepted", "Rejected"] = "Rejected"
    user_input:str

api_key = "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"
model = ChatGroq(groq_api_key=api_key,model_name="qwen-2.5-32b",streaming=True,temperature=0)

prompt ="""Generate a detailed requirement for a Agile user story for a finance application.
        The requirmeent should have business context & multiple Acceptance criteria
        """
def get_requirement(state:AgentState):
    print('get_requirement')
    llm =model.with_structured_output(UserStory)
    response =llm.invoke(
        [
            SystemMessage(
                content="You are an expert of creating business user stories for agile."
            ),
            HumanMessage(content=prompt),
        ]
        )
    print(response)
    print("==============================================================")
    return {"user_story":response}



def generate_test_scenario(state:AgentState):
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
    llm =model.with_structured_output(TestScenarios)
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


def review_test_scenario(state:AgentState):
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
    llm =model.with_structured_output(Feedback)
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


def generate_test_steps(state:AgentState):
    print('generate_test_steps')
    prompt ="""Generate test steps for each given scenario. User story details is provided.
                test scenario list- {test_scenario}
                User story - {user_story}
                Business context - {business_context}
                Acceptance criteria - {acceptance_criteria}
            """
    scenario = str(state["test_scenarios"].test_scenarios[0])
    scenario = scenario.replace("test_scenario=", "").replace("'", "").replace(":", "").replace(",", "").replace("/", "")
    print(scenario)
    prompt_formatted = prompt.format(
        user_story=state["user_story"].user_story, 
        business_context=state["user_story"].business_context, 
        acceptance_criteria=state["user_story"].acceptance_critera,
        test_scenario = scenario
        )
    
    #print(prompt_formatted)
    llm =model.with_structured_output(TestCases)
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
    

def review_steps(state:AgentState):
    print('review_steps')
    # prompt ="""Review the test steps and provide feedback to 
    #             Accept or Reject
    #             test steps = {test_steps}
    #         """
    # steps = str(state["test_case"].test_cases[0].ste)
    # print(steps)
    # prompt_formatted = prompt.format(
    #     test_steps = steps
    #     )
    # llm =model.with_structured_output(Feedback)
    # response = llm.invoke(
    #     [
    #     SystemMessage(
    #             content="You are an expert software qualty analyst in "
    #             "writing functional test cases."
    #         ),
    #         HumanMessage(content=prompt),
    #     ]
    #     )
    # print(response)
    # print("==============================================================")
    # return {"test_step_review":response}
    return {"test_step_review":"Accepted"}    

def finalize_content(state:AgentState):
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

def route_review_test_scenario(state: AgentState):
    """Route back to generate test scenario or genrate go to the 
    test case step based on the review feedback"""
    print(state["scenario_review"].feedback_decision)
    print("==============================================================")
    return state["scenario_review"].feedback_decision
    

def route_review_test_step(state: AgentState):
    """Route back to generate test steps or go to the finalize
      content based on the review feedback"""
    print(state["test_step_review"])
    print("==============================================================")
    return state["test_step_review"]
   

from langgraph.graph import START,END,StateGraph

#Grpah
builder = StateGraph(AgentState)

#nodes
builder.add_node("get_requirement",get_requirement)
builder.add_node("generate_test_scenario",generate_test_scenario)
builder.add_node("review_test_scenario",review_test_scenario)
builder.add_node("generate_test_steps",generate_test_steps)
builder.add_node("review_steps",review_steps)
builder.add_node("finalize_content",finalize_content)

#constuct edges
builder.add_edge(START,"get_requirement")
builder.add_edge("get_requirement","generate_test_scenario")

builder.add_edge("generate_test_scenario","review_test_scenario")
#builder.add_edge("review_test_scenario","generate_test_steps")
builder.add_conditional_edges(
    "review_test_scenario",
    route_review_test_scenario,
    {
        "Accepted": "generate_test_steps",
        "Rejected": "generate_test_scenario"
    }
)

builder.add_edge("generate_test_steps","review_steps")

#builder.add_edge("review_steps","finalize_content")
builder.add_conditional_edges(
    "review_steps",
    route_review_test_step,
    {
        "Accepted": "finalize_content",
        "Rejected": "generate_test_steps"
    }
)

builder.add_edge("finalize_content",END)

graph = builder.compile()

initial_state = {
    "test_step_review": "Rejected"
}

graph.invoke(initial_state)