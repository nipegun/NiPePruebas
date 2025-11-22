"""Red Team Base Agent"""

import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from cai.agents.guardrails import get_security_guardrails
from cai.sdk.agents import Agent, OpenAIChatCompletionsModel
from cai.tools.command_and_control.sshpass import run_ssh_command_with_credentials  # pylint: disable=import-error
from cai.tools.reconnaissance.exec_code import execute_code  # pylint: disable=import-error
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command  # pylint: disable=import-error
from cai.tools.reconnaissance.shodan import shodan_host_info, shodan_search  # pylint: disable=import-error
from cai.tools.web.search_web import make_google_search  # pylint: disable=import-error
from cai.util import create_system_prompt_renderer, load_prompt_template

load_dotenv()

bug_bounter_system_prompt = load_prompt_template("prompts/system_bug_bounter.md")

tools = [
  generic_linux_command,
  execute_code,
  shodan_search,
  shodan_host_info,
]

if os.getenv("GOOGLE_SEARCH_API_KEY") and os.getenv("GOOGLE_SEARCH_CX"):
  tools.append(make_google_search)

input_guardrails, output_guardrails = get_security_guardrails()

bug_bounter_agent = Agent(
  name="Bug Bounter",
  instructions=create_system_prompt_renderer(bug_bounter_system_prompt),
  description=(
    """Agent that specializes in bug bounty hunting and vulnerability discovery.
    Expert in web security, API testing, and responsible disclosure."""
  ),
  tools=tools,
  input_guardrails=input_guardrails,
  output_guardrails=output_guardrails,
  model=OpenAIChatCompletionsModel(
    model=os.getenv("CAI_MODEL", "alias0"),
    openai_client=AsyncOpenAI(),
  ),
)
