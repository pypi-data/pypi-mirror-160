"""Module for general toolkit functionalities"""


import importlib
import inspect
import pkgutil
from typing import Any, Dict, List


def get_implementations(package, interface: Any) -> Dict[str, Any]:
    """This function provides a way to discover class implementations of `interface`
    in a specific package `package`.

    Example:

    ```python
    from app import package_1

    implementations = get_implementations(package_1, interface)
    ```

    Args:
        package: Package to iterate, pass an imported module.
        interface (Any): Interface to discover implementations for.

    Returns:
        Dict: Pairs of class's name attribute mapped to the class itself.
    """
    class_implementations: List = []
    for module_info in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_info.name)
        classes_found = inspect.getmembers(
            module,
            lambda member: inspect.isclass(member)
            and issubclass(member, interface)
            and member != interface,
        )
        class_implementations = class_implementations + classes_found

    return {c[1].name: c[1] for c in class_implementations}


def add_slash(value: str = None):
    if value is None:
        return ""
    elif value.endswith("/"):
        return value
    else:
        return value + "/"
