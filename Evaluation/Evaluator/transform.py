if __name__ == "__main__":
    src_qrel = "qrels.txt"
    dst_qrel = "qrels.bin.txt"
    new_l = []
    with open(src_qrel, 'rU') as f:
        lines = f.readlines()
        for line in lines:
            split_lines = line.split()
            qID = split_lines[0]
            assessor = split_lines[1]
            doc = split_lines[2]
            grade = split_lines[3]

            if int(grade) > 1:
                grade = 1

            st = "{} {} {} {}\n".format(qID, assessor, doc, grade)
            new_l.append(st)


    with open(dst_qrel, 'w') as d:
        for l in new_l:
            d.write(l)



