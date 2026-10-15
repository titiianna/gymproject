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
        
    