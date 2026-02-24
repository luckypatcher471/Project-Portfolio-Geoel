import google.generativeai as genai

genai.configure(api_key="AIzaSyA_vGq9N5vFjpn4suG6Btcyy_yC2LsM-Ys")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)