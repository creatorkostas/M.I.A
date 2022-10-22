class MIA_online:
    
    def __init__(self, api_key):
        self.url = "https://api.carterapi.com/v0/chat"
        self.headers = {
          'Content-Type': 'application/json'
        }
        self.api_key = api_key
        
    def get_response(self, text):
        payload = self.json.dumps({
          "api_key": self.api_key,
          "query": text,
          "uuid": "0000"
        })

        agent_response = self.requests.request("POST", self.url, headers=self.headers, data=payload)
        agent_response = agent_response.json()
        print(agent_response["output"]["text"])

def load_MIA_bot(ChatBot,logger, bot_v="l",online=False,carter_key=""):
    if online and carter_key!="":
        logger.info("[INFO] Loading MIA Chat online module (Carter)")
        return MIA_online(carter_key)
    else:
        try:
            logger.info("[INFO] Loading MIA Chat module")
            if bot_v == "l":
                mia_chat = ChatBot(name='Mokia_Assistant_v0.0.1',
                        storage_adapter='chatterbot.storage.SQLStorageAdapter',
                        database_uri='sqlite:///core/modules_files/database.sqlite3',
                        logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                        'chatterbot.logic.BestMatch',
                                        #'chatterbot.logic.TimeLogicAdapter',
                                        'chatterbot.logic.UnitConversion'],
                        read_only=True)                                    
                logger.info("[INFO] MIA_Assistant_v0.0.1 (read_only) started")
            elif bot_v == "f":
                mia_chat = ChatBot(name='Mokia_Assistant_v0.0.1',
                        storage_adapter='chatterbot.storage.SQLStorageAdapter',
                        database_uri='sqlite:///core/modules_files/database.sqlite3',
                        logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                        'chatterbot.logic.BestMatch',
                                        #'chatterbot.logic.TimeLogicAdapter',
                                        'chatterbot.logic.UnitConversion'])
                logger.info("[INFO] MIA_Assistant_v0.0.1 started")

            return mia_chat
        except Exception as e:
            logger.critical("[CRITICAL] Critical Error while tring to load MIA_Assistant_v0.0.1: "+str(e))
        
def load_MIA_brain(ChatBot,logger,bot_v):
    try:
        logger.info("[INFO] Loading MIA Brain")
        if bot_v == "l":
            mia_brain = ChatBot(name='brain',
                                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                database_uri='sqlite:///core/modules_files/brain.sqlite3',
                                logic_adapters=[
                                                {
                                                    'import_path': 'chatterbot.logic.BestMatch',
                                                    'default_response': 'I am sorry, but I do not understand.',
                                                    'maximum_similarity_threshold': 0.90
                                                },
                                                #'chatterbot.logic.TimeLogicAdapter',
                                                'chatterbot.logic.BestMatch'],
                                read_only=True)                                    
            logger.info("[INFO] Brain (read only) started")
            
        elif bot_v == "f":
            mia_brain = ChatBot(name='brain',
                                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                database_uri='sqlite:///core/modules_files/brain.sqlite3',
                                logic_adapters=[
                                                {
                                                    'import_path': 'chatterbot.logic.BestMatch',
                                                    'default_response': 'I am sorry, but I do not understand.',
                                                    'maximum_similarity_threshold': 0.99
                                                },
                                                #'chatterbot.logic.TimeLogicAdapter',
                                                'chatterbot.logic.BestMatch']
                                )
            logger.info("[INFO] Brain started")

        return mia_brain
    except Exception as e:
        logger.critical("[CRITICAL] Critical Error while tring to load Brain: "+str(e))