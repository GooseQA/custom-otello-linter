import ast
import re
from typing import List, Optional, Tuple

from flake8_plugin_utils import Error

from custom_otello_linter.abstract_checkers import ScenarioChecker
from custom_otello_linter.errors import MissingPlatformInSubjectError, InvalidPlatformInSubjectError
from custom_otello_linter.visitors.scenario_visitor import Context, ScenarioVisitor
from custom_otello_linter.helpers.get_subject import get_subject


@ScenarioVisitor.register_scenario_checker
class SubjectChecker(ScenarioChecker):
    _LABEL_TO_SUBJECT_PLATFORM = {
        "MOBILE": "mobile",
        "IOS_WEB_MOBILE": "ios web",
        "ANDROID_WEB_MOBILE": "android web",
        "DESKTOP": "desktop",
        "MOBILE_APP": "mobile app",
        "ANDROID_MOBILE_APP": "android mobile app",
        "IOS_MOBILE_APP": "ios mobile app",
        "SBOL": "SBOL",
    }

    def check_scenario(self, context: Context, config) -> List[Error]:
        allowed_platforms = set(self._LABEL_TO_SUBJECT_PLATFORM.values()) | {"{platform}"}
        subject_value, subject_node = get_subject(context.scenario_node)

        # ищем указание платформы в последних круглых скобках сабджекта
        matches = re.findall(r"\(([^()]*)\)", subject_value)
        subject_platform = matches[-1].strip() if matches else None
        # проверяем, что платформа указана и она из заданного списка платформ
        if subject_platform not in allowed_platforms:
            return [MissingPlatformInSubjectError(
                lineno=subject_node.lineno,
                col_offset=subject_node.col_offset
            )]
        # проверяем, что платформа в subject соответствует указанной в allure_labels
        allure_platform, allure_platform_node = self._extract_allure_platform(context.scenario_node)
        if allure_platform is not None and subject_platform != allure_platform:
            node = allure_platform_node or subject_node
            return [InvalidPlatformInSubjectError(
                lineno=node.lineno,
                col_offset=node.col_offset
            )]

        return []

    def _extract_allure_platform(self, scenario_node: ast.ClassDef) -> Tuple[Optional[str], Optional[ast.AST]]:
        """
        Ищет в декораторе @allure_labels указание платформы вида Platform.X.
        Возвращает кортеж: (значение платформы для subject, AST-узел аргумента).
        Если платформа не найдена, возвращает (None, None).
        """
        allure_decorator = self.get_allure_labels_decorator(scenario_node)
        if not allure_decorator:
            return None, None

        for arg in allure_decorator.args:
            if (
                isinstance(arg, ast.Attribute)
                and isinstance(arg.value, ast.Name)
                and arg.value.id == "Platform"
                and arg.attr in self._LABEL_TO_SUBJECT_PLATFORM
            ):
                return self._LABEL_TO_SUBJECT_PLATFORM[arg.attr], arg

        return None, None
