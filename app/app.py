
from starlette.applications import Starlette
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.routing import Route

templates = Jinja2Templates(directory="templates")

CARDS = tuple()

async def homepage(request: Request):

    return templates.TemplateResponse("index.html", {'request': request, 'cards': CARDS})

app = Starlette(debug=False, routes=[
    Route('/', homepage),
])
