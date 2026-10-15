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

        max_num = 0

        if classes_list:
            for c in classes_list:
                cid = getattr(c, 'class_id', None) or getattr(c, 'id', None)

                if cid is None and isinstance(c, dict):
                    cid = c.get('class_id') or c.get('id')

                if isinstance(cid, str) and cid.startswith('C'):
                    num_part = cid[1:]
                    if num_part.isdigit():
                        num = int(num_part)
                        max_num = max(max_num, int(num_part))


        return f"C{max_num + 1:03d}"

