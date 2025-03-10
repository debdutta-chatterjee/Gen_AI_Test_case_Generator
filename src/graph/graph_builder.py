from src.state.state import AgentState
from langgraph.graph import StateGraph, START,END

class GraphBuilder():
    
    def __init__(self,node):
        self.node = node

    def build_test_case_graph(self):
        #Grpah
        builder = StateGraph(AgentState)

        #nodes
        builder.add_node("generate_test_steps",self.node.generate_test_steps)
        builder.add_node("finalize_content",self.node.finalize_content)

        #constuct edges
        builder.add_edge(START,"generate_test_steps")
        builder.add_edge("generate_test_steps","finalize_content")
        builder.add_edge("finalize_content",END)
        return builder


    def build_graph(self):
        #Grpah
        builder = StateGraph(AgentState)

        #nodes
        builder.add_node("get_requirement",self.node.get_requirement)
        builder.add_node("generate_test_scenario",self.node.generate_test_scenario)
        builder.add_node("review_test_scenario",self.node.review_test_scenario)
        builder.add_node("generate_test_steps",self.node.generate_test_steps)
        builder.add_node("review_steps",self.node.review_steps)
        builder.add_node("finalize_content",self.node.finalize_content)

        #constuct edges
        builder.add_edge(START,"get_requirement")
        builder.add_edge("get_requirement","generate_test_scenario")

        builder.add_edge("generate_test_scenario","review_test_scenario")
        #builder.add_edge("review_test_scenario","generate_test_steps")
        builder.add_conditional_edges(
            "review_test_scenario",
            self.node.route_review_test_scenario,
            {
                "Accepted": "generate_test_steps",
                "Rejected": "generate_test_scenario"
            }
        )

        builder.add_edge("generate_test_steps","review_steps")

        #builder.add_edge("review_steps","finalize_content")
        builder.add_conditional_edges(
            "review_steps",
            self.node.route_review_test_step,
            {
                "Accepted": "finalize_content",
                "Rejected": "generate_test_steps"
            }
        )

        builder.add_edge("finalize_content",END)
        return builder