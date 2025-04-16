import click
import yaml

from ftlagents.core import create_model, run_agent
from .default_tools import TOOLS
from ftlagents.tools import get_tool, load_tools
from smolagents.memory import ActionStep
from smolagents.agent_types import AgentText

# import logging
# logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.option("--tools", "-t", multiple=True)
@click.option("--tools-files", "-f", multiple=True)
@click.option("--prompt", "-p", prompt="What is the prompt?")
@click.option("--model", "-m", default="ollama_chat/deepseek-r1:14b")
@click.option("--info", "-i", multiple=True)
@click.option("--user-input", "-u", default="user_input.txt")
def main(
    tools,
    tools_files,
    prompt,
    model,
    info,
    user_input,
):
    """A agent that solves a prompt given a system design and a set of tools"""
    tool_classes = {}
    tool_classes.update(TOOLS)
    for tf in tools_files:
        tool_classes.update(load_tools(tf))
    model = create_model(model)
    state = {'user_input': []}

    parts = [prompt]

    if info:
        parts.append("Use this addition information:")

    for i in info:
        with open(i) as f:
            parts.append(f.read())

    prompt = "\n".join(parts)

    try:

        for o in run_agent(
            tools=[get_tool(tool_classes, t, state) for t in tools],
            model=model,
            prompt=prompt,
        ):
            if isinstance(o, ActionStep):
                pass
            elif isinstance(o, AgentText):
                print(o.to_string())
    finally:
        if state['user_input']:
            with open(user_input, 'w') as f:
                f.write(yaml.dump(state['user_input']))
