from models.hall import Hall
from utils.validators import Validators


class AdminService:
#بخش افزودن سالن جدید 

    @staticmethod
    def add_hall(name, capacity, equipment, is_active, halls_dict):