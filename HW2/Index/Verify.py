from HW2.Index.Search import Search
from stemming.porter2 import stem as porter2_stem


path = '/Users/admin/Documents/CS6200/HW2/output/'

def verify(index, name, stem=False):
    print "Verifying %s" %name
    search = Search(index)
    terms  = get_terms()
    write_lines = []
    for t in terms:
        if stem:
            stemmed = porter2_stem(t)

        res = search.get_tf(stemmed)
        s = output_string(t, res)
        write_lines.append(s)

    write(write_lines, name)


def write(lines, name):
    print "Writing the output for in file -> %s" %name
    with open(path+name, 'a') as f:
        for line in lines:
            f.write(line)


def output_string(t, res):
    if 'df' not in res:
        return "{} {} {}\n".format(t, 0, 0)
    return "{} {} {}\n".format(t, res['df'], res['ttf'])


def get_terms():
    with open('/Users/admin/Documents/CS6200/HW2/in.4', 'r') as f:
        terms = []
        for line in f.readlines():
            terms.append(line[:-1])
        print len(terms)
        return terms


if __name__ == '__main__':
    verify('stemmed', 'out.stem.stop.4', stem=True)
    # verify('withstop', 'out.no.stem.no.stop.4')
