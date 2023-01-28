import inspect
import logging
from inspect import Signature
from typing import Type


class ComponentNotFoundError(BaseException):
    pass


class DI(dict):
    autowiring = True
    _named_args: {} = {}

    def set_named_args(self, key: Type, args: dict):
        self._named_args[key] = args

    def create(self, key: Type) -> object:
        init_signature = inspect.signature(key.__init__)
        args = self._build_args(key, init_signature)

        try:
            if args:
                instance = key(**args)
            else:
                instance = key()
        except ValueError as error:
            logging.error(
                "Cannot create instance of %s with existed args: %s", key, args
            )
            raise error

        self[key] = instance

        return instance

    def get(self, key, default=None):
        if default:
            logging.warning(
                "Lazy getter called with default value %s, that ignored", default
            )

        return self[key]

    def __missing__(self, key):
        if self.autowiring:
            return self.create(key)

        raise ComponentNotFoundError(key)

    def _build_args(self, key: Type, signature: Signature) -> dict:
        args = {}
        registered_named_args: dict = self._named_args.get(key, {})
        for param_name in signature.parameters:
            if param_name in ["self", "args", "kwargs"]:
                continue

            if param_name in registered_named_args.keys():
                value = registered_named_args.get(param_name)
            else:
                param = signature.parameters.get(param_name)
                param_class = param.annotation
                if param_class is param.empty:
                    value = param.default
                elif self.autowiring:
                    value = self.get(param_class)
                else:
                    logging.warning(
                        "Pass empty value for %s, your can set autowiring=True, for prevent this issue"
                    )
                    value = None

            args[param_name] = value

        return args
