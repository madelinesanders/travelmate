import ollama

class OllamaClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print("Creating a new Ollama client instance...")
            cls._instance = ollama.Client(host='http://localhost:11434')
        return cls._instance
