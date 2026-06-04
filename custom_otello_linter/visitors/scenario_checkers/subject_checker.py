import ast
import re
from typing import List, Optional, Tuple

from flake8_plugin_utils import Error

from custom_otello_linter.dicts.platforms import Platforms
from custom_otello_linter.abstract_checkers import ScenarioChecker
from custom_otello_linter.errors import (
    MissingPlatformInSubjectError,
    NotMatchingPlatformInSubjectError,
    InvalidPlatformInSubjectError
)
from custom_otello_linter.visitors.scenario_visitor import Context, ScenarioVisitor
from custom_otello_linter.helpers.get_subject import get_subject


@ScenarioVisitor.register_scenario_checker
class SubjectChecker(ScenarioChecker):

    _ALLOWED_PLATFORMS = (set(Platforms.ALLURE_PLATFORM_TO_SUBJECT_PLATFORM.values()) | {"{platform}"})

    def check_scenario(self, context: Context, config) -> List[Error]:
        subject_value, subject_node = get_subject(context.scenario_node)
        # на всякий случай игнорируем (наш фреймворк не позволяет запускать тесты без сабджекта)
        if subject_value is None or subject_node is None:
            return []

        # ищем указание платформы в последних круглых скобках сабджекта
        subject_platform = self._extract_subject_platform(subject_value)
        # проверяем, что платформа указана и она из заданного списка платформ
        if subject_platform is None:
            return [MissingPlatformInSubjectError(
                lineno=subject_node.lineno,
                col_offset=subject_node.col_offset
            )]
        if subject_platform not in self._ALLOWED_PLATFORMS:
            return [InvalidPlatformInSubjectError(
                lineno=subject_node.lineno,
                col_offset=subject_node.col_offset
            )]
        # проверяем, что платформа в subject соответствует указанной в allure_labels
        allure_platform, allure_platform_node = self._extract_allure_platform(context.scenario_node)
        if allure_platform is not None and subject_platform != allure_platform:
            node = allure_platform_node or subject_node
            return [NotMatchingPlatformInSubjectError(
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
                and arg.attr in Platforms.ALLURE_PLATFORM_TO_SUBJECT_PLATFORM
            ):
                return Platforms.ALLURE_PLATFORM_TO_SUBJECT_PLATFORM[arg.attr], arg

        return None, None

    def _extract_subject_platform(self, subject_value: str) -> Optional[str]:
        """
        Извлекает платформу из последних круглых скобок в subject
        Возвращает нормализованное значение (заменяет "_" на пробел, чтобы mobile app и mobile_app считались равными)
        или None, если скобок в subject нет
        """
        matches = re.findall(r"\(([^()]*)\)", subject_value)
        if not matches:
            return None

        last_parens = matches[-1].strip()
        return last_parens.replace("_", " ")
