from models.hall import Hall
from models.subscription import Payment, SubscriptionPlan
from models.user import Coach, Member
from models.wallet import Wallet
from utils.constants import ROLE_ADMIN, ROLE_COACH, ROLE_MEMBER, SPORT_TYPES
from utils.decorators import log_action
from utils.id_generator import IdGenerator
from utils.validators import Validators
from datetime import date

from models.class_session import ClassSession


def _blank(value):
    return not isinstance(value, str) or not value.strip()


class AdminService:
    @staticmethod
    @log_action("add_user")
    def add_user(role, name, username, password, email, is_active, users_dict, wallets_dict):
        if role not in (ROLE_COACH, ROLE_MEMBER):
            return False, "Role must be coach or member."
        if not Validators.name_validate(name):
            return False, "Invalid name."
        if not Validators.username_validate(username):
            return False, "Username must start with an English letter and be 3 to 20 characters (letters, digits, _)."
        if not Validators.unique_username_validate(username, users_dict):
            return False, "This username is already taken."
        if not Validators.password_validate(password):
            return False, "Password must contain at least one English letter, one digit and one of @ or &."
        if not Validators.email_validate(email):
            return False, "Invalid email."
        if not isinstance(is_active, bool):
            return False, "Invalid active status."
        cls = Coach if role == ROLE_COACH else Member
        users_dict[username] = cls(name.strip(), username, password, email, is_active)
        if role == ROLE_MEMBER:
            wallets_dict.setdefault(username, Wallet(username))
        return True, "User added successfully."

    @staticmethod
    @log_action("edit_user")
    def edit_user(username, name, password, email, is_active, users_dict):
        user = users_dict.get(username)
        if user is None:
            return False, "User not found."
        if user.role == ROLE_ADMIN:
            return False, "Editing the admin account is not allowed."
        if name is not None and not Validators.name_validate(name):
            return False, "Invalid name."
        if password is not None and not Validators.password_validate(password):
            return False, "Invalid password."
        if email is not None and not Validators.email_validate(email):
            return False, "Invalid email."
        if is_active is not None and not isinstance(is_active, bool):
            return False, "Invalid active status."
        if name is not None:
            user.name = name.strip()
        if password is not None:
            user.password = password
        if email is not None:
            user.email = email
        if is_active is not None:
            user.is_active = is_active
        return True, "User updated."

    @staticmethod
    @log_action("toggle_user_status")
    def toggle_user_status(username, users_dict):
        user = users_dict.get(username)
        if user is None:
            return False, "User not found."
        if user.role == ROLE_ADMIN:
            return False, "Changing the admin account status is not allowed."
        user.is_active = not user.is_active
        return True, "Account activated." if user.is_active else "Account deactivated."

    @staticmethod
    def list_users(users_dict, role=None):
        """Coaches and members (the admin is not listed)."""
        return [u for u in users_dict.values()
                if u.role != ROLE_ADMIN and (role is None or u.role == role)]

    @staticmethod
    @log_action("add_hall")
    def add_hall(name, capacity, equipment, is_active, halls_dict):
        if _blank(name):
            return False, "Hall name cannot be empty."
        name = name.strip()
        if name in halls_dict:
            return False, "A hall with this name already exists."
        if not Validators.positive_int_validate(capacity):
            return False, "Capacity must be a positive integer."
        if not isinstance(equipment, list):
            return False, "Equipment must be a list."
        halls_dict[name] = Hall(name, int(capacity), [str(e).strip() for e in equipment if str(e).strip()],
                                bool(is_active))
        return True, "Hall added."

    @staticmethod
    @log_action("edit_hall")
    def edit_hall(old_name, new_name, capacity, equipment, halls_dict, classes_list):
        hall = halls_dict.get(old_name)
        if hall is None:
            return False, "Hall not found."
        if new_name is not None:
            if _blank(new_name):
                return False, "Hall name cannot be empty."
            new_name = new_name.strip()
            if new_name != old_name and new_name in halls_dict:
                return False, "A hall with this name already exists."
        if capacity is not None:
            if not Validators.positive_int_validate(capacity):
                return False, "Capacity must be a positive integer."
            capacity = int(capacity)
            for c in classes_list:
                if c.hall_name == old_name and c.capacity > capacity:
                    return False, f"Class '{c.title}' has a larger capacity than the new hall capacity."
        if equipment is not None and not isinstance(equipment, list):
            return False, "Equipment must be a list."
        if capacity is not None:
            hall.capacity = capacity
        if equipment is not None:
            hall.equipment = [str(e).strip() for e in equipment if str(e).strip()]
        if new_name is not None and new_name != old_name:
            del halls_dict[old_name]
            hall.name = new_name
            halls_dict[new_name] = hall
            for c in classes_list:
                if c.hall_name == old_name:
                    c.hall_name = new_name
        return True, "Hall updated."

    @staticmethod
    @log_action("toggle_hall_status")
    def toggle_hall_status(name, halls_dict):
        hall = halls_dict.get(name)
        if hall is None:
            return False, "Hall not found."
        hall.is_active = not hall.is_active
        return True, "Hall activated." if hall.is_active else "Hall deactivated."

    @staticmethod
    def list_halls(halls_dict):
        return list(halls_dict.values())

    @staticmethod
    def _check_class(title, sport_type, coach_username, hall_name, day, time, capacity,
                     users_dict, halls_dict, classes_list, exclude_id=None,
                     check_coach=True, check_hall=True, min_capacity=0):
        if _blank(title):
            return False, "Class title cannot be empty."
        if sport_type not in SPORT_TYPES:
            return False, "Invalid sport type."
        coach = users_dict.get(coach_username)
        if check_coach:
            if coach is None or coach.role != ROLE_COACH:
                return False, "Coach not found."
            if not coach.is_active:
                return False, "The coach is inactive."
        hall = halls_dict.get(hall_name)
        if hall is None:
            return False, "Hall not found."
        if check_hall and not hall.is_active:
            return False, "The hall is inactive."
        if not Validators.day_validate(day):
            return False, "Invalid day."
        if not Validators.time_validate(time):
            return False, "Time must be in HH:MM format."
        if not Validators.positive_int_validate(capacity):
            return False, "Capacity must be a positive integer."
        capacity = int(capacity)
        if capacity > hall.capacity:
            return False, "Class capacity exceeds the hall capacity."
        if capacity < min_capacity:
            return False, "Capacity is lower than the number of active enrollments."
        for c in classes_list:
            if (c.is_active and c.class_id != exclude_id and c.day == day and c.time == time
                    and (c.coach_username == coach_username or c.hall_name == hall_name)):
                return False, f"Time conflict with class '{c.title}' (the coach or hall is busy at this time)."
        return True, ""

    @staticmethod
    @log_action("create_class")
    def create_class(title, sport_type, coach_username, hall_name, day, time, capacity,
                     users_dict, halls_dict, classes_list):
        ok, msg = AdminService._check_class(title, sport_type, coach_username, hall_name, day,
                                            time, capacity, users_dict, halls_dict, classes_list)
        if not ok:
            return False, msg
        cid = IdGenerator.class_id(classes_list)
        classes_list.append(ClassSession(cid, title.strip(), sport_type, coach_username,
                                         hall_name, day, time, int(capacity)))
        return True, f"Class with ID {cid} created."

    @staticmethod
    @log_action("edit_class")
    def edit_class(class_id, title, sport_type, coach_username, hall_name, day, time, capacity,
                   users_dict, halls_dict, classes_list):
        cls = next((c for c in classes_list if c.class_id == class_id), None)
        if cls is None:
            return False, "Class not found."
        new = {
            "title": cls.title if title is None else title,
            "sport_type": cls.sport_type if sport_type is None else sport_type,
            "coach": cls.coach_username if coach_username is None else coach_username,
            "hall": cls.hall_name if hall_name is None else hall_name,
            "day": cls.day if day is None else day,
            "time": cls.time if time is None else time,
            "capacity": cls.capacity if capacity is None else capacity,
        }
        ok, msg = AdminService._check_class(
            new["title"], new["sport_type"], new["coach"], new["hall"], new["day"], new["time"],
            new["capacity"], users_dict, halls_dict, classes_list, exclude_id=class_id,
            check_coach=new["coach"] != cls.coach_username,
            check_hall=new["hall"] != cls.hall_name,
            min_capacity=len(cls.active_enrollments()))
        if not ok:
            return False, msg
        cls.title = new["title"].strip()
        cls.sport_type = new["sport_type"]
        cls.coach_username = new["coach"]
        cls.hall_name = new["hall"]
        cls.day = new["day"]
        cls.time = new["time"]
        cls.capacity = int(new["capacity"])
        return True, "Class updated."

    @staticmethod
    @log_action("toggle_class_status")
    def toggle_class_status(class_id, classes_list):
        cls = next((c for c in classes_list if c.class_id == class_id), None)
        if cls is None:
            return False, "Class not found."
        if not cls.is_active:  # Reactivation must not create a conflict
            for c in classes_list:
                if (c.is_active and c is not cls and c.day == cls.day and c.time == cls.time
                        and (c.coach_username == cls.coach_username or c.hall_name == cls.hall_name)):
                    return False, f"Cannot activate; conflicts with class '{c.title}'."
        cls.is_active = not cls.is_active
        return True, "Class activated." if cls.is_active else "Class deactivated."

    @staticmethod
    def list_classes(classes_list):
        return list(classes_list)

    @staticmethod
    @log_action("create_plan")
    def create_plan(title, duration_months, price, plans_dict):
        if _blank(title):
            return False, "Plan title cannot be empty."
        title = title.strip()
        if title in plans_dict:
            return False, "A plan with this title already exists."
        if not Validators.positive_int_validate(duration_months):
            return False, "Duration (months) must be a positive integer."
        if not Validators.positive_int_validate(price):
            return False, "Amount must be a positive integer."
        plans_dict[title] = SubscriptionPlan(title, int(duration_months), int(price))
        return True, "Plan created."

    @staticmethod
    def list_plans(plans_dict):
        return sorted(plans_dict.values(), key=lambda p: p.duration_months)

    @staticmethod
    @log_action("assign_subscription")
    def assign_subscription(member_username, plan_title, users_dict, plans_dict, payments_list):
        member = users_dict.get(member_username)
        if member is None or member.role != ROLE_MEMBER:
            return False, "Member not found."
        if not member.is_active:
            return False, "The member's account is inactive."
        plan = plans_dict.get(plan_title)
        if plan is None:
            return False, "Plan not found."
        start, end = member.activate_subscription(plan.title, plan.duration_months)
        payments_list.append(Payment(member_username, plan.title, plan.price,
                                     date.today().isoformat(), start, end,
                                     IdGenerator.tracking_id("PAY")))
        return True, f"Subscription {plan.title} from {start} to {end} recorded."

    @staticmethod
    def list_payments(payments_list, users_dict):
        rows = []
        for p in payments_list:
            row = p.to_dict()
            user = users_dict.get(p.member_username)
            row["member_name"] = user.name if user else p.member_username
            rows.append(row)
        return rows

    @staticmethod
    def list_subscription_statuses(users_dict):
        result = []
        for u in users_dict.values():
            if u.role == ROLE_MEMBER:
                result.append((u.name, u.refresh_subscription_status()))
        return result

    @staticmethod
    def generate_reports(users_dict, classes_list, payments_list):
        return {
            "active_members": sum(1 for u in users_dict.values() if u.role == ROLE_MEMBER and u.is_active),
            "active_coaches": sum(1 for u in users_dict.values() if u.role == ROLE_COACH and u.is_active),
            "active_classes": sum(1 for c in classes_list if c.is_active),
            "total_income": sum(p.amount for p in payments_list),
        }

    @staticmethod
    def advanced_reports(classes_list, payments_list):
        per_class = {c.title: len(c.active_enrollments()) for c in classes_list}
        income_by_plan = {}
        for p in payments_list:
            income_by_plan[p.plan_title] = income_by_plan.get(p.plan_title, 0) + p.amount
        top = max(per_class, key=per_class.get) if per_class else None
        return {"enrollments_per_class": per_class, "income_by_plan": income_by_plan,
                "top_class": top}
