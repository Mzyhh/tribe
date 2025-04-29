import clang.cindex as cl
from jinja2 import Template
import typing
import re


def parse_annotations(comment: str) -> dict[typing.Any, typing.Any]:
    '''Extracts Django-style annotations from comments'''
    return dict(re.findall(r'@(\w+)(?:=("[^"]*"|\S+))?', comment))

def gen_table_info(annotations={}) -> dict[str, str]:
    if 'table_name' in annotations:
        return {"table_name": annotations['table_name']}
    return {}

def cpp2sql_type(cpp_type: str, annotations={}) -> str:
    '''Converts original type from cpp file to assotiated SQL type:
        int, uint, etc. -> INTEGER,
        float, double -> REAL,
        string -> TEXT,
        bool -> BOOLEAN,
        year_month_day -> DATE,
        time_point -> DATETIME.'''
    type_map = {
        'int': 'INTEGER',
        'uint': 'INTEGER',
        'std::string': 'TEXT',
        'bool': 'BOOLEAN',
        'std::chrono::time_point': 'DATETIME',
        'std::chrono::year_month_day': 'DATE',
        'double': 'REAL'
    }

    base_type = type_map.get(cpp_type, 'UNRESOLVED')
    
    if 'pk' in annotations:
        base_type += " PRIMARY KEY"
    if 'autoincrement' in annotations:
        base_type += " AUTOINCREMENT"
    if 'unique' in annotations:
        base_type += " UNIQUE"
    if 'not_null' in annotations:
        base_type += " NOT NULL"
    if 'default' in annotations:
        base_type += f" DEFAULT {annotations['default']}"
    if 'max_length' in annotations and 'TEXT' in base_type:
        base_type = f"VARCHAR({annotations['max_length']})"

    return base_type

def set_foreign_keys(tables: typing.List[dict]) -> typing.List[dict]:
    for table in tables:
        for field in filter(lambda x: x['sql_type'] == 'UNRESOLVED' and 
                                      'fk' in x['annotations'], table['fields']): 
            field['sql_type'] = 'INTEGER'
            table["fields"].append({
                            "name": f"FOREIGN KEY ({field['name']}) REFERENCES {field['annotations']['fk']} (id)",
                            "cpp_type": "",
                            "annotations": "",
                            "sql_type": ""
                        })

    return tables


def parse_cpp(filename: str, only_one_file=True) -> typing.List[dict]:
    index = cl.Index.create()
    translation_unit = index.parse(filename, args=["-std=c++17"])
    classes = []

    for node in translation_unit.cursor.walk_preorder():
        if only_one_file and node.location.file and node.location.file.name != filename:
            continue
        if node.kind in [cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_DECL]:
            table_raw_comment = node.raw_comment or ""
            table_annotations = parse_annotations(table_raw_comment) 
            table_info = gen_table_info(table_annotations)
            class_info = {
                "name": node.spelling,
                "table_name": table_info["table_name"] if table_info != {} else node.spelling,
                "fields": []
            }
            for child in node.get_children():
                child_raw_comment = child.raw_comment or ""
                annotations = parse_annotations(child_raw_comment)
                if child.kind == cl.CursorKind.FIELD_DECL:
                    cpp_type = child.type.spelling
                    sql_type = cpp2sql_type(cpp_type, annotations)
                    class_info["fields"].append({
                        "name": child.spelling,
                        "cpp_type": cpp_type,
                        "annotations": annotations,
                        "sql_type": sql_type
                    })
            classes.append(class_info)
    classes = set_foreign_keys(classes)
    return classes


if __name__ == "__main__":
    classes = parse_cpp("db_models.hpp")

    template = Template("""
    {% for class in classes %}
    CREATE TABLE {{ class.table_name }} (
        {% for field in class.fields %}
        {{ field.name }} {{ field.sql_type }}{% if not loop.last %},{% endif %}
        {% endfor %}
    );
    {% endfor %}
    """)
    
    print(template.render(classes=classes), end="")
