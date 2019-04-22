import csv
import glob
import json
import os
import time

import meta
import util


def extract_json():
    os.system("rm -rf {0}".format(meta.JSON_DIR))
    os.system("mkdir {0}".format(meta.JSON_DIR))

    with open(meta.GIVEN_DIR + "182_instances.json") as file:
        index    = 0

        for line in file:
            filename = str(index).zfill(3)
            print("Extracting transaction #{0}".format(filename))
            data = json.loads(line)

            with open("{0}{1}.json".format(meta.JSON_DIR, filename), 'w+') as outfile:
                outfile.write(json.dumps(data, indent=4, sort_keys=True))

            index += 1


def process_param_line(tx_id, tx_dir, line):
    # Split row into tokens
    params             = line.split()

    num_inputs         = int(params[0])        # n
    num_outputs        = int(params[1])        # m
    out_value          = int(params[2])        # outValue
    max_size           = int(params[3])        # M
    fee_rate           = float(params[4])      # alpha
    dust_threshold     = int(params[5])        # T
    min_change_output  = int(params[6])        # epsilon
    change_output_size = int(params[7])        # beta
    tx_size            = int(params[8])        # txsize
    selected_io_size   = int(params[9])        # iosize
    has_change_output  = int(params[10])       # cout
    change_value       = int(params[11])       # coutValue

    # Naming values
    line_dict = {}

    line_dict['tx_id']              = tx_id
    line_dict['num_inputs']         = num_inputs
    line_dict['num_outputs']        = num_outputs
    line_dict['out_value']          = out_value
    line_dict['max_size']           = max_size
    line_dict['fee_rate']           = fee_rate
    line_dict['dust_threshold']     = dust_threshold
    line_dict['min_change_output']  = min_change_output
    line_dict['change_output_size'] = change_output_size
    line_dict['tx_size']            = tx_size
    line_dict['selected_io_size']   = selected_io_size
    line_dict['has_change_output']  = has_change_output
    line_dict['change_value']       = change_value

    # Filter only required fields for calculation
    row_values = util.filter_dict(line_dict, meta.PARAM_FIELDS)

    # Write to csv
    with open(tx_dir + "params.csv", "w+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(meta.PARAM_FIELDS)
        csv_writer.writerow(row_values)


def process_input_lines(tx_dir, lines):
    with open(tx_dir + "txinput.csv", "w+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        # Write field names
        csv_writer.writerow(meta.TX_IN_FIELDS)

        for line in lines:
            # Split input line into token
            tokens = line.split('\t')

            index         = int(tokens[0]) - 1    # starts with 0
            size          = int(tokens[1])
            value         = int(tokens[2])
            confirmations = int(tokens[3])
            vout          = int(tokens[4])
            choosen       = int(tokens[5])
            tx_id         = tokens[6][:-1]        # Windows' EOL

            # Naming values
            line_dict = {}

            line_dict['index']         = index
            line_dict['size']          = size
            line_dict['value']         = value
            line_dict['confirmations'] = confirmations
            line_dict['vout']          = vout
            line_dict['choosen']       = choosen
            line_dict['tx_id']         = tx_id

            # Filter only required fields for calculation
            row_values = util.filter_dict(line_dict, meta.TX_IN_FIELDS)

            # Write row to csv
            csv_writer.writerow(row_values)


def process_output_lines(tx_dir, lines):
    with open(tx_dir + "txoutput.csv", "w+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        # Write field names
        csv_writer.writerow(meta.TX_OUT_FIELDS)

        for line in lines:
            tokens = line.split('\t')

            index = int(tokens[0]) - 1  # starts with 0
            size  = int(tokens[1])
            value = int(tokens[2])

            line_dict = {}

            line_dict['index'] = index
            line_dict['size']  = size
            line_dict['value'] = value

            row_values = util.filter_dict(line_dict, meta.TX_OUT_FIELDS)
            csv_writer.writerow(row_values)


def gen_csv_files():
    if os.path.isdir(meta.PROCESSED_DIR):
        os.system("rm -rf " + meta.PROCESSED_DIR)

    os.system("mkdir " + meta.PROCESSED_DIR)

    json_file_names = sorted([f[len(meta.JSON_DIR):-5]
                              for f in glob.glob(meta.JSON_DIR + "*.json")])
    txt_file_names  = sorted([f[len(meta.GIVEN_DIR):-4]
                              for f in glob.glob(meta.GIVEN_DIR + "*.txt")])

    with open(meta.PROCESSED_DIR + "map.csv", "w+") as map_file:
        writer = csv.writer(map_file, delimiter=',')
        writer.writerow(['index', 'tx_id'])

    for index in json_file_names:
        tx_dir = meta.PROCESSED_DIR + index + '/'

        json_file_path = "{0}{1}.json".format(meta.JSON_DIR, index)

        with open(json_file_path) as json_file:
            tx_data = json.load(json_file)
            tx_id = tx_data["_id"]["$oid"]

        if tx_id in txt_file_names:
            print("Processing file: {0}.txt".format(index))

            # Create directory for tx dir
            os.system("mkdir {0}{1}".format(meta.PROCESSED_DIR, index))

            # Copy the txt file into the tx dir
            os.system("cp {0}/{1}.txt {2}/{1}.txt".format(meta.GIVEN_DIR, tx_id, tx_dir))

            # Create a file to later map index with tx_id
            with open(meta.PROCESSED_DIR + "map.csv", "a+") as map_file:
                writer = csv.writer(map_file, delimiter=',')
                writer.writerow([index, tx_id])

            with open(meta.GIVEN_DIR + tx_id + ".txt") as txt_file:
                count_fslash = 0
                '''
                    count_fslash = 2: reading parameters
                    count_fslash = 4: reading vin
                    count_fslash = 6: reading vout
                '''

                input_lines  = []
                output_lines = []

                for line in txt_file:
                        if len(line) == 1: # blank line
                            continue

                        if line[0] == '/':
                            count_fslash += 1
                        elif count_fslash == 2:
                            process_param_line(tx_id, tx_dir, line)
                        elif count_fslash == 4:
                            input_lines.append(line)
                        elif count_fslash == 6:
                            output_lines.append(line)

            process_input_lines(tx_dir, input_lines)
            process_output_lines(tx_dir, output_lines)
