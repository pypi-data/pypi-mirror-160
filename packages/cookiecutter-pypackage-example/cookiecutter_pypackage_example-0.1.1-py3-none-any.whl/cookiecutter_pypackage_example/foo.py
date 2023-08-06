def foo(bar: str) -> str:
    """Summary line.

    Extended description of function.

    Args:
        bar (str): Description of bar

    Returns:
        str: Description of return value
    """

    return f"foo{bar}"


if __name__ == "__main__":
    print(foo("bar"))
