from fastapi import Depends
from fastapi.routing import APIRoute
from qflash_jwt_package.jwt import JWT


jwt = JWT()


class AuthenticatedRoute(APIRoute):
    def __init__(self,*args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(jwt.auth_wrapper))
        kwargs["dependencies"] = dependencies
        super(AuthenticatedRoute, self).__init__(*args, **kwargs)
