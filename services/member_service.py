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


def _record_transaction(tx, transactions_list):
    transactions_list.append(tx)
    FileHandler.txt_append(data_path("transactions.txt"), tx.format_string() + "\n")


def _get_member(username, users_dict):
    user = users_dict.get(username)
    if user is None or user.role != ROLE_MEMBER:
        return None
    return user


class MemberService:
    @staticmethod
    def get_profile(username, users_dict):
        member = _get_member(username, users_dict)
        if member is None:
            return None
        member.refresh_subscription_status()
        return {
            "name": member.name, "username": member.username, "email": member.email,
            "account_status": "Active" if member.is_active else "Inactive",
            "subscription_type": member.subscription_type or "-",
            "subscription_start": member.subscription_start or "-",
            "subscription_end": member.subscription_end or "-",
            "subscription_status": member.subscription_status,
        }

    @staticmethod
    def get_balance(username, wallets_dict):
        wallet = wallets_dict.get(username)
        return wallet.balance if wallet else 0.0

    @staticmethod
    @log_action("deposit_wallet")
    def deposit_wallet(username, amount, card, exp_month, exp_year, password, cvv2,
                       wallets_dict, transactions_list):
        wallet = wallets_dict.get(username)
        if wallet is None:
            return False, "Wallet not found."
        if not Validators.positive_int_validate(amount):
            return False, "Amount must be a positive integer."
        amount = int(amount)
        try:
            exp_month, exp_year = int(exp_month), int(exp_year)
        except (TypeError, ValueError):
            return False, "Expiry month and year must be numbers."
        try:
            API().pay(str(card), exp_month, exp_year, str(password), str(cvv2), amount)
        except (ValueError, TypeError):
            return False, "Invalid card details; the payment was not made."
        wallet.deposit(amount)
        tx = Transaction(username, TX_DEPOSIT, amount, "Top up wallet", _now(),
                         IdGenerator.tracking_id("TX"))
        _record_transaction(tx, transactions_list)
        return True, f"Wallet charged. Tracking number: {tx.tracking_id}"

    @staticmethod
    def list_transactions(username, transactions_list):
        return [t for t in transactions_list if t.username == username]

    @staticmethod
    @log_action("subscribe")
    def subscribe(username, plan_title, plans_dict, wallets_dict, users_dict,
                  payments_list, transactions_list):
        member = _get_member(username, users_dict)
        if member is None:
            return False, "Member not found."
        plan = plans_dict.get(plan_title)
        if plan is None:
            return False, "Plan not found."
        wallet = wallets_dict.get(username)
        if wallet is None:
            return False, "Wallet not found."
        if wallet.balance < plan.price:
            return False, (f"Insufficient balance. Plan price is {plan.price:,} and your balance is "
                           f"{int(wallet.balance):,}.")
        wallet.withdraw(plan.price)
        start, end = member.activate_subscription(plan.title, plan.duration_months)
        pay_id = IdGenerator.tracking_id("PAY")
        payments_list.append(Payment(username, plan.title, plan.price,
                                     date.today().isoformat(), start, end, pay_id))
        _record_transaction(Transaction(username, TX_SUBSCRIPTION, plan.price,
                                        f"Subscription purchase {plan.title}", _now(), pay_id),
                            transactions_list)
        return True, f"Subscription {plan.title} from {start} to {end} activated. Tracking number: {pay_id}"

    @staticmethod
    def list_available_classes(classes_list):
        return [c for c in classes_list if c.is_active and not c.is_full]

    @staticmethod
    @log_action("enroll_class")
    def enroll_class(username, class_id, users_dict, classes_list):
        member = _get_member(username, users_dict)
        if member is None:
            return False, "Member not found."
        if not member.is_active:
            return False, "Your account is inactive."
        if not member.has_active_subscription():
            return False, "You need an active subscription to enroll."
        cls = next((c for c in classes_list if c.class_id == class_id), None)
        if cls is None:
            return False, "Class not found."
        if not cls.is_active:
            return False, "This class is inactive."
        if cls.has_active_member(username):
            return False, "You are already enrolled in this class."
        if cls.is_full:
            return False, "This class is full."
        tracking = IdGenerator.tracking_id("ENR")
        cls.enrollments.append(Enrollment(username, date.today().isoformat(), tracking))
        if class_id not in member.registered_classes:
            member.registered_classes.append(class_id)
        return True, f"Enrolled successfully. Tracking number: {tracking}"

    @staticmethod
    @log_action("cancel_class_enrollment")
    def cancel_class_enrollment(username, class_id, users_dict, classes_list):
        member = _get_member(username, users_dict)
        if member is None:
            return False, "Member not found."
        cls = next((c for c in classes_list if c.class_id == class_id), None)
        if cls is None:
            return False, "Class not found."
        enrollment = cls.get_enrollment(username)
        if enrollment is None:
            return False, "You have no active enrollment in this class."
        enrollment.cancel()
        if class_id in member.registered_classes:
            member.registered_classes.remove(class_id)
        return True, "Enrollment cancelled (history is kept)."

    @staticmethod
    def get_member_programs(username, programs_dict, classes_list):
        active_ids = {c.class_id for c in classes_list if c.has_active_member(username)}
        return [p for p in programs_dict.values()
                if p.member_username == username and p.class_id in active_ids]
