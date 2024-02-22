import torch
import torch.nn as nn


class AsyncModelMover:
    def __init__(self, buffer_size=2):
        self.stream = torch.cuda.Stream()
        self.events = [torch.cuda.Event() for _ in range(buffer_size)]
        self.buffer_size = buffer_size
        self.current_event_index = 0

    def initialize_stream(self):
        if not hasattr(self, 'stream') or not self.stream:
            self.stream = torch.cuda.Stream()

    def move_model_async(self, model):
        self.initialize_stream()
        with torch.cuda.stream(self.stream):
            model.to('cuda:0', non_blocking=True)
        self.events[self.current_event_index].record(self.stream)
        self.current_event_index = (self.current_event_index + 1) % self.buffer_size

    def synchronize(self):
        torch.cuda.current_stream().wait_event(self.events[self.current_event_index])
        self.events[self.current_event_index].synchronize()

def test_async_model_mover():
    model = nn.Linear(10, 10)
    mover = AsyncModelMover(buffer_size=3)
    mover.move_model_async(model)
    mover.synchronize()
    assert next(model.parameters()).is_cuda, "Model was not moved to CUDA successfully"

    # Test with multiple moves
    model2 = nn.Linear(20, 20)
    mover.move_model_async(model2)
    mover.synchronize()
    assert next(model2.parameters()).is_cuda, "Second model was not moved to CUDA successfully"

if __name__ == "__main__":
    test_async_model_mover()
