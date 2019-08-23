# Copyright 2019 President James Knox Polk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import hashlib
import math
import string
from typing import List

# Class to permute and encode nonnegative integers.
# As an example, these integers may be database IDs

# Benefits include easy-to-spot differences in IDs, ID shortening, and
# obfuscation.


class IDMixer:
    def __init__(self, id_bitlength: int, alphabet: List[str]):
        """
        Create and IDMixer instance.
        :param id_bitlength: The *maximum* length of an ID in bits. All IDs
        `x` must satisfy 0 <= x < pow(2, id_bitlength)
        :param alphabet: The output alphabet that will be used to encode the
        result. The larger the alphabet, the shorter the result.
        """
        self.id_bitlength = id_bitlength
        self.alphabet = alphabet
        self.left_bitlen = self.id_bitlength // 2
        self.right_bitlen = self.id_bitlength - self.left_bitlen
        self.r_mask = (1 << self.right_bitlen) - 1
        self.id_bytelen = (self.id_bitlength + 7) // 8
        self.right_bytelen = (self.right_bitlen + 7) // 8
        k = len(self.alphabet)
        lg_2 = math.log(2)
        lg_k = math.log(k)
        self.encodedlen = int(math.ceil(self.id_bitlength * lg_2 / lg_k))
        self.inverse_alphabet = dict((ch, i) for i, ch in enumerate(self.alphabet))

    def right_func(self, x: int) -> int:
        digest = hashlib.sha256(x.to_bytes(self.right_bytelen, 'big')).digest()
        return int.from_bytes(digest, 'big') & self.r_mask

# if performance is an issue you might replace right_func with the following

    def _faster_right_func(self, x: int) -> int:
        t = self.right_bitlen // 2
        t_mask = (1 << t) - 1
        l, r = x >> t, x & t_mask
        return (l*r + r + (l << t)) & self.r_mask

    def mix(self, id_in: int) -> int:
        L, R = id_in >> self.right_bitlen, id_in & self.r_mask
        L ^= self.right_func(R)
        R ^= self.right_func(L)
        return (L << self.right_bitlen) | R

    def unmix(self, mixed: int) -> int:
        L, R = mixed >> self.right_bitlen, mixed & self.r_mask
        R ^= self.right_func(L)
        L ^= self.right_func(R)
        return (L << self.right_bitlen) | R

    def base_n_encode(self, value: int) -> str:
        digits = []
        k = len(self.alphabet)
        for i in range(self.encodedlen):
            value, rem = divmod(value, k)
            digits.insert(0, rem)
        return ''.join(self.alphabet[digit] for digit in digits)

    def base_n_decode(self, encoded: str) -> int:
        digits = [self.inverse_alphabet[ch] for ch in encoded]
        result = 0
        for digit in digits:
            result = result * len(alphabet) + digit
        return result

    def encode(self, id_in: int) -> str:
        return self.base_n_encode(self.mix(id_in))

    def decode(self, encoded: str) -> int:
        return self.unmix(self.base_n_decode(encoded))


if __name__ == '__main__':
    alphabet = string.ascii_uppercase + string.digits
    mixer = IDMixer(44, alphabet)
    e1 = mixer.encode(13892359163211)
    e2 = mixer.encode(13992351216421)
    print('13892359163211 -> ' + e1)
    print('13992351216421 -> ' + e2)
    print(e1 + ' -> ' + str(mixer.decode(e1)))
    print(e2 + ' -> ' + str(mixer.decode(e2)))
