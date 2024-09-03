import openai

openai.api_key = str(open("token.txt").read())

class ChatGPT():
    def __init__(self):
        self.messages = [
            {
                "role": "system", "content": "You are a helpful assistant."
            }
        ]

    def ChatGPTResponse(self, user_text):
        self.messages.append({"role": "user", "content": user_text})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )

            assistant_response = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        except Exception as e:
            return f"An error occurred: {str(e)}"
