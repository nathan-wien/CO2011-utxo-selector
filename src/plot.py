import math
import matplotlib.pyplot as plt

import meta
from transaction import Transaction

model_names = [
    'model1',
    'model2-1',
    'model2-2',
    'model2-3',
    'model2-4',
    'realtx'
]

model_names_full = [
    'model1',
    'model2-1 (gamma = 10\%)',
    'model2-2 (gamma = 25\%)',
    'model2-3 (gamma = 40\%)',
    'model2-4 (gamma = 50\%)',
    'realtx'
]


def plot_tx_size():
    all_total_tx_size = [total_tx_size(model_name) for model_name in model_names]

    plt.bar(x      = model_names,
            height = all_total_tx_size,
            label  = 'Tx Size',
            color  = 'blue')

    plt.title("Transaction size")
    plt.legend()
    plt.show()


def plot_n_selected():
    all_total_n_selected = [total_n_selected(model_name) for model_name in model_names]

    plt.bar(x            = model_names,
            height       = all_total_n_selected,
            label        = '# Selected UTXOs',
            color        = 'red')

    plt.title("# Selected UTXOs")
    plt.legend()
    plt.show()


def plot_avg_utxo_val():
    all_avg = [average_tx_val(model_name)[0] for model_name in model_names]

    plt.bar(x      = model_names,
            height = all_avg,
            label  = 'average value',
            color  = 'green')

    plt.title("Average Selected Input Value")
    plt.legend()
    plt.show()


def plot_sd_utxo_val():
    all_sd = [average_tx_val(model_name)[1] for model_name in model_names]

    plt.bar(x      = model_names,
            height = all_sd,
            label  = 'standard deviation',
            color  = 'orange')

    plt.title("Standard Deviation of Selected Input Value")
    plt.legend()
    plt.show()


def total_tx_size(model_name):
    tx_indices = meta.get_all_tx_indices()

    total_size = 0

    for tx_index in tx_indices:
        tx      = Transaction(tx_index)
        summary = tx.load_model_summary(model_name)

        if summary is None:
            summary = tx.load_model_summary('model1')

        total_size += int(summary['tx_size'])

    return total_size


def total_n_selected(model_name):
    tx_indices = meta.get_all_tx_indices()

    total_n_selected = 0

    for tx_index in tx_indices:
        tx      = Transaction(tx_index)
        summary = tx.load_model_summary(model_name)

        if summary is None:
            summary = tx.load_model_summary('model1')

        total_n_selected += int(summary['n_selected'])

    return total_n_selected


def average_tx_val(model_name):
    tx_indices = meta.get_all_tx_indices()

    total_value = 0
    utxo_count  = 0

    for tx_index in tx_indices:
        tx      = Transaction(tx_index)
        selected = tx.load_model_selected(model_name)

        if selected is None:
            selected = tx.load_model_selected('model1')

        for utxo in selected:
            total_value += int(utxo['value'])
            utxo_count  += 1

    avg = total_value / utxo_count
    sd  = 0

    for tx_index in tx_indices:
        tx      = Transaction(tx_index)
        selected = tx.load_model_selected(model_name)

        if selected is None:
            selected = tx.load_model_selected('model1')

        for utxo in selected:
            sd += (int(utxo['value']) - avg) ** 2

    sd /= utxo_count
    sd  = math.sqrt(sd)

    return [avg, sd]
