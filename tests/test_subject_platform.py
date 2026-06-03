from flake8_plugin_utils import assert_error, assert_not_error

from custom_otello_linter.errors import (
    MissingPlatformInSubjectError,
    NotMatchingPlatformInSubjectError,
    InvalidPlatformInSubjectError
)
from custom_otello_linter.visitors import ScenarioVisitor
from custom_otello_linter.visitors.scenario_checkers.subject_checker import (
    SubjectChecker,
)


def test_subject_with_platform_placeholder():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout ({platform})"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_subject_with_concrete_allowed_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (mobile)"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_subject_with_underscore_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (mobile_app)"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_subject_with_long_platform_without_underscore():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (android mobile app)"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)



def test_subject_without_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, MissingPlatformInSubjectError)


def test_subject_with_unknown_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (web)"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, InvalidPlatformInSubjectError)


def test_subject_with_not_right_placed_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (mobile_app) (as abroad user)"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, InvalidPlatformInSubjectError)


def test_subject_with_not_lowercase_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (Mobile)"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, InvalidPlatformInSubjectError)


def test_subject_with_platform_without_spaces():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    class Scenario:
        subject = "Open checkout (mobileapp)"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, InvalidPlatformInSubjectError)


def test_allure_platform_matches_subject_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    @allure_labels(Platform.MOBILE)
    class Scenario:
        subject = "Open checkout (mobile)"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_allure_platform_mismatch_subject_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    @allure_labels(Platform.MOBILE)
    class Scenario:
        subject = "Open checkout (desktop)"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, NotMatchingPlatformInSubjectError)


def test_allure_platform_with_subject_placeholder_is_invalid():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    @allure_labels(Platform.MOBILE)
    class Scenario:
        subject = "Open checkout ({platform})"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, NotMatchingPlatformInSubjectError)


def test_only_allure_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    @allure_labels(Platform.MOBILE)
    class Scenario:
        subject = "Open checkout"

        def when_user_open_checkout(self):
            pass
    """
    assert_error(ScenarioVisitor, code, MissingPlatformInSubjectError)


def test_several_allure_labels_and_platform_matches_subject_platform():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(SubjectChecker)
    code = """
    @allure_labels(Feature.HOTEL, Story.HOTEL_CARD, Platform.MOBILE, Priority.P0)
    class Scenario:
        subject = "Open checkout (mobile)"

        def when_user_open_checkout(self):
            pass
    """
    assert_not_error(ScenarioVisitor, code)
