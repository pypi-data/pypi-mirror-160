from typing import List, Union

from captcharun.utils import to_base64


class BaseTask:
    captcha_type = None

    @property
    def data(self):
        return {
            "captchaType": self.captcha_type,
            **{k: v for k, v in self._data.items() if v is not None},
        }


class ReCaptchaV2Task(BaseTask):
    captcha_type = "ReCaptchaV2"

    def __init__(
        self,
        site_key: str,
        site_referer: str,
        use_cache: bool = True,
        is_invisible: bool = False,
    ):
        self._data = {
            "siteKey": site_key,
            "siteReferer": site_referer,
            "useCache": use_cache,
            "isInvisible": is_invisible,
        }


class ReCaptchaV3Task(BaseTask):
    captcha_type = "ReCaptchaV3"

    def __init__(
        self,
        site_key: str,
        site_referer: str,
        site_action: str,
    ):
        self._data = {
            "siteKey": site_key,
            "siteReferer": site_referer,
            "siteAction": site_action,
        }


class ReCaptchaV2ClassificationTask(BaseTask):
    captcha_type = "ReCaptchaV2Classification"

    def __init__(self, image: Union[bytes, str], question: str, resize: int = 0):
        image = to_base64(image)

        assert resize in (-1, 0, 1, 3, 4)

        self._data = {
            "image": image,
            "question": question,
            "resize": resize,
        }


class HCaptchaTask(BaseTask):
    captcha_type = "HCaptcha"

    def __init__(self, site_key: str, site_referer: str, use_cache: bool = True):
        self._data = {
            "siteKey": site_key,
            "siteReferer": site_referer,
            "useCache": use_cache,
        }


class HCaptchaClassificationTask(BaseTask):
    captcha_type = "HCaptchaClassification"

    def __init__(
        self,
        question: str,
        queries: List[Union[str, bytes]],
        anchors: List[Union[str, bytes]],
    ):
        queries = [to_base64(q) for q in queries]
        anchors = [to_base64(a) for a in anchors]

        self._data = {
            "question": question,
            "queries": queries,
            "anchors": anchors,
        }


class TextCaptchaTask(BaseTask):
    captcha_type = "TextCaptcha"

    def __init__(
        self,
        image: Union[bytes, str],
    ):
        self._data = {
            "image": to_base64(image),
        }
