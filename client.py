import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()
# --------------------------------
# LLM
# --------------------------------
llm = ChatGroq(
model="openai/gpt-oss-20b",
temperature=0
)
async def main():
   # --------------------------------
   # STEP 1: Connect to the MCP server
   # --------------------------------
   client = MultiServerMCPClient(
       {
           "demo_tools": {
               "command": "python",
               "args": ["server.py"],
               "transport": "stdio",
           }
       }
   )
   # --------------------------------
   # STEP 2: Discover tools at runtime
   # --------------------------------
   tools = await client.get_tools()
   print(f"\nDiscovered {len(tools)} tools from MCP server:")
   for tool in tools:
       print(f" - {tool.name}: {tool.description}")
   # --------------------------------
   # STEP 3: Bind discovered tools to the LLM
   # --------------------------------
   llm_with_tools = llm.bind_tools(tools)

   tool_map = {
       tool.name: tool
       for tool in tools
   }
   # --------------------------------
   # STEP 4: Run the agent loop
   # --------------------------------
   user_query = input("\nAsk a question: ")
   messages = [
       (
           "system",
           "You are a helpful assistant with access to "
           "dynamically discovered tools.",
       ),
       (
           "user",
           user_query,
       ),
   ]
   response = await llm_with_tools.ainvoke(messages)
   if not response.tool_calls:
       print("\n========== FINAL ANSWER ==========")
       print(response.content)
       return
   messages.append(response)
   for tool_call in response.tool_calls:
       tool = tool_map[tool_call["name"]]
       result = await tool.ainvoke(
           tool_call["args"]
       )
       messages.append(
           {
               "role": "tool",
               "content": str(result),
               "tool_call_id": tool_call["id"],
           }
       )
   final = await llm_with_tools.ainvoke(messages)
   print("\n========== FINAL ANSWER ==========")
   print(final.content)


if __name__ == "__main__":
   asyncio.run(main())