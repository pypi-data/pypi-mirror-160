from plotly.io import read_json






# fig = read_json("/Users/ardunn/alex/lbl/projects/common_env/dev_codes/matbench/docs_src/static/scaled_errors.json")
fig = read_json("/Users/ardunn/alex/lbl/projects/common_env/dev_codes/matbench/docs_src/static/task_matbench_v0.1_matbench_steels.json")

fig.write_html("./gap_expt.html")
