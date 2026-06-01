import ast
from typing import Optional, Tuple


def get_subject(scenario_node: ast.ClassDef) -> Tuple[Optional[str], Optional[ast.Assign]]:
    """
    Возвращает строковое значение атрибута `subject` и ast узел присваивания в классе сценария
    Если `subject` отсутствует или не является строкой возвращает (None, None)
    """
    for node in scenario_node.body:
        if isinstance(node, ast.Assign):
            has_subject_target = any(
                isinstance(target, ast.Name) and target.id == "subject"
                for target in node.targets
            )
            if has_subject_target and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                return node.value.value, node
    return None, None
