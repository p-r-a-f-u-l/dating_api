class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "message": args.get("message", "success"),
            "error": args.get(
                "error",
            ),
            "data": args.get("data", []),
        }
