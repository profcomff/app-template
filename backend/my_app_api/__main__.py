import uvicorn

from my_app_api.routes import app


if __name__ == '__main__':
    uvicorn.run(app)
