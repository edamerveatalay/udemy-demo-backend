from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

from app.routers import auth, courses, purchase, matching, payment
from app.routers import users as users_router
from app.routers import instructor as instructor_router
from app.routers import admin as admin_router

security_scheme = HTTPBearer()

app = FastAPI(
    title="Udemy Demo Backend",
    version="1.0.0",
    description="Demo amaçlı FastAPI backend",
)


app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(purchase.router)
app.include_router(matching.router)
app.include_router(payment.router)
app.include_router(users_router.router)
app.include_router(instructor_router.router)
app.include_router(admin_router.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Udemy Demo Backend",
        version="1.0.0",
        description="Demo backend API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Udemy Demo Backend is running"}
