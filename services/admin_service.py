from models.hall import Hall
from models.subscription import Payment, SubscriptionPlan
from models.user import Coach, Member
from models.wallet import Wallet
from utils.constants import ROLE_ADMIN, ROLE_COACH, ROLE_MEMBER, SPORT_TYPES
from utils.id_generator import IdGenerator
from utils.validators import Validators
from datetime import date

from models.class_session import ClassSession


# چک میکنه که مقدار رشته خالی یا None نباشه
def _blank(value):
    if isinstance(value, str) == False:
        return True
    if not value.strip():
        return True
    return False


class AdminService:
    @staticmethod
    def add_user(role, name, username, password, email, is_active, users_dict, wallets_dict):
        if role != ROLE_COACH:
            if role != ROLE_MEMBER:
                return False, "Role must be coach or member."
        if Validators.name_validate(name) == False:
            return False, "Invalid name."
        if Validators.username_validate(username) == False:
            return False, "Username must start with an English letter and be 3 to 20 characters (letters, digits, _)."
        if Validators.unique_username_validate(username, users_dict) == False:
            return False, "This username is already taken."
        if Validators.password_validate(password) == False:
            return False, "Password must contain at least one English letter, one digit and one of @ or &."
        if Validators.email_validate(email) == False:
            return False, "Invalid email."
        if isinstance(is_active, bool) == False:
            return False, "Invalid active status."

        # اگه کوچ بود از کلاس Coach وگرنه Member
        if role == ROLE_COACH:
            cls = Coach
        else:
            cls = Member

        users_dict[username] = cls(name.strip(), username, password, email, is_active)

        # برای ممبر یه کیف پول هم میسازیم
        if role == ROLE_MEMBER:
            wallets_dict.setdefault(username, Wallet(username))

        return True, "User added successfully."

    @staticmethod
    def edit_user(username, name, password, email, is_active, users_dict):
        user = users_dict.get(username)
        if user == None:
            return False, "User not found."
        # اجازه نمیدیم ادمین ویرایش بشه
        if user.role == ROLE_ADMIN:
            return False, "Editing the admin account is not allowed."
        if name != None:
            if Validators.name_validate(name) == False:
                return False, "Invalid name."
        if password != None:
            if Validators.password_validate(password) == False:
                return False, "Invalid password."
        if email != None:
            if Validators.email_validate(email) == False:
                return False, "Invalid email."
        if is_active != None:
            if isinstance(is_active, bool) == False:
                return False, "Invalid active status."

        if name != None:
            user.name = name.strip()
        if password != None:
            user.password = password
        if email != None:
            user.email = email
        if is_active != None:
            user.is_active = is_active

        return True, "User updated."

    @staticmethod
    def toggle_user_status(username, users_dict):
        user = users_dict.get(username)
        if user == None:
            return False, "User not found."
        # ادمین رو نمیشه غیرفعال کرد
        if user.role == ROLE_ADMIN:
            return False, "Changing the admin account status is not allowed."

        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True

        if user.is_active == True:
            return True, "Account activated."
        else:
            return True, "Account deactivated."

    @staticmethod
    def list_users(users_dict, role=None):
        result = []
        for u in users_dict.values():
            # ادمین توی لیست نمیاد
            if u.role == ROLE_ADMIN:
                continue
            if role == None:
                result.append(u)
            elif u.role == role:
                result.append(u)
        return result

    @staticmethod
    def add_hall(name, capacity, equipment, is_active, halls_dict):
        if _blank(name):
            return False, "Hall name cannot be empty."
        name = name.strip()
        if name in halls_dict:
            return False, "A hall with this name already exists."
        if Validators.positive_int_validate(capacity) == False:
            return False, "Capacity must be a positive integer."
        if isinstance(equipment, list) == False:
            return False, "Equipment must be a list."

        # فاصله‌های اضافی رو حذف میکنیم
        clean_equipment = []
        for e in equipment:
            text = str(e).strip()
            if text:
                clean_equipment.append(text)

        halls_dict[name] = Hall(name, int(capacity), clean_equipment, bool(is_active))
        return True, "Hall added."

    @staticmethod
    def edit_hall(old_name, new_name, capacity, equipment, halls_dict, classes_list):
        hall = halls_dict.get(old_name)
        if hall == None:
            return False, "Hall not found."

        if new_name != None:
            if _blank(new_name):
                return False, "Hall name cannot be empty."
            new_name = new_name.strip()
            if new_name != old_name:
                if new_name in halls_dict:
                    return False, "A hall with this name already exists."

        # ظرفیت جدید نباید از کلاس‌های موجود کمتر بشه
        if capacity != None:
            if Validators.positive_int_validate(capacity) == False:
                return False, "Capacity must be a positive integer."
            capacity = int(capacity)
            for c in classes_list:
                if c.hall_name == old_name:
                    if c.capacity > capacity:
                        return False, "Class '" + c.title + "' has a larger capacity than the new hall capacity."

        if equipment != None:
            if isinstance(equipment, list) == False:
                return False, "Equipment must be a list."

        if capacity != None:
            hall.capacity = capacity

        if equipment != None:
            clean_equipment = []
            for e in equipment:
                text = str(e).strip()
                if text:
                    clean_equipment.append(text)
            hall.equipment = clean_equipment

        # اگه اسم عوض شده، تو کلاس‌ها هم آپدیتش میکنیم
        if new_name != None:
            if new_name != old_name:
                del halls_dict[old_name]
                hall.name = new_name
                halls_dict[new_name] = hall
                for c in classes_list:
                    if c.hall_name == old_name:
                        c.hall_name = new_name

        return True, "Hall updated."

    @staticmethod
    def toggle_hall_status(name, halls_dict):
        hall = halls_dict.get(name)
        if hall == None:
            return False, "Hall not found."

        if hall.is_active == True:
            hall.is_active = False
        else:
            hall.is_active = True

        if hall.is_active == True:
            return True, "Hall activated."
        else:
            return True, "Hall deactivated."

    @staticmethod
    def list_halls(halls_dict):
        return list(halls_dict.values())

    # این تابع کلی چک‌های مربوط به کلاس رو انجام میده
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
            if coach == None:
                return False, "Coach not found."
            if coach.role != ROLE_COACH:
                return False, "Coach not found."
            if coach.is_active == False:
                return False, "The coach is inactive."

        hall = halls_dict.get(hall_name)
        if hall == None:
            return False, "Hall not found."
        if check_hall:
            if hall.is_active == False:
                return False, "The hall is inactive."

        if Validators.day_validate(day) == False:
            return False, "Invalid day."
        if Validators.time_validate(time) == False:
            return False, "Time must be in HH:MM format."
        if Validators.positive_int_validate(capacity) == False:
            return False, "Capacity must be a positive integer."

        capacity = int(capacity)

        if capacity > hall.capacity:
            return False, "Class capacity exceeds the hall capacity."
        if capacity < min_capacity:
            return False, "Capacity is lower than the number of active enrollments."

        # چک تداخل زمانی با کلاس‌های فعال دیگه
        for c in classes_list:
            if c.is_active:
                if c.class_id != exclude_id:
                    if c.day == day:
                        if c.time == time:
                            if c.coach_username == coach_username or c.hall_name == hall_name:
                                return False, "Time conflict with class '" + c.title + "' (the coach or hall is busy at this time)."

        return True, ""

    @staticmethod
    def create_class(title, sport_type, coach_username, hall_name, day, time, capacity,
                     users_dict, halls_dict, classes_list):
        result = AdminService._check_class(title, sport_type, coach_username, hall_name, day,
                                           time, capacity, users_dict, halls_dict, classes_list)
        ok = result[0]
        msg = result[1]
        if ok == False:
            return False, msg

        cid = IdGenerator.class_id(classes_list)
        classes_list.append(ClassSession(cid, title.strip(), sport_type, coach_username,
                                         hall_name, day, time, int(capacity)))
        return True, "Class with ID " + cid + " created."

    @staticmethod
    def edit_class(class_id, title, sport_type, coach_username, hall_name, day, time, capacity,
                   users_dict, halls_dict, classes_list):
        cls = None
        for c in classes_list:
            if c.class_id == class_id:
                cls = c
                break

        if cls == None:
            return False, "Class not found."

        # اگه مقداری None باشه، مقدار قبلی رو نگه میداریم
        new = {}

        if title == None:
            new["title"] = cls.title
        else:
            new["title"] = title

        if sport_type == None:
            new["sport_type"] = cls.sport_type
        else:
            new["sport_type"] = sport_type

        if coach_username == None:
            new["coach"] = cls.coach_username
        else:
            new["coach"] = coach_username

        if hall_name == None:
            new["hall"] = cls.hall_name
        else:
            new["hall"] = hall_name

        if day == None:
            new["day"] = cls.day
        else:
            new["day"] = day

        if time == None:
            new["time"] = cls.time
        else:
            new["time"] = time

        if capacity == None:
            new["capacity"] = cls.capacity
        else:
            new["capacity"] = capacity

        # فقط اگه کوچ یا سالن عوض شده، چکشون میکنیم
        if new["coach"] != cls.coach_username:
            check_coach = True
        else:
            check_coach = False

        if new["hall"] != cls.hall_name:
            check_hall = True
        else:
            check_hall = False

        result = AdminService._check_class(
            new["title"], new["sport_type"], new["coach"], new["hall"], new["day"], new["time"],
            new["capacity"], users_dict, halls_dict, classes_list, exclude_id=class_id,
            check_coach=check_coach, check_hall=check_hall,
            min_capacity=len(cls.active_enrollments()))

        ok = result[0]
        msg = result[1]
        if ok == False:
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
    def toggle_class_status(class_id, classes_list):
        cls = None
        for c in classes_list:
            if c.class_id == class_id:
                cls = c
                break

        if cls == None:
            return False, "Class not found."

        # موقع فعال‌سازی نباید تداخل داشته باشه
        if cls.is_active == False:
            for c in classes_list:
                if c.is_active:
                    if c is not cls:
                        if c.day == cls.day:
                            if c.time == cls.time:
                                if c.coach_username == cls.coach_username or c.hall_name == cls.hall_name:
                                    return False, "Cannot activate; conflicts with class '" + c.title + "'."

        if cls.is_active == True:
            cls.is_active = False
        else:
            cls.is_active = True

        if cls.is_active == True:
            return True, "Class activated."
        else:
            return True, "Class deactivated."

    @staticmethod
    def list_classes(classes_list):
        return list(classes_list)

    @staticmethod
    def create_plan(title, duration_months, price, plans_dict):
        if _blank(title):
            return False, "Plan title cannot be empty."
        title = title.strip()
        if title in plans_dict:
            return False, "A plan with this title already exists."
        if Validators.positive_int_validate(duration_months) == False:
            return False, "Duration (months) must be a positive integer."
        if Validators.positive_int_validate(price) == False:
            return False, "Amount must be a positive integer."

        plans_dict[title] = SubscriptionPlan(title, int(duration_months), int(price))
        return True, "Plan created."

    @staticmethod
    def list_plans(plans_dict):
        # مرتب‌سازی بر اساس تعداد ماه
        return sorted(plans_dict.values(), key=lambda p: p.duration_months)

    @staticmethod
    def assign_subscription(member_username, plan_title, users_dict, plans_dict, payments_list):
        member = users_dict.get(member_username)
        if member == None:
            return False, "Member not found."
        if member.role != ROLE_MEMBER:
            return False, "Member not found."
        if member.is_active == False:
            return False, "The member's account is inactive."

        plan = plans_dict.get(plan_title)
        if plan == None:
            return False, "Plan not found."

        result = member.activate_subscription(plan.title, plan.duration_months)
        start = result[0]
        end = result[1]

        # یه فاکتور پرداخت هم ثبت میکنیم
        payments_list.append(Payment(member_username, plan.title, plan.price,
                                     date.today().isoformat(), start, end,
                                     IdGenerator.tracking_id("PAY")))
        return True, "Subscription " + plan.title + " from " + start + " to " + end + " recorded."

    @staticmethod
    def list_payments(payments_list, users_dict):
        rows = []
        for p in payments_list:
            row = p.to_dict()
            user = users_dict.get(p.member_username)
            if user != None:
                row["member_name"] = user.name
            else:
                row["member_name"] = p.member_username
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
        active_members = 0
        for u in users_dict.values():
            if u.role == ROLE_MEMBER:
                if u.is_active == True:
                    active_members = active_members + 1

        active_coaches = 0
        for u in users_dict.values():
            if u.role == ROLE_COACH:
                if u.is_active == True:
                    active_coaches = active_coaches + 1

        active_classes = 0
        for c in classes_list:
            if c.is_active == True:
                active_classes = active_classes + 1

        # مجموع درآمد از همه پرداخت‌ها
        total_income = 0
        for p in payments_list:
            total_income = total_income + p.amount

        return {
            "active_members": active_members,
            "active_coaches": active_coaches,
            "active_classes": active_classes,
            "total_income": total_income,
        }

    @staticmethod
    def advanced_reports(classes_list, payments_list):
        # تعداد ثبت‌نام هر کلاس
        per_class = {}
        for c in classes_list:
            per_class[c.title] = len(c.active_enrollments())

        # درآمد به تفکیک پلن
        income_by_plan = {}
        for p in payments_list:
            if p.plan_title in income_by_plan:
                income_by_plan[p.plan_title] = income_by_plan[p.plan_title] + p.amount
            else:
                income_by_plan[p.plan_title] = p.amount

        # پرطرفدارترین کلاس
        top = None
        if per_class:
            best = None
            for title in per_class:
                if best == None:
                    best = title
                elif per_class[title] > per_class[best]:
                    best = title
            top = best

        return {
            "enrollments_per_class": per_class,
            "income_by_plan": income_by_plan,
            "top_class": top
        }