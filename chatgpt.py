# chatgpt.py

import pkg_resources
import os


model = 'gpt-3.5-turbo'


def query(query):
    global model
    if query.lower().startswith('using model '):
        close_brace = query.indexof(',', 12)
        model, query = query[12:close_brace], query[close_brace+1:]
        model = '-'.join(model.strip().lower().split())
    if 'OPENAI_API_KEY' not in os.environ:
        return "Please set environment variable OPENAI_API_KEY"
    try:
        import openai
    except ImportError:
        return "Please install openai package. E.g. \npip install openai"
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content":'. '.join((
                        "You are an AI emacs assistant",
                        "Respond to the user by describing or rewriting code",
                        "If the user's request sounds like a command that emacs"
                        " can do, generate the emacs-lisp code for that command",
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
    except Exception as exception:
        return str(exception)

import sys

_, *args = sys.argv
if args:
    print(query(' '.join(args)))
else:
    from epc.server import EPCServer
    server = EPCServer(('localhost', 0))
    server.register_function(query)
    server.print_port()
    server.serve_forever()
