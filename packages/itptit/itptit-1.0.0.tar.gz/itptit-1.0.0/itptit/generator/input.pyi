from typing import (
    Any,
    List,
    NoReturn,
    Optional
)
from ._base import (
    TestCaseFamily,
    _BaseGenerator
)


class Generator(_BaseGenerator):
    '''
    ### Test case's input generator.
    '''

    _static_write_mode: int = ...
    _default_write_mode: int = ...

    def __init__(
        self,
        target_dir: str,
        *test_case_families: TestCaseFamily,
        file_extension: str = ...,
        indexing: bool = ...,
        skip_errors: bool = ...,
        file_size_limit: Optional[int] = ...
    ):
        '''
        ### Input Generator constructor.

        ## Parameters

        #### Position/keyword arguments

        - target_dir: str

            The directory where the generator put generated testcases in.

            Đường dẫn chứa các test case sẽ sinh ra.

        - *test_case_families: TestCaseFamily

            All the TestCaseFamily that you want the generator to generate.

            Tất cả các TestCaseFamily sử dụng để sinh các test case.

        #### Keyword-only arguments

        - file_extension: str (Default: `'in'`)

            File extension of result files.

            Phần mở rộng (đuôi file) của các test case sinh ra.

        - indexing: bool (Default: `True`)

            Decide whether the file name containing the test case is indexed or not.

            Đánh số theo thứ tự cho từng file test case sinh ra (nếu không thì sinh theo tên của họ test case).

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
    def indexing(self) -> bool: ...
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
    @indexing.setter
    def indexing(self, value: bool) -> None: self.__indexing = value

    def add(self, *args: TestCaseFamily | Any) -> NoReturn:
        '''
        Add more TestCaseFamily or generate function to family pool.

        Thêm TestCaseFamily hoặc hàm sinh cho bộ sinh test.

        ## Parameters

        *args: TestCaseFamily | function

            If it is a function, it will be init with TestCaseFamily.

            Nếu đối số truyền vào là một function, nó sẽ được khởi tạo với 1 họ test case.

        Ex with foo():

        add(foo) == add(TestCaseFamily(foo))
        '''

    def remove(self, arg: TestCaseFamily | Any) -> NoReturn:
        '''
        Remove TestCaseFamily `arg` or TestCaseFamily has generate function is `arg` in pool.

        Xóa TestCaseFamily `arg` trong `family_pool` nếu `arg` là một TestCaseFamily.

        Xóa TestCaseFamily có hàm sinh là `arg` trong `family_pool` nếu `arg` là một function.

        ## Parameters

        arg: TestCaseFamily | function.
        '''

    @classmethod
    def generate(
        cls,
        target_dir: str,
        *families: TestCaseFamily,
        file_extension: str = ...,
        indexing: bool = ...,
        skip_errors: bool = ...,
        file_size_limit: Optional[int] = ...
    ) -> bool:
        '''
        ### Static generate.

        ## Parameters

        #### Position/keyword arguments

        - target_dir: str

            The directory where the generator put generated testcases in.

            Đường dẫn chứa các test case sinh ra.

        - *families: TestCaseFamily

            All the TestCaseFamily use to generate test cases.

            Tất cả các TestCaseFamily sử dụng để sinh các test case.

        #### Keyword-only arguments

        - file_extension: str (Default: `'in'`)

            File extension of result files.

            Phần mở rộng (đuôi file) của các test case sinh ra.

        - indexing: bool (Default: `True`)

            Decide whether the file name containing the test case is indexed or not.

            Đánh số theo thứ tự cho từng file test case sinh ra (nếu không thì sinh theo tên của họ test case).

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
