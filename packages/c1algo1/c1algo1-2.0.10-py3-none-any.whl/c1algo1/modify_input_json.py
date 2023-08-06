import json

# Give a source JSON, the header you want to copy ('historicalData', 'professors', 'schedule')
# and a destination JSON where the header will be copied to.
def set_input(src_file, src_header, dest_file):
    src = open(src_file, 'r')
    input = json.load(src)

    dest = open(dest_file, 'r')
    output = json.load(dest)

    #print(input[src_header])
    
    output[src_header] = input[src_header]

    dest.close()
    dest = open(dest_file, 'w')
    json.dump(output, dest)
    
    src.close()
    dest.close()