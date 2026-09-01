from mangum import Mangum
from app.main import app

# Use Magnum to translate FastAPI's ASGI interface with lambda's event/context invocation model.
handler = Mangum(app)