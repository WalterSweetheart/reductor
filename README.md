# REDUCTOR - mail system
- author: WalterSweetheart
## ABOUT
Reductor is a simple mail system, and a showcase of the pure architecture design. All modules are replaceable (as it may be seen if look at abadoned db's).
Also used DumbDatabase - simple and clean database built on pure python.
To add endpoint - add it to `__init__.py` in transport/sanic/endpoints (sanic only)
To change realisation of some part of the system just inject it in inject.py