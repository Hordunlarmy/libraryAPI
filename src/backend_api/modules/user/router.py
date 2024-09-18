from fastapi import APIRouter
from modules.user.manager import UserManager

user_router = APIRouter(prefix="/api/users")
user_manager = UserManager()


@user_router.get("/")
async def get_all_users():
    """
    Get all users
    """

    return await user_manager.get_all_users()


@user_router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Get user data
    """

    return await user_manager.get_user(user_id)
