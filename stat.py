import pandas as pd
from enum import Enum
import os
import shutil

class IntType(Enum):
    Discrete = 0
    Continuous = 1

class ProblemType(Enum):
    DiscreteConvex = 0
    DiscreteNonconvex = 1
    ContinuousNonconvex = 2

class ContRelaxType(Enum):
    QP = 0
    QCP = 1
    QCQP = 2

df = pd.read_csv('instancedata.csv')
lp_dir_path = os.getcwd() + "/lp"
all_dir_path = os.getcwd() + "/QPLib_All"
discreteconvex_dir_path = os.getcwd() + "/QPLib_DiscreteConvex"
continuousnonconvex_dir_path = os.getcwd() + "/QPLib_ContinuousConvex"
discretenonconvex_dir_path = os.getcwd() + "/QPLib_DiscreteNonconvex"



def Stat(name):
    return {"name": name, "problem_type": ProblemType.DiscreteConvex, "cont_relax_type": ContRelaxType.QCQP, "convex": True, "obj": 0}

keys = ["discreteconvex", "continuousnonconvex", "discretenonconvex"]
data = {"discreteconvex":([],[], pd.DataFrame(), "QPLib_DiscreteConvex"),
        "continuousnonconvex":([],[], pd.DataFrame(), "QPLib_ContinuousNononvex"),
        "discretenonconvex":([],[], pd.DataFrame(), "QPLib_DiscreteNonconvex")}
for row_ind in range(len(df)):
    row = df.iloc[row_ind]

    row_stat =  Stat(row["name"])
    row_stat["obj"] = row["solobjvalue"]
    row_stat["convex"]= row["convex"]

    continous_var = row["probtype"][1] == "C"
    row_stat["problem_type"] = IntType.Continuous if continous_var else IntType.Discrete


    linear_obj = row["probtype"][0] == "L"
    linear_constraints = row["probtype"][2] == "L"
    if linear_constraints:
        row_stat["cont_relax_type"] = ContRelaxType.QP
    elif linear_obj:
        row_stat["cont_relax_type"] = ContRelaxType.QCP
    else:
        row_stat["cont_relax_type"] = ContRelaxType.QCQP

    if not row_stat["convex"] and row_stat["problem_type"] == IntType.Continuous:
        data["continuousnonconvex"][1].append(row_stat)
        data["continuousnonconvex"][2]._append(row)
        data["continuousnonconvex"][0].append(row["name"])
        #print(row["name"], len(row["name"]))
    elif not row_stat["convex"] and row_stat["problem_type"] == IntType.Discrete:
        data["discreteconvex"][1].append(row_stat)
        data["discreteconvex"][2]._append(row)
        data["discreteconvex"][0].append(row["name"])
    elif not row_stat["convex"] and row_stat["problem_type"] == IntType.Discrete:
        data["discretenonconvex"][1].append(row_stat)
        data["discretenonconvex"][2]._append(row)
        data["discretenonconvex"][0].append(row["name"])

lp_instances = os.listdir(lp_dir_path)
lp_instances =  sorted(lp_instances)

#print(mps_instances)
#print(continuous_set)
# copy nonconvex lp, mps instance to discrete/continuous set
for key in keys:
    datadir = os.getcwd() + "/" + "lp2" + "/" + data[key][3]
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    for lp_instance in lp_instances:
        if lp_instance[:-3] in data[key][0]:
            shutil.copy2(lp_dir_path + "/" + lp_instance,  datadir)
    # write dataframes and benchmarks
    data[key][2].to_csv( data[key][3] +  ".csv")
