from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import delete, desc, func, select, update
from src.database.utils import exception_dal, exception_soft_dal
from src.database.dals import AccountBaseDAL

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class DataDAL(AccountBaseDAL):
    pass
