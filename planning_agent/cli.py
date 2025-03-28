import click

from .core import create_model, run_agent
from .default_tools import TOOLS
from .tools import get_tool, load_tools


@click.command()
@click.option("--tools", "-t", multiple=True)
@click.option("--tools-files", "-f", multiple=True)
@click.option("--prompt", "-p", prompt="What is the prompt?")
@click.option("--model", "-m", default="ollama_chat/deepseek-r1:14b")
@click.option("--info", "-i", multiple=True)
def main(
    tools,
    tools_files,
    prompt,
    model,
    info,
):
    """A agent that solves a prompt given a system design and a set of tools"""
    tool_classes = {}
    tool_classes.update(TOOLS)
    for tf in tools_files:
        tool_classes.update(load_tools(tf))
    model = create_model(model)
    state = {}

    parts = [prompt]

    if info:
        parts.append("Use this addition information:")

    for i in info:
        with open(i) as f:
            parts.append(f.read())

    prompt = "\n".join(parts)

    for o in run_agent(
        tools=[get_tool(tool_classes, t, state) for t in tools],
        model=model,
        prompt=prompt,
    ):
        print(o)
