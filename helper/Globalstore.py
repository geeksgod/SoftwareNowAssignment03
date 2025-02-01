class GLOBALSTORE:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GLOBALSTORE, cls).__new__(cls)
            cls._instance.data = {}  # Shared storage
        return cls._instance

global_store = GLOBALSTORE()
global_store.data["imgPath"] = ""
