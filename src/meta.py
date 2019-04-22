import csv
import glob


# GLOBAL VARIABLES

# Directories
DATASET_DIR   = "../dataset/"
JSON_DIR      = DATASET_DIR + "json/"
GIVEN_DIR     = DATASET_DIR + "given/"
PROCESSED_DIR = DATASET_DIR + "processed/"


# Fields of csv files
# Input files
PARAM_FIELDS = [
    'tx_id',
    'out_value',
    'max_size',
    'fee_rate',
    'dust_threshold',
    'min_change_output',
    'change_output_size',
    'has_change_output',
    'change_value'
]

TX_IN_FIELDS = [
    'index',
    'size',
    'value',
    'confirmations',
    'vout',
    'choosen',
    'tx_id'
]

TX_OUT_FIELDS = [
    'index',
    'size',
    'value'
]

# Output files
SUMMARY_FIELDS = [
    'n_selected',
    'tx_size',
    'tx_fee',
    'change_val'
]

SELECTED_FIELDS = [
    'index',
    'value',
    'confirmations',
    'vout',
    'tx_id'
]

# GLOBAL FUNCTIONS
def get_all_tx_indices():
    return sorted([d[len(PROCESSED_DIR):-1]
                   for d in glob.glob("{0}/*/".format(PROCESSED_DIR))])

def get_tx_map():
    tx_map = {}

    with open(PROCESSED_DIR + "map.csv", 'r') as mapfile:
        csv_reader = csv.DictReader(mapfile, delimiter=',')

        for row in csv_reader:
            tx_map[row['tx_id']] = row['index']

    return tx_map

def get_tx_dir(tx_index):
    return PROCESSED_DIR + tx_index + '/'
