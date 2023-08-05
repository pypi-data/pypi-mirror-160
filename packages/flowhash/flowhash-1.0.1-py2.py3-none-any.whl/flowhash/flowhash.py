import time
from typing import Any, Callable, Generic, Iterator, List, SupportsIndex, TypeVar


T = TypeVar('T')


class FlowHash(Generic[T]):


    def __init__(self, address_size: int, bit_count: int, hash_input: List[T] = None, hash_op: Callable[[T, T], T] = None, fold_register: int = 0):

        # check that address_size fits within the bitcount
        if address_size > bit_count:
            raise ValueError(f"address_size ({address_size}) must be <= bit_count ({bit_count})")

        # check that input is properly addressable
        if hash_input is None:
            hash_input = [0] * (1 << address_size)
        elif len(hash_input) != 1 << address_size:
            raise ValueError(f"input must be of length 2 ** address_size ({address_size})")

        # default hash_op is simple_hash_op
        if hash_op is None:
            hash_op = lambda x, y: (x + y + 1) % (1 << bit_count)

        # const props
        self.address_size = address_size
        self.bit_count = bit_count
        self.register_count = bit_count - address_size

        self.hash_op = hash_op # val #= x :: val = hash_op(val, x)

        # state
        self.programme = hash_input
        self.state_registers = list(range(self.register_count))
        self.fold_register = fold_register

        self.instruction_address = 0

    
    # repr and str

    def __repr__(self) -> str:
        return f"FlowHash(address_size={self.address_size}, bit_count={self.bit_count}, digest={self.programme}, hash_op={self.hash_op}, fold_register={self.fold_register})"

    def __str__(self) -> str:
        state_pretty = "::: FLOWHASH STATE :::"
        state_pretty += f"\nfold_register: {self.fold_register} state_registers: {self.state_registers}"
        state_pretty += f"\ninstruction_address: {self.instruction_address}"
        state_pretty += f"\programme: {self.programme}"
        return state_pretty
    

    # hashing engine
    
    def execute(self):
        # fetch
        instruction = self.programme[self.instruction_address]
        # decode
        goto = instruction % (1 << self.address_size)
        register_io = instruction >> self.address_size
        # execute
        input_registers = [i for i in range(self.register_count) if register_io & (1 << i)]
        output_registers = [i for i in range(self.register_count) if not register_io & (1 << i)]
        # go to address
        while self.instruction_address != goto:
            # churn programme: fold, *output_registers #= x #= fold, *input_registers
            input_value = self.fold_register
            for i in input_registers: input_value ^= self.state_registers[i]
            self.programme[self.instruction_address] = self.hash_op(self.programme[self.instruction_address], input_value)
            self.fold_register = self.hash_op(self.fold_register, self.programme[self.instruction_address])
            for i in output_registers: self.state_registers[i] = self.hash_op(self.state_registers[i], self.programme[self.instruction_address])
            # incriment memory address
            self.instruction_address += 1
            self.instruction_address %= (1 << self.address_size)
        # invert input and output for final churn, *input_registers #= x #= fold, *output_registers
        input_value = self.fold_register
        for i in output_registers: input_value ^= self.state_registers[i]
        self.programme[self.instruction_address] = self.hash_op(self.programme[self.instruction_address], input_value)
        self.fold_register = self.hash_op(self.fold_register, self.programme[self.instruction_address])
        for i in input_registers: self.state_registers[i] = self.hash_op(self.state_registers[i], self.programme[self.instruction_address])
        
        return self.fold_register

    def __call__(self, steps: int) -> int:
        for _ in range(steps):
            self.execute()
        return self.fold_register


    # define container access through to programme
    
    def __len__(self) -> int:
        return 2 ** self.address_size

    def __getitem__(self, index: SupportsIndex) -> T:
        return self.programme[index]

    def __setitem__(self, index: SupportsIndex, value: T) -> None:
        self.programme[index] = value

    def __iter__(self) -> Iterator[T]:
        return iter(self.programme)

    def __contains__(self, item: Any) -> bool:
        return item in self.programme


def flowhash(bit_count: int, hash_input: List[T], juice: int = 1, hash_op: Callable[[T, T], T] = None) -> T:
    hash_input = hash_input[:]
    if hash_op is None:
        hash_op = lambda x, y: (x + y + 1) % (1 << bit_count)
    size = len(hash_input)
    if size > 2 ** bit_count:
        raise ValueError(f"input length ({size}) must be <= 2 ** bit_count ({bit_count})")
    result = 0
    for i in range(bit_count):
        if len(hash_input) == 0:
            break
        section_size = (1 << i)
        if size & section_size:
            section = hash_input[:section_size]
            hash_input[:section_size] = []
            programme = FlowHash(address_size=i, bit_count=bit_count, hash_input=section, hash_op=hash_op, fold_register=result)
            result = programme(steps=(section_size * juice))
    return result
    

def curried_flowhash(bit_count: int, juice: int = 1, hash_op: Callable[[T, T], T] = None) -> Callable[[List[T]], T]:
    return lambda hash_input: flowhash(bit_count, hash_input, juice, hash_op)
    

