class SnapshotError(Exception):
    pass


class SnapshotNotFound(SnapshotError):
    def __init__(self, module, test_name):
        super().__init__(f"Snapshot '{test_name!s}' not found in {module.filepath!s}")
