def making_list(file):
    ls = []
    for line in file:
        x = []
        x.append(line.strip())
        for i in range(3):
            x.append(file.readline().strip())
        ls.append(x)
    return ls


def making_dict(ls):
    d = []
    for i in ls:
        d.append({'name': i[0], 'seq': i[1], 'plus': i[2], 'quality': i[3]})
    return d


def filter_len(listd, length_bounds):  #####!!!!!length bounds!!!!
    filtered = []
    for i in listd:
        if len(i['seq']) in range(length_bounds[0], length_bounds[1] + 1):
            filtered.append(i)
    return filtered


def filter_gc_percentage(listd, gc_bounds):  #####!!!!!gc bounds!!!!
    filtered = []
    for i in listd:
        c = 0
        for j in i['seq']:
            if j.upper() in ["G", "C"]:
                c += 1
        prc = (c / len(i['seq'])) * 100
        if gc_bounds[0] < prc < gc_bounds[1] + 1:
            filtered.append(i)
    return filtered


def filter_mean_quality(listd, qual_threshold):  #####!!!!!quality threshold!!!!
    filtered = []
    for i in listd:
        s = 0
        for j in i['quality']:
            s += ord(j)
        mean = s / len(i['quality'])
        if mean > qual_threshold:
            filtered.append(i)
    return filtered


def file_writing(filtered, failed, save_filt, prefix):
    with open(f'{prefix}_passed.fastq', 'w') as f:
        for i in filtered:
            for j in i.values():
                print(j, file=f)

    if save_filt:
        with open(f'{prefix}_failed.fastq', 'w') as f:
            for i in failed:
                for j in i.values():
                    print(j, file=f)


def main(input_fastq, output_file_prefix, gc_bounds=(0, 100),
         length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=True):
    with open(input_fastq) as file:  ####filename as var

        ls = making_list(file)
        dlist = making_dict(ls)

        len_filtered = filter_len(dlist, length_bounds)
        gc_filtered = filter_gc_percentage(len_filtered, gc_bounds)
        quality_filtered = filter_mean_quality(gc_filtered, quality_threshold)

        failed = []
        for i in dlist:
            if i not in quality_filtered:
                failed.append(i)

        file_writing(quality_filtered, failed,
                     save_filtered, output_file_prefix)


