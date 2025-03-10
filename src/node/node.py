import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from src.state.state import AgentState,TestCases

class Node:

    def __init__(self,model):
        self.model = model

    def generate_test_steps(self,state:AgentState):
        print('generate_test_steps')
        prompt ="""Generate test cases & test steps for the given User story details.
                    User story title- {user_story}
                    Business context - {business_context}
                    Acceptance criteria - {acceptance_criteria}
                """
        prompt_formatted = prompt.format(
            user_story=state["user_story"].title, 
            business_context=state["user_story"].business_context, 
            acceptance_criteria=state["user_story"].acceptance_critera
            )
        
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
        return {"test_cases":response}
            
    def finalize_content(self,state:AgentState):
        print('finalize_content')
        data = []
        for test_case in state["test_cases"].test_cases:
            for step in test_case.test_steps:
                data.append({
                    "Test Case id": test_case.test_case_id,
                    "Work Item type": "Test Case",
                    "Test Case Title": test_case.test_case_title,
                    "test Step": step.step_number,
                    "Step Action": step.step_action,
                    "Step Expected": step.step_expected,
                    "Area Path": "",
                    "Assigned To":"",
                    "State":"Ready"
                })

        df = pd.DataFrame(data)
        print(df)
        print("==============================================================")
        return {"final_data":df}
        
