import os

sey=1.50
with open(f"list_of_simulations_SEY{sey:.2f}.txt","r") as fid:
    simulations = fid.readlines()


current_dir = os.getcwd()
for sim_line in simulations:
    sim = sim_line.strip()
    os.chdir(current_dir + f"/simulations_SEY{sey:.2f}/" + sim)
    os.system("sbatch job.job")
    os.chdir(current_dir)
