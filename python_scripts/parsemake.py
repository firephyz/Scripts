import re
import functools as ft
import copy
import os
import pickle
import sys
import math

##############################################################################
# Pre-processing into make nodes
##############################################################################
if len(sys.argv) < 2:
    print('Please provide a debug make log to parse.')
    sys.exit(1)

logname = sys.argv[1]
tmp_logname = '/tmp/make.log'
filter_re = '\'(Trying (pattern|implicit)|Looking for|Avoiding implicit|Rejecting impossible|Prerequisite)\''
os.system('cat {} | grep -vE {} > {}'.format(logname, filter_re, tmp_logname))
f = open(tmp_logname, 'r').read()

#f = open('/home/builder/rpmbuild/BUILD/newlib-build/log.txt', 'r').read()
#f = open('/home/builder/rpmbuild/BUILD/newlib-build/strippedlog.txt', 'r').read()
#f = open('/home/builder/rpmbuild/BUILD/newlib-build/manual.log', 'r').read()
text = re.findall('.*?\n', f)

# Extract nodes of make invocations
makenodes = list(filter(lambda line: re.match('^make\[[0-9]+\].*', line[1]), enumerate(text)))

# Convert into (<depth>, <line-number>, <data>) tuples
make_node_re = re.compile('make\[([0-9]+)\]: ((Entering|Leaving)[^\']+\'/home/builder/rpmbuild/BUILD/newlib-build(.*?)\'|Nothing[^\']+\'([^\']+)\')')
nodes = list(map(lambda parse: (int(parse[1][0][0]),
                                parse[0],
                                # <entering|leaving>, <make path>, <'all' field>
                                *parse[1][0][2:]),
                 map(lambda node: (node[0], make_node_re.findall(node[1])),
                     makenodes)))

# Sort first by make depth and then by line number, we will skim across the deepest nodes first
nodes.sort(key=lambda x: (x[0], x[1]))

# Remove the unneeded 'all' nodes, and the 'all' field
nodes = list(filter(lambda x: x[4] == '', nodes))
nodes = list(map(lambda x: x[:-1], nodes))

# We will pair side-by-side elements into one. Since they are are the same depth
# and sorted (and only start and end nodes), they should correspond to the same
# make invocation. Do some sanity checks to make sure.
a = list(zip(nodes[0:len(nodes):2], nodes[1:len(nodes):2]))
# Make sure no pairs have same start/end type (they must be opposites)
assert len(list(filter(lambda x: x[0][2] == x[1][2], a))) == 0
# Make sure no pairs have paths that differ
assert len(list(filter(lambda x: x[0][3] != x[1][3], a))) == 0

##############################################################################
# Make Item Classes
##############################################################################
class MakeItem:
    def __init__(self):
        self.start = None
        self.end = None
        self.parts = None
        self.target = None

    def all_spans_numbered(self):
        global text
        text_starts = [self.start] + list(map(lambda submake: submake.end + 1, self.parts))
        text_ends = list(map(lambda submake: submake.start, self.parts)) + [self.end + 1]
        text_spans = list(map(lambda span: list(map(lambda line: (line[0] + span[0], line[1]),
                                                    enumerate(text[span[0]:span[1]]))),
                              zip(text_starts, text_ends)))
        # submake_headers = list(map(lambda make: (make.span, '<<< make {} >>>\n'.format(self.target)), self.parts))
        total_text = []
        # for span, submake_header in zip(text_spans[:-1], submake_headers):
        #     total_text += span + [submake_header]
        for span in text_spans[:-1]:
            total_text += span
        total_text += text_spans[-1]
        return total_text

    def all_spans(self):
        starts = [self.start] + list(map(lambda part: part.end+1, self.parts))
        ends = list(map(lambda part: part.start, self.parts)) + [self.end+1]
        spans = list(map(lambda span: (span[0], text[span[0]:span[1]]), zip(starts, ends)))
        span_parts = ft.reduce(lambda acc, span_and_item: acc + [*span_and_item],
                                   zip(spans[0:-1], self.parts),
                                   []) + [spans[-1]]
        total_text = []
        for span in span_parts:
            if isinstance(span, MakeItem):
                total_text += span.as_pseudo_span()
            else:
                span_start = span[0]
                span_text = span[1]
                total_text += list(map(lambda line: '{:>5}| {}'.format(span_start + line[0], line[1]), enumerate(span_text)))

        return total_text

    def pretty_str(self):
        text = self.all_spans()
        return ''.join(text)

    def get_path(self, path):
        node = self
        for index in path:
            node = node.parts[index]
        return node

    def get_identity_string(self):
        raise Exception('must implement get_identity_string')


class MakeInvocation(MakeItem):
    def __init__(self):
        super()
        self.depth = None
        self.path = None
        pass

    def from_start_end_nodes(start, end):
        make = MakeInvocation()
        make.depth = start[0]
        make.start = start[1]
        make.end = end[1]
        make.path = start[3]
        make.parts = []
        return make

    def from_submakes(makes):
        global text
        make = MakeInvocation()
        make.depth = 0
        make.start = 0
        make.end = len(text) - 1
        make.path = ''
        make.parts = makes
        make.target = 'all'
        return make

    def as_pseudo_span(self):
        return ['{:>5}|\n{:>5}| {}\n{:>5}|\n'.format(self.start, '...', self.get_identity_string(), self.end)]

    def get_identity_string(self):
        return 'make \'{}\' in \'{}\''.format(self.target, self.path)


class MakeSubItem(MakeItem):

    def __init__(self):
        super()
        self.item_type = None

    def from_start_end_nodes(start, end, parts):
        item = MakeSubItem()
        item.start = start['line_number']
        item.end = end['line_number']
        item.parts = parts

        if start['type'] == 'target_start':
            if start['target'] != end['target']:
                raise Exception('Start and end targets do not match')
            item.target = start['target']
            item.item_type = 'target'
        else:
            item.target = None
            item.item_type = 'configure'

        return item

    def as_pseudo_span(self):
        return ['{:>5}|\n{:>5}| {}\n{:>5}|\n'.format(self.start, '...', self.get_identity_string(), self.end)]

    def get_identity_string(self):
        return 'item {} \'{}\''.format(self.item_type, self.target)

# Pair make nodes into start/end combos representing an entire make invocation
makes = list(map(lambda pair: MakeInvocation.from_start_end_nodes(*pair),
                 zip(nodes[0:len(nodes):2],
                     nodes[1:len(nodes):2])))

# Sort makes according to start of invocation, last makes first
makes.sort(key=lambda x: x.start)

# Furthest makes first
makes = list(reversed(makes))

##############################################################################
# Makes List Post processing
##############################################################################
# Adjust the actual line of the start of the make invocation
start_of_make_re = re.compile('^GNU Make.*')
for make in makes:
    index = next(make.start - line[0] - 1
                 for line in enumerate(reversed(text[:make.start]))
                 if start_of_make_re.match(line[1]) != None)
    make.start = index

# Find the target for each make invocation
for make in makes:
    prelude_start = make.start
    prelude_end = make.end if len(make.parts) == 0 else make.parts[0].start - 1
    target_re = re.compile('^Considering target file \'(.*?)\'')
    first_target_matches = list(filter(lambda match: len(match) != 0,
                                       map(lambda line: target_re.findall(line),
                                           text[prelude_start:prelude_end])))
    target = first_target_matches[0][0]
    make.target = target

def get_subitem_node_parts(node_types, node_re_list, node_parsers, make):
    # Collect match variant data into useful data structures
    match_types = list(map(lambda data: {'type': data[0],
                                         're': data[1]},
                           zip(node_types, node_re_list)))
    match_parsers = dict(zip(node_types, node_parsers))

    # Test each line in the make span against each node match we have
    get_single_match = lambda single_match: None if single_match == [] else single_match[0]
    node_matches = list(filter(lambda matched_line: matched_line['match'] is not None,
                               map(lambda matched_line: {'line_number': matched_line['line_number'],
                                                         'match': get_single_match(list(filter(lambda match: match['re_groups'] != [],
                                                                                               matched_line['matches'])))},
                                   map(lambda line: {'line_number': line[0],
                                                     'matches': list(map(lambda pattern: {'type': pattern['type'],
                                                                                          're_groups': pattern['re'].findall(line[1])},
                                                                         match_types))},
                                       make.all_spans_numbered()))))

    # Extract the match results in each node match
    for matched_line in node_matches:
        parsed_match = match_parsers[matched_line['match']['type']](matched_line['match']['re_groups'][0])
        matched_line['type'] = matched_line['match']['type']
        matched_line['depth'] = parsed_match['depth']
        matched_line['target'] = parsed_match['target']
        del matched_line['match']

    # Make sure we are sorted by line number to prepare for depth-comparison node building
    node_matches.sort(key=lambda match: match['line_number'])

    return node_matches

def combine_node_parts(start_type, end_type, node_parts):
    nodes_todo = []
    nodes = []
    while node_parts != []:
        start_node = node_parts[0]
        if start_node['type'] != start_type: raise Exception('Not a start node')
        end_node_index, end_node = next((index+1, match)
                                        for index, match in enumerate(node_parts[1:])
                                        if match['depth'] == start_node['depth'])
        if end_node['type'] != end_type:
            raise Exception('Not an end node')

        # Turn start and end nodes into a MakeSubItem
        subparts = node_parts[1:end_node_index]
        node = MakeSubItem.from_start_end_nodes(start_node, end_node, subparts)
        nodes += [node]

        # Store for further processing of sub-nodes if necessary
        if node.parts != []:
            nodes_todo += [node]

        # Move onto the next node parts
        node_parts = node_parts[end_node_index+1:]

    return nodes, nodes_todo

##############################################################################
# Put makes into a make call hierarchy
##############################################################################
def merge(n):
    global makes_todo
    makes_todo[n].parts = list(reversed(makes_todo[:n]))
    makes_todo = makes_todo[n:]

def pop(n):
    global makes_todo, store
    makes_todo = store[-n:] + makes_todo; store = store[:-n]

def push(n):
    global makes_todo, store
    store = store + makes_todo[:n]; makes_todo = makes_todo[n:]

def determine_action():
    global makes_todo, store

    # Do a pop off of the store if necessary
    # Pops occur when the makes list has been merged up to the level that is equal
    # to the level of the most recent nodes on the store stack. These store nodes must
    # be available on the makes list for the next merge.
    if store != [] and makes_todo[0].depth == store[-1].depth:
        other_store_indicies = list(iter(store_node[0]
                                         for store_node in enumerate(reversed(store))
                                         if store_node[1].depth != store[-1].depth))
        if len(other_store_indicies) == 0:
            return len(store), 'pop'
        else:
            return other_store_indicies[0], 'pop'

    # Find the make nodes that differ in depth from the first make node
    diff_level_nodes_i = list(iter(dict(zip(['index', 'node'], node))
                                   for node in enumerate(makes_todo)
                                   if node[1].depth != makes_todo[0].depth))

    # No nodes differed in depth, merging is done
    if len(diff_level_nodes_i) == 0:
        return len(makes_todo), 'finish'
    else:
        diff_node = diff_level_nodes_i[0]

        # Is the diff node shallower? If so, merge the deeper nodes into it
        if diff_node['node'].depth < makes_todo[0].depth:
            return diff_node['index'], 'merge'
        # Diff node is deeper and cannot be merged into. Save the shallower makes for later
        else:
            node_and_last = list(map(lambda pair: dict(zip(['current', 'prev'], pair)),
                                     zip(makes_todo[1:], makes_todo[:-1])))
            # Find the index of the deepest node after monotonicly descending depths
            index_of_max = next(node[0]
                                for node in enumerate(node_and_last)
                                if node[1]['current'].depth < node[1]['prev'].depth)
            # Find the first node that occurs at the same depth as that deepest one
            start_of_deepest = next(node[0]
                                    for node in enumerate(makes_todo)
                                    if node[1].depth == makes_todo[index_of_max].depth)
            return start_of_deepest, 'push'

store = []
makes_todo = [] + makes
while makes_todo != []:
    n, action = determine_action()

    if action == 'merge':
        merge(n)
    elif action == 'push':
        push(n)
    elif action == 'pop':
        pop(n)
    elif action == 'finish':
        push(n)

# Finalize processing the make call tree
make_tree = list(reversed(store))
make_top = MakeInvocation.from_submakes(make_tree)

##############################################################################
# Tree post processing
##############################################################################
# Don't forget manually constructed top level
makes += [make_top]

def extract_targets(make):
    # Parsing info for target subitems
    match_type_names = [
        'target_start',
        'target_end']
    match_type_re = [
        re.compile('^(( )*)Considering target file \'(.*?)\''),
        re.compile('^(( )*)(Successfully remade target file \'(.*?)\'|No need to remake target \'(.*?)\'|File \'(.*?)\' was considered already)'),]
    def parse_target_end(groups):
        target
    match_type_parsers = [
        lambda groups: {'target': groups[2],
                        'depth': len(groups[0]) + 1 if len(groups[0]) % 2 == 1 else len(groups[0])},
        lambda groups: {'target': list(filter(lambda group: group != '', groups[3:6]))[0],
                        'depth': len(groups[0]) + 1 if len(groups[0]) % 2 == 1 else len(groups[0])}]

    # Parse span of this make into sub-item nodes
    node_parts = get_subitem_node_parts(match_type_names, match_type_re, match_type_parsers, make)

    # Combine parts into make sub-items
    top_items, items_todo = combine_node_parts(match_type_names[0], match_type_names[1], node_parts)
    all_items = [] + top_items

    # Keeping combining and items that still have sub-parts to combine
    while items_todo != []:
        item = items_todo[0]
        subitems, subitems_todo = combine_node_parts(match_type_names[0], match_type_names[1], item.parts)
        all_items += subitems
        item.parts = subitems
        items_todo += subitems_todo
        items_todo = items_todo[1:]

    # Now merge the make invocation tree with the item tree (makes are called as part of items)
    all_items.sort(key=lambda part: part.start)
    top_level_submakes = []
    for submake in make.parts:
        closest_item_index = None
        try:
            item_past_make_index = next(item[0] for item in enumerate(all_items)
                                        if item[1].start > submake.start)
            closest_item_index = item_past_make_index - 1
        except StopIteration:
            closest_item_index = len(all_items) - 1

        containing_item_index = None
        try:
            containing_item_index = next(closest_item_index - item[0] for item in enumerate(reversed(all_items[:closest_item_index+1]))
                                         if item[1].end > submake.end)
        except StopIteration:
            containing_item_index = None

        # submake isn't contained within an item and should be sorted in
        # parts list directly for this make invocation
        if containing_item_index is None:
            top_level_submakes += [submake]
        # submake is contained within a MakeSubItem so insert it in the right place
        else:
            container = all_items[containing_item_index]
            container.parts += [submake]
            container.parts.sort(key=lambda part: part.start)

    # Create new parts list with combined submakes and make items
    # Place submakes that belong in the top level parts list there there
    make.parts = top_items + top_level_submakes
    make.parts.sort(key=lambda part: part.start)

# Extract sub-items (configure, targets, etc.)
for make in makes:
    extract_targets(make)


##############################################################################
# REPL Helper functions
##############################################################################
def change_make_path(action, levels=0):
    global make_path, path_file
    if action == 'up':
        make_path = make_path[0:-levels]
    elif action == 'down':
        make_path += [levels]
    elif action == 'update':
        pass # Just saving

    # Save new path to file for later
    cmd_save('')

def print_target_node(target_node):
    print(target_node.pretty_str())
    print(target_node.get_identity_string())
    num_width = math.ceil(math.log10(len(target_node.parts) + 1))
    fmt_string = '  {{:>{}}} {{}}'.format(num_width)
    for ip, p in enumerate(target_node.parts):
        print(fmt_string.format(ip, p.get_identity_string()))

def get_work_filename(filename):
    global workdir
    return '{}/{}'.format(workdir, filename)

##############################################################################
# REPL Commands
##############################################################################
def cmd_down(args):
    global make_path
    if len(args) == 0:
        print('invalid')
    else:
        target = int(args)
        if target >= len(make_top.get_path(make_path).parts):
            print('child index too high ([0, {}])'.format(len(make_top.get_path(make_path).parts)))
            return
        change_make_path('down', target)
        cmd_print('')

def cmd_up(args):
    global make_path
    if len(args) == 0:
        levels = 1
    else:
        levels = int(args)
    if levels > len(make_path):
        print('too high ({} deep)'.format(len(make_path)))
        return
    change_make_path('up', levels)
    cmd_print('')

def cmd_load(args):
    global make_path, workdir
    if len(args) == 0:
        path_files = list(filter(lambda file: re.match('.*?\.path$', file), os.listdir(workdir)))
        for file in path_files:
            print(' - {}'.format(file))
        return
    else:
        path_filename = args
    pathfile = open(get_work_filename(path_filename), 'rb')
    make_path = pickle.load(pathfile)
    pathfile.close()
    cmd_path('')
    change_make_path('update')

def cmd_save(args):
    global make_path, path_file
    # Display available path files if none is given
    if len(args) == 0:
        path_filename = path_file
    else:
        path_filename = '{}.path'.format(args)
    pathfile = open(get_work_filename(path_filename), 'w+b')
    pickle.dump(make_path, pathfile)
    pathfile.close()

def cmd_path(args):
    global make_path
    print(make_path)

def cmd_print(args):
    global make_path
    print_target_node(make_top.get_path(make_path))

def cmd_dump(args):
    global make_path, dump_file
    if len(args) == 0:
        filename = dump_file
    else:
        filename = args[0]
    filename = '{}/{}'.format(workdir, filename)
    print('writing to \'{}\''.format(filename))
    file = open(filename, 'w+')
    file.write(make_top.get_path(make_path).pretty_str())
    file.close()

def cmd_less(args):
    global dump_file
    cmd_dump('')
    os.system('less {}'.format(get_work_filename(dump_file)))

def cmd_quit(args):
    raise Exception('quit')

cmd_actions = {'down': cmd_down,
               'up': cmd_up,
               'path': cmd_path,
               'print': cmd_print,
               'load': cmd_load,
               'save': cmd_save,
               'dump':cmd_dump,
               'less': cmd_less,
               'quit': cmd_quit}


##############################################################################
# REPL
##############################################################################
workdir = 'make.work'
path_file = 'make.path'
dump_file = 'make.dump'
make_path = []
last_cmd_line = ''

# Setup working dir
try:
    os.stat(workdir)
except FileNotFoundError:
    os.mkdir(workdir)

cmd_load('make.path')
cmd_print('')
while True:
    input_line = input(' > ')
    if len(input_line) == 0:
        input_line = last_cmd_line
    last_cmd_line = input_line

    cmd, rest = re.findall('[ ]*([^ ]+)[ ]*(.*)', input_line)[0]
    try:
        cmd_actions[cmd](rest)
    except KeyError:
        print('Unknown command \'{}\''.format(cmd))
    except Exception as e:
        if e.args[0] == 'quit':
            break
        else:
            raise e
