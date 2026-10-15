from utils.constants import ROLE_MEMBER

def active_members(users_dict):
    if not isinstance(users_dict, dict):
        return

    for user in users_dict.values():

        role = getattr(user, 'role', None)
        is_active = getattr(user, 'is_active', None)

        if role == ROLE_MEMBER and is_active:
            yield user

def coach_classes(coach_username, classes_list):

    if not classes_list:
        return

    for gym_class in classes_list:
        c_user = getattr(gym_class, 'coach_username', None)

        if c_user is None:
            coach_attr = getattr(gym_class, 'coach', None )
            c_user = getattr(coach_attr, 'username', coach_attr )

        if c_user == coach_username :
            yield gym_class
        
def class_members(class_obj, users_dict):

    if not class_obj or not users_dict:
        return

    #گرفتن لیست ثبت نامی های این کلاس
    enrollments = getattr(class_obj, 'enrollments', []) or []

    for enr in enrollments:

        #اول ببینم ثبت نامش فعاله یا نه
        enr_active = getattr(enr, 'is_active', True)
        if callable(enr_active):
            enr_active = enr_active()

        if not enr_active:
            continue

        #پیدا کردن یوزر نیم ممبر
        uname = getattr(enr, 'member_username', None) or getattr(enr, 'username', None)
        if not uname:
            continue

        #گرفتن شی ممبر از دیکشنری ممبرها
        user = users_dict.get(uname)
        if not user:
            continue

        # ببینم اصلاً خود کاربر فعال هست؟
        user_active = getattr(user, 'is_active', True)
        if callable(user_active):
            user_active = user_active()

        if user_active:
            yield user