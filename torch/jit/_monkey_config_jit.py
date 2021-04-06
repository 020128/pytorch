import monkeytype  # type: ignore

from typing import Optional, Dict, Iterable, List
from monkeytype.db.base import CallTraceStore
from monkeytype.config import default_code_filter
from monkeytype.tracing import CallTrace, CodeFilter
from collections import defaultdict

def get_qualified_name(func):
    return func.__module__ + '.' + func.__qualname__

class JitTypeTraceStore(CallTraceStore):
    def __init__(self):
        super().__init__()
        # A dictionary keeping all collected CallTrace
        # key is fully qualified name of called function
        # value is list of all CallTrace
        self.trace_records = defaultdict(list)

    def add(self, traces: Iterable[CallTrace]):
        for t in traces:
            qualified_name = get_qualified_name(t.func)
            self.trace_records[qualified_name].append(t)

    def filter(
        self,
        module: str,
        qualname_prefix: Optional[str] = None,
        limit: int = 2000
    ) -> List[CallTrace]:
        return self.trace_records[module]

    def analyze(self, qualified_name: str):
        # Analyze the types for the given module
        # and create a dictionary of all the types
        # for arguments and return values this module can take
        records = self.trace_records[qualified_name]
        all_args = defaultdict(set)  # type: ignore[var-annotated]
        for record in records:
            for arg, arg_type in record.arg_types.items():
                all_args[arg].add(arg_type)
            all_args["return_type"].add(record.return_type)
        return all_args

    def consolidate_types(self, qualified_name: str) -> Dict:
        all_args = self.analyze(qualified_name)
        # If there are more types for an argument,
        # then consolidate the type to `Any` and replace the entry
        # by type `Any`.
        # This currently handles only cases with only one return value
        # TODO: Consolidate types for multiple return values
        for args, types in all_args.items():
            if len(types) > 1:
                all_args[args] = {'Any'}
            else:
                _element_string_type = types.pop()
                all_args[args] = {_element_string_type.__name__}
        return all_args

    def get_args_types(self, qualified_name: str) -> Dict:
        return self.consolidate_types(qualified_name)

class JitTypeTraceConfig(monkeytype.config.Config):
    def __init__(self, s: JitTypeTraceStore):
        super().__init__()
        self.s = s

    def trace_store(self) -> CallTraceStore:
        return self.s

    def code_filter(self) -> Optional[CodeFilter]:
        return default_code_filter
type_trace_db = JitTypeTraceStore()
