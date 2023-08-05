from typing import get_args, get_origin, Iterable


def get_public_members(instance):
    for key in dir(instance):
        if not key.startswith('_'):
            yield key, getattr(instance, key)


def get_instance_members(instance, parent):
    members = dir(parent)

    for key, value in get_public_members(instance):
        if key not in members:
            yield key, value


def has_value(data, key):
    if hasattr(data, '__iter__'):
        return key in data
    else:
        return hasattr(data, key)


def get_value(data, key, default=None):
    if hasattr(data, '__iter__'):
        if type(key) is int:
            return data[key]
        elif key in data:
            return data[key]
        else:
            return default
    else:
        return getattr(data, key, default)


def _inherit_tree_mapper(class_object, mapper):
    yield from mapper(class_object)

    if not class_object.__bases__:
        return

    for base in class_object.__bases__:
        yield from _inherit_tree_mapper(base, mapper)


def _annotations_mapper(current_class):
    if hasattr(current_class, '__annotations__'):
        for key, bundle in current_class.__annotations__.items():
            if not key.startswith('_'):
                yield key, bundle


def get_annotations(dataclass):
    annotation_bundles = list(_inherit_tree_mapper(dataclass, _annotations_mapper))
    annotation_bundles.reverse()

    return {key: bundle for key, bundle in annotation_bundles}


def inspect_annotation(annotation):
    args = get_args(annotation)

    if len(args):
        result = {
            'origin': get_origin(annotation),
            'args': []
        }

        for arg in args:
            result['args'].append(
                inspect_annotation(arg)
            )

        return result

    return annotation


def inspect_annotations(annotations):
    return {key: inspect_annotation(typing) for key, typing in annotations.items()}

