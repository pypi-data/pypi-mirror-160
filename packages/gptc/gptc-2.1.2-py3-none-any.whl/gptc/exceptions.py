# SPDX-License-Identifier: LGPL-3.0-or-later


class GPTCError(BaseException):
    pass


class ModelError(GPTCError):
    pass


class UnsupportedModelError(ModelError):
    pass
