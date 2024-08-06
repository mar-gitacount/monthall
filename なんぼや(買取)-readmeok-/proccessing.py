import multiprocessing

# 利用可能なCPUコア数を取得する
num_cores = multiprocessing.cpu_count()
print("利用可能なCPUコア数:", num_cores)
