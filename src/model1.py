import csv
import glob
import os
import sys

import mosek

import meta
import util
from transaction import Transaction

model_name = "model1"


# ===== BEGIN MOSEK SEGMENT =====

# Since the actual value of Infinity is ignored, we define it solely
# for symbolic purposes:
inf = 0.0

def streamprinter(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def mosek_solve():
    # LOAD VARIABLES
    n_utxo = len(tx.utxo_set)
    n_out  = len(tx.outputs)
    U      = tx.utxo_set
    O      = tx.outputs
    Vu     = [int(U[j]['value']) for j in range(n_utxo)]
    Vo     = [int(O[j]['value']) for j in range(n_out)]
    Su     = [int(U[j]['size'])  for j in range(n_utxo)]
    So     = [int(O[j]['size'])  for j in range(n_out)]

    Ms     = int(tx.params['max_size'])
    alpha  = float(tx.params['fee_rate'])
    T      = int(tx.params['dust_threshold'])
    eps    = int(tx.params['min_change_output'])
    beta   = int(tx.params['change_output_size'])

    # Sum of input values
    sum_Vu = sum(Vu[j] for j in range(n_utxo))
    # Sum of output values
    sum_Vo = sum(Vo[j] for j in range(n_out))
    # Sum of output size
    sum_So = sum(So[j] for j in range(n_out))
    # Maximum change value = sum_Vu - sum_Vo
    Mc = sum_Vu - sum_Vo
    # Minimum utxo
    # Mc = min(Vu)

    # SOLVE
    # Make mosek environment
    with mosek.Env() as env:
        # Create a task object
        with env.Task(0, 0) as task:
            # Attach a log stream printer to the task
            task.set_Stream(mosek.streamtype.log, streamprinter)

            # Bound keys for constraints
            bkc = [
                mosek.boundkey.ra,
                mosek.boundkey.fx,
                mosek.boundkey.up
            ]

            # Bound values for constraints
            blc = [0.0,         sum_Vo + alpha * sum_So, -inf]
            buc = [Ms - sum_So, sum_Vo + alpha * sum_So, eps]


            # Bound keys for variables
            bkx = [mosek.boundkey.ra for j in range(n_utxo)] # l <= x <= u
            bkx.append(mosek.boundkey.ra)
            bkx.append(mosek.boundkey.ra)


            # Bound values for variables
            blx = [0.0 for j in range(n_utxo)] # x_i
            blx.append(0.0)                    # t
            blx.append(0.0)                    # z_v
            bux = [1.0 for j in range(n_utxo)]
            bux.append(1.0)
            bux.append(Mc)

            # Objective coefficients
            c = [Su[j] for j in range(n_utxo)]
            c.append(beta)
            c.append(0.0)

            # Below is the sparse representation of the A
            # matrix stored by column.
            asub = [
                [0, 1] for j in range(n_utxo)
            ]
            asub.append([0, 1, 2])
            asub.append([1, 2])

            aval = [
                [Su[j], Vu[j] - alpha * Su[j]] for j in range(n_utxo)
            ]
            aval.append([beta, -alpha * beta, -Mc])
            aval.append([-1.0, 1.0])


            # numcon and numvar
            numcon = len(bkc)
            numvar = len(bkx)

            assert numvar == n_utxo + 2
            assert numcon == 3

            # Append 'numcon' empty constraints.
            # The constraints will initially have no bounds.
            task.appendcons(numcon)
            # Append 'numvar' variables.
            # The variables will initially be fixed at zero (x=0).
            task.appendvars(numvar)

            for j in range(numvar):
                # Set the linear term c_j in the objective.
                task.putcj(j, c[j])

                # Set the bounds on variable j
                # blx[j] <= x_j <= bux[j]
                task.putvarbound(j, bkx[j], blx[j], bux[j])

                # Input column j of A
                task.putacol(
                    j,       # Variable (column) index.
                    asub[j], # Row index of non-zeros in column j.
                    aval[j]  # Non-zero Values of column j.
                )


            task.putconboundlist(range(numcon), bkc, blc, buc)

            # Input the objective sense (minimize/maximize)
            task.putobjsense(mosek.objsense.minimize)

            # Define variables to be integers
            task.putvartypelist(
                [j for j in range(n_utxo + 1)],
                [mosek.variabletype.type_int for j in range(n_utxo + 1)]
            )

            # Set max solution time
            task.putdouparam(mosek.dparam.mio_max_time, 200.0);

            # Solve the problem
            task.optimize()

            # Print a summary containing information
            # about the solution for debugging purposes
            task.solutionsummary(mosek.streamtype.msg)
            prosta = task.getprosta(mosek.soltype.itg)
            solsta = task.getsolsta(mosek.soltype.itg)

            # Output a solution
            xx = [0.] * numvar
            task.getxx(mosek.soltype.itg, xx)

            if solsta in [mosek.solsta.integer_optimal]:
                print("Optimal solution: %s" % xx)
                return xx
            elif solsta == mosek.solsta.prim_feas:
                print("Feasible solution: %s" % xx)
            elif mosek.solsta.unknown:
                if prosta == mosek.prosta.prim_infeas_or_unbounded:
                    print("Problem status Infeasible or unbounded.\n")
                elif prosta == mosek.prosta.prim_infeas:
                    print("Problem status Infeasible.\n")
                elif prosta == mosek.prosta.unkown:
                    print("Problem status unkown.\n")
                else:
                    print("Other problem status.\n")
            else:
                print("Other solution status")


# ===== END MOSEK SEGMENT =====


def solve(tx_index):
    # Load tx
    global tx
    tx = Transaction(tx_index)
    tx.load_params()
    tx.load_inputs()
    tx.load_outputs()

    # LOAD VARIABLES
    global n_utxo, n_out
    n_utxo = len(tx.utxo_set)
    n_out  = len(tx.outputs)

    global U, O, Vu, Vo, Su, So
    U      = tx.utxo_set
    O      = tx.outputs
    Vu     = [int(U[j]['value']) for j in range(n_utxo)]
    Vo     = [int(O[j]['value']) for j in range(n_out)]
    Su     = [int(U[j]['size'])  for j in range(n_utxo)]
    So     = [int(O[j]['size'])  for j in range(n_out)]

    global Ms, alpha, T, eps, beta
    Ms     = int(tx.params['max_size'])
    alpha  = float(tx.params['fee_rate'])
    T      = int(tx.params['dust_threshold'])
    eps    = int(tx.params['min_change_output'])
    beta   = int(tx.params['change_output_size'])

    global sum_Vu, sum_Vo, sum_So, Mc
    sum_Vu = sum(Vu[j] for j in range(n_utxo))
    sum_Vo = sum(Vo[j] for j in range(n_out))
    sum_So = sum(So[j] for j in range(n_out))
    Mc     = sum_Vu - sum_Vo

    # Solve with mosek
    try:
        result = mosek_solve()
    except mosek.Error as e:
        print("ERROR: %s" % str(e.errno))
        if e.msg is not None:
            print("\t%s" % e.msg)
            sys.exit(1)
    except:
        import traceback
        traceback.print_exc()
        sys.exit(1)

    if result == None:
        return False

    # Evaluate result
    selected   = [round(result[j]) for j in range(n_utxo)]

    n_selected = sum(selected[j] for j in range(n_utxo))
    change_val = round(result[-1])
    tx_size    = n_selected * 148 + n_out * 34 + (34 if change_val > 0 else 0)
    tx_fee     = round(alpha * tx_size)

    # Write result to csv file
    result_dir = meta.get_tx_dir(tx_index) + model_name

    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

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

    return True


def run():
    tx_indices = meta.get_all_tx_indices()

    log_file = "model1-log.txt"

    os.system("rm " + meta.PROCESSED_DIR + log_file)

    with open(meta.PROCESSED_DIR + log_file, "w+") as log_file:
        for tx_index in tx_indices:
            print("\n\n=================================================\n\n")
            print("Solving transaction {0}".format(tx_index))

            if solve(tx_index):
                log_file.write("Tx {0}: Solved\n".format(tx_index))
            else:
                log_file.write("Tx {0}: Unsolved\n".format(tx_index))
