def get_baudrate(port):
    import os
    input = "stty -f /dev/cu.{}".format(port)
    output = os.popen(input)
    first_line_output = output.readlines()[0]
    baudrate=""
    for x in first_line_output:
        if x.isdigit():
            baudrate +=x
    baudrate=int(baudrate)
    return baudrate