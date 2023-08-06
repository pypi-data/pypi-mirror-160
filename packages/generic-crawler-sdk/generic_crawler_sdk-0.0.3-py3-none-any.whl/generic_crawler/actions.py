from schema import Schema, Optional

ActionSchema = Schema(
    {
        'name': str,
        'url': str,
        'steps':
                 [
                     {
                        "name": str,
                        "action": str,
                        Optional("value"): str,
                        Optional("wait"): bool,
                        Optional("type"): str,
                        Optional("selector"): str,
                        Optional("depth"): {
                            "level": int
                        },
                        Optional("iteration_on"): {
                            "type": str,
                            "selector": str,
                            "look_for": str,
                            "when_found": str
                        },
                        Optional("scroll_to"): {
                            "direction": str,
                            Optional("repeat", default=1): int
                        },
                        Optional("duration"): int
                     }
                 ],
         'targets':
                 [
                     {
                         "name": str,
                         "type": str,
                         "selector": str,
                         Optional("nontext"): str,
                         Optional("extract-urls"): bool,
                         Optional("attribute"): str
                     },
                 ],
     }
)