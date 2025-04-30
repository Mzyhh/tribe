import clang.cindex as cl
from jinja2 import Template
import typing
import re
import sys


def parse_annotations(comment: str) -> dict[typing.Any, typing.Any]:
    '''Extracts Django-style annotations from comments'''
    return dict(re.findall(r'@(\w+)(?:=("[^"]*"|\S+))?', comment))

def cpp2sql_type(cpp_type: str, annotations={}) -> str:
    '''Converts original type from cpp file to assotiated SQL type:
        int, uint, etc. -> INTEGER,
        float, double -> REAL,
        string -> TEXT,
        bool -> BOOLEAN,
        year_month_day -> DATE,
        time_point -> DATETIME.'''
    print(cpp_type, annotations)
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
        base_type += " NOT NULL"
    if 'fk' in annotations:
        base_type = "INTEGER NOT NULL"
    if 'unique' in annotations:
        base_type += " UNIQUE"
    if 'not_null' in annotations:
        base_type += " NOT NULL"
    if 'default' in annotations:
        base_type += f" DEFAULT {annotations['default']}"
    if 'max_length' in annotations and 'TEXT' in base_type:
        base_type = f"VARCHAR({annotations['max_length']})"

    return base_type

def parse_cpp(filename: str, only_one_file=True) -> typing.Dict[typing.Any, typing.Any]:
    '''Parses cpp/hpp file into list of dictionaries. Each dict has
    the following keys:
        "class_name" - name of original class,
        "table_name" - name of table (@table_name in cpp/hpp or class_name),
        "primary_keys" - list of fields that is primary keys (@pk in cpp/hpp),
        "foreign_keys" - list of foreign keys (@fk in cpp/hpp), "fields" - list of all columns with their types and annotations (specifications).
        Each field is a dict with the following keys:
            "name", "cpp_type", "annotations", "sql_type".'''

    index = cl.Index.create()
    translation_unit = index.parse(filename, args=["-std=c++20"])
    tables = {} 

    for node in translation_unit.cursor.walk_preorder():
        if only_one_file and node.location.file and node.location.file.name != filename:
            continue
        if node.kind in [cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_DECL]:
            table_raw_comment = node.raw_comment or ""
            table_annotations = parse_annotations(table_raw_comment) 
            table_name = table_annotations.get("table_name") or node.spelling
            table = {
                "class_name": node.spelling,
                "fields": [],
                "primary_keys": [],
                "foreign_keys": []
            }
            for child in node.get_children():
                child_raw_comment = child.raw_comment or ""
                annotations = parse_annotations(child_raw_comment)
                if child.kind == cl.CursorKind.FIELD_DECL:
                    cpp_type = child.type.spelling
                    print(f"""
                        Field: {child.spelling}
                          Type.spelling: {child.type.spelling}
                          Type.kind: {child.type.kind}
                          Decl.type: {child.get_definition().type.spelling if child.get_definition() else None}
                          Final type: {cpp_type}
                        """)
                    sql_type = cpp2sql_type(cpp_type, annotations)
                    table["fields"].append({
                        "name": child.spelling,
                        "cpp_type": cpp_type,
                        "annotations": annotations,
                        "sql_type": sql_type
                    })
                if 'pk' in annotations:
                    table["primary_keys"].append(child.spelling)
                if 'fk' in annotations:
                    table["foreign_keys"].append({"name": child.spelling,
                                                  "reftable": annotations['fk']})
            tables[table_name] = table
    return tables

if __name__ == "__main__":
    classes = parse_cpp(sys.argv[1])
    template = Template("""
    {% for table_name, class in classes.items() %}
    CREATE TABLE IF NOT EXISTS {{ table_name }} (
        {% for field in class.fields %}
        {{ field.name }} {{ field.sql_type }}{% if not loop.last or class.primary_keys or class.foreign_keys %},{% endif %}
        {% endfor %}
        {% if class.primary_keys %}
        PRIMARY KEY ({% for pk in class.primary_keys %}{{pk}}){% if not loop.last or class.foreign_keys%},{%endif%}{%endfor%}
        {%endif%}
        {% for fk in class.foreign_keys %}
        FOREIGN KEY ({{ fk.name }}) REFERENCES {{ fk.reftable }} ({{ classes[fk.reftable].primary_keys[0] }}){% if not loop.last%},{%endif%}
        {% endfor %}
    );
    {% endfor %}
    """)
    
    print(template.render(classes=classes), end="")
