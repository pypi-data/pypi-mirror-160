#! /usr/bin/env python
# Copyright 2016 to 2022, Cisco Systems, Inc., all rights reserved.
import os
import logging
import traceback
from collections import OrderedDict
import itertools
import tempfile
import shutil
import argparse
from distutils import sysconfig
from six import string_types
from sly import Lexer
from grpc_tools import protoc

log = logging.getLogger('__name__')


class ProtoParserException(Exception):
    pass


class ProtoLexer(Lexer):
    """Token class that defines protobuf tokens."""

    # Set of token names.  This is always required before token rules
    tokens = {ID, SERVICE, RPC, MESSAGE, COMMENT, NEWLINE, LBRACE, RBRACE, # noqa
              LPAREN, RPAREN, LESS, GREATER, COMMA, SEMICOLON, DOT, TICK, # noqa
              EQUAL, SERVICE, RPC, MESSAGE, SYNTAX, PACKAGE, IMPORT, OPTION, # noqa
              EXTEND, RETURNS, STREAM, STRING, UINT32, INT32, UINT64, INT64, # noqa
              BOOL, BYTES, MAP, REPEATED, ENUM, ONEOF, BYTES, END_COMMENT, # noqa
              STAR, FLOAT, DOUBLE} # noqa

    # String containing ignored characters between tokens
    ignore = ' \t\r'

    # Regular expression rules for tokens
    COMMENT = r'\/\/|\/\*'
    END_COMMENT = r'\*\/'
    NEWLINE = r'\n'
    LBRACE = r'{'
    RBRACE = r'}'
    LPAREN = r'\('
    RPAREN = r'\)'
    LESS = r'\<'
    GREATER = r'\>'
    COMMA = r'\,'
    SEMICOLON = r'\;'
    DOT = r'\.'
    TICK = r"'"
    STAR = r'\*'
    EQUAL = r'='
    ID = r'[a-zA-Z0-9\"\.\,\:\/_\-\[\]][a-zA-Z0-9\"\.\:\/_\-\[\]]*'
    ID['service'] = SERVICE # noqa
    ID['rpc'] = RPC # noqa
    ID['message'] = MESSAGE # noqa
    ID['syntax'] = SYNTAX # noqa
    ID['package'] = PACKAGE # noqa
    ID['import'] = IMPORT # noqa
    ID['option'] = OPTION # noqa
    ID['extend'] = EXTEND # noqa
    ID['returns'] = RETURNS # noqa
    ID['stream'] = STREAM # noqa
    ID['string'] = STRING # noqa
    ID['uint32'] = UINT32 # noqa
    ID['sint32'] = INT32 # noqa
    ID['uint64'] = UINT64 # noqa
    ID['sint64'] = INT64 # noqa
    ID['float'] = FLOAT # noqa
    ID['double'] = DOUBLE # noqa
    ID['bool'] = BOOL # noqa
    ID['bytes'] = BYTES # noqa
    ID['map'] = MAP # noqa
    ID['repeated'] = REPEATED # noqa
    ID['enum'] = ENUM # noqa
    ID['oneof'] = ONEOF # noqa
    ID['bytes'] = BYTES # noqa


class ProtoParser:
    """Token parser logic to build jsTree."""

    # Should be at least package and syntax defined.
    #
    # syntax "proto3";
    # package gnoi.A;
    #
    MINIMUM_PROTO_SIZE = 35
    REQUIRED_CONTENT = ['syntax ', 'package ']
    SKIP = [
        'SYNTAX',
        'PACKAGE',
        'OPTION',
        'EXTEND'
    ]
    DATATYPE = [
        'STRING',
        'UINT32',
        'INT32',
        'UINT64',
        'INT64',
        'BOOL',
        'BYTES',
        'FLOAT',
        'DOUBLE',
    ]

    def __init__(self, counter=None):
        self.lexer = ProtoLexer()
        if counter is None:
            self.cntr = itertools.count(1)
        else:
            self.cntr = counter
        self.data = ''
        self.service_name = 'No service'
        self.service_comment = ''
        self.imports = []
        self.service = {
            'id': next(self.cntr),
            'text': '',
            'data': {'comment': ''},
            'children': [
                {
                    'id': next(self.cntr),
                    'text': 'rpcs',
                    'children': []
                }
            ]
        }
        self.rpcs = []
        self.messages = OrderedDict()
        self.enums = OrderedDict()
        self.oneofs = OrderedDict()
        self.tree = OrderedDict()

    def _validate_proto_str(self, proto_str):
        if not isinstance(proto_str, string_types):
            raise ProtoParserException(
                'Invalid string: {0}'.format(str(proto_str))
            )
        if len(proto_str) < self.MINIMUM_PROTO_SIZE:
            raise ProtoParserException(
                'Not enough content in proto file to be valid.'
            )
        for item in self.REQUIRED_CONTENT:
            if item not in proto_str:
                raise ProtoParserException(
                    'Proto file must have at least one {0}'.format(item)
                )

    def parse_from_file(self, proto_path):
        if not os.path.isfile(proto_path):
            raise ProtoParserException(
                'File path invalid: {0}'.format(proto_path)
            )
        self.service_name = proto_path[
            proto_path.rfind('/')+1: proto_path.rfind('.proto')
        ]
        self.data = open(proto_path).read()
        self._validate_proto_str(self.data)
        self.process_proto()

    def parse_from_str(self, proto_str):
        self.data = proto_str
        self._validate_proto_str(self.data)
        self.process_proto()

    def process_proto(self, proto_str=None):
        comment = ''
        index = ''
        import_proto = ''
        in_comment = False
        in_skip = False
        in_service = False
        in_rpc = False
        rpc_name = ''
        rpc_stream = False
        rpc = {}
        in_message = False
        message = ''
        message_child = {}
        datatype = ''
        in_enum = False
        enum_name = ''
        enum_child = {}
        in_repeated = False
        in_import = False
        in_oneof = False
        oneof_name = ''
        oneof_child = {}
        in_map = False
        map_first = {}
        map_second = {}
        in_equal = False

        if proto_str is not None:
            self._validate_proto_str(proto_str)
            self.data = proto_str

        for token in self.lexer.tokenize(self.data):

            if token.type == 'COMMENT':
                in_comment = True
            elif token.type != 'NEWLINE' and in_comment:
                if not in_skip:
                    comment += token.value + ' '
            elif token.type == 'NEWLINE':
                in_comment = False
                in_equal = False
                in_skip = False
            elif token.type in self.SKIP:
                in_skip = True
                comment = ''
            elif token.type == 'EQUAL':
                in_equal = True
            elif token.type == 'IMPORT':
                in_import = True
            elif token.type == 'SEMICOLON':
                continue
            elif in_skip:
                continue
            elif token.type == 'SERVICE':
                self.service_comment = comment
                comment = ''
                in_service = True
            elif token.type == 'RPC':
                in_rpc = True
            elif token.type == 'STREAM' and in_rpc:
                rpc_stream = True
            elif token.type == 'MESSAGE':
                in_message = True
            elif token.type in self.DATATYPE:
                if in_map:
                    if not map_first:
                        map_first = {
                            'text': 'name',
                            'data': {
                                'nodetype': 'map_name',
                                'datatype': token.value
                            }
                        }
                    elif not map_second:
                        map_second = {
                            'text': 'value',
                            'data': {
                                'nodetype': 'map_value',
                                'datatype': token.value
                            }
                        }
                        datatype = 'map'
                else:
                    datatype = token.value
            elif token.type == 'ENUM':
                in_enum = True
            elif token.type == 'ONEOF':
                in_oneof = True
            elif token.type == 'REPEATED':
                in_repeated = True
            elif token.type == 'MAP':
                in_map = True
            elif token.type == 'ID':
                if in_equal and any((in_message, in_enum)):
                    index = token.value
                elif in_import:
                    comment = ''
                    import_proto = token.value
                    if '/' in import_proto:
                        import_proto = import_proto[import_proto.rfind('/')+1:]
                        import_proto = import_proto.replace('"', '')
                    in_import = False
                    if import_proto in self.imports:
                        import_proto = ''
                        continue
                    prp = ProtoParser(counter=self.cntr)
                    prp.imports = self.imports
                    try:
                        prp.parse_from_file(import_proto)
                    except ProtoParserException:
                        log.warning(
                            'Imported {0} not found'.format(import_proto)
                        )
                    self.cntr = prp.cntr
                    self.messages.update(prp.messages)
                    self.enums.update(prp.enums)
                    self.imports.append(import_proto)
                    import_proto = ''

                elif in_service:
                    if in_rpc:
                        if not rpc_name:
                            rpc_name = token.value
                            rpc = {
                                'id': next(self.cntr),
                                'text': rpc_name,
                                'data': {
                                    'name': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'rpc',
                                },
                                'children': []
                            }
                            comment = ''
                        elif len(rpc['children']) == 0:
                            rpc['children'].append({
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': token.value,
                                    'rpc': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'request',
                                    'stream': rpc_stream
                                }
                            })
                            comment = ''
                            rpc_stream = False
                        elif len(rpc['children']) == 1:
                            rpc['children'].append({
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': token.value,
                                    'rpc': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'response',
                                    'stream': rpc_stream
                                }
                            })
                            comment = ''
                            rpc_stream = False
                    else:
                        self.service['text'] = token.value

                elif in_enum:
                    if not enum_name:
                        enum_name = token.value
                        self.enums.update({
                            enum_name: {
                                'id': next(self.cntr),
                                'text': enum_name,
                                'data': {
                                    'name': enum_name,
                                    'comment': comment,
                                    'nodetype': 'parameter',
                                    'datatype': 'enum',
                                    'options': []
                                },
                                'children': []
                            }
                        })
                        comment = ''
                        continue
                    else:
                        if enum_child:
                            self.enums[enum_name]['data']['options'].append(
                                [index, enum_child, comment]
                            )
                        enum_child = token.value
                        index = ''
                        comment = ''

                elif in_message:
                    if not message:
                        message = token.value
                        self.messages.update({
                            message: {
                                'id': next(self.cntr),
                                'text': message,
                                'data': {
                                    'name': message,
                                    'comment': comment,
                                    'nodetype': 'message'
                                }
                            }
                        })
                        comment = ''
                        continue
                    if in_oneof:
                        if not oneof_name:
                            oneof_name = token.value
                            oneof_message = {
                                'id': next(self.cntr),
                                'text': token.value,
                                'children': [],
                                'data': {
                                    'name': token.value,
                                    'comment': comment,
                                    'index': '',
                                    'nodetype': 'oneof',
                                    'message': message,
                                    'options': []
                                }
                            }
                            comment = ''
                            children = []
                            if message_child:
                                message_child['data']['index'] = index
                                message_child['data']['comment'] = comment
                                children.append(message_child)
                                message_child = {}
                            children.append(oneof_message)
                            if 'children' in self.messages[message]:
                                self.messages[message]['children'] += children
                            else:
                                self.messages[message]['children'] = children
                            continue
                        else:
                            if oneof_child:
                                oneof_child['data']['index'] = index
                                oneof_child['data']['comment'] = comment
                                oneof_message['children'].append(
                                    oneof_child
                                )
                                oneof_message['data']['options'].append([
                                    oneof_child['text'],
                                    # oneof_child['data']['datatype']
                                ])
                            datatype = datatype or token.value
                            oneof_child = {
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': token.value,
                                    'index': '',
                                    'comment': '',
                                    'oneof': oneof_name,
                                    'nodetype': 'oneof',
                                    'datatype': datatype
                                }
                            }
                            continue
                    if datatype:
                        if message_child:
                            message_child['data']['index'] = index
                            message_child['data']['comment'] = comment
                            if 'children' in self.messages[message]:
                                self.messages[message]['children'].append(
                                    message_child
                                )
                            else:
                                self.messages[message]['children'] = [
                                    message_child
                                ]
                            index = ''
                            comment = ''
                        message_child = {
                            'id': next(self.cntr),
                            'text': token.value,
                            'data': {
                                'name': token.value,
                                'comment': '',
                                'index': '',
                                'nodetype': 'parameter',
                                'datatype': datatype,
                                'message': message
                            }
                        }
                        if datatype == 'bool':
                            message_child['data']['options'] = [
                                ['true', True, ''],
                                ['false', False, '']
                            ]
                        if in_map and map_first and map_second:
                            map_first['data']['map'] = token.value
                            map_second['data']['map'] = token.value
                            message_child['children'] = [map_first, map_second]
                            in_map = False
                            map_first = {}
                            map_second = {}
                        if in_repeated:
                            message_child['data']['repeated'] = True
                            in_repeated = False
                        comment = ''
                        datatype = ''
                    else:
                        datatype = token.value

            elif token.type == 'LBRACE':
                if in_service:
                    self.service['data']['comment'] = comment
                    comment = ''
                continue
            elif token.type == 'RBRACE':
                if in_service and in_rpc:
                    self.rpcs.append(rpc)
                    rpc = {}
                    in_rpc = False
                    rpc_name = ''
                elif in_service:
                    in_service = False
                    comment = ''
                elif in_enum:
                    if enum_child:
                        self.enums[enum_name]['data']['options'].append(
                            [index, enum_child, comment]
                        )
                    index = ''
                    comment = ''
                    in_enum = False
                    enum_name = ''
                    enum_child = {}
                    datatype = ''
                elif in_message:
                    if in_oneof:
                        if oneof_child:
                            oneof_child['data']['index'] = index
                            oneof_child['data']['comment'] = comment
                            oneof_message['children'].append(oneof_child)
                            oneof_message['data']['options'].append([
                                oneof_child['text'],
                                oneof_child['data']['datatype']
                            ])
                        in_oneof = False
                        oneof_name = ''
                        oneof_child = {}
                        datatype = ''
                    elif message_child:
                        message_child['data']['index'] = index
                        message_child['data']['comment'] = comment
                        if in_map:
                            message_child['children'] = [map_first, map_second]
                            map_first = {}
                            map_second = {}
                            datatype = ''
                            in_map = False
                        if 'children' in self.messages[message]:
                            self.messages[message]['children'].append(
                                message_child
                            )
                        else:
                            self.messages[message]['children'] = [
                                message_child
                            ]
                        index = ''
                        comment = ''
                        in_message = False
                        datatype = ''
                        message = ''
                        message_child = {}
                        in_map = False

    def _get_enums_for_tree(self):
        enums = []
        for key in self.enums.keys():
            enums.append({
                'id': next(self.cntr),
                'text': key,
                'children': [{'text': e} for e in self.enums[key]]
            })
        return enums

    def _get_messages_for_rpcs(self):
        if self.rpcs:
            for key in self.messages.keys():
                for rpc in self.rpcs:
                    children = []
                    for idx, ch in enumerate(rpc.get('children', [])):
                        ch['data']['rpc'] = rpc['data']['name']
                        if idx == 0:
                            ch['data']['nodetype'] = 'request'
                        else:
                            ch['data']['nodetype'] = 'response'
                        if ch.get('text', '') == key:
                            children.append(self.messages[key])
                        else:
                            children.append(ch)
                        for c in ch.get('children', []):
                            c['data']['rpc'] = rpc['data']['name']

                    if 'children' in rpc:
                        rpc['children'] = children

    def _get_nested_children(self, chkey, child, items):
        for ch in child.get('children'):
            dt = ch['data'].get('datatype', '')
            if dt[dt.find('.')+1:] == chkey:
                ch['data']['messagetype'] = dt
                if 'options' in items[chkey]['data']:
                    ch['data']['options'] = items[chkey]['data'][
                        'options'
                    ]
                    ch['data']['datatype'] = items[chkey]['data'][
                        'datatype'
                    ]
                else:
                    ch['children'] = items[chkey]['children']

    def _get_nested_messages(self, items={}):
        if not items:
            return
        for key in self.messages.keys():
            for chkey in items.keys():
                children = []
                for ch in self.messages[key].get('children', []):
                    dt = ch['data'].get('datatype', '')
                    if key == chkey == dt:
                        # TODO: message is inside of itself, now what?
                        children = []
                        break
                    if dt[dt.find('.')+1:] == chkey:
                        ch['data']['messagetype'] = dt
                        if 'options' in items[chkey]['data']:
                            ch['data']['options'] = items[chkey]['data'][
                                'options'
                            ]
                            ch['data']['datatype'] = items[chkey]['data'][
                                'datatype'
                            ]
                        else:
                            ch['children'] = items[chkey]['children']
                    children.append(ch)
                if children:
                    self.messages[key]['children'] = children

    def to_tree(self):
        if self.messages:
            self._get_nested_messages(self.messages)
            self._get_nested_messages(self.enums)
            # self._get_nested_messages(self.oneofs)
        if self.rpcs:
            self._get_messages_for_rpcs()
            self.service['children'][0]['children'] = self.rpcs
            self.service['data'] = {'comment': self.service_comment}
        else:
            self.service = {
                'id': 0,
                'text': self.service_name,
                'nodetype': 'service',
                'data': {'comment': self.service_comment},
                'children': []
            }
            if self.enums:
                enums = {
                    'id': next(self.cntr),
                    'text': 'enums',
                    'nodetype': 'enum',
                    'data': 'Defined ENUMs',
                    'children': [v for v in self.enums.values()]
                }
                self.service['children'].append(enums)
            if self.messages:
                messages = {
                    'id': next(self.cntr),
                    'text': 'messages',
                    'nodetype': 'message',
                    'data': {'comment': 'Defined messages'},
                    'children': [v for v in self.messages.values()]
                }
                self.service['children'].append(messages)

        return self.service


class ProtoCompile:

    def __init__(self, proto, repo='./'):
        self.proto = proto
        self.proto_file = proto + '.proto'
        self.tmpdir = tempfile.mkdtemp()
        self.proto_dir = repo
        self.lib_dir = os.path.dirname(os.path.abspath(__file__))
        self.import_protos = []

    def fixup_proto_imports(self, protos=[]):
        fixup = []
        import_protos = []

        for proto in protos:
            if proto in os.listdir(self.tmpdir):
                continue
            if not os.path.exists(
                os.path.join(self.proto_dir, proto)
            ):
                log.info('Import {0} not found'.format(proto))
                continue
            proto_str = open(os.path.join(self.proto_dir, proto)).read()

            for line in proto_str.splitlines():
                if line.startswith('import') and 'github.com' in line:
                    import_proto = line[
                        line.rfind('/')+1:
                    ].strip().replace('";', '')
                    if import_proto not in self.import_protos:
                        import_protos.append(import_proto)
                        self.import_protos.append(import_proto)
                    line = 'import "' + import_proto + '";'
                fixup.append(line)
            open(os.path.join(self.tmpdir, proto), 'w').write('\n'.join(fixup))
            fixup = []
        if import_protos:
            self.fixup_proto_imports(import_protos)

    def fixup_python_imports(self, proto):
        fixup = []

        if not os.path.exists(proto):
            log.info('Import {0} module not found'.format(proto))
            return
        proto_str = open(proto).read()
        for line in proto_str.splitlines():
            if line and line.startswith('import') and \
                'google.protobuf' not in line and \
                    not line.endswith(' grpc'):
                line = line.replace('import', 'from . import')
            fixup.append(line)
        open(proto, 'w').write('\n'.join(fixup))

    def compile_command(self, proto):
        _proto = os.path.join(
            sysconfig.get_python_lib(),
            'grpc_tools',
            '_proto'
        )
        cmd = [
            'grpc_tools.protoc',
            '--proto_path=' + self.tmpdir,
            '--proto_path=' + _proto,
            '--python_out=' + self.tmpdir,
            '--grpc_python_out=' + self.tmpdir
        ]
        for imp_proto in reversed(self.import_protos):
            if imp_proto == 'descriptor.proto':
                continue
            cmd.append(os.path.join(self.tmpdir, imp_proto))
            result = protoc.main(cmd)
            log.info(result)
            cmd.pop()
        cmd.append(os.path.join(self.tmpdir, proto))
        result = protoc.main(cmd)
        log.info(result)

    def compile_libs(self):
        try:
            self.fixup_proto_imports([self.proto_file])
            self.compile_command(self.proto_file)
            for pfile in os.listdir(self.tmpdir):
                if pfile.endswith('py'):
                    self.fixup_python_imports(
                        os.path.join(self.tmpdir, pfile)
                    )
                    shutil.copy(
                        os.path.join(self.tmpdir, pfile),
                        self.lib_dir
                    )
        except Exception:
            traceback.format_exc()
        finally:
            if os.path.isdir(self.tmpdir):
                shutil.rmtree(self.tmpdir)
        

def main(action, proto):
    if action == 'compile':
        pc = ProtoCompile(proto)
        pc.compile_libs()
    elif action == 'parse':
        from pprint import pprint as ppr
        pp = ProtoParser()
        pp.parse_from_file(proto)
        ppr(pp.to_tree())
    else:
        print('parse or compile, not {0}'.format(action))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
    Parse a protobuf file and return a python dict for a jstree.
        or
    Compile a protobuf file and create a python library.
    """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-a', '--action', default='compile',
                        help='Parse or compile a protobuf file.',
                        choices=['compile', 'parse'])
    parser.add_argument('-f', '--file', type=str,
                        help='File path to protobuf.')

    args = parser.parse_args()

    main(args.action, args.file)
