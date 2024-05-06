import json

from aiohttp import web

from tools import get_sha256_hash

async def healthchecker_view(request):
    data = json.dumps({})
    return web.HTTPOk(body=data)

async def hash_view(request):
    string = (await request.json()).get("string")
    
    if not string:
        answer = web.HTTPBadRequest
        data = json.dumps({"validation_errors": "Missing required field 'string'"})
    else:
        answer = web.HTTPOk
        hashed_string = get_sha256_hash(string)
        data = json.dumps({"hash_string": hashed_string})

    return answer(body=data)
