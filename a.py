from typing import Annotated, Sequence
from typing_extensions import TypedDict,Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq 
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

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
    test_scenaris: List[TestScenario]  = Field(
        description="list of test scenarios",
    )

class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    #messages: Annotated[Sequence[BaseMessage], add_messages]
   
    user_story : UserStory
    test_scenarios: TestScenarios
    scenario_review: Literal["Accepted", "Rejected"] = "Rejected"
    test_step_review: Literal["Accepted", "Rejected"] = "Rejected"
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
    "scenario_review": "Rejected",
    "test_step_review": "Rejected",
    "user_input": "s"
}

graph.invoke(initial_state)