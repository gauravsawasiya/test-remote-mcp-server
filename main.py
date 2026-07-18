from fastmcp import FastMCP
import random
import json

mcp = FastMCP("Simple calculator server")

@mcp.tool
def add(a: int, b:int):
    """add two numbers """

    return a + b

@mcp.tool
def random_number(min_val = 1, max_val= 100):

    return random.randint(min_val,max_val)

@mcp.resource("info://server")
def server_info():

    info = {
        "name": "Simple calculator server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools",
        "tools": ["add","random number"],
        "author": "Gaurav"
    }

    return json.dumps(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", host = "0.0.0.0", port = 8000)
