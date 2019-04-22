import csv
import os

import meta
from transaction import Transaction
import util


def summarize():
    tx_indices = meta.get_all_tx_indices()

    for tx_index in tx_indices:
        tx_dir     = meta.get_tx_dir(tx_index)
        result_dir = tx_dir + "realtx"

        if not os.path.isdir(result_dir):
            os.makedirs(result_dir)

        tx = Transaction(tx_index)
        tx.load_params()
        tx.load_inputs()
        tx.load_outputs()

        n_out = len(tx.outputs)
        alpha = float(tx.params['fee_rate'])

        n_selected = 0
        selected   = [0 for i in range(len(tx.utxo_set))]

        for i in range(len(tx.utxo_set)):
            if int(tx.utxo_set[i]['choosen']) != 0:
                n_selected += 1
                selected[i] = 1

        change_val = int(tx.params['change_value'])
        tx_size    = n_selected * 148 + n_out * 34 + (34 if change_val > 0 else 0)
        tx_fee     = round(alpha * tx_size)

        # Summary file
        summary_file_path = "{0}/summary.csv".format(result_dir)

        with open(summary_file_path, 'w+') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(meta.SUMMARY_FIELDS)

            values               = {}
            values['n_selected'] = n_selected
            values['tx_size']    = tx_size
            values['tx_fee']     = tx_fee
            values['change_val'] = change_val

            csv_writer.writerow(util.filter_dict(values, meta.SUMMARY_FIELDS))

        # Selected file
        selected_file_path = "{0}/selected.csv".format(result_dir)

        selected_file_fields = [
            'index',
            'value',
            'confirmations',
            'vout',
            'tx_id'
        ]

        with open(selected_file_path, 'w+') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(selected_file_fields)

            for i in range(len(selected)):
                if selected[i]:
                    values = util.filter_dict(tx.utxo_set[i], selected_file_fields)
                    csv_writer.writerow(values)
