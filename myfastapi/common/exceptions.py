class BaseError(Exception):
    def __init__(self):
        self._code = 500
        self._message = "internal server error"

    @property
    def message(self):
        return self._message

    @property
    def detail(self):
        return self._message

    @property
    def code(self):
        return self._code

    def __str__(self) -> str:
        return f"code={self.code}, message=`{self.message}`"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


class CommonError(BaseError):
    def __init__(self, message):
        self._code = 400001
        self._message = message


class UserError(BaseError):
    def __init__(self, message="User Error", code=400):
        self._code = code
        self._message = message


class ValidationError(UserError):
    """兼容旧"""

    def __init__(self, message="Parameter Validation Error", code=400):
        self._code = code
        self._message = message


class ApplicationError(BaseError):
    def __init__(self, message="Application Error", code=500):
        self._code = code
        self._message = message


class NotFoundError(BaseError):
    def __init__(self, message="资源不存在", code=404):
        self._code = code
        self._message = message

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code


class ModelClassNotFoundException(BaseError):
    def __init__(self, model_name, message="对应的Model类不存在, 请确保该model是document或entity类型", code=404):
        self._model_name = model_name
        self._code = code
        self._message = f"{model_name}: {message}"


class InvalidOperationError(ApplicationError):
    pass


class InvalidConfigurationError(ApplicationError):
    pass


class InvalidUserOperationError(UserError):
    pass


class InvalidPermissionError(BaseError):
    def __init__(self, message="权限不允许", code=403):
        self._code = code
        self._message = message

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code


class InvalidOperationPermissionError(BaseError):
    def __init__(self, message="权限不允许", code=403):
        self._code = code
        self._message = message

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code
