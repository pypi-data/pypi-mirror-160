"""
Hash Chunker helper to provide hash ranges for distributed data processing.
"""
import math
from typing import List, Tuple


class HashChunker(object):
    """Main module class."""

    hash_ranges_accuracy = 5
    md5_length = 32
    hex_base = 16
    hex_zero = '0'
    hex_f = 'f'
    hex_format = 'x'
    hash_length_limit = 10

    def get_chunks(
        self,
        batch: int,
        all_items_count: int,
    ) -> List[Tuple[str, str]]:
        """
        Return hash ranges.

        :param batch: batch limit
        :param all_items_count: dataset length
        :return: list of ranges hash
        """
        if all_items_count == 0 or batch == 0:
            return []
        (
            all_items_count,
            batch,
            current_position,
            previous_position,
        ) = self._get_positions(all_items_count, batch)
        return self._add_ranges(
            all_items_count,
            batch,
            current_position,
            previous_position,
        )

    def _add_ranges(
        self,
        all_items_count: int,
        batch: int,
        current_position: int,
        previous_position: int,
    ) -> List[Tuple[str, str]]:
        ranges = []
        while current_position < all_items_count:
            start = self._position_to_hex(previous_position)
            stop = self._position_to_hex(current_position)
            ranges.append((
                start[:self.hash_length_limit],
                stop[:self.hash_length_limit],
            ))
            previous_position = current_position
            current_position += batch
        start = self._position_to_hex(previous_position)
        stop = self.hex_f * self.md5_length
        ranges.append(
            (start[:self.hash_length_limit], stop[:self.hash_length_limit]),
        )
        return ranges

    def _get_positions(
        self,
        all_items_count: int,
        batch_limit: int,
    ) -> Tuple[int, int, int, int]:
        scale = self.hex_base ** self.hash_ranges_accuracy / all_items_count
        batch_limit = math.ceil(batch_limit * scale)
        all_items_count *= scale
        previous_position = 0
        current_position = batch_limit
        return (
            all_items_count,
            batch_limit,
            current_position,
            previous_position,
        )

    def _position_to_hex(self, position: int) -> str:
        hexed = format(position, self.hex_format)
        if len(hexed) < self.hash_ranges_accuracy:
            zeros_count = self.hash_ranges_accuracy - len(hexed)
            hexed = self.hex_zero * zeros_count + hexed
        hexed += self.hex_zero * (self.md5_length - len(hexed))
        return hexed
