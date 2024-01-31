class Environment:
    Development = "development"
    Production = "production"


class State:
    Inactive = "inactive"
    Active = "active"
    Idle = "idle"
    Disconnected = "disconnected"
    Error = "error"
    Prompting = "prompting"
    Printing = "printing"
    Calibrating = "calibrating"


class NodeType:
    import InputNode
    import RootNode

    Input = InputNode
    Root = RootNode
