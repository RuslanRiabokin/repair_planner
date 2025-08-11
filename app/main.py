from fastapi import FastAPI
from nicegui import ui
from app.api import routes_repair
from app.gui import dashboard

app = FastAPI()

# Роуты API
app.include_router(routes_repair.router)

# Роут NiceGUI
@ui.page('/')
def index():
    dashboard.show()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
