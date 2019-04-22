import csv
import os

import meta


class Transaction:
    def __init__(self, tx_index):
        self.tx_dir = meta.get_tx_dir(tx_index)

    def load_model1_result(self):
        with open("{0}model1/summary.csv".format(self.tx_dir), 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                self.model1_summary = line

        self.model1_selected = []

        with open("{0}model1/selected.csv".format(self.tx_dir), 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                self.model1_selected.append(line)

    def load_params(self):
        with open("{0}params.csv".format(self.tx_dir), 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                self.params = line

    def load_inputs(self):
        self.utxo_set = []

        with open("{0}txinput.csv".format(self.tx_dir), 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                self.utxo_set.append(line)

    def load_outputs(self):
        self.outputs = []

        with open("{0}txoutput.csv".format(self.tx_dir), 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                self.outputs.append(line)

    def load_model_summary(self, model_name):
        summary_file_path = "{0}{1}/summary.csv".format(self.tx_dir, model_name)

        if not os.path.isfile(summary_file_path):
            return None

        with open(summary_file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            for line in csv_reader:
                model_summary = line

            return model_summary

    def load_model_selected(self, model_name):
        summary_file_path = "{0}{1}/selected.csv".format(self.tx_dir, model_name)

        if not os.path.isfile(summary_file_path):
            return None

        with open(summary_file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')

            selected = []

            for line in csv_reader:
                selected.append(line)

            return selected
