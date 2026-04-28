import multiprocessing
import queue
import time

import pytest

"""
Implement a 'Drop-Frame' producer-consumer pipeline suitable for high-volume image processing.

Requirements:
1. `FrameBuffer` must expose a fixed-capacity queue-like buffer that is usable across processes.
2. `produce_frame` must attempt to add a frame without blocking; if the buffer is full the frame is discarded and a dropped counter increments.
3. `consume_frame` must retrieve frames, blocking when the buffer is empty.
4. The buffer must accurately report processed and dropped frame counts across process boundaries.
"""


class FrameBuffer:
    def __init__(self, max_size: int):
        self._queue = multiprocessing.Queue(maxsize=max_size)
        raise NotImplementedError()

    def produce_frame(self, frame_data):
        """Adds frame to queue or increments dropped counter if full. Non-blocking."""
        raise NotImplementedError()

    def consume_frame(self):
        """Retrieves a frame from the queue. Blocks if empty."""
        raise NotImplementedError()

    def get_stats(self):
        """Returns a tuple of (processed_count, dropped_count)."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_frame_buffer_basic():
    fb = FrameBuffer(max_size=10)
    fb.produce_frame("frame1")
    assert fb.consume_frame() == "frame1"


def test_frame_buffer_drop_logic():
    # Small buffer to force drops
    fb = FrameBuffer(max_size=2)

    # Fill buffer
    fb.produce_frame("f1")
    fb.produce_frame("f2")

    # These should be dropped
    fb.produce_frame("f3")
    fb.produce_frame("f4")

    _, dropped = fb.get_stats()
    assert dropped == 2

    # Queue should still contain f1, f2
    assert fb.consume_frame() == "f1"
    assert fb.consume_frame() == "f2"


def test_frame_buffer_multiprocessing():
    fb = FrameBuffer(max_size=5)

    def producer(buffer, count):
        for i in range(count):
            buffer.produce_frame(f"data_{i}")
            time.sleep(0.01)

    # Start a slow producer
    p = multiprocessing.Process(target=producer, args=(fb, 20))
    p.start()

    processed = 0
    # Consumer tries to read 10 frames
    for _ in range(10):
        try:
            fb.consume_frame()
            processed += 1
        except:
            break

    p.join()
    _, dropped = fb.get_stats()
    # Total produced (20) = processed + dropped + remaining_in_queue
    # We just check if the counters are accessible and non-zero
    assert (processed + dropped) > 0


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - Use `queue.Full` exception to detect a full buffer.
# - Use `multiprocessing.Value` for cross-process counters.
# - `Queue.put()` has a `block` parameter and a `timeout` parameter.
