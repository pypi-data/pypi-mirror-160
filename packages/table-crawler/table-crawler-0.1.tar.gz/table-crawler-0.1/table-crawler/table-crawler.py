import os
import pandas as pd
import re
import requests
from opencc import OpenCC
import openpyxl


def exist():
    file_list = ['_'.join(item.split('.')[0].split('_')[:-1]) for item in os.listdir('data')]
    file_set = set()
    for item in set(file_list):
        if file_list.count(item) <= 3:
            file_set.add(item)
    return file_set


def crawler_html(url):
    html = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.119 Safari/537.36'})
    html = html.content.decode('utf-8', 'ignore')
    return html


def read_list_names():
    data = []
    file = open('zhwiki-latest-pages-articles-multistream-index.txt')
    for line in file:
        query = line.strip().split(':')[-1]
        if '列表' in query:
            data.append(query)
    print('before: {}'.format(len(data)))

    exist_queries = exist()
    data = list(set(data) - exist_queries)
    print('after: {}'.format(len(data)))
    return data


def clean(df):
    columns = list(df.columns)
    if '备注' in set(columns):
        df = df.drop(columns=['备注'])
    for col in columns:
        if 'Unnamed' in col:
            df = df.rename(columns={col: ''})
        elif isinstance(col, tuple):
            length = len(col)
            df = df.drop(index=list(range(length - 1)))
            break
        elif '[' in col:
            new_col = re.sub('\[.+\]', '', col)
            df = df.rename(columns={col: new_col})
        elif len(col) > 100:
            df = df.rename(columns={col: col.split('.')[0]})
    return df


def crawler():
    query_pool = read_list_names()
    for query in query_pool:
        url = 'http://zh.wikipedia.org/wiki/' + query
        print(url)
        html = crawler_html(url)
        try:
            html_data = pd.read_html(html, attrs={'class': 'wikitable'})
        except:
            continue

        for i, item in enumerate(html_data):
            table_data = pd.DataFrame(item)
            try:
                table_data = clean(table_data)
            except:
                pass
            table_data.to_csv('tables/{}_{}.csv'.format(query.replace('/', '_'), i), index=False)


def tradition_to_simple(df):
    if df is None:
        return None
    cc = OpenCC('t2s')
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            df.iat[i, j] = cc.convert(str(df.iat[i, j]))
    new_df_columns = []
    for item in df.columns:
        new_df_columns.append(cc.convert(str(item)))
    df.columns = new_df_columns
    return df


def remove_upprintable_chars(s):
    """移除所有不可见字符"""
    return ''.join(x for x in s if x.isprintable())


# 去除大括号、中括号、小括号、尖括号中的内容
# 注意：因为muti_index_process()函数中会生成小括号，本函数必须在其前面运行！
def brackets_remove(df):
    if df is None:
        return None
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            df.iat[i, j] = remove_upprintable_chars(re.sub(u"{.*?}|\\[.*?]|<.*?>", "", str(df.iat[i, j])))
            # 这里我们认为-的效果和没有是一样的，并且去掉？和nan
            df.iat[i, j] = df.iat[i, j].replace('？', '').replace('nan', '')
            if df.iat[i, j] == '' or df.iat[i, j] == '－':
                df.iat[i, j] = None

    new_df_columns = []
    for item in df.columns:
        new_df_columns.append(re.sub(u"{.*?}|\\[.*?]|<.*?>", "", str(item)))
    df = df[new_df_columns]
    return df


def empty_column_remove(df, if_strict=False):
    if df is None:
        return None
    try:
        # 删除有效内容过少的列
        delete_index_list = []
        for df_index, row in df.iteritems():
            if float(sum(row.isnull() == True)) / (0.01 + df.shape[0]) > 0.3:
                delete_index_list.append(df_index)
        df.drop(delete_index_list, axis=1, inplace=True)

        # 删除有效内容过少的行
        delete_index_list = []
        for df_index, row in df.iterrows():
            if float(sum(row.isnull() == True)) / (0.01 + df.shape[1]) > 0.3:
                delete_index_list.append(df_index)
        df.drop(delete_index_list, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # 删除索引是数字或是与其他列相同的列
        delete_index_list = []
        for df_index, row in df.iteritems():
            if str(df_index).isdigit() or 'Unnamed' in str(df_index) \
                    or '参考' in str(df_index) or '来源' in str(df_index) or '#' in str(df_index):
                delete_index_list.append(df_index)
        df.drop(delete_index_list, axis=1, inplace=True)

        # 删除一行内容都相同的行
        delete_index_list = []
        for df_index, row in df.iterrows():
            flag = True
            for i in range(df.shape[1] - 1):
                if row[i] != row[i + 1]:
                    flag = False
                    break
            if flag:
                delete_index_list.append(df_index)
        df.drop(delete_index_list, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # 删除一列内容都相同的列
        delete_index_list = []
        for df_index, row in df.iteritems():

            flag = True
            for i in range(df.shape[0] - 1):
                if row[i] != row[i + 1]:
                    flag = False
                    break
            if flag:
                delete_index_list.append(df_index)
        df.drop(delete_index_list, axis=1, inplace=True)

        if df.empty or df.shape[1] == 1 or df.shape[0] <= 2:
            if if_strict:
                return None
            else:
                return df
        else:
            return df
    except Exception as e:
        print(e)
        return None


# 判断重复表头，并将两个重复的表头合并
def muti_index_process(df, if_strict=False):
    if df is None:
        return None
    flag = False
    for i in range(df.shape[1]):
        if str(df.iloc[[0], [i]].values[0][0]) == str(df.columns[i]):
            flag = True
            break
    if flag:
        index_list = []
        for i in range(df.shape[1]):
            if str(df.iloc[[0], [i]].values[0][0]) != str(df.columns[i]):
                index_list.append(str(df.columns[i]) + '(' + str(df.iloc[[0], [i]].values[0][0]) + ')')
            else:
                index_list.append(str(df.columns[i]))
        df.columns = index_list
        df.drop([0], axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)

    if df.empty or df.shape[1] == 1 or df.shape[0] <= 2:
        if if_strict:
            return None
        else:
            return df
    else:
        return df


# 对第一行进行检验
def first_column_check(df):
    if df is None:
        return None
    if str(df.iat[0, 0]).isdigit() or str(df.iat[1, 0]).isdigit() \
            or '.' in str(df.iat[0, 0]) or '.' in str(df.iat[0, 0]) or str(df.iat[0, 0]) == '':
        new_index_list = []
        for item in df.columns[1:]:
            new_index_list.append(item)
        new_index_list.append(df.columns[0])
        df = df[new_index_list]
    return df


# 对表头做校验
def index_check(df):
    if df is None:
        return None
    new_index_list = []
    if '名' in df.columns[0] or '标题' in df.columns[0]:
        return df
    if '日期' in df.columns[0] or '时间' in df.columns[0] or '年' in df.columns[0] or '数' in df.columns[0]:
        for item in df.columns[1:]:
            new_index_list.append(item)
        new_index_list.append(df.columns[0])
        df = df[new_index_list]
    for df_index in df.columns:
        if '名' in df_index or '标题' in df_index:
            new_index_list = [df_index]
            for item in df.columns:
                if item != df_index:
                    new_index_list.append(item)
            df = df[new_index_list]
            return df
    return df


def table_crawler(website: str, query: str, option: str, csv_path='tables/', origin=False, json_orient="columns"):
    cc = OpenCC('t2s')
    html = crawler_html(website + query)
    simple_query = cc.convert(query)

    try:
        html_data = pd.read_html(html, attrs={'class': 'wikitable'})
    except Exception as e:
        print(e)
        return
    table_list = []
    for i, item in enumerate(html_data):
        table_data = pd.DataFrame(item)
        # 原始数据
        if origin:
            print(table_data)
        try:
            table_list.append(clean(table_data))
        except:
            table_list.append(table_data)

    # my processes for table_list

    # 如果列表表头是元组，则取第一项作为表头
    for item in table_list:
        index_list = []
        for item_index in item.columns:
            if isinstance(item_index, tuple):
                item_index = str(item_index[0])
            index_list.append(item_index)
        item.columns = index_list

    last_item_columns = []
    union_item_list = []
    res_list = []

    # 表格的合并
    for item in table_list:

        # 繁体转化为简体
        item = tradition_to_simple(item)

        # 对能够合并的表格进行合并，此处设置相似度大于70%进行合并
        union_item_columns = list(set(item.columns) & set(last_item_columns))
        similary_value = 2.0 * float(len(union_item_columns)) / (len(item.columns) + len(last_item_columns))
        # print(similary_value)
        if similary_value > 0.7:
            union_item_list.append(item)
        else:
            if len(union_item_list) != 0:
                res_list.append(union_item_list)
            union_item_list = [item]
        last_item_columns = item.columns
    if len(union_item_list) != 0:
        res_list.append(union_item_list)
    table_list = []
    for item in res_list:
        table_list.append(pd.concat(item, ignore_index=True))

    # 对表格进行清洗
    clean_table_list = []
    for item in table_list:
        # print(item)
        # 去除其中的中括号、大括号、尖括号
        new_item = brackets_remove(item)
        new_item = empty_column_remove(new_item)
        new_item = muti_index_process(new_item)
        new_item = first_column_check(new_item)
        new_item = index_check(new_item)
        if new_item is not None:
            clean_table_list.append(new_item)
    table_list = clean_table_list

    # 出口处理
    if len(table_list) == 0:
        print("No table found with query: " + query + " !")
    else:
        if option == 'stdout':
            print("共计" + str(len(table_list)) + "张表格： ")
            for item in table_list:
                print(item)
        elif option == 'csv':
            if len(table_list) == 1:
                table_list[0].to_excel(csv_path + str(simple_query).replace('/', '_') + '.csv', encoding='utf-8',
                                       index=False)
            else:
                i = 0
                for item in table_list:
                    i += 1
                    item.to_excel(csv_path + str(simple_query).replace('/', '_') + '_' + str(i) + '.csv',
                                  encoding='utf-8', index=False)
        elif option == 'excel':
            if len(table_list) == 1:
                table_list[0].to_excel(csv_path + str(simple_query).replace('/', '_') + '.xlsx', encoding='utf-8',
                                       index=False)
            else:
                i = 0
                for item in table_list:
                    i += 1
                    item.to_excel(csv_path + str(simple_query).replace('/', '_') + '_' + str(i) + '.xlsx',
                                  encoding='utf-8', index=False)
        elif option == 'json':
            if len(table_list) == 1:
                table_list[0].to_json(csv_path + str(simple_query).replace('/', '_') + '.json', force_ascii=False,
                                      orient=json_orient)
            else:
                i = 0
                for item in table_list:
                    i += 1
                    item.to_json(csv_path + str(simple_query).replace('/', '_') + '_' + str(i) + '.json',
                                 force_ascii=False, orient=json_orient)


if __name__ == '__main__':
    table_crawler('http://zh.wikipedia.org/wiki/', '古巴机场列表', option='json', csv_path='./', origin=True,
                  json_orient="columns")
