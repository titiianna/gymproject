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
        user.subscription_status = "No subscription"
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
            return False, "The entered amount is invalid."

        wallet = wallets_dict.get(username)
        if not wallet:
            return False, "User wallet not found."

        try:
            int_exp_month = int(exp_month)
            int_exp_year = int(exp_year)
            str_card = str(card)
            str_password = str(password)
            str_cvv2 = str(cvv2)

            bank_api = API()
            bank_api.pay(str_card, int_exp_month, int_exp_year, str_password, str_cvv2, amount)

        except(ValueError,TypeError):
            return False, "Error processing card or connecting to the bank."

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

        return True, f"Wallet deposit successful. Tracking code : {tracking_id}"

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
            return False, "User not found or unouthorized access."

        if not plans_dict or plan_title not in plans_dict:
            return False, "The requested plan was not found."

        
        plan = plans_dict[plan_title]


        price = getattr(plan, "price", None) if not isinstance(plan, dict) else plan.get("price")
        duration = getattr(plan, "duration", None) if not isinstance(plan, dict) else plan.get("duration")

        if price is None or duration is None:
            return False, "Invalid plan information."

        if not wallets_dict or username not in wallets_dict:
            return False, "User wallet was not found."

        wallet = wallets_dict[username]

        current_balance = MemberService.get_balance(username, wallets_dict)

        if current_balance < price:
            return False, "Insufficient wallet balance to purchase this subscription."

        wallet.withdraw(price)

        duration = getattr(plan, 'duration', None) or plan.get('duration', 30)
        member.activate_subscription(duration)

        tracking_id = IdGenerator.tracking_id('PAY')

        payment = Payment(
            username=username,
            amount=price,
            plan_title=plan_title,
            tracking_id=tracking_id,
            timestamp=_now()
        )
        if payments_list is not None:
            payments_list.append(payment)


        tx_data = {
            "username": username,
            "amount": price,
            "type": TX_SUBSCRIPTION,
            "tracking_id": tracking_id,
            "timestamp": _now()
        }

        _record_transaction(tx_data, transactions_list)

        return True, "Subscription purchased successfully."

    @staticmethod
    def list_available_classes(classes_list):

        if not classes_list:
            return []

        available = []
        for c in classes_list:

            active = getattr(c, 'is_active', True)
            if callable(active):
                active = active()

            capacity = getattr(c, 'capacity', 0)
            enrolled = len(getattr(c, 'enrolled_members', getattr(c, 'enrolled', [])))

            is_full = getattr(c, 'is_full', False)

            if callable(is_full):
                is_full = is_full()
            else:
                is_full = bool(is_full) or (capacity > 0 and enrolled >= capacity)

            if active and not is_full:
                available.append(c)

        return available

    @staticmethod
    @log_action('enroll_class')
    def enroll_class(username, class_id, users_dict, classes_list):

        if not users_dict or username not in users_dict:
            return False, "Member not found."

        member = users_dict[username]

        is_active_member = getattr(member, 'is_active', True)
        if callable(is_active_member):
            is_active_member = is_active_member()

        if not is_active_member:
            return False, "Member account is inactive."

        has_subscription = getattr(member, 'has_active_subscription', None)
        if not callable(has_subscription) or not has_subscription():
            return False, "Member does not have an active subscription."

            
        target_class = None
        for gym_class in classes_list or []:
            current_id = getattr(
                gym_class,
                'id',
                getattr(gym_class, 'class_id', None)
            )
            if current_id == class_id:
                target_class = gym_class
                break

            if target_class is None:
                return False, "Class not found."

            class_active = getattr(target_class, 'is_active', False)
            if callable(class_active):
                class_active = class_active()

            if not class_active:
                return False, "Class is inactive."
            
            #ممبر قبلا در این کلاس ثبت نام کرده یا نه
            registered_classes = getattr(member, 'registered_classes', [])
            if class_id in registered_classes:
                return False, "Member is already enrolled in this class."
            
            #ظرفیت کلاس پر نشده باشد
            is_full = getattr(target_class, 'is_full', False)
            if callable(is_full):
                is_full = is_full()

            if is_full:
                return False, "Class is full."

            #رسید ثبت نام
            tracking_id = IdGenerator.trackimg_id('ENR')
            enrollment_date = date.today().isoformat()

            enrollment = Enrollment(username, enrollment_date, tracking_id)

            #ثبت رسید و اتصال به کلاس ممبر
            if not hasattr(target_class, 'enrollments') or target_class.enrollments is None:
                target_class.enrollments = []
                target_class.enrollments.append(enrollment)

            #کلاس آیدی را به لیست کلاس های ثبت نامی خود عضو متصل می کنم
            if not hasattr(member, 'registered_classes') or member.registered_classes is None:
                member.registered_classes = []
                member.registered_classes.append(class_id)

            return True, f"Enrollment successful. Tracking ID: {tracking_id}"

            