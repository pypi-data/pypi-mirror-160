from __future__ import annotations

from typing import Any, Optional, Union


def prompt_input(
    text: Optional[str] = None, target_type: Optional[Union[Any, list[Any]]] = None
) -> str:
    if text is None:
        text = "Enter value"

    annotate = "any"
    if target_type is not None:
        if type(target_type) is not list:
            target_type = [target_type]
        annotate = f"{target_type[0]}"
        for _target_type in target_type[1:]:
            annotate += f"| {_target_type}"
        annotate = f"({str.__name__})"

    while True:
        value = input(f"{text}\n {annotate}:")
        try:
            value = eval(value)
        except (SyntaxError, NameError) as e:
            if not str in target_type:
                raise e

        if target_type is not None:
            if type(value) not in target_type:
                print("invalid type, please try again.")
                continue
        break

    return value
