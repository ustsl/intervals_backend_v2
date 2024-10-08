from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes import main_api_router

#########################
# BLOCK WITH API ROUTES #
#########################

# create instance of the app
app = FastAPI(title="INTERVALS BACK-END. BY USTSL.RU")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_api_router)
