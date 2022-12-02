import os

import parameterized.parameterized


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def customize_class_name(cls, parameter_number, params_dict):
    class_name = cls.__name__
    class_subname = parameterized.parameterized.to_safe_name(params_dict['subname'])

    return f"{class_name}{class_subname}"
