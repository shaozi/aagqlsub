import asyncio
from ariadne import SubscriptionType, make_executable_schema
from ariadne.asgi import GraphQL

type_def = """
    type Query {
        _unused: Boolean
    }

    type Subscription {
        counter: Int!
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


schema = make_executable_schema(type_def, subscription)
app = GraphQL(schema, debug=True)
