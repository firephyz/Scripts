import sys
import functools
import itertools as IT
from pprint import pprint

class LinuxEvent:
    e_time = None
    e_type = None
    e_code = None
    e_value = None

    def __init__(self, *args, **kwards):
        if type(args[0]) == str:
            # (self, byte_string)
            self.__init__(*LinuxEvent.parse_byte_string(args[0]))
        else:
            # (self, time, type, code, value)
            self.e_time = args[0]
            self.e_type = args[1]
            self.e_code = args[2]
            self.e_value = args[3]


    @staticmethod
    def parse_byte_string(byte_string):
        # timeval split in two to reorder from little endian
        field_sizes = [8, 8, 2, 2, 4]

        byte_string = iter(byte_string)

        byte_splitter = lambda byte_count: (
            int(LinuxEvent.endian(''.join(IT.islice(byte_string, 2*byte_count))), 16))
        mapped_bytes = list(map(byte_splitter, field_sizes))

        timeval = {'tv_sec': mapped_bytes[0], 'tv_usec': mapped_bytes[1]}
        if mapped_bytes[4] > 0x8000_0000:
            "Neg: {}".format(mapped_bytes[4])
            mapped_bytes[4] -= 0x1_0000_0000
        mapped_bytes = [timeval] + mapped_bytes[2:]

        return mapped_bytes


    # swaps byte endianess
    @staticmethod
    def endian(value):
        return ''.join(map(lambda pair: ''.join(pair),
                           reversed(list(zip(value[::2], value[1::2])))))

# 4 4
# 1 {272, 273}
# 0 0
#
# 2 {0,1}
# 0 0
#
# 2 8
# 2 11
# 0 0

class Builder:
    self_spec = None
    requirements = None

    local_state = None

    evolutions = None
    valid = True

    def __init__(self, self_spec, subevols):
        self.self_spec = self_spec
        self.evolutions = subevols
        self.requirements = self_spec.union(reduce(lambda total, deps: total.union(deps), subevols.deps()))


    def deps(self):
        return self.requirements


    # is matched evol propagated to the instance evolutions?
    # compute self needed data, subevol needed data (immediately recursively)
    # union to find data local to this processing node.
    # prematching only occurs at initial pass of node,
    def match(data):
        if not self.prematch(data):
            return False

        for evol in self.evolutions:
            if not evol.match(data):
                evolutions.remove(evol)

        return True


    # TODO, check if supplied data fits or doesn't fit spec,
    # don't just store the state
    def prematch(data):
        for var in self.self_spec:
            local_state[var] = data[var]

        return True


class MouseEventForm(MouseEvent):
    types = None
    codes = None

    def __init__(types, codes):
        self.types = types
        self.codes = codes


    def match(event):
        if not event.e_type in self.types:
            return False
        if not event.e_code in self.codes:
            return False
        return True


class MouseEvent:
    kind = None
    value = None

    data = []
    cont = self.start_build
    initial_forms = None

    def __init__(linux_event):
        initial_forms = {}
        initial_forms['button'] = MouseEventForm([1], [272, 273])
        initial_forms['motion'] = MouseEventForm([2], [0, 1])
        initial_forms['scroll'] = MouseEventForm([2], [8])

        self.cont(linux_event)


    def cont(event):
        for form in initial_forms:
            form.match(linux_event)

if len(sys.argv) == 1:
    print('Please supply file from which to read.');
    sys.exit(1)

mouse = open(sys.argv[1], 'rb')
out_file = open('mouse_out.txt', 'w')

mouse_event = None
for i in range(10000):
    event = LinuxEvent(mouse.read(24).hex())

    # if mouse_event == None or mouse_event.is_built():
    #     mouse_event = MouseEvent(event)
    # else:
    #     mouse_event.cont(event)
    #print('Read time: {}'.format(time.time() - start_time))
    #print('{}'.format(mouse.read(24).hex()))

    pprint(vars(event))
    #out_file.write('{:x}'.format(event.e_time) + '\n')

out_file.close()

# Max_Bytes = 24*20
# byte_count = 0
# buffer = []
# for i in range(20):
#     buffer.append(mouse.read(24).hex())
