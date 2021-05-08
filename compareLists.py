import sys
import string
import math

from typing import Dict
from typing import List
from collections import Counter
from collections import OrderedDict
from Levenshtein import ratio as levenRatio # type: ignore


def getBookList(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        books = [book.strip() for book in f]
    return books


def normalizeList(table: List[str]) -> List[str]:
    transform = str.maketrans("", "", string.punctuation+string.whitespace)
    return [word.replace('.pdf', '').translate(transform) for word in table]


def getLetterCount(word: str) -> Dict[str, int]:
    return Counter(word)


def innerProduct(d1: Dict[str, int], d2: Dict[str, int]) -> float:
    sum = 0.0
    for key in d1:
        if key in d2:
            sum += d1[key] * d2[key]
    return sum


def vectorAngle(d1: Dict[str, int], d2: Dict[str, int]) -> float:
    numerator = innerProduct(d1, d2)
    denominator = math.sqrt(innerProduct(d1,d1) * innerProduct(d2, d2))
    return math.acos(numerator / denominator)


def main(args: list):

    books = normalizeList(getBookList(args[1]))
    booksCompare = normalizeList(getBookList(args[2]))

    for book in books:
        print(f"Checking {book}...")
        bookDict = getLetterCount(book)
        for bookC in booksCompare:
            ratio = levenRatio(book.lower(), bookC.lower())
            if ratio > .5:
                print(f"\t{book} is close to {bookC} LEVEN: ({ratio})")
            # arccos = vectorAngle(bookDict, getLetterCount(bookC))
            # if arccos < .75:
            #     print(f"\t\t{book} is close to {bookC} ARC: ({arccos})")


        


if __name__ == "__main__":
    main(sys.argv)