from configparser import ConfigParser

class Config:
    def __init__(self, config_file="./src/langgraphagenticai/ui/uiconfigfile.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self) -> str:
        return self.config.get('DEFAULT', 'PAGE_TITLE', fallback='LangGraph Agentic AI Chatbot')

    def get_llm_options(self) -> list:
        llm_options = self.config.get('DEFAULT', 'LLM_OPTIONS', fallback='')
        return [option.strip() for option in llm_options.split(',') if option.strip()]

    def get_usecase_options(self) -> list:
        usecase_options = self.config.get('DEFAULT', 'USECASE_OPTIONS', fallback='')
        return [option.strip() for option in usecase_options.split(',') if option.strip()]

    def get_groq_model_options(self) -> list:
        groq_model_options = self.config.get('DEFAULT', 'GROQ_MODEL_OPTIONS', fallback='')
        return [option.strip() for option in groq_model_options.split(',') if option.strip()]