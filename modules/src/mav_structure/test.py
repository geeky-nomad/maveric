"""
The web entrypoint to the application.
"""
from schemas.partners import say_hello_from_partner

print(say_hello_from_partner())