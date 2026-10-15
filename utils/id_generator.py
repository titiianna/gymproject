import uuid
from datetime import datetime

class IdGenerator:

    @staticmethod
    def tracking_id(prefix):

        date_str = datetime.now().strftime("%Y%m%d")

        random_hex = uuid.uuid4().hex[:8].upper()

        return f"{prefix.upper()}-{date_str}-{random_hex}"

    @staticmethod
    def class_id(classes_list):

        if classes_list:
            for c in classes_list:
                cid = getattr(c, 'class_id', None) or getattr(c, 'id', None)
                if cid is None and isinstance(c, dict):
                    cid = c.get('class_id') or c.get('id')

