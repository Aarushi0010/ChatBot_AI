import openai 


openai.api_key = str(open("token.txt").read())

class ChatGPT():
    def __init__(self):
        self.messages = [
            {
                "role": "system", "content" : "You are a helpful assistant,"
            }
        ]
    def ChatGPTResponse(self , user_text):
        self.user_text = user_text

        while True :
            self.messages.append({"role":"user" , "content":"user_text"})

            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = self.messages 
            )

            self.messages.append({"role":"assistant" , "content": str(response['choices'][0]['message']['content'])})
             
            print(response['choices'][0]['message']['content'])
            return response['choices'][0]['message']['content']