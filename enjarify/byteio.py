# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
from ctypes import *

from .util import signExtend

btio = CDLL("enjarify/lib/byte_util.so")

class Reader:

    btio.ru16.argtypes = [POINTER(c_char)]
    btio.ru32.argtypes = [POINTER(c_char)]
    btio.ru64.argtypes = [POINTER(c_char)]

    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos

    def read(self, size):
        end = self.pos + size
        if end > len(self.data):
            raise IndexError
        result = self.data[self.pos:end]
        self.pos = end
        return result

    def u8(self): return self.read(1)[0]
    def u16(self): return btio.ru16(self.read(2));
    def u32(self): return btio.ru32(self.read(4));
    def u64(self): return btio.ru64(self.read(8));

    def uleb128(self, signed=False):
        result = 0
        size = 0
        while self.data[self.pos] >> 7:
            result ^= (self.data[self.pos] & 0x7f) << size
            size += 7
            self.pos += 1
        result ^= (self.data[self.pos] & 0x7f) << size
        size += 7
        self.pos += 1

        if signed:
            result = signExtend(result, size)
        return result

    def sleb128(self): return self.uleb128(signed=True)

    # Maintain strings in binary encoding instead of attempting to decode them
    # since the output will be using the same encoding anyway
    def readCStr(self):
        oldpos, self.pos = self.pos, self.data.find(b'\0', self.pos)
        return self.data[oldpos:self.pos]

class Writer:
    def __init__(self):
        self.buf = bytearray()

    def write(self, s):
        self.buf += s

    def _pack(self, fmt, arg):
        return self.write(struct.pack(fmt, arg))

    def u8(self, x): return self.write(bytes([x]))
    def u16(self, x): return self._pack('>H', x)
    def u32(self, x): return self._pack('>I', x)
    def u64(self, x): return self._pack('>Q', x)

    def toBytes(self):
        return bytes(self.buf)
