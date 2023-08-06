from typing import Dict, List, overload


def isprime(integer: int) -> bool:
    '''
    Check if `integer` is prime or not.

    Kiểm tra số nguyên tố.
    '''


def factorization(integer: int) -> Dict[int, int]:
    '''
    Integer factorization.

    Phân tích thừa số nguyên tố.
    '''


def divisors(integer: int) -> List[int]:
    '''
    Return a list of integers which is divisors of `integer`.

    Trả về list ước của `integer`.
    '''


@overload
def Eratosthenes(end: int) -> Dict[int, bool]:
    '''
    Sieve of Eratosthenes from 1 to `end`. 

    Sàng nguyên tố Eratosthenes từ 1 cho tới `end`.
    '''


@overload
def Eratosthenes(start: int, end: int) -> Dict[int, bool]:
    '''
    Sieve of Eratosthenes from `start` to `end`. Constraint: |`end` - `start`| ≤ 1_000_000.

    Sàng nguyên tố Eratosthenes từ `start cho tới `end`. Ràng buộc: |`end` - `start`| ≤ 1_000_000.
    '''
