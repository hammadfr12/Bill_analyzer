from typing import List
from backend.models import ReceiptORM

def sort(receipts: List[ReceiptORM], key: str, algo="timsort") -> List[ReceiptORM]:
    if algo == "quicksort":
        return _quicksort(receipts, key)
    elif algo == "mergesort":
        return _mergesort(receipts, key)
    else:
        return sorted(receipts, key=lambda r: getattr(r, key))

def _quicksort(arr, key):
    if len(arr) <= 1:
        return arr
    pivot = getattr(arr[len(arr)//2], key)
    left  = [x for x in arr if getattr(x, key) < pivot]
    mid   = [x for x in arr if getattr(x, key) == pivot]
    right = [x for x in arr if getattr(x, key) > pivot]
    return _quicksort(left, key) + mid + _quicksort(right, key)

def _mergesort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = _mergesort(arr[:mid], key)
    right= _mergesort(arr[mid:], key)
    return _merge(left, right, key)

def _merge(left, right, key):
    result=[]
    i=j=0
    while i < len(left) and j < len(right):
        if getattr(left[i], key) <= getattr(right[j], key):
            result.append(left[i]); i+=1
        else:
            result.append(right[j]); j+=1
    result.extend(left[i:]); result.extend(right[j:])
    return result
