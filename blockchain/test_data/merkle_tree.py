import hashlib
import binascii
from blake3 import blake3  # Import blake3 library

class MerkleTree(object):
    def __init__(self, hash_type="sha256"):
        self.set_hash_function(hash_type)
        self.reset_tree()

    def set_hash_function(self, hash_type):
        hash_type = hash_type.lower()
        if hash_type == "blake3":
            # Explicit support for Blake3
            self.hash_function = lambda data: blake3(data).digest()
        elif hash_type in hashlib.algorithms_available:
            self.hash_function = getattr(hashlib, hash_type)
        else:
            raise ValueError(f"Hashing algorithm '{hash_type}' is not supported.")

    def _to_hex(self, x):
        return x.hex()

    def reset_tree(self):
        self.leaves = list()
        self.levels = None
        self.is_ready = False

    def add_leaf(self, values, do_hash=False):
        self.is_ready = False
        # Check if single leaf
        if not isinstance(values, (tuple, list)):
            values = [values]
        for v in values:
            if do_hash:
                v = v.encode('utf-8')
                if self.hash_function == blake3().digest:  # Special case for Blake3
                    v = blake3(v).hexdigest()
                else:
                    v = self.hash_function(v).hexdigest()
            v = bytearray.fromhex(v)
            self.leaves.append(v)

    def get_leaf(self, index):
        return self._to_hex(self.leaves[index])

    def get_leaf_count(self):
        return len(self.leaves)

    def get_tree_ready_state(self):
        return self.is_ready

    def _calculate_next_level(self):
        solo_leave = None
        N = len(self.levels[0])  # Number of leaves on the level
        if N % 2 == 1:  # If odd number of leaves on the level
            solo_leave = self.levels[0][-1]
            N -= 1

        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            if self.hash_function == blake3().digest:  # Special case for Blake3
                new_level.append(blake3(l + r).digest())
            else:
                new_level.append(self.hash_function(l + r).digest())
        if solo_leave is not None:
            new_level.append(solo_leave)
        self.levels = [new_level, ] + self.levels  # Prepend new level

    def make_tree(self):
        self.is_ready = False
        if self.get_leaf_count() > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.is_ready = True

    def get_merkle_root(self):
        if self.is_ready:
            if self.levels is not None:
                return self._to_hex(self.levels[0][0])
            else:
                return None
        else:
            return None