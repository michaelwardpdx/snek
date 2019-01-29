#!/usr/bin/python3

import sys
import argparse

builtin_id = 1

class SnekBuiltin:
    name = ""
    id = 0
    nformal = 0
    keyword = False
    def __init__(self, name, param):
        global builtin_id
        self.name = name
        if param[0].isalpha():
            self.keyword = param
        else:
            self.keyword = False
            self.nformal = int(param)
            self.id = builtin_id
            builtin_id += 1

    def __eq__(self,other):
        return self.name == other.name

    def __lt__(self,other):
        return self.name < other.name

    def snek_name(self):
        return self.name

    def cpp_name(self):
        return "SNEK_BUILTIN_%s" % (self.name.replace(".", "_"))

    def func_name(self):
        return "snek_builtin_%s" % (self.name.replace(".", "_"))


    def func_field(self):
        if self.nformal == -1:
            return ".funcv"
        return ".func%d" % self.nformal

headers=[]
builtins = []

def add_builtin(name, id):
    global builtins
    builtins += [SnekBuiltin(name, id)]

def load_builtins(filename):
    global headers
    f = open(filename)
    for line in f.readlines():
        if line[0] == '#':
            headers += [line]
        else:
            bits = line.split(",")
            add_builtin(bits[0].strip(), bits[1].strip())

def dump_headers(fp):
    for line in headers:
        print("%s" % line, file=fp)

def dump_max_len(fp):
    max_len = 0
    for name in builtins:
        if len(name.name) > max_len:
            max_len = len(name.name)
    print("#define SNEK_BUILTIN_NAMES_MAX_LEN %d" % max_len, file=fp)

def dump_names(fp):
    print("static const uint8_t SNEK_BUILTIN_NAMES_DECLARE(snek_builtin_names)[] = {", file=fp)
    total = 0
    print("0,", file=fp);
    total += 1
    for name in sorted(builtins):
        if name.keyword:
            print("\t%s | 0x80, " % name.keyword, end='', file=fp)
        else:
            print("\t%d, " % name.id, end='', file=fp)
        total += 1
        for c in name.name:
            print("'%c', " % c, end='', file=fp)
            total += 1
        print("0,", file=fp)
        total += 1
    print("};", file=fp)
    print("#define SNEK_BUILTIN_NAMES_SIZE %d" % total, file=fp)

def dump_decls(fp):
    for name in sorted(builtins):
        if name.keyword or name.nformal == -2:
            continue
        print("extern snek_poly_t", file=fp)
        print("%s(" % name.func_name(), file=fp, end='')
        if name.nformal == -1:
            print("uint8_t nposition, uint8_t nnamed, snek_poly_t *args", end='', file=fp)
        elif name.nformal == 0:
            print("void", end='', file=fp)
        else:
            for a in range(name.nformal):
                print("snek_poly_t a%d" % a, end='', file=fp)
                if a < name.nformal-1:
                    print(", ", file=fp)
        print(");", file=fp)
        print(file=fp)

def dump_builtins(fp):
    print("const snek_builtin_t SNEK_BUILTIN_DECLARE(snek_builtins)[] = {", file=fp)

    for name in sorted(builtins):
        if name.keyword or name.nformal == -2:
            continue

        print("\t[%s - 1] {" % name.cpp_name(), file=fp)
        print("\t\t.nformal=%d," % name.nformal, file=fp)
        print("\t\t%s = %s," % (name.func_field(), name.func_name()), file=fp)
        print("\t},", file=fp)
    print("};", file=fp)

def dump_cpp(fp):
    for name in sorted(builtins):
        if name.keyword:
            continue
        print("#define %s %d" % (name.cpp_name(), name.id), file=fp)

    print("#define SNEK_BUILTIN_END %d" % (builtin_id), file=fp)


def builtin_main():

    parser = argparse.ArgumentParser(description="Construct Snek builtin data.")
    parser.add_argument('builtins', metavar='F', nargs='+',
                        help='input files describing builtins')
    parser.add_argument('-o', '--output', dest='output', help='output file')

    args=parser.parse_args()

    for b in args.builtins:
        load_builtins(b)

    fp = sys.stdout

    if args.output:
        fp = open(args.output, mode='w')

    print("#ifdef SNEK_BUILTIN_DATA", file=fp)
    print("#undef SNEK_BUILTIN_DATA", file=fp)
    print("#ifndef SNEK_BUILTIN_NAMES_DECLARE", file=fp)
    print("#define SNEK_BUILTIN_NAMES_DECLARE(n) n", file=fp)
    print("#endif", file=fp)

    dump_names(fp)

    print(file=fp)

    print("#ifndef SNEK_BUILTIN_DECLARE", file=fp)
    print("#define SNEK_BUILTIN_DECLARE(n) n", file=fp)
    print("#define SNEK_BUILTIN_NFORMAL(b) ((b)->nformal)", file=fp)
    print("#define SNEK_BUILTIN_FUNC0(b) ((b)->func0)", file=fp)
    print("#define SNEK_BUILTIN_FUNC1(b) ((b)->func1)", file=fp)
    print("#define SNEK_BUILTIN_FUNC2(b) ((b)->func2)", file=fp)
    print("#define SNEK_BUILTIN_FUNC3(b) ((b)->func3)", file=fp)
    print("#define SNEK_BUILTIN_FUNC4(b) ((b)->func4)", file=fp)
    print("#endif", file=fp)

    dump_builtins(fp)

    print(file=fp)

    print("#else /* SNEK_BUILTIN_DATA */", file=fp)

    print("#ifdef SNEK_BUILTIN_DECLS", file=fp)
    print("#undef SNEK_BUILTIN_DECLS", file=fp)
    dump_decls(fp)
    print("#else /* SNEK_BUILTIN_DECLS */", file=fp)

    dump_max_len(fp)

    dump_headers(fp)

    dump_cpp(fp)

    print("#endif /* SNEK_BUILTIN_DECLS */", file=fp)
    print("#endif /* SNEK_BUILTIN_DATA */", file=fp)

builtin_main()