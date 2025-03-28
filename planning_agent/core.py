from smolagents import CodeAgent, LiteLLMModel


def create_model(model_id, context=8192, llm_api_base=None):
    return LiteLLMModel(
        model_id=model_id,
        num_ctx=context,
        api_base=llm_api_base,
    )


def make_agent(tools, model):
    agent = CodeAgent(
        tools=tools,
        model=model,
        verbosity_level=4,
    )
    return agent


def run_agent(tools, model, prompt):
    agent = make_agent(tools, model)
    return agent.run(prompt, stream=True)
