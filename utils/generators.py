from utils.constants import ROLE_MEMBER

def active_members(users_dict):
    if not isinstance(users_dict, dict):
        return

    for user in users_dict.values():

        role = getattr(user, 'role', None)
        is_active = getattr(user, 'is_active', None)

        if role == ROLE_MEMBER and is_active:
            yield user