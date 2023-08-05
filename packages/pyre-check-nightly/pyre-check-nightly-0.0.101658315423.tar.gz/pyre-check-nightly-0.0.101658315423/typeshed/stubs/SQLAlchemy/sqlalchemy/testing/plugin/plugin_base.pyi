import abc
from typing import Any

bootstrapped_as_sqlalchemy: bool
log: Any
py3k: Any
ABC = abc.ABC

fixtures: Any
engines: Any
exclusions: Any
warnings: Any
profiling: Any
provision: Any
assertions: Any
requirements: Any
config: Any
testing: Any
util: Any
file_config: Any
include_tags: Any
exclude_tags: Any
options: Any

def setup_options(make_option) -> None: ...
def configure_follower(follower_ident) -> None: ...
def memoize_important_follower_config(dict_) -> None: ...
def restore_important_follower_config(dict_) -> None: ...
def read_config() -> None: ...
def pre_begin(opt) -> None: ...
def set_coverage_flag(value) -> None: ...
def post_begin() -> None: ...

pre_configure: Any
post_configure: Any

def pre(fn): ...
def post(fn): ...
def want_class(name, cls): ...
def want_method(cls, fn): ...
def generate_sub_tests(cls, module) -> None: ...
def start_test_class_outside_fixtures(cls) -> None: ...
def stop_test_class(cls) -> None: ...
def stop_test_class_outside_fixtures(cls) -> None: ...
def final_process_cleanup() -> None: ...
def before_test(test, test_module_name, test_class, test_name) -> None: ...
def after_test(test) -> None: ...
def after_test_fixtures(test) -> None: ...

class FixtureFunctions(ABC, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def skip_test_exception(self, *arg, **kw): ...
    @abc.abstractmethod
    def combinations(self, *args, **kw): ...
    @abc.abstractmethod
    def param_ident(self, *args, **kw): ...
    @abc.abstractmethod
    def fixture(self, *arg, **kw): ...
    def get_current_test_name(self) -> None: ...
    @abc.abstractmethod
    def mark_base_test_class(self): ...

def set_fixture_functions(fixture_fn_class) -> None: ...
