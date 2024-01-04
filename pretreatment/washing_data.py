import os
import glob
import pandas as pd

PATH_ORIGIN = "data/training_set"
PATH_NORMAL = "data/training_set_normal"


# 获取所有txt文件的路径
file_paths = glob.glob(os.path.join(PATH_ORIGIN, '*.txt'))

# 创建三个空的DataFrame，用于保存电影的评价数量、平均评分和评分的方差
df_counts = pd.DataFrame(columns=['MovieID', 'Count'])
df_means = pd.DataFrame(columns=['MovieID', 'Mean'])
df_vars = pd.DataFrame(columns=['MovieID', 'Variance'])

# 遍历每个txt文件
for file_path in file_paths:
    # 从文件名中获取MovieID
    movie_id = os.path.basename(file_path).split('.')[0].replace('mv_', '')
    # 打开并读取文件
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 创建一个新的txt文件，用于保存规范化后的数据
        with open(os.path.join(PATH_NORMAL, f'mv_{movie_id}.csv'), 'w') as output_file:
            output_file.write("MovieID,CustomerID,Rating,Date\n")
            for line in lines[1:]:  # 跳过第一行，因为第一行是MovieID
                # 这是一个客户ID，评分和日期
                customer_id, rating, date = line.strip().split(',')
                # 检查评分是否在1-5之间
                if not 1 <= float(rating) <= 5:
                    # 如果评分不在1-5之间，用该txt文件的平均评分填充
                    ratings = [float(line.split(',')[1]) for line in lines[1:] if 1 <= float(line.split(',')[1]) <= 5]
                    avg_rating = sum(ratings) / len(ratings) if ratings else 0
                    rating = str(avg_rating)
                # 将这一行数据添加到新的txt文件
                output_file.write(f'{movie_id},{customer_id},{rating},{date}\n')
        df = pd.read_csv(os.path.join(PATH_NORMAL, f'mv_{movie_id}.csv'))
        # 将"Rating"列转换为数值类型
        df["Rating"] = pd.to_numeric(df["Rating"])
    
        # 计算平均评分
        avg_rating = df['Rating'].mean()
    
        # 计算评分的方差
        var_rating = df['Rating'].var()
    
        # 计算电影的评价数量
        count_rating = df['Rating'].count()
    
        # 将统计结果添加到相应的DataFrame
        df_counts = pd.concat([df_counts, pd.DataFrame({'MovieID': [movie_id], 'Count': [count_rating]})], ignore_index=True)
        df_means = pd.concat([df_means, pd.DataFrame({'MovieID': [movie_id], 'Mean': [avg_rating]})], ignore_index=True)
        df_vars = pd.concat([df_vars, pd.DataFrame({'MovieID': [movie_id], 'Variance': [var_rating]})], ignore_index=True)

# 将统计结果保存为新的txt文件
df_counts.to_csv('data/counts.csv', index=False)
df_means.to_csv('data/means.csv', index=False)
df_vars.to_csv('data/vars.csv', index=False)