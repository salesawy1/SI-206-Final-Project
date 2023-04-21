def python_to_sql_types(type):
    types_map = {
        'str': 'TEXT',
        'int': 'INTEGER',
        'bool': 'BOOLEAN',
        'float': 'FLOAT',
    }

    return types_map[type]

# generate the sql column types using data we have
def generate_sql_columns_from_data(data):
    column_map = []
    for key in data[0].keys():
        value = data[0][key]
        value_type = type(value).__name__
        if value_type == 'dict':
            for sub_key in value.keys():
                sub_value = value[sub_key]
                sub_value_type = type(sub_value).__name__
                sql_value_type = python_to_sql_types(sub_value_type)
                column_map.append({
                    'name': key + '_' + sub_key,
                    'type': sql_value_type
                })
        else:
            sql_value_type = python_to_sql_types(value_type)
            column_map.append({
                'name': key,
                'type': sql_value_type
            })

    return column_map