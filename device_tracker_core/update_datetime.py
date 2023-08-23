from datetime import datetime

def update_obj_updated_datetime(obj):
    obj.updated_at = datetime.now()
    obj.save(update_fields=["updated_at"])