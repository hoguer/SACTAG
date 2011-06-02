
def file_dict(ref_file):
    """returns a dictionary of 'subcorpus: TLG file list' pairs from the reference
    file"""
    
    output_dict = {}
    for line in open(ref_file):
        line = line.strip()
        line_list = line.split('\t')
        for item in line_list:
            item = item.strip()
        output_dict[line_list[0]] = line_list[1:]

    return output_dict
