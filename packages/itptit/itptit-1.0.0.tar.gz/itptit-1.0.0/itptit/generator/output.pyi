from typing import (
    List,
    Optional
)
from ._base import (
    TestCaseFamily,
    _BaseGenerator
)


class Generator(_BaseGenerator):
    '''
    ### Test case's output generator.
    '''

    _static_write_mode: int = ...
    _default_write_mode: int = ...

    def __init__(
        self,
        input_testsuite_dir: str,
        solution_path: str,
        target_dir: str,
        *,
        input_file_extension: str = ...,
        file_extension: str = ...,
        skip_errors: bool = ...,
        file_size_limit: Optional[int] = ...
    ):
        '''
        ### Output Generator constructor.

        ## Parameters

        #### Position/keyword arguments

        - input_testsuite_dir: str

            The directory where input of all test cases located.

            Đường dẫn chứa tất cả các file input của các test case.

        - solution_path: str

            The path of the solution.

            Đường dẫn tới lời giải.

        - target_dir: str

            The directory where the generator put generated testcases in.

            Đường dẫn chứa các test case sẽ sinh ra.

        #### Keyword-only arguments

        - input_file_extension: str (Default: `'in'`)

            The file extension of input files.

            Phần mở rộng (đuôi file) của các file input.

        - file_extension: str (Default: `'out'`)

            File extension of result files.

            Phần mở rộng (đuôi file) của các test case sinh ra.

        - skip_errors: bool (Default: `False`)

            Skip (auto-catch) all exceptions encountered during process.

            Bỏ qua các ngoại lệ xảy ra trong quá trình sinh test.

        - file_size_limit: int (Default: `None`)

            Size limit of each test case file that will be generated (in bytes).

            Giới hạn dung lượng file cho mỗi file test case sinh ra.
        '''

    @property
    def target_dir(self) -> str: ...
    @property
    def file_extension(self) -> str: ...
    @property
    def write_mode(self) -> int: ...
    @property
    def skip_errors(self) -> bool: ...
    @property
    def file_size_limit(self) -> int: ...
    @property
    def family_pool(self) -> List[TestCaseFamily]: ...
    @property
    def input_testsuite_dir(self) -> str: ...
    @property
    def solution_path(self) -> str: ...
    @property
    def input_file_extension(self) -> str: ...
    @target_dir.setter
    def target_dir(self, value: str) -> None:  ...
    @file_extension.setter
    def file_extension(self, value: str) -> None: ...
    @write_mode.setter
    def write_mode(self, value: int) -> None: ...
    @skip_errors.setter
    def skip_errors(self, value: bool) -> None: ...
    @file_size_limit.setter
    def file_size_limit(self, value: int) -> None: ...
    @family_pool.setter
    def family_pool(self, value: List[TestCaseFamily]) -> None: ...
    @input_testsuite_dir.setter
    def input_testsuite_dir(self, value) -> None: ...
    @solution_path.setter
    def solution_path(self, value) -> None: ...
    @input_file_extension.setter
    def input_file_extension(self, value) -> None: ...

    @classmethod
    def generate(
        cls,
        input_testsuite_dir: str,
        solution_path: str,
        target_dir: str,
        *,
        input_file_extension: str = ...,
        file_extension: str = ...,
        skip_errors: bool = ...,
        file_size_limit: Optional[int] = ...
    ) -> bool:
        '''
        ### Static generate.

        ## Parameters

        #### Position/keyword arguments

        - input_testsuite_dir: str

            The directory where input of all test cases located.

            Đường dẫn chứa tất cả các file input của các test case.

        - solution_path: str

            The path of the solution.

            Đường dẫn tới lời giải.

        - target_dir: str

            The directory where the generator put generated testcases in.

            Đường dẫn chứa các test case sẽ sinh ra.

        #### Keyword-only arguments

        - input_file_extension: str (Default: `'in'`)

            The file extension of input files

            Phần mở rộng (đuôi file) của các file input.

        - file_extension: str (Default: `'out'`)

            File extension of result files.

            Phần mở rộng (đuôi file) của các test case sinh ra.

        - skip_errors: bool (Default: `False`)

            Skip (auto-catch) all exceptions encountered during process.

            Bỏ qua các ngoại lệ xảy ra trong quá trình sinh test.

        - file_size_limit: int (Default: `None`)

            Size limit of each test case file that will be generated (in bytes).

            Giới hạn dung lượng file cho mỗi file test case sinh ra.

        ## Returns

        True if generated cleanly - no failed creation, else False.

        True nếu tất cả các test case được sinh ra thành công.
        '''

    def start(self) -> bool:
        '''
        ### Run the generator.

        ## Returns

        True if generated cleanly - no failed creation, else False.

        True nếu tất cả các test case được sinh ra thành công.
        '''
