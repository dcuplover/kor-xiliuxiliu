from utils import get_schema
from kor import from_pydantic

def get_schema_and_validator(schema_name=''):
    schema, description, examples, many = get_schema(schema_name)

    # 生成schema, validator
    schema, validator = from_pydantic(
        schema,
        description=description,
        examples=examples,
        many=many,
    )

    return schema, validator