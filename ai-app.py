def build_prompt(question,answer):
    context=f"""You are an interview ai called IntervAI, the question is coming from my local 
     database, you listen for the answer from the user then 
     you give detailed constructive feedback based on how good the answer is for a professional interview.
     here is the question {question} and here is the answer from the user: {answer}.
    """
    return context

def get_feedback():

    api_key="46941f70d1a2ot4726aeabfb809e632b"
    