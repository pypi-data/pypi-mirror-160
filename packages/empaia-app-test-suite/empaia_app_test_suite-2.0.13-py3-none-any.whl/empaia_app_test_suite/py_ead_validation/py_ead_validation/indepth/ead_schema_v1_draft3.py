from ..exceptions import ConfigValidationError, EadContentValidationError

ANNOTATION_TYPES = ("point", "line", "arrow", "rectangle", "polygon", "circle")
PRIMITIVE_TYPES = ("bool", "integer", "float", "string")


def validate_ead(ead, namespaces):
    for io in ("inputs", "outputs"):
        for key, spec in ead[io].items():
            _validate_recursive(ead, io, key, spec, namespaces)
    _validate_config_spec(ead)


def validate_config(config, ead):
    config_spec = ead.get("configuration", {})
    config = config if config else {}
    for key, entry_spec in config_spec.items():
        if not entry_spec.get("optional", False) and key not in config:
            raise ConfigValidationError(f"Parameter {key} is missing in given configuration")
        if key in config:
            # str[ing], int[eger], bool, float
            if not entry_spec["type"].startswith(type(config[key]).__name__):
                raise ConfigValidationError(f"Parameter {key} has wrong type in given configuration")
    for key in config.keys():
        if key not in config_spec:
            raise ConfigValidationError(f"Parameter {key} is not part of the configuration specification")


def _validate_recursive(ead, io, key, spec, namespaces):
    if "reference" in spec:
        _validate_reference(ead, io, key, spec)
    if "classes" in spec:
        _validate_classes(ead, io, spec, namespaces)
    if spec["type"] == "collection":
        _validate_recursive(ead, io, key + ".items", spec["items"], namespaces)


def _validate_reference(ead, io, key, spec):
    if io == "inputs" and spec["reference"].startswith("outputs."):
        raise EadContentValidationError(f"Inputs must not reference outputs (inputs.{key} -> {spec['reference']})")
    head, *tail = spec["reference"].split(".")
    reference = ead[head]
    for node in tail:
        if node not in reference:
            raise EadContentValidationError(f"{spec['reference']} referenced by {io}.{key} not found")
        reference = reference[node]
    _validate_reference_type(spec["type"], reference["type"])


def _validate_classes(ead, io, spec, namespaces):
    if io == "outputs":
        raise EadContentValidationError("Outputs must not have class constraints")
    for class_value in spec["classes"]:
        _validate_class_value(ead, class_value, namespaces)


def _validate_class_value(ead, class_value, namespaces):
    split_target = ".classes."
    if class_value.endswith(".classes"):
        split_target = ".classes"
    if split_target not in class_value:
        raise EadContentValidationError(f"Class value {class_value} is malformed")
    class_namespace, class_suffix = class_value.split(split_target)
    if class_namespace.startswith("org.empaia.global."):
        for namespace_id, namespace in namespaces.items():
            if namespace_id == class_namespace:
                class_node = namespace["classes"]
                break
        else:
            raise EadContentValidationError(f"Global namespace not found for class value {class_value}")
    elif class_namespace == f"{ead['namespace']}":
        class_node = ead.get("classes", {})
    else:
        raise EadContentValidationError(f"Namespace not valid for class value {class_value}")

    if class_suffix:  # empty if class value is the classes root
        for item in class_suffix.split("."):
            if item not in class_node:
                raise EadContentValidationError(f"Class value {class_value} not found in class hierarchy")
            class_node = class_node[item]


def _validate_reference_type(source_type, target_type):
    if source_type == "collection":
        if target_type != "wsi" and target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Collections may only reference WSIs or annotations")
    if source_type in PRIMITIVE_TYPES:
        if target_type != "wsi" and target_type != "collection" and target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Primitives may only reference WSIs, collections or annotations")
    if source_type in ANNOTATION_TYPES:
        if target_type != "wsi":
            raise EadContentValidationError("Annotations must reference WSIs")
    if source_type == "class":
        if target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Classes must reference annotations")


def _validate_config_spec(ead):
    if "configuration" in ead:
        for entry in ead["configuration"].values():
            if entry["storage"] != "global":
                raise EadContentValidationError("Only global storage is supported for the configuration entries")
