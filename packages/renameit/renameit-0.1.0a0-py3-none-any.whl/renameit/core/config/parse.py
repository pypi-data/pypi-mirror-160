"""
This module acts as the center point for reconciling user input from config files, env vars
and other external configuration services.

Everything related to loading, parsing and rendering configurations can be implemented here.

The result data can be used as input for config classes like the ones in
[project][renameit.core.config.project]
"""

from collections import OrderedDict

import confight


def load_config(user_file_path: str = None, user_dir_path: str = None) -> OrderedDict:
    """Load configurations from files.

    Args:
        user_file_path (str, optional): Path to the base config file. Defaults to None.
        user_dir_path (str, optional): Path to the extension config directory. Defaults to None.

    Returns:
        Single dict with all the loaded config
    """
    kwargs = {}
    if user_file_path is not None:
        kwargs.update({"user_file_path": user_file_path})

    if user_dir_path is not None:
        kwargs.update({"user_dir_path": user_dir_path})

    config = confight.load_user_app("renameit", **kwargs)

    return config
