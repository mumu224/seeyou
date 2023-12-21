import streamlit as st
import requests
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import WordCloud
from collections import Counter
import re
import random
import thulac


def crawl_webpage(url):
    thu1 = thulac.thulac()
    headers = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      r"Chrome/114.0.0.0"
                      r"Safari/537.36 Edg/114.0.1823.67"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    text_content = response.text
    pattern = r"[\u4E00-\u9FA5]+"
    content = re.findall(pattern, text_content)
    content = [z[0] for i in content for z in thu1.cut(i, text=False) if ('n' in z[1] or 'a' in z[1]) and len(z[0]) > 1]
    content = Counter(content)
    return content

#柱状图
def bar(key, value):
    colors = ['#5793f3', '#d14a61', '#675bba', '#36cbcb', '#da70d6']  # 定义多种颜色
    option_1 = {
        "title": {"text": "页面词频"},
        "tooltip": {},
        "xAxis": {
            "data": key
        },
        "yAxis": {},
        "series": [
            {
                "name": "词汇",
                "type": "bar",
                "data": []
            }
        ]
    }

    for i in range(len(value)):
        item = {"value": value[i]}
        color_index = i % len(colors)  # 使用取余运算循环使用颜色列表中的颜色
        item["itemStyle"] = {"color": colors[color_index]}
        option_1["series"][0]["data"].append(item)

    st_echarts(options=option_1,width="800px", height="500px")




def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgb({r}, {g}, {b})'
#饼图
def pie(data):
    num_colors = len(data) # 需要生成的随机颜色数量
    colors = [random_color() for _ in range(num_colors)] # 生成随机颜色列表
    options_2 = {
        "title": {"text": ""},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                "name": "词汇",
                "type": "pie",
                "radius": ['40%', '70%'],
                "center": ['50%', '50%'],
                "label": {
                    "show": True,
                    "position": 'inside',
                    "formatter": '{b}: {@2015} ({d}%)'
                },
                "labelLine": {
                    "show": False
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
                "data": [
                    {"name": item["name"], "value": item["value"], "itemStyle": {"color": colors[i]}}
                    for i, item in enumerate(data)
                ]
            }
        ]
    }
    st_echarts(options=options_2, height="500px")




#折线图
def line(key, value):
    option_3 = {
        "title": {"text": "页面词频"},
        "tooltip": {},
        "xAxis": {
            "type": "category",
            "data": key
        },
        "yAxis": {
            "type": "value",
            "data": [0, 5, 10, 20, 30, 60, 100]
        },
        "series": [
            {
                "name": "词汇",
                "type": "line",
                "data": value
            }
        ]
    }
    st_echarts(options=option_3)



#面积图
def area(key, value):
    option_4 = {
        "title": {"text": "页面访问量"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "line"}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": key,
            "axisLabel": {"rotate": 45, "interval": 0}
        },
        "yAxis": {"type": "value", "splitLine": {"show": False}},
        "series": [
            {
                "name": "访问量",
                "data": value,
                "type": "line",
                "smooth": True,
                "symbol": "none",
                "sampling": "average",
                "itemStyle": {"color": "#6c5ce7"},
                "areaStyle": {"color": "#dfe6e9"}
            }
        ]
    }
    st_echarts(options=option_4)



def scatter(data):
    option_5 = {
        "xAxis": {
            "type": "value",
            "splitLine": {"show": False},
            "axisTick": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "splitLine": {"show": False},
            "axisTick": {"show": False},
        },
        "series": [
            {
                "data": data,
                "type": "scatter",
                "symbolSize": 8,
                "itemStyle": {"color": "#6c5ce7"},
                "emphasis": {"itemStyle": {"color": "#0984e3"}},
            }
        ],
    }
    st_echarts(options=option_5)





def line_bar(key, value):
    option_6 = {
        "title": {
            "text": "折线柱状组合图",
            "left": "center",
            "top": "5%",  # 将标题位置移到顶部
            "textStyle": {
                "color": "#555",  # 标题颜色
                "fontSize": 16,
            },
        },
        "tooltip": {"trigger": "axis"},
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "15%",  # 调整图表位置
            "containLabel": True,
        },
        "legend": {
            "data": ["折线图", "柱状图"],
            "top": "90%",  # 将图例位置移到底部
            "textStyle": {
                "color": "#666",
            },
        },
        "xAxis": [
            {
                "type": "category",
                "data": key,
                "axisPointer": {
                    "type": "shadow",
                },
                "axisLine": {  # 坐标轴线样式
                    "lineStyle": {
                        "color": "#999",  # 坐标轴线颜色
                    }
                },
                "axisLabel": {  # 标签样式
                    "color": "#333",  # 标签颜色
                    "fontSize": 12,
                },
            }
        ],
        "yAxis": [
            {
                "type": "value",
                "name": "折线图",
                "min": 0,
                "max": value[0],
                "interval": value[0] / 5,
                "axisLabel": {
                    "color": "#666",
                    "fontSize": 12,
                },
                "axisLine": {
                    "lineStyle": {
                        "color": "#999",
                    }
                },
                "splitLine": {  # 分隔线样式
                    "show": True,
                    "lineStyle": {
                        "color": "#eee",
                    }
                },
            },
            {
                "type": "value",
                "name": "柱状图",
                "min": 0,
                "max": value[0],
                "interval": value[0] / 5,
                "axisLabel": {
                    "color": "#666",
                    "fontSize": 12,
                },
                "axisLine": {
                    "lineStyle": {
                        "color": "#999",
                    }
                },
                "splitLine": {
                    "show": True,
                    "lineStyle": {
                        "color": "#eee",
                    }
                },
            },
        ],
        "series": [
            {
                "name": "折线图",
                "type": "line",
                "data": value,
                "smooth": True,  # 圆滑曲线
                "symbolSize": 8,  # 折线拐点大小
                "lineStyle": {
                    "color": "#5470c6",  # 折线颜色
                    "width": 2,
                },
                "itemStyle": {
                    "color": "#5470c6",  # 拐点颜色
                },
            },
            {
                "name": "柱状图",
                "type": "bar",
                "yAxisIndex": 1,
                "data": value,
                "barWidth": 20,  # 柱状图宽度
                "itemStyle": {
                    "color": "#666666",  # 柱状图颜色
                },
            },
        ],
    }
    st_echarts(options=option_6)



def wordcloud(words):
   WD = WordCloud()
   WD.add("", words, word_size_range=[20, 100])
   st_pyecharts(WD)


def main():
    st.title('欢迎使用网页爬虫小程序')
    st.image("xiugou.png")
    session_state = st.session_state
    if "data" not in st.session_state:
        session_state.key = None
        session_state.value = None
        session_state.data = None

    if url := st.chat_input("爬取静态网址"):
        counts = crawl_webpage(url)
        session_state.key = [key for key, _ in counts.most_common(20)]
        session_state.value = [value for _, value in counts.most_common(20)]
        session_state.data = [{"value": i, "name": j} for i, j in zip(session_state.value, session_state.key)]

    if session_state.key:
        session_state['page'] = '柱状图'
        page = st.sidebar.radio('选择你想要的样式',
                                ['柱状图', '饼图', '折线图', '面积图', '散点图', '折线柱状组合图', '词云'])
        if page == '柱状图':
            bar(session_state.key, session_state.value)

        elif page == '饼图':
            pie(session_state.data)

        elif page == '折线图':
            line(session_state.key, session_state.value)

        elif page == "面积图":
            area(session_state.key, session_state.value)

        elif page == "散点图":
            scatter([[i, i] for i in session_state.value])

        elif page == "折线柱状组合图":
            line_bar(session_state.key, session_state.value)

        elif page == "词云":
            wordcloud(zip(session_state.key, session_state.value))


if __name__ == "__main__":
    main()
