import sys

def rpartition(string, sep):

    if sys.hexversion >= 0x02060000:
        return string.rpartition(sep)
    else:
        parts = string.split(sep)
        if len(parts) == 1:
            return ('', '', parts[0])
        else:
            toReturn = ["", "", ""]
            toReturn[0]=""
            for item in parts[:-1]:
                toReturn[0] += item + sep
            toReturn[0] = toReturn[0][:-1]
            toReturn[1] = sep
            toReturn[2] = parts[-1]
            return toReturn

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
