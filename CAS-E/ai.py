#step2 text generation using gemini api
import google.generativeai as genai

#configure the Gemini API client
genai.configure(api_key="")#add in the api key in here

def gemini_api(text):
    #initialize the Gemini API client   
    model=genai.GenerativeModel("models/gemini-2.5-flash")
    convo=model.start_chat()
    #generate a response based on input text
    response=model.generate_content(text)
    print(response.text)

#-----Main----
text="what is the weather like in kerala?"  

gemini_api(text)

