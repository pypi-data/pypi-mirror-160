from typing import (
    Dict,
    List,
    MutableSequence,
    Sequence,
    TypeVar,
    overload
)

_T = TypeVar("_T")


class ItRandom:
    '''
    Random number generator class.
    '''

    def __init__(self) -> None: ...

    # lucky()
    @overload
    def lucky(self) -> bool:
        '''
        Random choice between True and False with ratio 1:1.

        ## Vietsub

        Lựa chọn ngẫu nhiên giữa True và False với tỉ lệ 1:1.
        '''
    @overload
    def lucky(self, true_percent: float) -> bool:
        '''
        Random choice between True and False with percentage returns True of `true_percent`. Constraint: 0 ≤ `true_percent` ≤ 1.

        ## Vietsub

        Lựa chọn ngẫu nhiên giữa True và False với tỉ lệ phần trăm trả về True là `true_percent`. Ràng buộc: 0 ≤ `true_percent` ≤ 1.
        '''

    # rdint()
    @overload
    def rdint(self, end: int, /) -> int:
        '''
        Return a random integer in range [0, `end`].

        ## Vietsub

        Trả về ngẫu nhiên một số nguyên trong đoạn [0, `end`].
        '''
    @overload
    def rdint(self, start: int, end: int, /) -> int:
        '''
        Return a random integer in range [`start`, `end`].

        ## Vietsub

        Trả về ngẫu nhiên một số nguyên trong đoạn [`start`, `end`].
        '''
    @overload
    def rdint(self, start: int, end: int, step: int, /) -> int:
        '''
        Return a random integer in range [`start`, `end`] with step is `step`.

        ## Vietsub

        Trả về ngẫu nhiên một số nguyên trong đoạn [`start`, `end`] với bước nhảy là `step`.

        -> Random in `range(start, end + 1, step)`.
        '''

    # rdfloat()
    @overload
    def rdfloat(self) -> float:
        '''
        Return a random float in [0, 1].

        ## Vietsub

        Trả về ngẫu nhiên một số thực trong đoạn [0, 1].
        '''
    @overload
    def rdfloat(self, end: float, /) -> float:
        '''
        Return a random float in [0, `end`].

        ## Vietsub

        Trả về ngẫu nhiên một số thực trong đoạn [0, `end`].
        '''
    @overload
    def rdfloat(self, start: float, end: float, /) -> float:
        '''
        Return a random float in [`start`, `end`].

        ## Vietsub

        Trả về ngẫu nhiên một số thực trong đoạn [`start`, `end`].
        '''
    @overload
    def rdfloat(self, start: float, end: float, gather_at: float, /) -> float:
        '''
        Return a random float in [`start`, `end`] but tends to be close to `gather_at`.

        ## Vietsub

        Trả về ngẫu nhiên một số thực trong đoạn [0, 1] nhưng có xu hướng gần với giá trị `gather_at`.
        '''

    # choices()
    @overload
    def choices(self, population: Sequence[_T], length: int) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.
        '''
    @overload
    def choices(self, population: Sequence[_T], length: int, probabilities: Sequence[int]) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement.

        The probability of selection of each element is based on `probabilities`, map by element index.

        The probability at the missing indexes will be 1.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.

        Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi vị trí các phần tử.

        Xác suất tại các chỉ mục bị khuyết sẽ là 1.

        ## Example

        For each element in `choices([1, 1, 2, 3, 4, 5], 3, [6, 1, 0])`:
            - 70% choose 1.
            - 0% choose 2.
            - 10% choose 3.
            - 10% choose 4.
            - 10% choose 5.
        '''
    @overload
    def choices(self, population: Sequence[_T], length: int, probabilities: Dict[_T, int]) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement.

        The probability of selection of each element is based on `probabilities`, map by element value.

        The probability for missing value will be 1.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.

        Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi giá trị các phần tử.

        Xác suất cho các giá trị bị khuyết sẽ là 1.

        ## Example

        For each element in `choices([1, 1, 2, 3, 4, 5], 3, {0:100, 1:7, 2:0})`:
            - 70% choose 1.
            - 0% choose 2.
            - 10% choose 3.
            - 10% choose 4.
            - 10% choose 5.
        '''

    # choice()
    @overload
    def choice(self, population: Sequence[_T]) -> _T:
        '''
        Return a random element from `population`.

        ## Vietsub

        Trả về một phần tử ngẫu nhiên của `population`.
        '''
    @overload
    def choice(self, population: Sequence[_T], probabilities: Sequence[int]) -> _T:
        '''
        Return a random element from `population` with probabilities is `probabilities`, map by element index.

        The probability at the missing indexes will be 1.

        ## Vietsub

        Trả về một phần tử ngẫu nhiên của `population` với xác suất lựa chọn là `probabilities`, ánh xạ bởi vị trí các phần tử.

        Xác suất tại các chỉ mục bị khuyết sẽ là 1.

        ## Example

        Return value of `choice([1, 1, 2, 3, 4, 5], [6, 1, 0])`:
            - 70% is 1.
            - 0% is 2.
            - 10% is 3.
            - 10% is 4.
            - 10% is 5.
        '''
    @overload
    def choice(self, population: Sequence[_T], probabilities: Dict[_T, int]) -> _T:
        ''' 
        Return random element from `population` with probabilities is `probabilities`, map by element value.

        The probability for missing value will be 1.

        ## Vietsub

        Trả về một phần tử ngẫu nhiên của `population` với xác suất lựa chọn là `probabilities`, ánh xạ bởi giá trị các phần tử.

        Xác suất cho các giá trị bị khuyết sẽ là 1.

        ## Example

        Return value of `choice([1, 1, 2, 3, 4, 5], {0:100, 1:7, 2:0})`:
            - 70% is 1.
            - 0% is 2.
            - 10% is 3.
            - 10% is 4.
            - 10% is 5.
        '''

    # shuffle()
    def shuffle(self, sequence: MutableSequence[_T]) -> None:
        '''
        Shuffle the sequence.

        ## Vietsub

        Xáo trộn dãy.
        '''

    # once()
    @overload
    def once(self, population: Sequence[_T], length: int) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.
        '''
    @overload
    def once(self, population: Sequence[_T], length: int, probabilities: Sequence[int]) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

        The probability of selection of each element is based on `probabilities`, map by element index.

        The probability at the missing indexes will be 1.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.

        Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi vị trí các phần tử.

        Xác suất tại các chỉ mục bị khuyết sẽ là 1.
        '''
    @overload
    def once(self, population: Sequence[_T], length: int, probabilities: Dict[_T, int]) -> List[_T]:
        '''
        Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

        The probability of selection of each element is based on `probabilities`, map by element value.

        The probability for missing value will be 1.

        ## Vietsub

        Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.

        Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi giá trị các phần tử.

        Xác suất cho các giá trị bị khuyết sẽ là 1.
        '''

    # withsum()
    @overload
    def withsum(self, sumvalue: int, length: int) -> List[int]:
        '''
        Returns a integer list with `length` elements whose sum is `sumvalue`.

        Lower bound is 0.

        ## Vietsub

        Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

        Cận dưới là 0.
        '''
    @overload
    def withsum(self, sumvalue: int, length: int, *, upperbound: int) -> List[int]:
        '''
        Returns a integer list with `length` elements whose sum is `sumvalue`.

        Lower bound is 0.

        Upper bound is `upperbound`.

        ## Vietsub

        Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

        Cận dưới là 0.

        Cận trên là `upperbound`.
        '''
    @overload
    def withsum(self, sumvalue: int, length: int, *, lowerbound: int, upperbound: int) -> List[int]:
        '''
        Returns a integer list with `length` elements whose sum is `sumvalue`.

        Lower bound is `lowerbound`.

        Upper bound is `upperbound`.

        ## Vietsub

        Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

        Cận dưới là `lowerbound`.

        Cận trên là `upperbound`.
        '''

# lucky()


@overload
def lucky() -> bool:
    '''
    Random choice between True and False with ratio 1:1.

    ## Vietsub

    Lựa chọn ngẫu nhiên giữa True và False với tỉ lệ 1:1.
    '''


@overload
def lucky(true_percent: float) -> bool:
    '''
    Random choice between True and False with percentage returns True of `true_percent`. Constraint: 0 ≤ `true_percent` ≤ 1.

    ## Vietsub

    Lựa chọn ngẫu nhiên giữa True và False với tỉ lệ phần trăm trả về True là `true_percent`. Ràng buộc: 0 ≤ `true_percent` ≤ 1.
    '''

# rdint()


@overload
def rdint(end: int, /) -> int:
    '''
    Return a random integer in range [0, `end`].

    ## Vietsub

    Trả về ngẫu nhiên một số nguyên trong đoạn [0, `end`].
    '''


@overload
def rdint(start: int, end: int, /) -> int:
    '''
    Return a random integer in range [`start`, `end`].

    ## Vietsub

    Trả về ngẫu nhiên một số nguyên trong đoạn [`start`, `end`].
    '''


@overload
def rdint(start: int, end: int, step: int, /) -> int:
    '''
    Return a random integer in range [`start`, `end`] with step is `step`.

    ## Vietsub

    Trả về ngẫu nhiên một số nguyên trong đoạn [`start`, `end`] với bước nhảy là `step`.

    -> Random in `range(start, end + 1, step)`.
    '''

# rdfloat()


@overload
def rdfloat(self) -> float:
    '''
    Return a random float in [0, 1].

    ## Vietsub

    Trả về ngẫu nhiên một số thực trong đoạn [0, 1].
    '''


@overload
def rdfloat(end: float, /) -> float:
    '''
    Return a random float in [0, `end`].

    ## Vietsub

    Trả về ngẫu nhiên một số thực trong đoạn [0, `end`].
    '''


@overload
def rdfloat(start: float, end: float, /) -> float:
    '''
    Return a random float in [`start`, `end`].

    ## Vietsub

    Trả về ngẫu nhiên một số thực trong đoạn [`start`, `end`].
    '''


@overload
def rdfloat(start: float, end: float, gather_at: float, /) -> float:
    '''
    Return a random float in [`start`, `end`] but tends to be close to `gather_at`.

    ## Vietsub

    Trả về ngẫu nhiên một số thực trong đoạn [0, 1] nhưng có xu hướng gần với giá trị `gather_at`.
    '''

# choices()


@overload
def choices(population: Sequence[_T], length: int) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.
    '''


@overload
def choices(population: Sequence[_T], length: int, probabilities: Sequence[int]) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement.

    The probability of selection of each element is based on `probabilities`, map by element index.

    The probability at the missing indexes will be 1.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.

    Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi vị trí các phần tử.

    Xác suất tại các chỉ mục bị khuyết sẽ là 1.

    ## Example

    For each element in `choices([1, 1, 2, 3, 4, 5], 3, [6, 1, 0])`:
        - 70% choose 1.
        - 0% choose 2.
        - 10% choose 3.
        - 10% choose 4.
        - 10% choose 5.
    '''


@overload
def choices(population: Sequence[_T], length: int, probabilities: Dict[_T, int]) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement.

    The probability of selection of each element is based on `probabilities`, map by element value.

    The probability for missing value will be 1.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`.

    Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi giá trị các phần tử.

    Xác suất cho các giá trị bị khuyết sẽ là 1.

    ## Example

    For each element in `choices([1, 1, 2, 3, 4, 5], 3, {0:100, 1:7, 2:0})`:
        - 70% choose 1.
        - 0% choose 2.
        - 10% choose 3.
        - 10% choose 4.
        - 10% choose 5.
    '''

# choice()


@overload
def choice(population: Sequence[_T]) -> _T:
    '''
    Return a random element from `population`.

    ## Vietsub

    Trả về một phần tử ngẫu nhiên của `population`.
    '''


@overload
def choice(population: Sequence[_T], probabilities: Sequence[int]) -> _T:
    '''
    Return a random element from `population` with probabilities is `probabilities`, map by element index.

    The probability at the missing indexes will be 1.

    ## Vietsub

    Trả về một phần tử ngẫu nhiên của `population` với xác suất lựa chọn là `probabilities`, ánh xạ bởi vị trí các phần tử.

    Xác suất tại các chỉ mục bị khuyết sẽ là 1.

    ## Example

    Return value of `choice([1, 1, 2, 3, 4, 5], [6, 1, 0])`:
        - 70% is 1.
        - 0% is 2.
        - 10% is 3.
        - 10% is 4.
        - 10% is 5.
    '''


@overload
def choice(population: Sequence[_T], probabilities: Dict[_T, int]) -> _T:
    ''' 
    Return random element from `population` with probabilities is `probabilities`, map by element value.

    The probability for missing value will be 1.

    ## Vietsub

    Trả về một phần tử ngẫu nhiên của `population` với xác suất lựa chọn là `probabilities`, ánh xạ bởi giá trị các phần tử.

    Xác suất cho các giá trị bị khuyết sẽ là 1.

    ## Example

    Return value of `choice([1, 1, 2, 3, 4, 5], {0:100, 1:7, 2:0})`:
        - 70% is 1.
        - 0% is 2.
        - 10% is 3.
        - 10% is 4.
        - 10% is 5.
    '''

# shuffle()


def shuffle(sequence: MutableSequence[_T]) -> None:
    '''
    Shuffle the sequence.

    ## Vietsub

    Xáo trộn dãy.
    '''

# once()


@overload
def once(population: Sequence[_T], length: int) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.
    '''


@overload
def once(population: Sequence[_T], length: int, probabilities: Sequence[int]) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

    The probability of selection of each element is based on `probabilities`, map by element index.

    The probability at the missing indexes will be 1.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.

    Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi vị trí các phần tử.

    Xác suất tại các chỉ mục bị khuyết sẽ là 1.
    '''


@overload
def once(population: Sequence[_T], length: int, probabilities: Dict[_T, int]) -> List[_T]:
    '''
    Return a `length` sized list of `population` elements chosen with replacement, but each element appearing only once.

    The probability of selection of each element is based on `probabilities`, map by element value.

    The probability for missing value will be 1.

    ## Vietsub

    Trả về một list có `length` phần tử. Các phần tử trong list này được chọn ngẫu nhiên từ `population`, mỗi phần tử chỉ xuất hiện 1 lần.

    Xác suất lựa chọn của mỗi phần tử được dựa trên `probabilities`, ánh xạ bởi giá trị các phần tử.

    Xác suất cho các giá trị bị khuyết sẽ là 1.
    '''

# withsum()


@overload
def withsum(sumvalue: int, length: int) -> List[int]:
    '''
    Returns a integer list with `length` elements whose sum is `sumvalue`.

    Lower bound is 0.

    ## Vietsub

    Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

    Cận dưới là 0.
    '''


@overload
def withsum(sumvalue: int, length: int, *, upperbound: int) -> List[int]:
    '''
    Returns a integer list with `length` elements whose sum is `sumvalue`.

    Lower bound is 0.

    Upper bound is `upperbound`.

    ## Vietsub

    Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

    Cận dưới là 0.

    Cận trên là `upperbound`.
    '''


@overload
def withsum(sumvalue: int, length: int, *, lowerbound: int, upperbound: int) -> List[int]:
    '''
    Returns a integer list with `length` elements whose sum is `sumvalue`.

    Lower bound is `lowerbound`.

    Upper bound is `upperbound`.

    ## Vietsub

    Trả về một list số nguyên với `length` phần tử có tổng là `sumvalue`.

    Cận dưới là `lowerbound`.

    Cận trên là `upperbound`.
    '''
