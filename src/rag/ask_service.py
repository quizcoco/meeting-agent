from src.config.settings import GENERATE_LAMBDA_NAME, ROUTER_LAMBDA_NAME
from src.rag.retrieval.retrieval import Retriever
from src.agent.executor import execute_tool
from src.services.context_service import build_context
from src.services.lambda_service import invoke_lambda
from src.utils.parse_service import parse_claude_json




class AskService:

    def __init__(self, embedder, vector_store):

        self.retriever = Retriever(
            embedder, 
            vector_store
            )

    def ask(self, query):

        tool_call_raw = invoke_lambda(
        {
            "query": query
        },
        ROUTER_LAMBDA_NAME
        )
        tool_call = parse_claude_json(tool_call_raw) # 파싱


        # 도구 실행
        tool_result = execute_tool(
            tool_call["name"],
            tool_call["arguments"],
            self.retriever
        )
        # 검색 결과로 컨텍스트 만들기
        context = build_context(
            tool_result
        )

        answer = invoke_lambda(
            {
                "query": query,
                "context": context
            },
            GENERATE_LAMBDA_NAME
        )
        return answer