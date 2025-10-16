from langchain_core.tools import tool
from langgraph.types import interrupt

def multiply(a:int,b:int)->int:
    """Multiply a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a*b

def addition(a:int,b:int)->int:
    """Addition a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a+b

def subtraction(a:int,b:int)->int:
    """Subtract a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a-b

def division(a:int,b:int)->int:
    """Divide a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a/b

def power(base: float, exponent: float) -> float:
    """Raise a base number to a given power.
    
    Args:
        base (float): The base number to raise.
        exponent (float): The power to raise the base number to.
    Returns:
        float: The result of the base raised to the power.
    """
    return base ** exponent

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]