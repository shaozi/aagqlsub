import uvicorn
from quotes import Quotes
import asyncio
from ariadne import SubscriptionType, make_executable_schema
from ariadne.asgi import GraphQL

type_def = """
    type Quote {
        name: String
        progress: Int
        quote: String
    }
    type Query {
        _unused: Boolean
    }
    type Subscription {
        quote(author: String!): Quote!
    }
"""

subscription = SubscriptionType()
q = Quotes()

@subscription.source('quote')
async def quote_gen(obj, info, author):
    try:
        print(info.context)
        print('quote generator started')
        seq = 0
        for i in range(100):
            await asyncio.sleep(1)
            quote = q.random()
            print(f'generate quotei {i}')
            yield {
                'name': quote[0] + ' ' + author,
                'progress': i,
                'quote': quote[1]
            }
    finally:
        print('quote generator done')

@subscription.field('quote')
async def get_quote(q, info, author):
    return q



schema = make_executable_schema(type_def, subscription)
app = GraphQL(schema, debug=False)

if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8000, log_level="debug", access_log=False)