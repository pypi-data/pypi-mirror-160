class _Singleton:
    """
    Singleton pattern realization.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

        return cls.__instance


__all__ = ['_Singleton']