import datasrc
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line, Scatter, Bar
import numpy as np
import os

# 可靠度分级
real_grade = ['4', '3', '2', '1']
conf_grade = {key: real_grade[0] for key in ['0', '1', '4', '5', '9']}
conf_grade.update({key: real_grade[1] for key in ['A', 'C', 'I', 'M', 'P', 'R', 'U']})
conf_grade.update({key: real_grade[2] for key in ['2', '6']})
conf_grade.update({key: real_grade[3] for key in ['3', '7']})

# 得到数据库中的所有记录并以dataframe形式返回, 方便分析和展示数据
def getdf():
    mysqlite = datasrc.SqliteTool()
    df = mysqlite.db2df()
    print(df)

# 一个使用pyechart的例子
def example():
    size = ['35.5', '36.0', '36.5', '37.5', '38.0', '38.5', '39.0', '40.0']  # 元素必须是str类型，否则不能显示折线
    profit = [132, 123, 129, 134, 134, 99, 140, 119]
    sold_num = [10, 31, 26, 43, 18, 27, 7, 6]
    line1 = Line()
    line1.add_xaxis(size)
    line1.add_yaxis(series_name="利润", y_axis=profit)
    line1.extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}双"),
                                          axisline_opts=opts.AxisLineOpts(
                                              linestyle_opts=opts.LineStyleOpts(color='blue'))))  # 添加一条蓝色的y轴
    line1.set_global_opts(title_opts=opts.TitleOpts(title="利润与销量"),
                          toolbox_opts=opts.ToolboxOpts(is_show=True, feature=opts.ToolBoxFeatureOpts(
                              data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False))),
                          yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}元"),
                                                   axisline_opts=opts.AxisLineOpts(
                                                       linestyle_opts=opts.LineStyleOpts(color="red"))),  # 设置y轴单位和颜色
                          )
    line1.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    line2 = Line().add_xaxis(size).add_yaxis("销量", sold_num, yaxis_index=1)  # 创建一个新的Line对象,并且设置y轴索引，即挂在新建的y轴上
    line1.overlap(line2)  # 将line2叠加在line1图上
    line1.set_colors(["red", "blue"])  # 为了区分两条line，设置不同颜色

    # 显示图表
    line1.render("double_axis_line_chart.html")

# 获取指定时间段的气象数据，考虑到代码的复用定义了这个函数
def spectime(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    mysqlite = datasrc.SqliteTool()
    newend = end[:-2] + ('0' if len(str(int(end[-2:]) + 1)) == 1 else '') + str(int(end[-2:]) + 1)  # 结束日期要加1
    # 执行查询语句
    # print(((stat + ',' + begin), (stat + ',' + newend)))
    mysqlite._cur.execute("select * from datasource where stat_date between ? and ?",
                          ((stat + ',' + begin), (stat + ',' + newend)))
    # 获取查询结果
    result = mysqlite._cur.fetchall()
    # 获取查询的字段名
    columns = [desc[0] for desc in mysqlite._cur.description]
    # 使用查询结果和字段名创建 DataFrame
    df = pd.DataFrame(result, columns=columns)
    # 关闭游标和连接
    mysqlite.close_con()
    return df

# 展示指定站点在指定时间段的露点数据
def showdew(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    df = spectime(stat, begin, end)
    # 准备数据
    x_data = [(iter.split(',')[1]).split('T')[0] + '日' + (iter.split(',')[1]).split('T')[1][:2] + '时'  for iter in df['stat_date']]
    y_data = [int(iter.split(',')[0])/10 for iter in df['dew']]
    conf = [str(int(iter.split(',')[1])) for iter in df['dew']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_date = Line()
    # line_conf = Line()
    line_conf = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_date.add_xaxis(xaxis_data=x_data)
    line_date.add_yaxis(series_name='露点数据(°C)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False), yaxis_index=0)
    line_date.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    line_conf.add_xaxis(xaxis_data=x_data)
    line_conf.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4, label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_date.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n露点数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}°C")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_conf.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_date.overlap(line_conf)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok = True)
    line_date.render(current_directory + '/html/' + 'dew.html')
# showdew('55279099999', '2022-12-03', '2023-12-05')

# 展示指定站点在指定时间段的海平面压力数据
def showslp(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    df = spectime(stat, begin, end)
    # 准备数据
    x_data = [(iter.split(',')[1]).split('T')[0] + '日' + (iter.split(',')[1]).split('T')[1][:2] + '时'  for iter in df['stat_date']]
    y_data = [int(iter.split(',')[0])/10 for iter in df['slp']]
    conf = [str(int(iter.split(',')[1])) for iter in df['slp']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_date = Line()
    # line_conf = Line()
    line_conf = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_date.add_xaxis(xaxis_data=x_data)
    line_date.add_yaxis(series_name='气压数据(hPa)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False), yaxis_index=0)
    line_date.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    line_conf.add_xaxis(xaxis_data=x_data)
    line_conf.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4, label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_date.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n气压数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}hPa")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_conf.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_date.overlap(line_conf)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok = True)
    line_date.render(current_directory + '/html/' + 'slp.html')
# showslp('55279099999', '2022-12-03', '2023-12-05')

# 展示指定站点在指定时间段的温度数据
def showtmp(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    df = spectime(stat, begin, end)
    # 准备数据
    x_data = [(iter.split(',')[1]).split('T')[0] + '日' + (iter.split(',')[1]).split('T')[1][:2] + '时' for iter in
              df['stat_date']]
    y_data = [int(iter.split(',')[0]) / 10 for iter in df['tmp']]
    conf = [str(int(iter.split(',')[1])) for iter in df['tmp']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_date = Line()
    # line_conf = Line()
    line_conf = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_date.add_xaxis(xaxis_data=x_data)
    line_date.add_yaxis(series_name='气温数据(°C)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False), yaxis_index=0)
    line_date.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    line_conf.add_xaxis(xaxis_data=x_data)
    line_conf.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4,
                        label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_date.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n气温数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}°C")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_conf.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_date.overlap(line_conf)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok=True)
    line_date.render(current_directory + '/html/' + 'tmp.html')
# showtmp('55279099999', '2022-12-03', '2023-12-05')

# 展示指定站点在指定时间段的可见度数据
def showvis(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    df = spectime(stat, begin, end)
    # 准备数据
    x_data = [(iter.split(',')[1]).split('T')[0] + '日' + (iter.split(',')[1]).split('T')[1][:2] + '时' for iter in
              df['stat_date']]
    y_data = [int(iter.split(',')[0]) for iter in df['vis']]
    conf = [str(int(iter.split(',')[1])) for iter in df['vis']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_date = Line()
    # line_conf = Line()
    line_conf = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_date.add_xaxis(xaxis_data=x_data)
    line_date.add_yaxis(series_name='可视距离数据(m)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False), yaxis_index=0)
    line_date.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    line_conf.add_xaxis(xaxis_data=x_data)
    line_conf.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4,
                        label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_date.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n可视距离数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}m")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_conf.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_date.overlap(line_conf)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok=True)
    line_date.render(current_directory + '/html/' + 'vis.html')
showvis('55279099999', '2022-12-03', '2023-12-05')

# 展示指定站点在指定时间段的风速数据
def showwnd(stat, begin, end):
    '''
    stat: 站点编号，字符串
    begin: 开始日期，传入形式为字符串，格式为“xxxx-xx-xx”
    end: 结束日期，传入形式为字符串，格式为“xxxx-xx-xx”
    '''
    df = spectime(stat, begin, end)
    # 准备数据，制作风向数据展示图
    x_data = [(iter.split(',')[1]).split('T')[0] + '日' + (iter.split(',')[1]).split('T')[1][:2] + '时' for iter in
              df['stat_date']]
    y_data = [int(iter.split(',')[0]) for iter in df['wnd']]
    conf = [str(int(iter.split(',')[1])) for iter in df['wnd']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_dire = Line()
    # line_conf = Line()
    conf_dire = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_dire.add_xaxis(xaxis_data=x_data)
    line_dire.add_yaxis(series_name='风向数据(°, 从正北方向顺时针开始)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False), yaxis_index=0)
    line_dire.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    conf_dire.add_xaxis(xaxis_data=x_data)
    conf_dire.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4,
                        label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_dire.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n风向数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}m")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    conf_dire.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_dire.overlap(conf_dire)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok=True)
    line_dire.render(current_directory + '/html/' + 'wnddire.html')

    # 数据准备，制作风速数据展示图
    y_data = [int(iter.split(',')[3]) for iter in df['wnd']]
    conf = [str(int(iter.split(',')[4])) for iter in df['wnd']]
    conf = [conf_grade[iter] for iter in conf]
    # 创建 Line 图表
    line_sped = Line()
    # line_conf = Line()
    conf_sped = Scatter()  # 使用 Scatter 类型来表示散点图
    # 添加数据
    line_sped.add_xaxis(xaxis_data=x_data)
    line_sped.add_yaxis(series_name='风速数据(m/s)', y_axis=y_data, label_opts=opts.LabelOpts(is_show=False),
                        yaxis_index=0)
    line_sped.extend_axis(yaxis=opts.AxisOpts(axisline_opts=opts.AxisLineOpts()))  # 添加一条蓝色的y轴
    conf_sped.add_xaxis(xaxis_data=x_data)
    conf_sped.add_yaxis(series_name='可信度', y_axis=conf, symbol='circle', symbol_size=4,
                        label_opts=opts.LabelOpts(is_show=False), yaxis_index=1)
    # 设置图表标题和其他配置
    line_sped.set_global_opts(
        title_opts=opts.TitleOpts(title='站点编号' + stat + '(' + df['name'].loc[0] + ')' + '\n风速数据展示'),
        xaxis_opts=opts.AxisOpts(type_='category'),
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter="{value}m")),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    conf_sped.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="category"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_top="top")
    )
    line_sped.overlap(conf_sped)
    # 渲染图表到 HTML 文件
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(current_directory + '/html', exist_ok=True)
    line_sped.render(current_directory + '/html/' + 'wndsped.html')

showwnd('55279099999', '2022-12-03', '2023-12-05')