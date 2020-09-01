#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-08-19 <br>
# Time: 10:17 <br>
# Desc: 信-Canal客户端

import time

from canal.client import Client
from canal.protocol import EntryProtocol_pb2
from canal.protocol import CanalProtocol_pb2


def main():
    client = Client()
    client.connect(host='192.168.37.121', port=11111)
    client.check_valid(username=b'', password=b'')
    client.subscribe(client_id=b'1001', destination=b'example', filter=b'xintg\\..*')
    try:
        while True:
            message = client.get(100)
            entries = message['entries']
            for entry in entries:
                entry_type = entry.entryType
                if entry_type in [EntryProtocol_pb2.EntryType.TRANSACTIONBEGIN,
                                  EntryProtocol_pb2.EntryType.TRANSACTIONEND]:
                    continue
                row_change = EntryProtocol_pb2.RowChange()
                row_change.MergeFromString(entry.storeValue)
                header = entry.header
                database = header.schemaName
                table = header.tableName
                event_type = header.eventType
                for row in row_change.rowDatas:
                    format_data = dict()
                    event_type_name = ""
                    if entry_type not in [EntryProtocol_pb2.EventType.DELETE,
                                          EntryProtocol_pb2.EventType.INSERT,
                                          EntryProtocol_pb2.EventType.UPDATE]:
                        continue

                    if event_type == EntryProtocol_pb2.EventType.DELETE:
                        event_type_name = EntryProtocol_pb2.EventType.Name(event_type)
                        for column in row.beforeColumns:
                            format_data = {
                                column.name: column.value
                            }
                    elif event_type == EntryProtocol_pb2.EventType.INSERT:
                        event_type_name = EntryProtocol_pb2.EventType.Name(event_type)
                        for column in row.afterColumns:
                            format_data = {
                                column.name: column.value
                            }
                    elif event_type == EntryProtocol_pb2.EventType.UPDATE:
                        event_type_name = EntryProtocol_pb2.EventType.Name(event_type)
                        for column in row.afterColumns:
                            format_data = {
                                column.name: column.value
                            }

                    format_data['before'] = format_data['after'] = dict()
                    for column in row.beforeColumns:
                        format_data['before'][column.name] = column.value
                    for column in row.afterColumns:
                        format_data['after'][column.name] = column.value
                    data = dict(
                        db=database,
                        table=table,
                        event=event_type_name,
                        data=format_data,
                    )
                    print(data)
            time.sleep(1)
    except Exception as e:
        pass
    finally:
        client.disconnect()
