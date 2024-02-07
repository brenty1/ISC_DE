from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    field_validator,
    json
)
import json
import datetime
from typing import Optional

class ModelItem(BaseModel):
    id: int
    code: str
    description: Optional[str]
    status: str
    date_opened: Optional[str]
    date_closed: Optional[str]

    #status closed AND date_closed not null
    @field_validator('date_closed')
    @classmethod
    def check_closed(cls, v: str, info: ValidationInfo) -> str:
        if info.data['status'] == 'CLOSED' and v is None:
            raise Exception('When status is "Closed" date_closed field must be populated: ' + str(info.data))
        return v or None

    #status opened AND date_opened not null
    @field_validator('date_opened')
    @classmethod
    def check_opened(cls, v: str, info: ValidationInfo) -> str:
        if info.data['status'] == 'OPEN' and v is None:
            raise Exception('When status is "Open" date_opened field  must be populated: ' + str(info.data))
        return v or None

    #status both and date_opened not null and date_closed not null
    @field_validator('date_opened','date_closed')
    @classmethod
    def check_both(cls, v: str, info: ValidationInfo) -> str:
        if info.data['status'] == 'BOTH':
            if v is None:
                raise Exception('When status is "Both" date_opened and date_closed fields must be populated: ' + str(info.data))
        return v or None

    #convert empty strings to Null
    @field_validator('code','description','status','date_opened','date_closed')
    @classmethod
    def convert_nulls(cls, v: str) -> str:
        if v == '':
            v = None
        return v

#check if duplicate IDs are in the file
def check_dupes(model):
    dupelist = []
    newlist= []
    for i in model:
        if i.id not in newlist:
            newlist.append(i.id)
        else:
            dupelist.append(i)
    if len(dupelist) > 0:
        raise Exception('Duplicate IDs detected. Check file : ' + str(dupelist))

def read_file():
    #update file path
    in_file = open(r"C:\XXXXXXXXXXXXXXXXXXX.json")
    obj_json = json.load(in_file)
    model = [ModelItem(**d) for d in obj_json]
    check_dupes(model)
    #convert to JSON string
    json_string = json.loads(json.dumps(model, default=vars))
    output_file(json_string)

def output_file(json_string):
    if len(json_string) < 1 or json_string is None:
        raise Exception('Output file not created, check string: ' + json_string)
    format_json = json.dumps(json_string, indent=4)

    #Update file path
    with open(r"C:\XXXXXXXXXXXXXXXXXXXX.json", 'w') as f:
        f.write(format_json)

if __name__ == '__main__':
    read_file()
