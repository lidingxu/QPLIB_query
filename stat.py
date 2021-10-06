import pandas as pd
from enum import Enum
import os
import shutil

class ProblemType(Enum):
    Discrete = 0
    Continuous = 1

class ContRelaxType(Enum):
    QP = 0
    QCP = 1
    QCQP = 2

df = pd.read_csv('instancedata.csv')
lp_dir_path = os.getcwd() + "/lp"
mps_dir_path = os.getcwd() + "/mps"
continuous_dir_path = os.getcwd() + "/Continuous"
discrete_dir_path = os.getcwd() + "/Discrete"



def Stat(name):
    return {"name": name, "problem_type": ProblemType.Continuous, "cont_relax_type": ContRelaxType.QCQP, "convex": True, "obj": 0}


discrete_set=[]
continuous_set=[]
discrete_benchmark = []
discrete_df = pd.DataFrame()
continuous_benchmark = []
continuous_df = pd.DataFrame()
for row_ind in range(len(df)):
    row = df.iloc[row_ind]

    row_stat =  Stat(row["name"])
    row_stat["obj"] = row["solobjvalue"]
    row_stat["convex"]= row["convex"]

    continous_var = row["probtype"][1] == "C"
    row_stat["problem_type"] = ProblemType.Continuous if continous_var else ProblemType.Discrete


    linear_obj = row["probtype"][0] == "L"
    linear_constraints = row["probtype"][2] == "L"
    if linear_constraints:
        row_stat["cont_relax_type"] = ContRelaxType.QP
    elif linear_obj:
        row_stat["cont_relax_type"] = ContRelaxType.QCP
    else:
        row_stat["cont_relax_type"] = ContRelaxType.QCQP

    if not row_stat["convex"]:
        if row_stat["problem_type"] == ProblemType.Continuous:
            continuous_benchmark.append(row_stat)
            continuous_df = continuous_df.append(row)
            continuous_set.append(row["name"])
            #print(row["name"], len(row["name"]))
        elif row_stat["problem_type"] == ProblemType.Discrete:
            discrete_benchmark.append(row_stat)
            discrete_df = discrete_df.append(row)
            discrete_set.append(row["name"])

lp_instances = os.listdir(lp_dir_path)
mps_instances = os.listdir(mps_dir_path)
mps_instances =  sorted(mps_instances)
lp_instances =  sorted(lp_instances)

#print(mps_instances)
#print(continuous_set)
# copy nonconvex lp, mps instance to discrete/continuous set
for lp_instance in lp_instances:
    #print(lp_instance[:-4])
    if lp_instance[:-3] in continuous_set:
        shutil.copy2(lp_dir_path + "/" + lp_instance, continuous_dir_path + "/lp")
    elif lp_instance[:-3] in discrete_set:
        shutil.copy2(lp_dir_path + "/" + lp_instance, discrete_dir_path + "/lp")
    
for i, mps_instance in enumerate(mps_instances):
    print(i, mps_instance, mps_instance[:-4], mps_instance[:-4] in continuous_set)
    if mps_instance[:-4] in continuous_set:
        shutil.copy2(mps_dir_path + "/" + mps_instance, continuous_dir_path + "/mps")
    elif mps_instance[:-4] in discrete_set:
        shutil.copy2(mps_dir_path + "/" + mps_instance, discrete_dir_path + "/mps")
# write dataframes and benchmarks
discrete_df.to_csv("nonconvex_discrete_data.csv")
continuous_df.to_csv("nonconvex_continous_data.csv")



print(continuous_df)