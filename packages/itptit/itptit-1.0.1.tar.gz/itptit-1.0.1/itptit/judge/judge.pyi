class SingleJudge:
    '''
    #### Judge the test cases in turn, suitable for simple programs.

    ## Vietsub

    #### Chấm các test case lần lượt, thích hợp cho chương trình đơn giản. 
    '''

    def __init__(
        self,
        intestsuite_dir: str,
        outtestsuite_dir: str,
        solution_path: str,
        *,
        time_limit: float = ...,
        input_extension: str = ...,
        output_extension: str = ...,
        actualout_dir: str = ...
    ) -> None:
        '''
        ### SingleJudge constructor.

        ## Parameters

        #### Position/keyword arguments

            - intestsuite_dir: str

                The directory where input of all test cases located.

                Đường dẫn chứa tất cả các file input của các test case.

            - outtestsuite_dir: str

                The directory where output of all test cases located.

                Đường dẫn chứa tất cả các file output của các test case.

            - solution_path: str

                The path of the judgment target.

                Đường dẫn tới lời giải cần chấm.

        #### Keyword-only arguments

            - time_limit: float (Default: `None`)

                Time limit by seconds for each test case.

                Giới hạn thời gian bằng giây cho mỗi test case. 

            - input_extension: str (Default: `'in'`)

                The file extension of test case's input files.

                Phần mở rộng (đuôi file) các file input của các test case.

            - output_extension: str (Default: `'out'`)

                The file extension of test case's output files

                Phần mở rộng (đuôi file) các file output của các test case.

            - actualout_dir: str (Default: `None`)

                The path contains the actual outputs for each test case that the solution being graded will output.

                Đường dẫn chứa các output thực cho mỗi test case mà lời giải đang chấm sẽ xuất ra.
        '''

    def start(self) -> None:
        '''
        ### Start judgment
        '''


class MultiJudge:
    '''
    #### Judge the test cases with multithreading, judge multiple tests at the same time, suitable for time-consuming programs.

    ## Vietsub

    #### Dùng đa luồng để chấm các test case, chấm nhiều test case cùng lúc, thích hợp cho chương trình chạy tốn thời gian.
    '''

    def __init__(
        self,
        intestsuite_dir: str,
        outtestsuite_dir: str,
        solution_path: str,
        *,
        number_of_judges: int = ...,
        time_limit: float = ...,
        input_extension: str = ...,
        output_extension: str = ...,
        actualout_dir: str = ...
    ) -> None:
        '''
        ### MultiJudge constructor.

        ## Parameters

        #### Position/keyword arguments

            - intestsuite_dir: str

                The directory where input of all test cases located.

                Đường dẫn chứa tất cả các file input của các test case.

            - outtestsuite_dir: str

                The directory where output of all test cases located.

                Đường dẫn chứa tất cả các file output của các test case.

            - solution_path: str

                The path of the judgment target.

                Đường dẫn tới lời giải cần chấm.

        #### Keyword-only arguments

            - number_of_judges: int (Default: `os.cpu_count()` or `4`)

                Number of judges.

                Số lượng máy chấm.

            - time_limit: float (Default: `None`)

                Time limit by seconds for each test case.

                Giới hạn thời gian bằng giây cho mỗi test case. 

            - input_extension: str (Default: `'in'`)

                The file extension of test case's input files.

                Phần mở rộng (đuôi file) các file input của các test case.

            - output_extension: str (Default: `'out'`)

                The file extension of test case's output files

                Phần mở rộng (đuôi file) các file output của các test case.

            - actualout_dir: str (Default: `None`)

                The path contains the actual outputs for each test case that the solution being graded will output.

                Đường dẫn chứa các output thực cho mỗi test case mà lời giải đang chấm sẽ xuất ra.
        '''

    def start(self) -> None:
        '''
        ### Start judgment
        '''
