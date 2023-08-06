class Config(dict):
    """Basic configuration class"""

    def __get_all_configs_user__(self) -> dict:
        """Returns all user-defined configurations"""
        return {key: value for key, value in self.__class__.__dict__.items() if not key.startswith("_")}

    def __init__(self, *args, **kwargs):
        """Initializes the dictionary"""
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs |= args[0]
        else:
            for key, item in enumerate(args):
                kwargs[str(key)] = item

        list_arg = self.__get_all_configs_user__() | kwargs
        super().__init__(list_arg)
