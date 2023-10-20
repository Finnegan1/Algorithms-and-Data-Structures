import numpy as np
import math
from typing import TypeVar, Generic, Dict

T = TypeVar('T')


class ArrayBuffer(Generic[T]):

    TYPE_MAP: Dict[type, np.dtype] = {
        int: np.int32,
        float: np.float64,
        str: np.unicode_(256),
        # Add other type mappings as needed
    }

    def __init__(self, start_size:int=100, grow_factor:float=1.5):
        self.dtype = self.TYPE_MAP.get(T, object)
        self.buffer = np.empty(start_size, dtype=self.dtype)
        self.grow_factor = grow_factor
        self.head = math.floor(start_size / 2)
        self.tail = None
        self.size = start_size

    def __len__(self)->int:
        return self.length

    def get(self, index:int)->T:
        index = index + self.head
        if self.head % self.size < self.tail % self.size:
            if index >= self.head and index <= self.tail:
                return self.buffer[index]
            else:
                raise Exception('Index out of Boundry')
        elif self.head % self.size > self.tail % self.size:
            if index % self.size >= self.head or index % self.size <= self.tail:
                return self.buffer[index % self.size]
            else:
                raise Exception('Index out of Boundry')

    def push(self, value:T):

        if self.tail == None:
            self.buffer[self.head] = value
            self.tail = self.head
            return

        self.tail = self.tail + 1

        if self.tail % self.size == self.head % self.size:
            self.resize()

        self.buffer[self.tail % self.size] = value

    def shift(self, value:T):
        if self.tail == None:
            self.buffer[self.head] = value
            self.tail = self.head
            return


        if (self.head -1) % self.size == self.tail % self.size:
            self.resize()


        if self.head - 1 >= 0:
            self.head = self.head - 1
        else:
            self.head = self.size -1


        self.buffer[self.head % self.size] = value


    def resize(self):
        new_size:int = math.floor(self.size * self.grow_factor)
        new_buffer = np.empty(new_size, dtype=self.dtype)
        new_head:int = math.floor(new_size * 0.5)
        new_tail:int = new_head + (self.tail - self.head)

        for i in range(self.size):
            new_buffer[(new_head + i) % new_size] = self.buffer[(self.head + i)
                                                                % self.size]

        self.size = new_size
        self.buffer = new_buffer
        self.head = new_head
        self.tail = new_tail

        print(self)


    def __str__(self) -> str:
        return f"ArrayBuffer<Type: {T}, Size: {self.size}, Head: {self.head}, Tail: {self.tail}, Buffer: {self.buffer}>"











print("test")

myArrayBuffer = ArrayBuffer[int](4)


for i in range(5):
    print("____________________________")
    myArrayBuffer.push(i)
    print(myArrayBuffer)


print(" ")
print("##############################")
print(" ")

for i in range(5):
    print("____________________________")
    myArrayBuffer.shift(-i)
    print(myArrayBuffer)
