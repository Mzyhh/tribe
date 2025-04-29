import clang.cindex as cl
from jinja2 import Template
import typing


def cpp2sql_type(cpp_type: str) -> str:
    if "int" in cpp_type:
        return "INTEGER"
    elif cpp_type in ["float", "double"]:
        return "REAL"
    elif "string" in cpp_type:
        return "TEXT"
    elif "bool" in cpp_type:
        return "BOOLEAN"
    elif "year_month_day" in cpp_type:
        return "DATE"
    elif "time_point" in cpp_type:
        return "DATETIME"
    else:
        return "WTF"

def parse_cpp(filename: str, only_one_file=True) -> typing.List[dict]:
    index = cl.Index.create()
    translation_unit = index.parse(filename, args=["-std=c++17"])
    classes = []

    for node in translation_unit.cursor.walk_preorder():
        if only_one_file and node.location.file and node.location.file.name != filename:
            continue
        if node.kind in [cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_DECL]:
            class_info = {
                "name": node.spelling,
                "fields": []
            }
            for child in node.get_children():
                if child.kind == cl.CursorKind.FIELD_DECL:
                    cpp_type = child.type.spelling
                    sql_type = cpp2sql_type(cpp_type)
                    class_info["fields"].append({
                        "name": child.spelling,
                        "cpp_type": cpp_type,
                        "sql_type": sql_type
                    })
            classes.append(class_info)

    return classes


if __name__ == "__main__":
    classes = parse_cpp("db_models.hpp")

    template = Template("""
    {% for class in classes %}
    CREATE TABLE {{ class.name }} (
        {% for field in class.fields %}
        {{ field.name }} {{ field.sql_type }}{% if not loop.last %},{% endif %}
        {% endfor %}
    );
    {% endfor %}
    """)
    
    print(template.render(classes=classes), end="")
