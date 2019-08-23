# IDMixer
A simple python 3 class for permuting an encoding an
integer. The goals are:
* small differences in two ints are magnified by the permutation
* The encoding alphabet is as large as is allowed by other constraints.

## Usage
```python
import string
if __name__ == '__main__':
    alphabet = string.ascii_uppercase + string.digits
    mixer = IDMixer(44, alphabet)
    e1 = mixer.encode(13892359163211)
    e2 = mixer.encode(13992351216421)
    print('13892359163211 -> ' + e1)
    print('13992351216421 -> ' + e2)
    print(e1 + ' -> ' + str(mixer.decode(e1)))
    print(e2 + ' -> ' + str(mixer.decode(e2)))
```
produces the output
```none
13892359163211 -> BC33VXN8A
13992351216421 -> D1UOW6SLL
BC33VXN8A -> 13892359163211
D1UOW6SLL -> 13992351216421
```

## Alphabets
The alphabet is arbitrary, but ASCII uppercase letters plus digits makes
a nice visual impression. Another obvious candidate is upper and lower case
letters plus digits. Larger alphabets can be experimented with.

## Customize
I still consider this to be more of a working example than a
finished product. There is one unused function called `_faster_right_func`
that is available for inspection. The function currently used
is based on SHA256, which is certainly overkill and too slow if
many integers are to be converted. On the other hand, if relatively
few are being encoded than the slowness of SHA256 is not an issue.

## Buggy?

Almost no testing has been performed so there are undoubtedly
bugs present.

## Credit
Inspired by [this question](https://stackoverflow.com/q/57624017/238704) on Stackoverflow.