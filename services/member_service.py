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

def _refresh_subscription_status(user):

    sub_end = getattr(user, 'subscription_end', '-')
    if not sub_end or sub_end == "-":
        user.subscription_status = "بدون اشتراک"
        return

    try:
        
        end_date = datetime.strptime(str(sub_end), "%Y-%m-%d %H:%M:%S")
        
        
        now = datetime.strptime(_now(), "%Y-%m-%d %H:%M:%S")

        if now > end_date:
            user.subscription_status = "Expired"
        else:
            user.subscription_status = "Active"

    except (ValueError, TypeError):
        pass


def _get_member(username, users_dict):

    user = users_dict.get(username)

    if user and getattr(user, 'role', None) == ROLE_MEMBER:
        return user

    return None


class MemberService:

    @staticmethod
    def get_profile(username, users_dict):

        user = _get_member(username, users_dict)

        if not user:
            return None

        _refresh_subscription_status(user)

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

    @staticmethod
    def get_balance(username, wallets_dict):

        wallet = wallets_dict.get(username)

        if not wallet:
            return 0.0

        wallet_balance = getattr(wallet, 'balance', 0.0)

        return wallet_balance

    @staticmethod
    @log_action('deposit_wallet')
    def deposit_wallet(username, amount, card, exp_month, exp_year, password, cvv2, wallets_dict, transactions_list):

        if not Validators.positive_int_validate(amount):
            return False, "مبلغ وارد شده نامعتبر است."

        wallet = wallets_dict.get(username)
        if not wallet:
            return False, "کیف پول کاربر یافت نشد."

        try:
            int_exp_month = int(exp_month)
            int_exp_year = int(exp_year)
            str_card = str(card)
            str_password = str(password)
            str_cvv2 = str(cvv2)

            bank_api = API()
            bank_api.pay(str_card, int_exp_month, int_exp_year, str_password, str_cvv2, amount)

        except(ValueError,TypeError):
            return False, "خطا در پردازش اطلاعات کارت یا خطا در ارتباط با بانک"


        tracking_id = IdGenerator.tracking_id('TX')
        current_time = _now

        wallet.deposit(amount)

        tx = Transaction(
            tracking_id=tracking_id,
            username=username,
            type=TX_DEPOSIT,
            amount=amount,
            date=current_time
        )

        _record_transaction(tx, transactions_list)

        return True, f"شارژ کیف پول با موفقیت انجام شد. کد پیگیری: {tracking_id}"

    @staticmethod
    def list_transactions(username, transactions_list):

        if not username or not transactions_list:
            return []

        user_transactions = []

        for tx in transactions_list:

            if isinstance(tx, dict):
                tx_username = tx.get("username")

            else:
                tx_username = getattr(tx, "username", None)

            if tx_username == username:
                user_transactions.append(tx)

        return user_transactions

    @staticmethod
    @log_action('subscribe')
    def subscribe(username, plan_title, plans_dict, wallets_dict, users_dict, payments_list, transactions_list):

        member = _get_member(username, users_dict)
        if not member:
            return False, "کاربر یافت نشد یا دسترسی غیرمجاز است."

        if not plans_dict or plan_title not in plans_dict:
            return False, "طرح مورد نظر یافت نشد."

        
        plan = plans_dict[plan_title]


        price = getattr(plan, "price", None) if not isinstance(plan, dict) else plan.get("price")
        duration = getattr(plan, "duration", None) if not isinstance(plan, dict) else plan.get("duration")

        if price is None or duration is None:
            return False, "اطلاعات طرح نامعتبر است."

        if not wallets_dict or username not in wallets_dict:
            return False, "کیف پول کاربر یافت نشد."

        wallet = wallets_dict[username]

        current_balance = MemberService.get_balance(username, wallets_dict)

        if current_balance < price:
            return False, "موجودی کیف پول برای خرید این اشتراک کافی نیست."

        wallet.withdraw(price)
        

        
