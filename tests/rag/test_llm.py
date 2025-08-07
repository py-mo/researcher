from researcher import LLMInference

def test_ask_simple_query():
    llm = LLMInference(model="phi3:mini")
    response = llm.ask("What is AI?", options={"num_predict": 5})
    assert isinstance(response, str)
    assert len(response) >= 10