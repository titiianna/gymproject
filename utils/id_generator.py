import uuid
from datetime import datetime

class IdGenerator:

    @staticmethod
    def tracking_id(prefix):

        date_str = datetime.now().strftime("%Y%m%d")

        random_hex = uuid.uuid4().hex[:8].upper()

        return f"{prefix.upper()}-{date_str}-{random_hex}"