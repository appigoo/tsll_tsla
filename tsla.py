import streamlit as st
import yfinance as yf
import pandas as pd

# 设置页面标题和描述
st.title("🚀 TSLA 和 TSLL 关系计算器")
st.write("""
TSLL 是 TSLA 的 2 倍杠杆 ETF，目标是提供 TSLA **每日**价格变动的 200% 回报。
- 输入假设的 TSLA 新价格，程序会计算单日变化下的 TSLL 预期价格。
- **警告**：杠杆 ETF 不适合长期持有，受波动衰减影响。仅供参考，请咨询专业顾问。
""")

# 获取实时当前价格（使用 yfinance）
@st.cache_data  # 缓存数据以提高性能
def get_current_prices():
    tsla_ticker = yf.Ticker("TSLA")
    tsll_ticker = yf.Ticker("TSLL")
    
    # 获取最近一个交易日的收盘价
    tsla_data = tsla_ticker.history(period="1d")
    tsll_data = tsll_ticker.history(period="1d")
    
    if not tsla_data.empty and not tsll_data.empty:
        current_tsla = tsla_data['Close'].iloc[-1]
        current_tsll = tsll_data['Close'].iloc[-1]
        return current_tsla, current_tsll
    else:
        # 如果获取失败，使用默认值（基于 2025-10-17 数据）
        st.warning("无法获取实时数据，使用默认值。")
        return 439.31, 20.17

# 获取价格
current_tsla, current_tsll = get_current_prices()

# 显示当前价格
col1, col2 = st.columns(2)
col1.metric("当前 TSLA 价格", f"${current_tsla:.2f}")
col2.metric("当前 TSLL 价格", f"${current_tsll:.2f}")

# 用户输入
st.subheader("模拟计算")
new_tsla_price = st.number_input(
    "输入假设的 TSLA 新价格（美元）:", 
    min_value=0.0, 
    value=current_tsla, 
    step=0.01
)

# 计算变化率
if new_tsla_price != current_tsla:
    tsla_change = (new_tsla_price - current_tsla) / current_tsla
    tsll_change = 2 * tsla_change  # 2 倍杠杆
    expected_tsll = current_tsll * (1 + tsll_change)
    
    # 显示结果
    st.subheader("计算结果")
    col1, col2, col3 = st.columns(3)
    col1.metric("TSLA 变化率", f"{tsla_change:+.2%}")
    col2.metric("TSLL 变化率", f"{tsll_change:+.2%}")
    col3.metric("预期 TSLL 价格", f"${expected_tsll:.2f}")
    
    # 额外说明
    if tsla_change > 0:
        st.success("上涨情景：TSLL 放大收益，但风险更高。")
    else:
        st.error("下跌情景：TSLL 放大损失，极端波动可能导致更大衰减。")
else:
    st.info("请输入不同的 TSLA 价格进行模拟。")

# 底部说明
st.sidebar.title("关于杠杆 ETF")
st.sidebar.write("""
- **公式**：TSLL 新价格 ≈ 当前 TSLL × (1 + 2 × (TSLA 新价 - 当前 TSLA) / 当前 TSLA)
- **风险**：每日重置导致长期持有时复合效应（volatility decay），尤其在震荡市场。
- 数据来源：Yahoo Finance（实时更新）。
""")
