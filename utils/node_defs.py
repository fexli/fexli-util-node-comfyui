class FEAlwaysChangeNode:
    """This is a node that always changes. It is used to force the node to be executed every time."""

    @classmethod
    def IS_CHANGED(self, **kwargs):
        return float("nan")
