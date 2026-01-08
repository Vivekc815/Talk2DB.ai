import re
FORBIDDEN_SQL_KEYWORDS = [
    "delete",
    "drop",
    "truncate",
    "alter",
    "update",
    "insert"
]

def sql_safety(sql : str):
    sql_lower = sql.lower()
    for keyword in FORBIDDEN_SQL_KEYWORDS:
        if re.search(rf'\b{keyword}\b', sql_lower):
            return (False, f"Might be dangerous {keyword}")
    # 2. Check for multiple statements 
    if sql.count(';') > 1:
        return (False, "Multiple statements not allowed")
    return (True, None)