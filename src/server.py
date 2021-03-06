import asyncio
from ariadne import SubscriptionType, make_executable_schema
from ariadne.asgi import GraphQL
import uvicorn
from quotes import Quotes

type_def = """
    type Query {
        _unused: Boolean
    }

    type Quote {
        name: String
        progress: Int
        quote: String
    }

    type Subscription {
        counter: Int!
        
        quote(author: String!): Quote!
    }

"""

subscription = SubscriptionType()


@subscription.source("counter")
async def counter_generator(obj, info):
    print('generator started')
    for i in range(50):
        await asyncio.sleep(1)
        print(f'generate {i}')
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1


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
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")
