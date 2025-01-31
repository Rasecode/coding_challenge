from pydantic import BaseModel
from datetime import datetime

class HiredEmployeeSchema(BaseModel):
    id: int
    name: str
    datetime: datetime  # O str, si prefieres tratarlo como string
    department_id: int
    job_id: int