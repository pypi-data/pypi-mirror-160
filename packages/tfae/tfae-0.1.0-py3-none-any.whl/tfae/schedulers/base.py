import tensorflow as tf
from typing import Callable, Literal, Optional
from functools import cached_property


class BaseScheduler(tf.keras.callbacks.Callback):
    """
    Represents base variable
    """

    def __init__(
        self,
        update_on: Literal["batch", "epoch"],
        skew: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.update_on = update_on
        self.skew = skew

    @cached_property
    def initial_value(self) -> float:
        raise NotImplementedError('property "initial_value" was not implemented')

    # @cached_property
    # def final_value(self) -> float:
    #     raise NotImplementedError('property "final_value" was not implemented')

    @cached_property
    def duration(self) -> int:
        raise NotImplementedError('property "duration" was not implemented')

    def calc(self, n: int) -> float:
        raise NotImplementedError('method "calc" was not implemented')

    @cached_property
    def value(self) -> tf.Variable:
        return tf.Variable(
            initial_value=self.initial_value, trainable=False, dtype=tf.float32
        )

    def update(self, n: int) -> None:
        if n > self.duration + 1:
            return

        # if n < self.duration + 1:
        #     next_value = self.calc(n)
        # else:
        #     next_value = self.final_value
        next_value = self.calc(n)

        if self.skew is not None:
            next_value = self.skew(next_value)

        print("-------------->", next_value)

        self.value.assign(next_value)

    def on_batch_begin(self, batch: int, logs: Optional[dict] = None):
        if self.update_on == "batch":
            self.update(batch)

    def on_epoch_begin(self, epoch: int, logs: Optional[dict] = None):
        if self.update_on == "epoch":
            self.update(epoch)
