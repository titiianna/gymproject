from datetime import date, datetime
from models.enrollment import Enrollment
from models.subscription import Payment
from models.wallet import Transaction
from utils.Bank import API
from utils.constants import ROLE_MEMBER, TX_DEPOSIT, TX_SUBSCRIPTION, data_path
from utils.decorators import log_action
from utils.file_handler import FileHandler
from utils.id_generator import IdGenerator
from utils.validators import Validators


def _now():

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _record_transaction(tx, transaction_list):

    transaction_list.append(tx)

    line = tx.format_string + "\n"

    FileHandler.txt_append(data_path("transactions.txt"), line)

def _get_member(username, users_dict):

    user = users_dict.get(username)

    if user and getattr(user, 'role', None) == ROLE_MEMBER:
        return True

    return False


class MemberService:

    @staticmethod
    def get_profile(username, users_dict):

        user = _get_member(username, users_dict)

        if not user:
            return None

        return {
            "name": getattr(user, 'name', '-'),
            "username": getattr(user, 'username', '-'),
            "email": getattr(user, 'email', '-'),
            "account_status": getattr(user, 'account_status', '-'),
            "subscription_type": getattr(user, 'subscription_type', '-'),
            "subscription_start": getattr(user, 'subscription_start', '-'),
            "subscription_end": getattr(user, 'subscription_end', '-'),
            "subscription_status": getattr(user, 'subscription_status', '-')
        }



