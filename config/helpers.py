from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])

class BaseModelCamel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, 
        alias_generator=to_camel, 
        populate_by_name=True)
