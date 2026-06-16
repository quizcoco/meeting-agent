from src.agent.tool_map import TOOL_MAP


def execute_tool(
    name,
    arguments,
    retriever=None
):

    if name == "search_meetings":

        return TOOL_MAP[name](
            arguments["query"],
            retriever
        )

    return TOOL_MAP[name](
        **arguments # **은 딕셔너리를 언팩하는 연산자입니다. 딕셔너리의 키-값 쌍을 함수의 인자로 전달할 때 사용됩니다.
    )