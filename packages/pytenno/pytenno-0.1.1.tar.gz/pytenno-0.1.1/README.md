# PyTenno
PyTenno is an asynchronous wrapper for the [warframe.market](https://warframe.market) API, written in Python.

[Read Documentation](https://pytenno.readthedocs.io/en/latest/index.html)

### Disclaimer
PyTenno is not associated with warframe.market or any of its affiliates.
PyTenno is not associated with Digital Extremes or any of its affiliates.

## Installation

### Git
Use your favorite spice of the following:

```bash
py -m pip install git+https://github.com/ShadowMagic896/pytenno.git
```
- [Git-SCM](https://git-scm.com/) is required for direct installation

### PyPi

```bash
py -m pip install pytenno
```

## Requirements
The project's only requirement is aiohttp, which is available on PyPi.

[aiohttp](https://aiohttp.readthedocs.io/en/stable/index.html) >= 3.8.1

## Skill-Set Requirements

### PyTenno Requires Fundamental understanding of the following:
1. Python datatypes, attributes, etc.
2. Asyncrhonous programming in Python (Coroutines, `async`, `await`)
3. Fundamental understanding of context managers in Python (`async with`)
4. How [warframe.market](https://warframe.market) works 
5. [Warframe](https://warframe.com/) mechanics

## Examples

### The Following Code Will Be Used in the Examples
```python

import asyncio # To use asynchronous programming
import pytenno
from pytenno.models.enums import Platform # To specify platforms for requests

async def main(): # PyTenno is asynchronous, so it must be done in an asynchronous context
    default_language = "en" # Set default response language to English
    default_platform = Platform.pc # Set default platform to PC

    # Create a client with the default language and platform
    # This must be done in an asynchronous context manager (async with ... [as ...])
    async with pytenno.PyTenno(default_language, default_platform) as tenno:
        ... # Example code goes here
    
if __name__ == "__main__":
    asyncio.run(main()) # Create a new asyncio loop and run the coroutine
```

### Log into warframe.market
```python
        email = "you@example.com" # Email to account
        password = "password123" # Password to account
        current_user = await tenno.Auth.login(
            email=email,
            password=password
        ) # Log in to warframe.market
        # Note: the API stores absoloutely zero information about data passed. All code
        # is open-source and available at https://github.com/ShadowMagic896/pytenno
        print(current_user.ingame_name) # Print the ingame name of the user that was logged in
```


