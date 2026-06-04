from flake8_plugin_utils import Error

# Ошибки типа OCS1XX - относятся к ошибкам сценария
# Ошибки типа OCS3XX - относятся к ошибкам внутри шагов


class DecoratorVedroParams(Error):
    code = 'OCS101'
    message = 'decorator @vedro.params or params decorator from vedro package should not be presented'


class MultipleScreenshotsError(Error):
    code = 'OCS300'
    message = 'step "{step_name}" make_screenshot_for_comparison is used more than once'


class MissingScreenshotsAllureLabelError(Error):
    code = 'OCS102'
    message = 'test contains "make_screenshot_for_comparison" but is missing label "SCREENSHOTS"'


class MissingMakeScreenshotFuncCallError(Error):
    code = 'OCS301'
    message = 'test is marked with label "SCREENSHOTS" but doesn`t contain "make_screenshot_for_comparison" call'


class MissingPlatformArgError(Error):
    code = 'OCS302'
    message = 'test is missing "platform" argument in page opening context call'


class MissingPlatformInSubjectError(Error):
    code = "OCS103"
    message = ('missing platform in subject: must contain one of platform from dicts.platforms as (platform)'
               'or ({{platform}}) placeholder')


class InvalidPlatformInSubjectError(Error):
    code = "OCS104"
    message = ('invalid platform in subject: platform in subject must be placed in the end of the subject '
               'and be one of dicts.platforms as (platform) or ({{platform}}) placeholder')


class NotMatchingPlatformInSubjectError(Error):
    code = "OCS105"
    message = 'platform in subject doesn`t match platform in allure labels'
