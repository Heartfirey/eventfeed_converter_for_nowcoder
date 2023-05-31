import pandas as pd

# 读取Excel文件
df = pd.read_excel('info.xls')

# 处理团队信息数据
team_df = df[['团队ID', '昵称', '默认学校']].rename(columns={'团队ID': 'team_id', '昵称': 'team_name', '默认学校': 'name'})
team_df['group_ids'] = 3

# 处理学校信息数据
school_df = pd.DataFrame({'id': range(1, len(df['默认学校'].unique())+1), 
                          'name': df['默认学校'].unique(), 
                          'formal_name': df['默认学校'].unique()})

# 将处理后的数据分别写入CSV文件
school_df.to_csv('school_info.csv', index=False)

# 根据学校名称添加对应的ID
school_id_mapping = school_df[['name', 'id']]
team_df = pd.merge(team_df, school_id_mapping, on='name', how='left')
team_df = team_df.drop('name', axis=1).rename(columns={'id': 'organizations_id'})

# 将处理后的团队信息数据写入CSV文件
team_df.to_csv('team_info.csv', index=False)