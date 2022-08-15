```python
#python==3.10.5

from addlogging import async_addloging, addlogging
import asyncio

@async_addlogging
async def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"
    
asyncio.run(make_greeting("Misaki"))
```

```
INFO    - addlogging.wrapper_addlogging: Calling make_greeting('Misaki')
INFO    - addlogging.wrapper_addlogging: 'make_greeting' returned 'Howdy Misaki!'
```
