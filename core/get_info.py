from dotenv import load_dotenv
import os
load_dotenv()

def ask(speak,logger,wolframalpha,takeCommand):
    speak('I can answer to computational and geographical questions  and what question do you want to ask now')
    question=takeCommand()
    logger.info("[INFO] Wolframalpth questions: "+question)
    app_id=[os.getenv('WOLFRAMALPTH_KEY1'), os.getenv('WOLFRAMALPTH_KEY1')]
    try:
        client = wolframalpha.Client(app_id[1])
        res = client.query(question)
    except:
        client = wolframalpha.Client(app_id[0])
        res = client.query(question)
    answer = next(res.results).text
    speak(answer)
    print(answer)

def wiki(speak,logger,statement,wikipedia):
    if "search" is statement:
        statement =statement.replace("search", "")
        if "max sentences" in statement:
            max_sentences = statement.split(" ")
            max_sentences = max_sentences[max_sentences.index("sentences") + 1]
            if max_sentences is not int:
                max_sentences = 3
        else:
            max_sentences = 3
        
        statement =statement.replace("wikipedia", "")
        speak('Searching in Wikipedia for '+statement)
        logger.info("[INFO] Wikipedia search or: "+statement)
        results = wikipedia.summary(statement, sentences=max_sentences)
        speak("According to Wikipedia")
        print(results)
        speak(results)