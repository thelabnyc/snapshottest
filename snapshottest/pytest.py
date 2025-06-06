import re

import pytest

from .diff import PrettyDiff
from .module import SnapshotModule, SnapshotTest
from .reporting import diff_report, reporting_lines


def pytest_addoption(parser):
    group = parser.getgroup("snapshottest")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        dest="snapshot_update",
        help="Update the snapshots.",
    )
    group.addoption(
        "--snapshot-verbose",
        action="store_true",
        default=False,
        help="Dump diagnostic and progress information.",
    )


class PyTestSnapshotTest(SnapshotTest):
    def __init__(self, request=None):
        self.request = request
        super().__init__()

    @property
    def module(self):
        return SnapshotModule.get_module_for_testpath(self.request.node.fspath.strpath)

    @property
    def update(self):
        return self.request.config.option.snapshot_update

    @property
    def test_name(self):
        cls_name = getattr(self.request.node.cls, "__name__", "")
        flattened_node_name = re.sub(
            r"\s+", " ", self.request.node.name.replace(r"\n", " ")
        )
        return "{}{} {}".format(
            f"{cls_name}." if cls_name else "",
            flattened_node_name,
            self.curr_snapshot,
        )


class SnapshotSession:
    def __init__(self, config):
        self.verbose = config.getoption("snapshot_verbose")
        self.config = config

    def display(self, tr):
        if not SnapshotModule.has_snapshots():
            return

        tr.write_sep("=", "SnapshotTest summary")

        for line in reporting_lines("pytest"):
            tr.write_line(line)


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, PrettyDiff) and op == "==":
        return diff_report(left, right)


@pytest.fixture
def snapshot(request):
    with PyTestSnapshotTest(request) as snapshot_test:
        yield snapshot_test


def pytest_terminal_summary(terminalreporter):
    if terminalreporter.config.option.snapshot_update:
        for module in SnapshotModule.get_modules():
            module.delete_unvisited()
            module.save()

    terminalreporter.config._snapshotsession.display(terminalreporter)


# force the other plugins to initialise first
# (fixes issue with capture not being properly initialised)
@pytest.mark.trylast
def pytest_configure(config):
    config._snapshotsession = SnapshotSession(config)
    # config.pluginmanager.register(bs, "snapshottest")
