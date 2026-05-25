import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

st.set_page_config(page_title="REV AGENCY レース管理", layout="wide")

# 保存用のCSVファイル名
SAVE_FILE_NAME = "rev_racing_data.csv"

# ==========================================
# 🎨 究極のレーシングサイバーデザイン（CSS注入）
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #060606 !important;
    color: #f5f5f5 !important;
    font-family: 'Inter', 'Helvetica Neue', 'Segoe UI', 'Hiragino Kaku Gothic ProN', sans-serif !important;
}
p, span, label, .stMarkdown {
    color: #e0e0e0 !important;
    font-weight: 500;
}
h1, h2, h3 {
    font-style: italic !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    background: linear-gradient(90deg, #FFFFFF, #FF003C) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    border-left: None !important;
    padding-left: 0px !important;
    margin-top: 30px !important;
    margin-bottom: 15px !important;
}
.title-text {
    font-size: 3.5rem;
    font-weight: 950;
    font-style: italic;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #FFFFFF 30%, #FF003C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0px 0px 30px rgba(255, 0, 60, 0.2);
    margin-bottom: 5px;
    text-align: center;
}
.subtitle-text {
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 6px;
    color: #666666 !important;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 40px;
}
div[data-testid="stMetricValue"] {
    color: #FF003C !important;
    font-style: italic;
    font-weight: 900;
    text-shadow: 0px 0px 15px rgba(255, 0, 60, 0.6);
    font-size: 2.8rem;
    letter-spacing: -1px;
}
div[data-testid="stMetricLabel"] p {
    color: #888888 !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}
div[data-testid="stMetric"] {
    background: #111111 !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 8px !important;
    padding: 15px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
button[kind="primary"] {
    background: #FF003C !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-style: italic !important;
    letter-spacing: 1px !important;
    padding: 12px 24px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0px 0px 15px rgba(255, 0, 60, 0.4) !important;
}
button[kind="primary"]:hover {
    background: #ff2a5f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0px 0px 25px rgba(255, 0, 60, 0.7) !important;
}
div[data-testid="stForm"] {
    background: #111111 !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 8px !important;
    padding: 30px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
}

div[data-testid="stDataFrame"] {
    background-color: #0d0d0d !important;
    border: 1px solid #262626 !important;
    border-radius: 6px !important;
    padding: 4px !important;
}
div[data-testid="stDataFrame"] iframe, div[data-testid="stDataFrame"] table {
    background-color: #0d0d0d !important;
}
.rendered_html table {
    border-collapse: collapse !important;
    border: 1px solid #262626 !important;
}
.rendered_html th {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid #FF003C !important;
}
.rendered_html td {
    background-color: #0d0d0d !important;
    color: #e0e0e0 !important;
}

button[data-baseweb="tab"] {
    color: #555555 !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 12px 20px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FF003C !important;
    background: transparent !important;
    border-bottom: 2px solid #FF003C !important;
}
input[type="text"], input[type="password"], input[type="number"] {
    background-color: #161616 !important;
    color: #ffffff !important;
    border: 1px solid #252525 !important;
    border-radius: 4px !important;
}
input:focus {
    border-color: #FF003C !important;
}
div[data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid #222222 !important;
    border-radius: 4px !important;
}
hr {
    border-top: 1px solid #222222 !important;
}

.podium-container {
    background: #111111;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid #222;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.rank-gold { border-left: 5px solid #FFD700 !important; box-shadow: 0 0 15px rgba(255, 215, 0, 0.15); }
.rank-silver { border-left: 5px solid #C0C0C0 !important; }
.rank-bronze { border-left: 5px solid #CD7F32 !important; }

.podium-badge {
    font-size: 1.2rem;
    font-weight: 900;
    font-style: italic;
    padding: 2px 10px;
    border-radius: 4px;
}
.badge-gold { background: #FFD700; color: #000 !important; text-shadow: 0 0 5px #FFF; }
.badge-silver { background: #C0C0C0; color: #000 !important; }
.badge-bronze { background: #CD7F32; color: #000 !important; }

.podium-name {
    font-size: 1.3rem;
    font-weight: 800;
    color: #FFF !important;
}
.podium-stats {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FF003C !important;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ロゴとタイトル表示
logo_file = "logo.png"
if os.path.exists(logo_file):
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    with col2:
        st.image(logo_file, use_container_width=True)

st.markdown('<div class="title-text">REV AGENCY</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Racing Management System</div>', unsafe_allow_html=True)

# ==========================================
# 💾 📂 ローカルCSVファイル自動セーブ・ロード機構
# ==========================================
if os.path.exists(SAVE_FILE_NAME):
    try:
        loaded_df = pd.read_csv(SAVE_FILE_NAME, dtype={"パスワードデータ": str, "レース日時": str})
        loaded_df["順位"] = pd.to_numeric(loaded_df["順位"], errors="coerce").fillna(0).astype(int)
        loaded_df["獲得ポイント"] = pd.to_numeric(loaded_df["獲得ポイント"], errors="coerce").fillna(0).astype(int)
        loaded_df["獲得賞金"] = pd.to_numeric(loaded_df["獲得賞金"], errors="coerce").fillna(0).astype(int)
        
        st.session_state.history_df = loaded_df
        st.session_state.player_names = sorted(list(set(loaded_df["プレイヤー名"].unique())))
        if "使用車種" in loaded_df.columns:
            st.session_state.vehicle_names = sorted(list(set(loaded_df["使用車種"].dropna().unique())))
        if "コース名" in loaded_df.columns:
            st.session_state.course_names = sorted(list(set(loaded_df["コース名"].dropna().unique())))
    except Exception as e:
        st.error(f"データ自動同期エラー: {e}")
        st.session_state.history_df = pd.DataFrame(columns=["レース日時", "順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "レース名", "コース名", "パスワードデータ"])
else:
    if "history_df" not in st.session_state:
        st.session_state.history_df = pd.DataFrame(columns=["レース日時", "順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "レース名", "コース名", "パスワードデータ"])

if "racer_accounts" not in st.session_state:
    st.session_state.racer_accounts = {}

if "player_names" not in st.session_state:
    st.session_state.player_names = []
if "vehicle_names" not in st.session_state:
    st.session_state.vehicle_names = []
if "course_names" not in st.session_state:
    st.session_state.course_names = []

def save_data_to_local_csv():
    st.session_state.history_df.to_csv(SAVE_FILE_NAME, index=False, encoding='utf-8-sig')

if not st.session_state.history_df.empty and "パスワードデータ" in st.session_state.history_df.columns:
    for _, row in st.session_state.history_df.iterrows():
        p_name = row["プレイヤー名"]
        p_pwd = str(row.get("パスワードデータ", "")).strip()
        if p_pwd.endswith(".0"):
            p_pwd = p_pwd[:-2]
            
        if p_name and p_pwd and p_pwd != "nan" and p_pwd != "":
            st.session_state.racer_accounts[p_name] = p_pwd

for name in st.session_state.racer_accounts.keys():
    if name not in st.session_state.player_names:
        st.session_state.player_names.append(name)
st.session_state.player_names.sort()

# ライセンス条件初期値
if "rank_b_threshold" not in st.session_state:
    st.session_state.rank_b_threshold = 50
if "rank_a_threshold" not in st.session_state:
    st.session_state.rank_a_threshold = 150
if "rank_s_threshold" not in st.session_state:
    st.session_state.rank_s_threshold = 300

# ランク差連動型下剋上パラメータの初期化
if "gekokujo_bonus_multiplier" not in st.session_state:
    st.session_state.gekokujo_bonus_multiplier = 2  
if "gekokujo_penalty_multiplier" not in st.session_state:
    st.session_state.gekokujo_penalty_multiplier = 2 

def get_rank_info(pt):
    b_val = st.session_state.rank_b_threshold
    a_val = st.session_state.rank_a_threshold
    s_val = st.session_state.rank_s_threshold
    
    if pt < b_val: return "C (ルーキー)", 1
    elif pt < a_val: return "B (ブロンズ)", 2
    elif pt < s_val: return "A (シルバー)", 3
    else: return "S (ゴールド)", 4

player_names = st.session_state.player_names
vehicle_names = st.session_state.vehicle_names
course_names = st.session_state.course_names
history_df = st.session_state.history_df

player_totals = history_df.groupby("プレイヤー名")["獲得ポイント"].sum().to_dict() if not history_df.empty else {}

# ==========================================
# 🔐 セッション制御・ログアウト
# ==========================================
ADMIN_PASSWORD = "rev123"

if "racer_name" not in st.session_state:
    st.session_state.racer_name = None

if "gate_mode" not in st.session_state:
    st.session_state.gate_mode = "login"

if "selected_profile_racer" not in st.session_state:
    st.session_state.selected_profile_racer = None

col_space, col_admin_panel, col_logout_panel = st.columns([3, 1, 1])

with col_admin_panel:
    with st.expander("🔑 運営スタッフ専用"):
        pwd = st.text_input("パスワードキー", type="password", key="admin_pwd_field")
        if pwd == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("管理者認証に成功")
        else:
            st.session_state.is_admin = False

with col_logout_panel:
    if st.session_state.get("is_admin") or st.session_state.racer_name is not None:
        if st.button("🚪 システムログアウト", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.racer_name = None
            st.session_state.gate_mode = "login"
            st.session_state.selected_profile_racer = None
            st.success("ログアウトしました。")
            st.rerun()

# ==========================================
# 🏁 レーサー用ログイン・登録ブロック画面
# ==========================================
if not st.session_state.get("is_admin") and st.session_state.racer_name is None:
    st.markdown("---")
    col_g1, col_g2, col_g3 = st.columns([1, 1.8, 1])
    with col_g2:
        if st.session_state.gate_mode == "login":
            st.subheader("🔑 既存アカウントでログイン")
            st.write("登録済みのレーサー名とパスワードを入力してください。")
            
            login_name_input = st.text_input(
                "レーサー名 (ドライバー名)",
                placeholder="名前を入力、またはダブルクリックして名簿から選択...",
                key="racer_login_name"
            )
            login_pwd_input = st.text_input("パスワード", type="password", placeholder="••••••••", key="racer_login_pwd")
            
            if player_names:
                options_html = "".join([f'<option value="{name}">' for name in player_names])
                st.markdown(f"""
                <script>
                    const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                    inputs.forEach(input => {{
                        if (input.placeholder.includes("名簿から選択")) {{
                            input.setAttribute('list', 'gate_player_list');
                        }}
                    }});
                </script>
                <datalist id="gate_player_list">{options_html}</datalist>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            c_btn1, c_btn2 = st.columns([3, 2])
            with c_btn1:
                if st.button("ダッシュボードに入る", type="primary", use_container_width=True):
                    l_name = login_name_input.strip()
                    l_pwd = str(login_pwd_input).strip()
                    
                    if l_name in st.session_state.racer_accounts:
                        if str(st.session_state.racer_accounts[l_name]) == l_pwd:
                            st.session_state.racer_name = l_name
                            st.rerun()
                        else:
                            st.error("🔒 パスワードが間違っています。")
                    elif l_name in player_names and l_name not in st.session_state.racer_accounts:
                        st.session_state.racer_accounts[l_name] = l_pwd
                        st.session_state.racer_name = l_name
                        st.rerun()
                    else:
                        st.error("❌ 登録のないレーサー名です。新規登録を行ってください。")
                        
            with c_btn2:
                if st.button("ログインに困ったとき", use_container_width=True):
                    st.info("💡 **【ログインでお困りの方へ】**\n\nパスワードを忘れてしまった場合は運営スタッフへお声がけください。")
            
            st.markdown("<br><br><hr style='border-top: 1px dashed #333;'><br>", unsafe_allow_html=True)
            st.write("💡 まだアカウントをお持ちでない方はこちら")
            if st.button("✍️ 新規レーサー登録画面へ切り替える", use_container_width=True):
                st.session_state.gate_mode = "signup"
                st.rerun()
                    
        else:
            st.subheader("✍️ 新規レーサー登録")
            reg_name_input = st.text_input("登録するレーサー名", placeholder="例：Ryunosuke", key="racer_reg_name")
            reg_pwd_input = st.text_input("パスワードを設定", type="password", placeholder="••••••••", key="racer_reg_pwd")
            reg_pwd_confirm = st.text_input("パスワード（確認用）", type="password", placeholder="••••••••", key="racer_reg_confirm")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("公式アカウントを作成する", type="primary", use_container_width=True):
                r_name = reg_name_input.strip()
                r_pwd = str(reg_pwd_input).strip()
                r_conf = str(reg_pwd_confirm).strip()
                
                if not r_name or not r_pwd:
                    st.warning("⚠️ レーサー名とパスワードは必須項目です。")
                elif r_pwd != r_conf:
                    st.error("❌ 確認用のパスワードが一致しません。")
                elif r_name in player_names:
                    st.error("❌ そのレーサー名はすでにエントリーされています。")
                else:
                    st.session_state.racer_accounts[r_name] = r_pwd
                    if r_name not in st.session_state.player_names:
                        st.session_state.player_names.append(r_name)
                    
                    new_acc_row = pd.DataFrame([{
                        "レース日時": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "順位": 0, "プレイヤー名": r_name, "使用車種": "新規登録", "コース名": "ロビー",
                        "獲得ポイント": 0, "獲得賞金": 0, "レース名": "SYSTEM_SIGNUP",
                        "パスワードデータ": r_pwd
                    }])
                    st.session_state.history_df = pd.concat([st.session_state.history_df, new_acc_row], ignore_index=True)
                    save_data_to_local_csv()
                    
                    st.session_state.racer_name = r_name
                    st.rerun()
            
            st.markdown("<br><br><hr style='border-top: 1px dashed #333;'><br>", unsafe_allow_html=True)
            if st.button("⬅️ ログイン画面に戻る", use_container_width=True):
                st.session_state.gate_mode = "login"
                st.rerun()
    st.stop()

if "パスワードデータ" not in st.session_state.history_df.columns:
    st.session_state.history_df["パスワードデータ"] = ""
if "コース名" not in st.session_state.history_df.columns:
    st.session_state.history_df["コース名"] = "未登録"

# ==========================================
# 🚀 タブの作成
# ==========================================
if st.session_state.get("is_admin"):
    tabs = st.tabs(["✍️ レース結果入力", "📝 履歴＆データ一括修正", "🏆 総合ランキング", "🏎️ 分析スタッツ", "👤 個人の成績確認", "⚙️ システム管理"])
    tab_input, tab_history, tab_rank, tab_car, tab_personal, tab_setting = tabs
else:
    tabs = st.tabs(["🏆 総合ランキング", "🏎️ 分析スタッツ", "👤 個人の成績確認"])
    tab_rank, tab_car, tab_personal = tabs
    tab_input, tab_history, tab_setting = None, None, None

# ==========================================
# 【管理者専用】タブ：✍️ レース結果入力
# ==========================================
if tab_input:
    with tab_input:
        if st.session_state.get("save_success"):
            st.success(st.session_state.save_success)
            st.session_state.save_success = ""

        st.subheader("🏁 レース基本情報 ＆ 今回の賞金配分設定")
        
        col_capacity, col_pool = st.columns([1, 2])
        p_count = col_capacity.number_input("🏎️ 今回の出走人数", min_value=1, max_value=30, value=3)
        total_prize = col_pool.number_input("💰 今回の賞金総額 (ドル)", min_value=0, value=1000000, step=50000)

        with st.form("race_input_form_ultimate"):
            st.markdown("##### 📊 このレース限定の賞金配分率 (%)")
            col_r1, col_r2, col_r3 = st.columns(3)
            race_p1_rate = col_r1.number_input("1位の配分 (%)", min_value=0, max_value=100, value=50)
            race_p2_rate = col_r2.number_input("2位の配分 (%)", min_value=0, max_value=100, value=30)
            race_p3_rate = col_r3.number_input("3位の配分 (%)", min_value=0, max_value=100, value=20)
            
            if (race_p1_rate + race_p2_rate + race_p3_rate) != 100:
                st.warning("⚠️ 注意: 3つの配分比率の合計が100%になっていません。確認してください。")
            
            st.markdown("---")
            col_n, col_co, col_d, col_t = st.columns([2, 2, 1, 1])
            jst = pytz.timezone('Asia/Tokyo')
            race_name = col_n.text_input("🏁 レース名・イベント名", value="フリーレース")
            course_name_input = col_co.text_input("🛣️ 開催コース名", placeholder="コース名を入力、またはダブルクリック...", value="アロヨ・グランプリ")
            race_date = col_d.date_input("開催日", datetime.now(jst).date())
            race_time = col_t.time_input("開催時刻", datetime.now(jst).time(), step=60)

            st.markdown("---")
            st.markdown("### 🥇 順位ごとの結果入力")
            
            input_results = []
            for i in range(int(p_count)):
                rank_num = i + 1
                st.markdown(f"**【 {rank_num}位 】**")
                c1, c2 = st.columns(2)
                
                if player_names:
                    p_name = c1.selectbox(f"ドライバーを選択", player_names, key=f"p_select_{rank_num}")
                else:
                    p_name = None
                    c1.warning("登録レーサーがありません。")
                
                v_name = c2.text_input(f"使用車種", placeholder="車種名を入力...", key=f"v_input_{rank_num}").strip()
                input_results.append({"順位": rank_num, "プレイヤー名": p_name, "使用車種": v_name})

            vehicle_options_html = "".join([f'<option value="{car}">' for car in vehicle_names])
            course_options_html = "".join([f'<option value="{c_name}">' for c_name in course_names])
            
            st.markdown(f"""
            <script>
                const formInputs = window.parent.document.querySelectorAll('input[type="text"]');
                formInputs.forEach(input => {{
                    if (input.placeholder && input.placeholder.includes("車種名を入力")) {{
                        input.setAttribute('list', 'form_vehicle_master_list');
                    }}
                    if (input.placeholder && input.placeholder.includes("コース名を入力")) {{
                        input.setAttribute('list', 'form_course_master_list');
                    }}
                }});
            </script>
            <datalist id="form_vehicle_master_list">{vehicle_options_html}</datalist>
            <datalist id="form_course_master_list">{course_options_html}</datalist>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("レース結果を計算して公式記録にセーブ", type="primary")

        if submit_btn:
            has_error = False
            for res in input_results:
                if not res["プレイヤー名"]:
                    st.error(f"{res['順位']}位のドライバー名が選択されていません。")
                    has_error = True
            
            final_course_name = course_name_input.strip()
            if not final_course_name:
                st.error("コース名が空欄です。")
                has_error = True
            
            if not has_error:
                participants_data = []
                # 💡 秒単位（:00）まで含めた一意のタイムスタンプ文字列を作成して主キー化
                race_datetime_str = f"{race_date} {race_time.strftime('%H:%M')}:00"
                
                if final_course_name not in st.session_state.course_names:
                    st.session_state.course_names.append(final_course_name)
                
                for res in input_results:
                    p = res["プレイヤー名"]
                    v = res["使用車種"]
                    if v and v not in ["", "None", "nan"] and v not in st.session_state.vehicle_names:
                        st.session_state.vehicle_names.append(v)
                        
                    pt = player_totals.get(p, 0)
                    _, rank_lvl = get_rank_info(pt)
                    participants_data.append({"placement": res["順位"], "p_name": p, "v_name": v, "rank_lvl": rank_lvl})
                
                st.session_state.vehicle_names.sort()
                st.session_state.course_names.sort()
                records_to_add = []
                
                bonus_mult = st.session_state.get("gekokujo_bonus_multiplier", 2)
                penalty_mult = st.session_state.get("gekokujo_penalty_multiplier", 2)
                
                for current_pilot in participants_data:
                    placement = current_pilot["placement"]
                    my_lvl = current_pilot["rank_lvl"]
                    
                    base_pt = max(2, 12 - (placement * 2))
                    下剋上補正 = 0
                    
                    for other_pilot in participants_data:
                        if current_pilot["p_name"] == other_pilot["p_name"]:
                            continue
                        
                        other_lvl = other_pilot["rank_lvl"]
                        other_placement = other_pilot["placement"]
                        
                        if my_lvl < other_lvl and placement < other_placement:
                            ランク差 = other_lvl - my_lvl
                            下剋上補正 += (ランク差 * bonus_mult)
                            
                        if my_lvl > other_lvl and placement > other_placement:
                            ランク差 = my_lvl - other_lvl
                            下剋上補正 -= (ランク差 * penalty_mult)
                    
                    final_pt = int(max(1, base_pt + 下剋上補正))
                    
                    if placement == 1: final_prize = int(total_prize * (race_p1_rate / 100))
                    elif placement == 2: final_prize = int(total_prize * (race_p2_rate / 100))
                    elif placement == 3: final_prize = int(total_prize * (race_p3_rate / 100))
                    else: final_prize = 0
                    
                    saved_pwd = st.session_state.racer_accounts.get(current_pilot["p_name"], "")
                    
                    records_to_add.append({
                        "レース日時": race_datetime_str,
                        "順位": placement,
                        "プレイヤー名": current_pilot["p_name"],
                        "使用車種": current_pilot["v_name"],
                        "コース名": final_course_name,
                        "獲得ポイント": final_pt,
                        "獲得賞金": final_prize,
                        "レース名": race_name,
                        "パスワードデータ": str(saved_pwd)
                    })
                
                new_df = pd.DataFrame(records_to_add)
                st.session_state.history_df = pd.concat([st.session_state.history_df, new_df], ignore_index=True)
                
                save_data_to_local_csv()
                st.session_state.save_success = f"保存完了: 「{race_name}」の結果をオートセーブしました！"
                st.rerun()

# ==========================================
# 【管理者専用】タブ：📝 履歴＆データ一括修正
# ==========================================
if tab_history:
    with tab_history:
        st.subheader("⚡ 名簿＆履歴の完全一括修正（誤字・表記揺れの修正）")
        if not player_names and not vehicle_names:
            st.info("データがありません。")
        else:
            col_rep1, col_rep2, col_rep3 = st.columns(3)
            replace_target = col_rep1.selectbox("修正対象のデータ", ["プレイヤー名", "使用車種", "コース名"])
            if replace_target == "プレイヤー名": options_list = player_names
            elif replace_target == "使用車種": options_list = vehicle_names
            else: options_list = course_names
            
            old_name = col_rep2.selectbox("修正前（古い記述）", ["選択してください"] + options_list)
            new_name = col_rep3.text_input("修正後（正しい記述）")
            
            if st.button("指定した名前を一括置換する", type="primary", use_container_width=True):
                if old_name != "選択してください" and new_name:
                    new_name = new_name.strip()
                    st.session_state.history_df.loc[st.session_state.history_df[replace_target] == old_name, replace_target] = new_name
                    
                    if replace_target == "プレイヤー名":
                        st.session_state.player_names = [new_name if x == old_name else x for x in st.session_state.player_names]
                        if old_name in st.session_state.racer_accounts:
                            st.session_state.racer_accounts[new_name] = st.session_state.racer_accounts.pop(old_name)
                    elif replace_target == "使用車種":
                        st.session_state.vehicle_names = [new_name if x == old_name else x for x in st.session_state.vehicle_names]
                    else:
                        st.session_state.course_names = [new_name if x == old_name else x for x in st.session_state.course_names]
                    
                    for name, pwd_str in st.session_state.racer_accounts.items():
                        st.session_state.history_df.loc[st.session_state.history_df["プレイヤー名"] == name, "パスワードデータ"] = str(pwd_str)
                        
                    save_data_to_local_csv()
                    st.success("一括置換処理が完了しました。")
                    st.rerun()

        st.divider()
        st.subheader("⚠️ 過去データの直接個別修正＆パスワードリセット用エディタ")
        edited_history = st.data_editor(st.session_state.history_df, num_rows="dynamic", use_container_width=True, key="history_editor")
        if st.button("エディタの変更内容でローカルファイルを上書き保存", type="primary"):
            edited_history = edited_history.fillna("")
            for col in ["順位", "獲得ポイント", "獲得賞金"]:
                if col in edited_history.columns:
                    edited_history[col] = pd.to_numeric(edited_history[col], errors='coerce').fillna(0).astype(int)
            st.session_state.history_df = edited_history
            save_data_to_local_csv()
            st.success("手動変更内容を完全に保存しました。")
            st.rerun()

# ==========================================
# 【管理者専用】タブ：⚙️ システム管理
# ==========================================
if tab_setting:
    with tab_setting:
        st.subheader("⚙️ レース報酬・ランクのルールチューニング")
        
        st.markdown("### ⚔️ ランク差連動型・下剋上倍率の調整")
        c_bonus_mult = st.session_state.get("gekokujo_bonus_multiplier", 2)
        c_penalty_mult = st.session_state.get("gekokujo_penalty_multiplier", 2)
        
        st.session_state.gekokujo_bonus_multiplier = st.slider(
            "🟩 下剋上ボーナス倍率（格上に勝った時：ランク差 × N点プラス）",
            min_value=0, max_value=5, value=int(c_bonus_mult), step=1, key="cfg_b_m"
        )
        st.session_state.gekokujo_penalty_multiplier = st.slider(
            "🟥 油断ペナルティ倍率（格下に負けた時：ランク差 × N点マイナス）",
            min_value=0, max_value=5, value=int(c_penalty_mult), step=1, key="cfg_p_m"
        )
        
        st.divider()
        
        st.markdown("### 🏆 ライセンス（クラス）の昇格条件pt")
        col_th1, col_th2, col_th3 = st.columns(3)
        st.session_state.rank_b_threshold = col_th1.number_input("Bクラス昇格に必要な累計pt", min_value=1, value=st.session_state.rank_b_threshold)
        st.session_state.rank_a_threshold = col_th2.number_input("Aクラス昇格に必要な累計pt", min_value=1, value=st.session_state.rank_a_threshold)
        st.session_state.rank_s_threshold = col_th3.number_input("Sクラス昇格に必要な累計pt", min_value=1, value=st.session_state.rank_s_threshold)

        st.divider()

        st.markdown("### 💾 データバックアップ・ポータル")
        col_down, col_up = st.columns(2)
        with col_down:
            if not st.session_state.history_df.empty:
                csv_data = st.session_state.history_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="マスターデータ(CSV)をダウンロード",
                    data=csv_data,
                    file_name=f"rev_master_backup_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        with col_up:
            uploaded_file = st.file_uploader("外部のバックアップCSVファイルをインポート", type=["csv"])
            if uploaded_file is not None:
                try:
                    loaded_df = pd.read_csv(uploaded_file, dtype={"パスワードデータ": str})
                    loaded_df["順位"] = pd.to_numeric(loaded_df["順位"], errors="coerce").fillna(0).astype(int)
                    loaded_df["獲得ポイント"] = pd.to_numeric(loaded_df["獲得ポイント"], errors="coerce").fillna(0).astype(int)
                    loaded_df["獲得賞金"] = pd.to_numeric(loaded_df["獲得賞金"], errors="coerce").fillna(0).astype(int)
                    st.session_state.history_df = loaded_df
                    save_data_to_local_csv()
                    st.success("同期完了。")
                except Exception as e:
                    st.error(f"ファイル展開エラー: {e}")

# ==========================================
# 【共通】タブ：🏆 総合ランキング（💡レース別閲覧の大革命）
# ==========================================
with tab_rank:
    st.subheader("🏆 GLOBAL LEADERBOARD")
    
    if not st.session_state.get("is_admin") and st.session_state.racer_name:
        st.write(f"ログイン中のレーサー: **{st.session_state.racer_name}**")
        
    clean_history = history_df[history_df["レース名"] != "SYSTEM_SIGNUP"] if not history_df.empty else history_df
        
    if clean_history.empty:
        st.info("レースデータがありません。")
    else:
        ranking_base = clean_history.groupby("プレイヤー名").agg(
            出走回数=("順位", "count"), 累計ポイント=("獲得ポイント", "sum"),
            通算獲得賞金=("獲得賞金", "sum"), 平均順位=("順位", "mean"),
            優勝回数=("順位", lambda x: (x == 1).sum())
        ).reset_index()
        ranking_base["平均順位"] = ranking_base["平均順位"].round(1)
        ranking_base["ランク"] = ranking_base["累計ポイント"].apply(lambda x: get_rank_info(x)[0])
        
        st.markdown("### 🥇 SEASON TOP 3 PILOTS")
        top3_df = ranking_base.sort_values("累計ポイント", ascending=False).head(3).reset_index(drop=True)
        
        for idx, row in top3_df.iterrows():
            rank_num = idx + 1
            if rank_num == 1:
                p_class, b_class, medal = "rank_gold", "badge-gold", "🥇 CHAMPION"
            elif rank_num == 2:
                p_class, b_class, medal = "rank_silver", "badge-silver", "🥈 2ND PLACE"
            else:
                p_class, b_class, medal = "rank_bronze", "badge-bronze", "🥉 3RD PLACE"
                
            st.markdown(f"""
            <div class="podium-container {p_class}">
                <div>
                    <span class="podium-badge {b_class}">{medal}</span> &nbsp;&nbsp;
                    <span class="podium-name">{row['プレイヤー名']}</span> &nbsp;
                    <span style="color:#666; font-size:0.9rem;">[{row['ランク']}]</span>
                </div>
                <div class="podium-stats">
                    {row['累計ポイント']} pt &nbsp;|&nbsp; 優勝: {row['優勝回数']}回 &nbsp;|&nbsp; 賞金: ${row['通算獲得賞金']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 💰 通算獲得賞金ランキング")
            prize_ranking = ranking_base.sort_values("通算獲得賞金", ascending=False)
            st.dataframe(prize_ranking[["プレイヤー名", "ランク", "通算獲得賞金", "出走回数"]], hide_index=True, use_container_width=True)
        with col2:
            st.markdown("##### 👑 シーズン累計ポイントランキング")
            point_ranking = ranking_base.sort_values("累計ポイント", ascending=False)
            st.dataframe(point_ranking[["プレイヤー名", "ランク", "累計ポイント", "優勝回数", "平均順位"]], hide_index=True, use_container_width=True)
            
        st.markdown("---")
        st.subheader("🔗 レーサー名をクリックして個別データを引き出す")
        selected_click_name = st.selectbox(
            "詳細データ（個人成績）を見たいレーサー名を選択してください", 
            ["選択してください"] + list(ranking_base["プレイヤー名"].unique()),
            key="ranking_click_detector"
        )
        if selected_click_name != "選択してください":
            st.session_state.selected_profile_racer = selected_click_name
            
        # 💡【ここが今回の大幅強化！】開催「時間（時・分）」まで完全に切り分けたレース別公式リザルト表示
        st.divider()
        st.subheader("🔍 レース別公式リザルト（1戦ごとに完全分離閲覧）")
        
        if not clean_history.empty:
            log_selector_df = clean_history.copy()
            
            # 🚨 「レース日時」文字列が空でないことを担保
            log_selector_df["レース日時"] = log_selector_df["レース日時"].fillna("不明")
            
            # プルダウンの見た目を極限まで分かりやすく整える（例： 🏁【2026-05-24 19:30】フリーレース ＠ アロヨ・グランプリ）
            log_selector_df["一意のレース識別ラベル"] = "🏁【" + log_selector_df["レース日時"].str.slice(0, 16) + "】 " + log_selector_df["レース名"] + " ＠ " + log_selector_df["コース名"]
            
            # 「レース日時」の降順（最新のレースが一番上にくるようにソート）
            log_selector_df = log_selector_df.sort_values("レース日時", ascending=False)
            
            # ソート順を維持したまま、重複のない綺麗な選択肢リストを作成
            unique_race_labels = []
            for lbl in log_selector_df["一意のレース識別ラベル"].unique():
                if lbl not in unique_race_labels:
                    unique_race_labels.append(lbl)
            
            selected_race_label = st.selectbox(
                "閲覧したい『開催枠』をプルダウンから選択してください（最新のレース順に並んでいます）", 
                unique_race_labels, 
                key="race_log_selector_v3"
            )
            
            if selected_race_label:
                # 🚨 他のレースと混ざらないよう、時・分・秒が完全に一致する「その1戦だけ」をピンポイント抽出
                matched_race_data = log_selector_df[log_selector_df["一意のレース識別ラベル"] == selected_race_label]
                
                # スタイリッシュデザインの表で表示（順位でソート）
                st.dataframe(
                    matched_race_data[["順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "コース名", "レース名", "レース日時"]].sort_values("順位"), 
                    hide_index=True, 
                    use_container_width=True
                )
        else:
            st.info("保存されている有効なレースログがありません。")

# ==========================================
# 【共通】タブ：🏎️ 分析スタッツ
# ==========================================
with tab_car:
    st.subheader("🏎️ SERVER PERFORMANCE STATISTICS")
    clean_history = history_df[history_df["レース名"] != "SYSTEM_SIGNUP"] if not history_df.empty else history_df
    
    if clean_history.empty:
        st.info("分析するためのレースデータが不足しています。")
    else:
        sub_tab_vehicle, sub_tab_course = st.tabs(["🏎️ 車種別データ分析", "🛣️ コース別データ分析"])
        
        with sub_tab_vehicle:
            car_df = clean_history[clean_history["使用車種"].notna() & (clean_history["使用車種"] != "")].groupby("使用車種").agg(
                使用回数=("順位", "count"), 平均順位=("順位", "mean"), 優勝回数=("順位", lambda x: (x == 1).sum())
            ).reset_index()
            car_df["平均順位"] = car_df["平均順位"].round(1)
            car_df["勝率(%)"] = ((car_df["優勝回数"] / car_df["使用回数"]) * 100).round(1)
            st.dataframe(car_df.sort_values("使用回数", ascending=False), hide_index=True, use_container_width=True)
            
        with sub_tab_course:
            if "コース名" in clean_history.columns and not clean_history[clean_history["コース名"] != "未登録"].empty:
                course_analysis_records = []
                grouped_course = clean_history.groupby("コース名")
                
                for c_name, c_group in grouped_course:
                    total_races_in_course = c_group["レース日時"].nunique()
                    total_runs = len(c_group)
                    
                    winners = c_group[c_group["順位"] == 1]
                    top_win_car = winners["使用車種"].value_counts().idxmax() if not winners.empty and len(winners["使用車種"].dropna().replace("", pd.NA).dropna()) > 0 else "なし"
                    top_used_car = c_group["使用車種"].value_counts().idxmax() if not c_group["使用車種"].dropna().empty and len(c_group["使用車種"].dropna().replace("", pd.NA).dropna()) > 0 else "なし"
                    
                    avg_placement = c_group["順位"].mean().round(1)
                    
                    course_analysis_records.append({
                        "開催コース名": c_name,
                        "総開催レース数": f"{total_races_in_course} 戦",
                        "総エントリー台数": f"{total_runs} 台",
                        "コース平均順位": avg_placement,
                        "最多優勝車種 (最強)": top_win_car,
                        "最多エントリー車種": top_used_car
                    })
                    
                st.dataframe(pd.DataFrame(course_analysis_records), hide_index=True, use_container_width=True)
            else:
                st.info("コースデータがまだありません。")

# ==========================================
# 【共通】タブ：👤 個人の成績確認
# ==========================================
with tab_personal:
    st.subheader("👤 PERSONAL TELEMETRY DASHBOARD")
    if not player_names:
        st.info("データに登録されているレーサーが見つかりません。")
    else:
        if st.session_state.selected_profile_racer in player_names:
            default_index = player_names.index(st.session_state.selected_profile_racer)
        elif st.session_state.racer_name in player_names:
            default_index = player_names.index(st.session_state.racer_name)
        else:
            default_index = 0
            
        target_player = st.selectbox("リザルトを確認したいレーサーを選択してください", player_names, index=default_index, key="profile_select_box")
        
        if target_player:
            clean_history = history_df[history_df["レース名"] != "SYSTEM_SIGNUP"] if not history_df.empty else history_df
            player_data = clean_history[clean_history["プレイヤー名"] == target_player]
            
            if player_data.empty:
                st.info("このドライバーの有効なレース出走データがまだありません。")
            else:
                total_races = len(player_data)
                total_prize = player_data["獲得賞金"].sum()
                total_points = player_data["獲得ポイント"].sum()
                win_count = (player_data["順位"] == 1).sum()
                avg_rank = player_data["順位"].mean().round(1)
                fav_car = player_data["使用車種"].value_counts().idxmax() if not player_data["使用車種"].replace("", pd.NA).dropna().empty else "データなし"
                
                current_rank, _ = get_rank_info(total_points)
                titles = []
                if total_prize >= 1000000: titles.append("💰 億万長者")
                elif total_prize >= 500000: titles.append("💸 賞金王")
                if win_count >= 3: titles.append("👑 ドリフトマスター")
                elif win_count >= 1: titles.append("⚡ スピードスター")
                
                st.markdown(f"### ドライバーリザルト: **{target_player}**")
                st.markdown(f"**現在の所持ライセンス:** {current_rank}  | **獲得称号:** {' / '.join(titles) if titles else '🌱'}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("出走回数", f"{total_races} 戦")
                m2.metric("通算獲得賞金", f"${total_prize:,}")
                m3.metric("累計ポイント", f"{total_points} pt")
                m4.metric("平均順位", f"{avg_rank} 位")
                st.markdown(f"**🚗 メインビークル (最多使用):** `{fav_car}`")
                
                st.markdown("<br>", unsafe_allow_html=True)
                display_cols = ["レース名", "コース名", "順位", "使用車種", "獲得ポイント", "獲得賞金", "レース日時"]
                st.dataframe(player_data[display_cols].sort_values("レース日時", ascending=False), hide_index=True, use_container_width=True)
