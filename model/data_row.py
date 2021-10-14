from dataclasses import dataclass, fields
from typing import List

need_quotations = [
    str
]


@dataclass
class DataRow:
    @classmethod
    def field_names_list(cls):
        fields_str_list = list(map(lambda x: str(x.name), fields(cls)))
        return list(filter(lambda x: not x.startswith('_'), fields_str_list))

    @classmethod
    def field_names_sql_str(cls):
        field_names_list = cls.field_names_list()
        field_names_str = ", ".join(field_names_list)
        return f"({field_names_str})"

    # reflection tostring method for SQL
    def field_values(self) -> List[str]:
        field_values_as_strings = []
        for field_name in self.__class__.field_names_list():
            field_type = self.__annotations__[field_name]
            field_value = self.__getattribute__(field_name)
            if field_value is None:
                field_value = "null"
            elif field_type in need_quotations:
                sanitized_field_value =str(field_value).replace("'", '')
                field_value = f"'{sanitized_field_value}'"
            field_values_as_strings.append(str(field_value))
        return field_values_as_strings
