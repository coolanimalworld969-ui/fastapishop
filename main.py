from fastapi import FastAPI

from routers import auth, users, categories, products, orders

app = FastAPI(
    swagger_ui_parameters={
        'persistAuthorization' : True
    }
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
