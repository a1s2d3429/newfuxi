import streamlit as st
import pandas as pd
import os

# 页面基础全局配置
st.set_page_config(page_title="赣州富硒农产品产销便民服务平台", layout="wide")
st.title("赣州富硒农产品产销便民服务平台")

# 读取CSV，兼容Windows中文编码
df = pd.read_csv("data.csv", encoding="gbk")
st.success("数据加载完成，可切换下方板块查看对应内容")

# 左侧身份下拉选择
identity = st.selectbox("请选择您的身份", ["消费者（购买用户）", "经销商（收购商）", "农户（种植户）"])

# ---------------------- 1、消费者板块：表格保留 + 下方图文百科 ----------------------
if identity == "消费者（购买用户）":
    st.header("🛒 消费者产品选购专区")
    st.subheader("全部富硒农产品介绍与售价（完整数据表）")
    # 【保留原始完整表格，不删除】
    consumer_df = df[["产品名称", "产品分类", "产地", "单价", "富硒等级", "上市季节"]]
    st.dataframe(consumer_df, use_container_width=True)

    st.divider()
    st.subheader("📖 农产品百科图文详情（下方可查看单品图文介绍）")
    st.markdown("每条数据自动匹配对应产品图片，信息全部读取自表格")
    st.divider()

    # 循环读取CSV每一行数据，生成图文卡片
    for index, row in df.iterrows():
        product_name = row["产品名称"]
        # 拼接本地图片路径（你自己存放图片的文件夹）
        img_path = f"./product_img/{product_name}.jpg"

        col1, col2 = st.columns([1, 3])
        with col1:
            # 判断图片是否存在，不存在则展示默认占位图
            if os.path.exists(img_path):
                st.image(img_path, width=220, caption=product_name)
            else:
                st.image("https://img0.baidu.com/it/u=3511123102,3922111230&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800", width=220, caption="暂无自定义产品图")

        with col2:
            st.subheader(f"【{product_name}】产品详情")
            # 自动从表格读取所有数据，以文字展示
            st.markdown(f"""
            - 产品分类：{row['产品分类']}
            - 原产地：{row['产地']}
            - 零售单价：{row['单价']}
            - 富硒品质等级：{row['富硒等级']}
            - 最佳采购/上市时段：{row['上市季节']}
            """)
            st.info(f"选购说明：{product_name}产自赣州富硒土壤产区，天然富含硒元素，推荐在{row['上市季节']}采购，新鲜度更高。")
        st.divider()

# ---------------------- 2、经销商板块（原有表格完全不变） ----------------------
elif identity == "经销商（收购商）":
    st.header("🤝 经销商收购参考专区")
    st.subheader("全部富硒农产品产地、单价、供货销量明细")
    dealer_df = df[["产品名称", "产品分类", "产地", "单价", "月度销量"]]
    st.dataframe(dealer_df, use_container_width=True)
    st.info("提示：您可以横向对比不同县城同款农产品的售价
            ，选择性价比更高的货源收购。")

# ---------------------- 3、农户板块：新增县域筛选，展示本县单品+汇总销量 ----------------------
elif identity == "农户（种植户）":
    st.header("👨‍🌾 农户种植参考专区")
    # 下拉选择种植县域
    all_county = df["产地"].unique()
    select_county = st.selectbox("请选择您的种植县城", all_county)
    # 筛选出当前县城所有产品数据
    county_all_product = df[df["产地"] == select_county]

    st.subheader(f"【{select_county}】全部种植产品明细")
    # 展示本县每一款产品完整信息（名称/分类/单价/销量）
    st.dataframe(county_all_product[["产品名称", "产品分类", "单价", "月度销量"]], use_container_width=True)

    st.divider()
    st.subheader("各县农产品月度总销量统计表（全县汇总）")
    # 保留你原本的全县总销量汇总表
    farmer_data = df.groupby("产地")["月度销量"].sum().reset_index()
    farmer_data.columns = ["产地", "月度销量"]
    st.dataframe(farmer_data, use_container_width=True)
    st.info("提示：表格里销量越高的县域，市场需求越大，优先规划种植本地热销品类，减少滞销风险。")
