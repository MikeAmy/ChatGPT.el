# chatgpt.py

import pkg_resources
import openai
import os
assert 'OPENAI_API_KEY' in os.environ


def query(query):
    response = openai.ChatCompletion.create(
        model="gpt4",
        messages=[
            {
                "role": "system",
                "content":'. '.join((
                    "You are an AI emacs assistant",
                    "Respond to the user's requests by describing or rewriting code",
                    "If the user's request sounds like a command that emacs can do,"
                    " generate the emacs-lisp code for that command",
                ))
            },
            {
                "role": "user",
                "content": query
            },
        ],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content']


from epc.server import EPCServer
server = EPCServer(('localhost', 0))
server.register_function(query)
server.print_port()
server.serve_forever()


#if __name__ == '__main__':
#    print(query('hello'))
