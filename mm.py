import streamlit as st

# 1. 網頁初始化設定（必須放在程式碼第一行）
# layout="wide" 會把網頁兩邊的留白填滿，變成寬螢幕，最適合看多欄位的看板
st.set_page_config(layout="wide")

st.title("階段一：Trello 畫布空間規劃測試")
st.caption("授權標註：edit by 闕河正 | 專屬資淺初學者講義")

st.write("---")

# 2. 呼叫 st.columns(3)，在網頁橫向切出三個一模一樣寬度的大直欄變數
col1, col2, col3, col4 = st.columns(4)

# 3. 運用 with 語法，像填空一樣把文字塞進對應的直欄空間裡
with col1:
    st.markdown("### To Do (待辦)")
    st.write("這裡未來要放『待辦事項』的卡片")

with col2:
    st.markdown("### In Progress (執行中)")
    st.write("這裡未來要放『執行中』的卡片")

with col3:
    st.markdown("### Done (已完成)")
    st.write("這裡未來要放『已完成』的卡片")

with col4:
    st.markdown("### Backlog (後備任務)")
    st.write("這裡未來要放『後備任務』的卡片")



import streamlit as st
# 導入服務帳戶連接核心套件
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")
st.title("階段二：雲端資料庫讀取與原始表格分析")
st.caption("授權標註：edit by 闕河正")

# 1. 建立雲端連接器
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 從 Google 試算表讀取 "Tasks" 工作表
# 核心細節：ttl="0" 代表快取時間為 0 秒，強迫它每次重整都即時去雲端抓最新，不准用舊記憶
df = conn.read(worksheet="Tasks", ttl="0")

st.write("---")
st.write("### 這是從 Google 雲端硬碟抓回來的原始黑白表格（Bare Data）：")

# 3. 直接用 st.dataframe() 把整張表格原汁原味印在網頁上
st.dataframe(df)

# 4. 拆解底層資訊給學生看
st.write("經過 Python 分析，這張表格擁有的『直欄欄位名稱（Columns）』有：", list(df.columns))



import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")
st.title("階段 2.5：DataFrame 數據單點座標拆解實驗")
st.caption("授權標註：edit by 闕河正")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Tasks", ttl="0")

st.write("### 目前的雲端原始表格：")
st.dataframe(df)

st.write("---")
st.write("### 精準座標抽離實驗：")

# 使用 .loc[行號, 欄位名] 精準抓取特定格子
first_title = df.loc[2, "title"]
first_owner = df.loc[2, "owner"]

st.write(f"機器人回報：我們發現第 2 列（第三行任務）的名稱是：**{first_title}**")
st.write(f"機器人回報：這一行的負責人是：**{first_owner}**")



import streamlit as st 

from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide") 

st.title(" 階段三：外星文濾網分流與空間歸隊測試") 

st.caption("授權標註：edit by 闕河正")

conn = st.connection("gsheets", type=GSheetsConnection) 

df = conn.read(worksheet="Tasks", ttl="0")

st.write("---")

col1, col2, col3 = st.columns(3)

with col1: 

    st.markdown("###  To Do") 

    #  內層做濾網，外層做篩選：只抓出狀態為 To Do 的小表格 

    todo_df = df[df["status"] == "To Do"] # 把它印在左邊這欄 
    st.dataframe(todo_df)

with col2: 

    st.markdown("###  In Progress") 

    #  只抓出狀態為 In Progress 的小表格 

    ip_df = df[df["status"] == "In Progress"] 

    st.dataframe(ip_df)

with col3: 

    st.markdown("###  Done") 

    #  只抓出狀態為 Done 的小表格 

    done_df = df[df["status"] == "Done"] 

    st.dataframe(done_df)



import streamlit as st

from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")

st.title(" 階段 3.5：iterrows 迴圈解構點名現場實驗") 

st.caption("授權標註：edit by 闕河正")

conn = st.connection("gsheets", type=GSheetsConnection) 

df = conn.read(worksheet="Tasks", ttl="0")

todo_df = df[df["status"] == "To Do"]

st.write("---") 

st.write("###  進入 Python 迴圈自動化點名現場：")

for idx, row in todo_df.iterrows(): 

    # 每一圈，我們用一個小紅框（st.error）來代表一次巡迴 

    st.error(f" 迴圈巡邏：目前點名點到了第 {idx} 行的任務：") 

    st.write(f" ➔ 【title 任務名稱】這一格拿到了： {row['title']}") 

    st.write(f" ➔ 【owner 負責人】這一格拿到了： {row['owner']}")





import streamlit as st

import pandas as pd

from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")

st.title(" 階段四終極完成版：GitHub 雲端同步 Trello 看板")

st.caption("授權標註：edit by 闕河正 | 完整功能版")

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Tasks", ttl="0")

# ==========================================

#  區塊一：上方新增任務輸入表單

# ==========================================

st.write("###  指派新任務")

with st.form("task_input_form", clear_on_submit=True):

    c_title, c_status, c_owner = st.columns([2, 1, 1]) # 運用權重比例切分表單

    with c_title:

        new_title = st.text_input(" 任務名稱", placeholder="輸入任務名稱...")

    with c_status:

        new_status = st.selectbox(" 狀態", ["To Do", "In Progress", "Done"])

    with c_owner:

        new_owner = st.text_input(" 負責人", placeholder="誰來負責...")

    

    submit_btn = st.form_submit_button("確認指派並同步雲端")

if submit_btn and new_title and new_owner:

    new_data = {"title": new_title, "status": new_status, "owner": new_owner}

    new_row = pd.DataFrame([new_data])

    #  核心安全：新版 Python 廢棄 .append()，在雲端必須改用 pd.concat() 進行表格拼接

    updated_df = pd.concat([df, new_row], ignore_index=True)

    conn.update(worksheet="Tasks", data=updated_df)

    st.success(" 資料已跨越限制，成功同步寫入 Google 試算表！")

    st.rerun() # 強制網頁自我重整，重新讀取，讓新卡片亮起來

st.write("---")

# ==========================================

#  區塊二：下方 Trello 三縱欄畫布與卡片渲染

# ==========================================

st.write("###  看板動態狀態監控")

trello_col1, trello_col2, trello_col3 = st.columns(3)

#  【第一欄：To Do】

with trello_col1:

    st.markdown("### <span style='color:red'> To Do (待辦)</span>", unsafe_allow_html=True)

    todo_list = df[df["status"] == "To Do"] # 階段三學的濾網分流

    

    if not todo_list.empty:

        for idx, row in todo_list.iterrows(): # 階段 3.5 學的迴圈點名

            #  呼叫 border=True，幫每筆點名到的資料揉出一個精緻卡片外框

            with st.container(border=True):

                st.write(f"** {row['title']}**")      # 粗體印出任務名稱

                st.caption(f"負責人: {row['owner']}")   # 灰色小字印出負責人

    else:

        st.info("暫無待辦任務")

#  【第二欄：In Progress】

with trello_col2:

    st.markdown("### <span style='color:orange'> In Progress (執行中)</span>", unsafe_allow_html=True)

    ip_list = df[df["status"] == "In Progress"]

    

    if not ip_list.empty:

        for idx, row in ip_list.iterrows():

            with st.container(border=True):

                st.write(f"** {row['title']}**")

                st.caption(f"負責人: {row['owner']}")

    else:

        st.info("暫無執行中任務")

#  【第三欄：Done】

with trello_col3:

    st.markdown("### <span style='color:green'> Done (已完成)</span>", unsafe_allow_html=True)

    done_list = df[df["status"] == "Done"]

    

    if not done_list.empty:

        for idx, row in done_list.iterrows():

            with st.container(border=True):

                #  貼心小視覺：用 文字 幫已完成的任務加上刪除線，更有完工的體感！

                st.write(f"** {row['title']}**")

                st.caption(f"負責人: {row['owner']}")

    else:

        st.info("暫無已完成任務")




# ==========================================
# 區塊二：下方 Trello 三縱欄畫布與卡片渲染
# ==========================================

st.write("### 📊 看板動態狀態監控")

trello_col1, trello_col2, trello_col3 = st.columns(3)

status_list = ["To Do", "In Progress", "Done"]

# ==========================================
# 共用卡片函式
# ==========================================

def render_cards(dataframe, column_obj, status_name, color):

    with column_obj:

        st.markdown(
            f"### <span style='color:{color}'>{status_name}</span>",
            unsafe_allow_html=True
        )

        task_list = dataframe[dataframe["status"] == status_name]

        if not task_list.empty:

            for idx, row in task_list.iterrows():

                with st.container(border=True):

                    st.write(f"### 📌 {row['title']}")
                    st.caption(f"👤 負責人：{row['owner']}")

                    # 狀態轉換下拉選單
                    new_status = st.selectbox(
                        "變更狀態",
                        status_list,
                        index=status_list.index(row["status"]),
                        key=f"status_{idx}"
                    )

                    # 更新按鈕
                    if st.button("更新狀態", key=f"btn_{idx}"):

                        # 修改 dataframe
                        df.loc[idx, "status"] = new_status

                        # 同步回 Google Sheets
                        conn.update(
                            worksheet="Tasks",
                            data=df
                        )

                        st.success(f"✅ 任務已更新為 {new_status}")

                        st.rerun()

        else:
            st.info("目前沒有任務")


# ==========================================
# 三大欄位
# ==========================================

render_cards(df, trello_col1, "To Do", "red")

render_cards(df, trello_col2, "In Progress", "orange")

render_cards(df, trello_col3, "Done", "green")
