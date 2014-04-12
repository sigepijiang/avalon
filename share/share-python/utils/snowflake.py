# -*- coding: utf-8 -*-

import time


avalon_epoch = 1395309318
# worker_id_len = 5
# data_center_id_len = 5
worker_id_len = 4
data_center_id_len = 4
max_worker_id = -1L ^ (-1L << worker_id_len)
max_data_center_id = -1L ^ (-1L << data_center_id_len)
# sequence_len = 12
sequence_len = 10

worker_id_off = sequence_len
data_id_off = sequence_len + worker_id_len
timestamp_off = sequence_len + worker_id_len + data_center_id_len
max_sequence = -1L ^ (-1L << sequence_len)
last_timestamp = -1L
sequence = 0L


class SnowFlake(object):
    work_id_len = 5
    data_center_id_len = 5
    sequence_len = 12
    timestamp_factor = 1000

    def _get_worker_id(self):
        return

    def _get_data_center_id(self):
        return

    def _get_timestamp(self):
        return long(time.time() * self.timestamp_factor)

    def __init__(self, work_id_len=5, data_center_id_len=5, sequence_len=12,
                 timestamp_factor=1000):
        self.work_id_len = work_id_len
        self.data_center_id_len = data_center_id_len
        self.sequence_len = sequence_len
        self.timestamp_factor = timestamp_factor

    def get_id(self, worker, data_center):
        global sequence, last_timestamp

        max_worker_id = -1L ^ (-1L << self.worker_id_len)
        max_data_center_id = -1L ^ (-1L << self.data_center_id_len)
        max_sequence = -1L ^ (-1L << self.sequence_len)
        worker_id_off = self.sequence_len
        data_id_off = self.sequence_len + self.worker_id_len
        timestamp_off = (
            self.sequence_len + self.worker_id_len + self.data_center_id_len)

        worker_id = self._get_worker_id(worker)
        data_center_id = self._get_data_center_id(data_center)
        timestamp = self._get_timestamp()

        if worker_id > max_worker_id or worker_id < 0:
            raise

        if data_center_id > max_data_center_id or data_center_id < 0:
            raise

        if timestamp < last_timestamp:
            raise

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & max_sequence
            if sequence == 0:
                timestamp = self._til_next_millis(last_timestamp)
        else:
            sequence = 0

        last_timestamp = timestamp
        return (
            ((timestamp - avalon_epoch) << timestamp_off)
            | (data_center_id << data_id_off)
            | (worker_id << worker_id_off)
            | sequence
        )

        def _til_next_millis(self, last_timestamp):
            timestamp = _get_timestamp()
            while timestamp <= last_timestamp:
                timestamp = _get_timestamp()
            return timestamp


def _get_worker_id(worker):
    return 1


def _get_data_center_id(data_center):
    return 1


def _get_timestamp():
    # return long(time.time() * 1000)  # snowflake 使用毫秒
    return long(time.time())


def _til_next_millis(last_timestamp):
    timestamp = _get_timestamp()
    while timestamp <= last_timestamp:
        timestamp = _get_timestamp()
    return timestamp


def get_id(worker, data_center):
    global sequence, last_timestamp

    worker_id = _get_worker_id(worker)
    data_center_id = _get_data_center_id(data_center)

    if worker_id > max_worker_id or worker_id < 0:
        raise

    if data_center_id > max_data_center_id or data_center_id < 0:
        raise

    timestamp = _get_timestamp()
    if timestamp < last_timestamp:
        raise

    if last_timestamp == timestamp:
        sequence = (sequence + 1) & max_sequence
        if sequence == 0:
            timestamp = _til_next_millis(last_timestamp)
    else:
        sequence = 0

    last_timestamp = timestamp
    return (
        ((timestamp - avalon_epoch) << timestamp_off)
        | (data_center_id << data_id_off)
        | (worker_id << worker_id_off)
        | sequence
    )
