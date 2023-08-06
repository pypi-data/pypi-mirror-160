#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-ignore-all-errors[2]: Allow `Any` in type annotations

import asyncio
import unittest
import uuid
from contextlib import contextmanager

from typing import Any, Awaitable, Callable, Dict, Generator, TypeVar, Union
from unittest import mock

import torch
import torch.distributed.launcher as pet
from torch.distributed._shard.sharded_tensor import ShardedTensor


def _tensor_eq(lhs: Union[torch.Tensor, ShardedTensor], rhs: Any) -> bool:
    if type(lhs) != type(rhs):
        return False
    if isinstance(lhs, ShardedTensor):
        for l_shard, r_shard in zip(lhs.local_shards(), rhs.local_shards()):
            if not torch.allclose(l_shard.tensor, r_shard.tensor):
                return False
        return True
    elif isinstance(lhs, torch.Tensor):
        return torch.allclose(lhs, rhs)
    else:
        raise AssertionError("The lhs operand must be a Tensor or ShardedTensor.")


@contextmanager
def _patch_tensor_eq() -> Generator[None, None, None]:
    patchers = [
        mock.patch("torch.Tensor.__eq__", _tensor_eq),
        mock.patch(
            "torch.distributed._shard.sharded_tensor.ShardedTensor.__eq__", _tensor_eq
        ),
    ]
    for patcher in patchers:
        patcher.start()
    try:
        yield
    finally:
        for patcher in patchers:
            patcher.stop()


def assert_state_dict_eq(
    tc: unittest.TestCase,
    lhs: Dict[Any, Any],
    rhs: Dict[Any, Any],
) -> None:
    """
    assertDictEqual except that it knows how to handle tensors.

    Args:
        tc: The test case.
        lhs: The left-hand side operand.
        rhs: The right-hand side operand.
    """
    with _patch_tensor_eq():
        tc.assertDictEqual(lhs, rhs)


def check_state_dict_eq(lhs: Dict[Any, Any], rhs: Dict[Any, Any]) -> bool:
    """
    dict.__eq__ except that it knows how to handle tensors.

    Args:
        lhs: The left-hand side operand.
        rhs: The right-hand side operand.

    Returns:
        Whether the two dictionaries are equal.
    """
    with _patch_tensor_eq():
        return lhs == rhs


def get_pet_launch_config(nproc: int) -> pet.LaunchConfig:
    """
    Initialize pet.LaunchConfig for single-node, multi-rank tests.

    Args:
        nproc: The number of processes to launch.

    Returns:
        An instance of pet.LaunchConfig for single-node, multi-rank tests.
    """
    return pet.LaunchConfig(
        min_nodes=1,
        max_nodes=1,
        nproc_per_node=nproc,
        run_id=str(uuid.uuid4()),
        rdzv_backend="c10d",
        rdzv_endpoint="localhost:0",
        max_restarts=0,
        monitor_interval=1,
    )


T = TypeVar("T")


def async_test(coro: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """
    Decorator for testing asynchronous code.
    Once we drop support for Python 3.7.x, we can use `unittest.IsolatedAsyncioTestCase` instead.

    Usage:
        class MyTest(unittest.TestCase):
            @async_test
            async def test_x(self):
                ...
    """

    def wrapper(*args, **kwargs) -> T:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()

    return wrapper
