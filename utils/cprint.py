def cprint(condition: bool, *args, **kwargs) -> None:
    """
    Prints on a condition
    :param bool condition: The condition
    :param args: Arguments of builtin print
    :param kwargs: The specified kwargs of builtin print.
    :return: None
    """
    if condition:
        print(*args, **kwargs)


if __name__ == "__main__":
    cprint(False, "Hello World")