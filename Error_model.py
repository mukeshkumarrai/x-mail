from dataclasses import dataclass

@dataclass
class Error_log(object):
  def __init__(self):
        error_msg: any
        error_type: str
        error_source: str
        error_url: str
        created_on: str
        created_by: str
        user_id: int
        hotel_id: int
        service_name: str
        error_priority : str

# example = Error('','','','','','','','','')
# example.field_a = 10
# print(example)  # SimpleDataObject(field_a=1, field_b='b')