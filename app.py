import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

st.set_page_config(page_title="REV AGENCY", layout="wide")

SAVE_FILE_NAME = "rev_racing_data.csv"

# ==========================================
# 🎨 究極グラフィック：超視認性ネオンサイバースキン（CSS）
# ==========================================
st.markdown("""
<style>
/* 画面全体を重厚な超漆黒に固定 */
.stApp {
    background: #040406 !important;
    color: #ffffff !important;
    font-family: 'Inter', 'Space Grotesk', 'Hiragino Kaku Gothic ProN', sans-serif !important;
}

/* サブタイトル：文字単体で魅せるミニマルデザイン */
.subtitle-text {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 12px;
    color: #ffffff !important;
    text-align: center;
    text-transform: uppercase;
    margin-top: 15px;
    margin-bottom: 40px;
    text-shadow: 0px 0px 15px rgba(255, 0, 60, 0.4);
}

/* フォーム・カード：視認性の高いエッジ */
div[data-testid="stForm"], div[data-testid="stExpander"], .custom-panel {
    background: linear-gradient(145deg, #0d0d14, #07070a) !important;
    border: 1px solid #2a1a20 !important;
    border-radius: 6px !important;
    padding: 30px !important;
    box-shadow: 0 15px 50px rgba(0,0,0,0.9) !important;
}

/* ヘッダー専用トグルボックスの微調整 */
div[data-testid="stHeader"] {
    background: transparent !important;
}

/* 入力エリア・セレクトボックスの文字を100%白くクリアに固定 */
input[type="text"], input[type="password"], input[type="number"], select, div[data-baseweb="select"] {
    background-color: #181825 !important;
    color: #ffffff !important;
    border: 1px solid #3f3f4e !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
}
/* ドロップダウンポップアップ内の暗転対策 */
div[data-shaded="true"], ul[role="listbox"], li[role="option"], div[role="presentation"] {
    background-color: #181825 !important;
    color: #ffffff !important;
}
input:focus {
    border-color: #ff003c !important;
    box-shadow: 0 0 15px rgba(255, 0, 60, 0.4) !important;
}

/* メトリクス */
div[data-testid="stMetricValue"] {
    color: #ff003c !important;
    font-style: italic;
    font-weight: 955;
    font-size: 2.8rem;
    letter-spacing: -1px;
    filter: drop-shadow(0 0 10px rgba(255, 0, 60, 0.6));
}
div[data-testid="stMetricLabel"] p {
    color: #a1a1aa !important;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.8rem !important;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #11111a, #08080c) !important;
    border: 1px solid #2e1e22 !important;
    border-radius: 6px !important;
    padding: 15px 20px !important;
}

/* ボタン共通規格 */
button[kind="primary"], button[kind="secondary"] {
    border: none !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    font-style: italic !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
    transition: all 0.15s ease-in-out !important;
}
button[kind="primary"] {
    background: linear-gradient(90deg, #ff003c, #cc0030) !important;
    box-shadow: 0px 4px 20px rgba(255, 0, 60, 0.4) !important;
}
button[kind="primary"]:hover {
    background: linear-gradient(90deg, #ff2a5f, #ff003c) !important;
    box-shadow: 0px 0px 25px rgba(255, 0, 60, 0.8) !important;
}
/* ヘッダー専用フラットセカンダリボタン */
button[key^="btn_nav_"], button[key="header_logout_trigger"] {
    background: #181825 !important;
    border: 1px solid #3f3f4e !important;
    height: 42px !important;
    font-size: 0.85rem !important;
}
button[key^="btn_nav_"]:hover, button[key="header_logout_trigger"]:hover {
    border-color: #ff003c !important;
    background: #221216 !important;
    color: #ff003c !important;
}

/* タブ */
button[data-baseweb="tab"] {
    color: #71717a !important;
    font-weight: 800 !important;
    letter-spacing: 2px !important;
    font-size: 0.9rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ff003c !important;
    border-bottom: 3px solid #ff003c !important;
    text-shadow: 0 0 10px rgba(255, 0, 60, 0.5);
}

/* データフレーム */
div[data-testid="stDataFrame"] {
    background-color: #08080c !important;
    border: 1px solid #272732 !important;
}
.rendered_html th {
    background-color: #12121a !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    border-bottom: 2px solid #ff003c !important;
}
.rendered_html td {
    background-color: #08080c !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* 🥇 表彰台ハイライトカード */
.podium-container {
    border-radius: 6px;
    padding: 16px 24px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}
.rank-gold { 
    background: linear-gradient(90deg, rgba(255, 215, 0, 0.18), rgba(0,0,0,0)) !important; 
    border: 1px solid rgba(255, 215, 0, 0.4) !important;
    border-left: 6px solid #ffd700 !important; 
}
.rank-silver { 
    background: linear-gradient(90deg, rgba(161, 161, 170, 0.15), rgba(0,0,0,0)) !important; 
    border: 1px solid rgba(161, 161, 170, 0.3) !important;
    border-left: 6px solid #a1a1aa !important; 
}
.rank-bronze { 
    background: linear-gradient(90deg, rgba(205, 127, 50, 0.15), rgba(0,0,0,0)) !important; 
    border: 1px solid rgba(205, 127, 50, 0.3) !important;
    border-left: 6px solid #cd7f32 !important; 
}

.podium-badge {
    font-size: 0.75rem;
    font-weight: 950;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 3px;
    text-transform: uppercase;
}
.badge-gold { background: #ffd700; color: #000 !important; font-weight:900; box-shadow: 0 0 10px rgba(255,215,0,0.5); }
.badge-silver { background: #a1a1aa; color: #000 !important; }
.badge-bronze { background: #cd7f32; color: #000 !important; }
.podium-name { font-size: 1.4rem; font-weight: 900; color: #ffffff !important; font-style: italic; }
.podium-stats { font-size: 1.15rem; font-weight: 900; color: #ff003c !important; font-style: italic; text-shadow: 0 0 8px rgba(255,0,60,0.4); }

.section-title {
    font-style: italic;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #FFFFFF, #FF003C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 30px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 💾 データプロセッサ＆初期化設定
# ==========================================
if "current_season" not in st.session_state: st.session_state.current_season = "Season 1"
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "show_admin_auth_input" not in st.session_state: st.session_state.show_admin_auth_input = False

if os.path.exists(SAVE_FILE_NAME):
    try:
        loaded_df = pd.read_csv(SAVE_FILE_NAME, dtype={"パスワードデータ": str, "レース日時": str, "シーズン": str})
        for col in ["順位", "獲得ポイント", "獲得賞金"]:
            loaded_df[col] = pd.to_numeric(loaded_df[col], errors="coerce").fillna(0).astype(int)
        if "シーズン" not in loaded_df.columns: loaded_df["シーズン"] = "Season 1"
        st.session_state.history_df = loaded_df
        
        existing_seasons = loaded_df["シーズン"].dropna().unique()
        if len(existing_seasons) > 0:
            sorted_seasons = sorted(list(existing_seasons))
            st.session_state.current_season = sorted_seasons[-1]
            
        st.session_state.player_names = sorted(list(set(loaded_df["プレイヤー名"].unique())))
        st.session_state.vehicle_names = sorted(list(set(loaded_df["使用車種"].dropna().unique()))) if "使用車種" in loaded_df.columns else []
        st.session_state.course_names = sorted(list(set(loaded_df["コース名"].dropna().unique()))) if "コース名" in loaded_df.columns else []
    except:
        st.session_state.history_df = pd.DataFrame(columns=["レース日時", "順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "レース名", "コース名", "パスワードデータ", "シーズン"])
else:
    if "history_df" not in st.session_state:
        st.session_state.history_df = pd.DataFrame(columns=["レース日時", "順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "レース名", "コース名", "パスワードデータ", "シーズン"])

if "racer_accounts" not in st.session_state: st.session_state.racer_accounts = {}
if "player_names" not in st.session_state: st.session_state.player_names = []
if "vehicle_names" not in st.session_state: st.session_state.vehicle_names = []
if "course_names" not in st.session_state: st.session_state.course_names = []

def save_data_to_local_csv():
    st.session_state.history_df.to_csv(SAVE_FILE_NAME, index=False, encoding='utf-8-sig')

if not st.session_state.history_df.empty and "パスワードデータ" in st.session_state.history_df.columns:
    for _, row in st.session_state.history_df.iterrows():
        p_name = row["プレイヤー名"]
        p_pwd = str(row.get("パスワードデータ", "")).strip()
        if p_pwd.endswith(".0"): p_pwd = p_pwd[:-2]
        if p_name and p_pwd and p_pwd not in ["nan", ""]:
            st.session_state.racer_accounts[p_name] = p_pwd

for name in st.session_state.racer_accounts.keys():
    if name not in st.session_state.player_names: st.session_state.player_names.append(name)
st.session_state.player_names.sort()

if "rank_b_threshold" not in st.session_state: st.session_state.rank_b_threshold = 50
if "rank_a_threshold" not in st.session_state: st.session_state.rank_a_threshold = 150
if "rank_s_threshold" not in st.session_state: st.session_state.rank_s_threshold = 300
if "gekokujo_bonus_multiplier" not in st.session_state: st.session_state.gekokujo_bonus_multiplier = 2  
if "gekokujo_penalty_multiplier" not in st.session_state: st.session_state.gekokujo_penalty_multiplier = 2 

def get_rank_info(pt):
    b = st.session_state.rank_b_threshold
    a = st.session_state.rank_a_threshold
    s = st.session_state.rank_s_threshold
    if pt < b: return "C", 1
    elif pt < a: return "B", 2
    elif pt < s: return "A", 3
    else: return "S", 4

player_names = st.session_state.player_names
vehicle_names = st.session_state.vehicle_names
course_names = st.session_state.course_names
history_df = st.session_state.history_df

current_season_data = history_df[history_df["シーズン"] == st.session_state.current_season] if not history_df.empty else pd.DataFrame()
player_totals = current_season_data.groupby("プレイヤー名")["獲得ポイント"].sum().to_dict() if not current_season_data.empty else {}

# ==========================================
# 🔐 超精密水平アライメント・ヘッダー
# ==========================================
ADMIN_PASSWORD = "rev123"
if "racer_name" not in st.session_state: st.session_state.racer_name = None
if "gate_mode" not in st.session_state: st.session_state.gate_mode = "login"

col_header_left, col_header_right = st.columns([3, 2])

with col_header_left:
    if not st.session_state.is_admin and st.session_state.racer_name:
        st.markdown(f"<div style='padding-top:12px; color:#a1a1aa; font-size:0.95rem; font-weight:800; letter-spacing:1px;'>RACER ID: <span style='color:#ffffff; font-style:italic;'>{st.session_state.racer_name.upper()}</span></div>", unsafe_allow_html=True)
    elif st.session_state.is_admin:
        st.markdown("<div style='padding-top:12px; color:#ff003c; font-size:0.95rem; font-weight:800; letter-spacing:1px; font-style:italic;'>⚙️ SYSTEM ADMINISTRATOR MODE</div>", unsafe_allow_html=True)

with col_header_right:
    c_btn_adm, c_btn_logo = st.columns(2)
    with c_btn_adm:
        adm_label = "🔒 認証解除" if st.session_state.is_admin else "🔑 運営スタッフ認証"
        if st.button(adm_label, use_container_width=True, key="btn_nav_admin_toggle"):
            if st.session_state.is_admin:
                st.session_state.is_admin = False
                st.session_state.show_admin_auth_input = False
                st.rerun()
            else:
                st.session_state.show_admin_auth_input = not st.session_state.show_admin_auth_input
                st.rerun()
                
    with c_btn_logo:
        if st.session_state.is_admin or st.session_state.racer_name is not None:
            if st.button("🚪 ログアウト", use_container_width=True, key="header_logout_trigger"):
                st.session_state.is_admin = False
                st.session_state.racer_name = None
                st.session_state.show_admin_auth_input = False
                st.session_state.gate_mode = "login"
                st.rerun()

if st.session_state.show_admin_auth_input and not st.session_state.is_admin:
    _, col_auth_box = st.columns([3, 2])
    with col_auth_box:
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        pwd_input = st.text_input("運営用パスワードキーを入力", type="password", placeholder="PASSWORD...", key="fields_stealth_auth")
        if pwd_input == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.session_state.show_admin_auth_input = False
            st.rerun()

st.markdown("<hr style='margin-top:12px; margin-bottom:20px;'>", unsafe_allow_html=True)

# ==========================================
# 🖼️ メインロゴ ＆ サブタイトル
# ==========================================
logo_file = "logo.png"
if os.path.exists(logo_file):
    col1, col2, col3 = st.columns([1.8, 1, 1.8]) 
    with col2: st.image(logo_file, use_container_width=True)

st.markdown('<div class="subtitle-text">DATA TELEMETRY SYSTEM</div>', unsafe_allow_html=True)

# ==========================================
# 🏁 ゲート認証画面
# ==========================================
if not st.session_state.is_admin and st.session_state.racer_name is None:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_gate, _ = st.columns([1, 1.4, 1])
    with col_gate:
        if st.session_state.gate_mode == "login":
            st.markdown("### 既存レーサー ログイン")
            login_name_input = st.text_input("レーサー名", placeholder="名前を入力...")
            login_pwd_input = st.text_input("パスワード", type="password", placeholder="••••••••")
            
            if player_names:
                options_html = "".join([f'<option value="{name}">' for name in player_names])
                st.markdown(f"""<script>const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                inputs.forEach(input => {{ if (input.placeholder && input.placeholder.includes("名前")) input.setAttribute('list', 'p_list'); }});
                </script><datalist id="p_list">{options_html}</datalist>""", unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ダッシュボードに入る", type="primary", use_container_width=True):
                l_name = login_name_input.strip()
                l_pwd = login_pwd_input.strip()
                if l_name in st.session_state.racer_accounts and str(st.session_state.racer_accounts[l_name]) == l_pwd:
                    st.session_state.racer_name = l_name
                    st.rerun()
                elif l_name in player_names and l_name not in st.session_state.racer_accounts:
                    st.session_state.racer_accounts[l_name] = l_pwd
                    st.session_state.racer_name = l_name
                    st.rerun()
                else:
                    st.error("認証に失敗しました。")
            
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            if st.button("新規レーサー登録はこちら", use_container_width=True):
                st.session_state.gate_mode = "signup"
                st.rerun()
                    
        else:
            st.markdown("### 新規レーサー登録")
            reg_name_input = st.text_input("登録するレーサー名", placeholder="例：Ryunosuke...")
            reg_pwd_input = st.text_input("パスワードを設定", type="password", placeholder="••••••••")
            reg_pwd_confirm = st.text_input("パスワード（確認用）", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("公式アカウント作成", type="primary", use_container_width=True):
                r_name = reg_name_input.strip()
                r_pwd = reg_pwd_input.strip()
                if r_name and r_pwd == reg_pwd_confirm.strip() and r_name not in player_names:
                    st.session_state.racer_accounts[r_name] = r_pwd
                    st.session_state.player_names.append(r_name)
                    new_row = pd.DataFrame([{"レース日時": datetime.now().strftime("%Y-%m-%d %H:%M"), "順位": 0, "プレイヤー名": r_name, "使用車種": "新規登録", "コース名": "ロビー", "獲得ポイント": 0, "獲得賞金": 0, "レース名": "SYSTEM_SIGNUP", "パスワードデータ": r_pwd, "シーズン": st.session_state.current_season}])
                    st.session_state.history_df = pd.concat([st.session_state.history_df, new_row], ignore_index=True)
                    save_data_to_local_csv()
                    st.session_state.racer_name = r_name
                    st.rerun()
                else:
                    st.error("入力内容が無効か、既に登録されている名前です。")
            
            st.markdown("<br><hr><br>", unsafe_allow_html=True)
            if st.button("ログイン画面に戻る", use_container_width=True):
                st.session_state.gate_mode = "login"
                st.rerun()
    st.stop()

# ==========================================
# 🚀 モード別タブ展開
# ==========================================
if st.session_state.is_admin:
    tabs = st.tabs(["📝 レース結果入力", "🛠️ 履歴＆一括置換修正", "🏆 総合ランキング", "📊 サーバーデータ分析", "👤 個人成績ログ", "⚙️ 条件＆シーズン管理"])
    tab_input, tab_history, tab_rank, tab_car, tab_personal, tab_setting = tabs
else:
    tabs = st.tabs(["🏆 総合ランキング", "📊 サーバーデータ分析", "👤 個人成績ログ"])
    tab_rank, tab_car, tab_personal = tabs
    tab_input, tab_history, tab_setting = None, None, None

# ==========================================
# タブ：レース結果入力
# ==========================================
if tab_input:
    with tab_input:
        st.markdown(f"##### 📢 現在記録中のシーズン: **{st.session_state.current_season}**")
        if st.session_state.get("save_success"): st.success(st.session_state.save_success); st.session_state.save_success = ""
        
        col_c, col_p = st.columns([1, 2])
        p_count = col_c.number_input("今回の出走人数 (グリッド数)", min_value=1, max_value=30, value=3)
        total_prize = col_p.number_input("賞金総額 ($)", min_value=0, value=1000000, step=50000)

        with st.form("race_input_ultimate"):
            col_r1, col_r2, col_r3 = st.columns(3)
            p1_r = col_r1.number_input("1位の配分率 (%)", min_value=0, max_value=100, value=50)
            p2_r = col_r2.number_input("2位の配分率 (%)", min_value=0, max_value=100, value=30)
            p3_r = col_r3.number_input("3位の配分率 (%)", min_value=0, max_value=100, value=20)
            
            col_n, col_co, col_d, col_t = st.columns([2, 2, 1, 1])
            jst = pytz.timezone('Asia/Tokyo')
            r_name = col_n.text_input("レース・イベント名", value="フリーレース")
            c_name_in = col_co.text_input("開催コース名", placeholder="コースを入力...", value="アロヨ・グランプリ")
            r_date = col_d.date_input("開催日", datetime.now(jst).date())
            r_time = col_t.time_input("開催時刻", datetime.now(jst).time(), step=60)

            st.markdown("---")
            input_results = []
            for i in range(int(p_count)):
                st.markdown(f"**【 {i+1} 位 】**")
                c1, c2 = st.columns(2)
                p_name = c1.selectbox(f"ドライバー枠_{i+1}", player_names, key=f"p_sel_{i+1}", label_visibility="collapsed")
                v_name = c2.text_input(f"車種枠_{i+1}", placeholder="使用車種を入力...", key=f"v_in_{i+1}", label_visibility="collapsed").strip()
                input_results.append({"順位": i+1, "プレイヤー名": p_name, "使用車種": v_name})

            vehicle_options_html = "".join([f'<option value="{car}">' for car in vehicle_names])
            course_options_html = "".join([f'<option value="{c_name}">' for c_name in course_names])
            st.markdown(f"""<script>
                const formInputs = window.parent.document.querySelectorAll('input[type="text"]');
                formInputs.forEach(input => {{
                    if (input.placeholder && input.placeholder.includes("使用車種")) input.setAttribute('list', 'v_list');
                    if (input.placeholder && input.placeholder.includes("コース")) input.setAttribute('list', 'c_list');
                }});
            </script><datalist id="v_list">{vehicle_options_html}</datalist><datalist id="c_list">{course_options_html}</datalist>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("レース結果を公式記録にセーブ", type="primary"):
                race_datetime_str = f"{r_date} {r_time.strftime('%H:%M')}:00"
                f_course = c_name_in.strip()
                if f_course and not any(res["プレイヤー名"] is None for res in input_results):
                    if f_course not in st.session_state.course_names: st.session_state.course_names.append(f_course)
                    
                    participants = []
                    for res in input_results:
                        if res["使用車種"] and res["使用車種"] not in st.session_state.vehicle_names: st.session_state.vehicle_names.append(res["使用車種"])
                        pt = player_totals.get(res["プレイヤー名"], 0)
                        _, lvl = get_rank_info(pt)
                        participants.append({"placement": res["順位"], "p_name": res["プレイヤー名"], "v_name": res["使用車種"], "rank_lvl": lvl})
                    
                    st.session_state.vehicle_names.sort(); st.session_state.course_names.sort()
                    records = []
                    b_mult = st.session_state.get("gekokujo_bonus_multiplier", 2)
                    p_mult = st.session_state.get("gekokujo_penalty_multiplier", 2)
                    
                    for cur in participants:
                        b_pt = max(2, 12 - (cur["placement"] * 2))
                        補正 = 0
                        for oth in participants:
                            if cur["p_name"] == oth["p_name"]: continue
                            if cur["rank_lvl"] < oth["rank_lvl"] and cur["placement"] < oth["placement"]:
                                補正 += ((oth["rank_lvl"] - cur["rank_lvl"]) * b_mult)
                            if cur["rank_lvl"] > oth["rank_lvl"] and cur["placement"] > oth["placement"]:
                                補正 -= ((cur["rank_lvl"] - oth["rank_lvl"]) * p_mult)
                        
                        f_prize = int(total_prize * (p1_r/100 if cur["placement"]==1 else p2_r/100 if cur["placement"]==2 else p3_r/100 if cur["placement"]==3 else 0))
                        records.append({
                            "レース日時": race_datetime_str, "順位": cur["placement"], "プレイヤー名": cur["p_name"], "使用車種": cur["v_name"],
                            "コース名": f_course, "獲得ポイント": int(max(1, b_pt + 補正)), "獲得賞金": f_prize, "レース名": r_name, 
                            "パスワードデータ": str(st.session_state.racer_accounts.get(cur["p_name"], "")), "シーズン": st.session_state.current_season
                        })
                    st.session_state.history_df = pd.concat([st.session_state.history_df, pd.DataFrame(records)], ignore_index=True)
                    save_data_to_local_csv()
                    st.session_state.save_success = "レース結果を安全に同期し、ロックしました。"
                    st.rerun()

# ==========================================
# タブ：🛠️ 履歴＆一括置換修正
# ==========================================
if tab_history:
    with tab_history:
        st.markdown("### 指定表記の一括置換（表記揺れ・誤字修正用）")
        col_t, col_o, col_n = st.columns(3)
        target = col_t.selectbox("修正対象カラム", ["プレイヤー名", "使用車種", "コース名"])
        options = player_names if target=="プレイヤー名" else vehicle_names if target=="使用車種" else course_names
        old = col_o.selectbox("置換前のデータ", ["置換する名簿を選択してください..."] + options)
        new = col_n.text_input("置換後の正しいデータ（確定文字列）").strip()
        if st.button("一括置換処理を実行する", type="primary") and old != "置換する名簿を選択してください..." and new:
            st.session_state.history_df.loc[st.session_state.history_df[target] == old, target] = new
            save_data_to_local_csv()
            st.success("指定されたデータの一括置換が完了しました。")
            st.rerun()

        st.markdown("<br>### データベース・直接個別修正エディタ", unsafe_allow_html=True)
        ed = st.data_editor(st.session_state.history_df, num_rows="dynamic", use_container_width=True)
        if st.button("エディタの変更内容でCSVを上書き保存"):
            st.session_state.history_df = ed
            save_data_to_local_csv()
            st.success("エディタの変更内容を永久セーブしました。")
            st.rerun()

# ==========================================
# タブ：⚙️ 条件＆シーズン管理（💡ズレを完全修正完了）
# ==========================================
if tab_setting:
    with tab_setting:
        st.markdown("### 🏁 シーズン移行管理（終了と次シーズン始動）")
        st.info(f"現在の稼働シーズン： **{st.session_state.current_season}**")
        
        try:
            current_num = int(st.session_state.current_season.replace("Season ", ""))
            next_season_guess = f"Season {current_num + 1}"
        except:
            next_season_guess = "Season 2"
            
        # 💡横並びを完全に辞め、縦一列のソリッドなブロック構造に再配置
        next_season_input = st.text_input("次期シーズンの名称を設定してください", value=next_season_guess)
        
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🔥 上記の名称でシーズンを終了して次へ移行する", type="primary", use_container_width=True):
            if next_season_input.strip():
                st.session_state.current_season = next_season_input.strip()
                st.success(f"新しいシーズン【 {st.session_state.current_season} 】が開始されました！")
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 下剋上（ジャイアントキリング）システム・倍率設定")
        st.session_state.gekokujo_bonus_multiplier = st.slider("🟩 下剋上ボーナス倍率（格上に勝った時：ランク差 × N点プラス）", 0, 5, int(st.session_state.get("gekokujo_bonus_multiplier", 2)))
        st.session_state.gekokujo_penalty_multiplier = st.slider("🟥 油断ペナルティ倍率（格下に負けた時：ランク差 × N点マイナス）", 0, 5, int(st.session_state.get("gekokujo_penalty_multiplier", 2)))
        
        st.markdown("<br>### 各ライセンス（クラス）スレッショルド境界設定", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        st.session_state.rank_b_threshold = c1.number_input("Bクラス昇格条件pt", value=st.session_state.rank_b_threshold)
        st.session_state.rank_a_threshold = c2.number_input("Aクラス昇格条件pt", value=st.session_state.rank_a_threshold)
        st.session_state.rank_s_threshold = c3.number_input("Sクラス昇格条件pt", value=st.session_state.rank_s_threshold)

# ==========================================
# タブ：🏆 総合ランキング
# ==========================================
with tab_rank:
    clean_df = history_df[history_df["レース名"] != "SYSTEM_SIGNUP"] if not history_df.empty else history_df
    
    if clean_df.empty:
        st.info("レースデータがありません。")
    else:
        all_seasons_available = ["📊 全シーズン累計"] + sorted(list(clean_df["シーズン"].dropna().unique()), reverse=True)
        selected_season_scope = st.selectbox("🏆 集計対象のシーズンを選択", all_seasons_available, key="rank_season_selector")
        
        if selected_season_scope == "📊 全シーズン累計":
            scope_df = clean_df
        else:
            scope_df = clean_df[clean_df["シーズン"] == selected_season_scope]
            
        if scope_df.empty:
            st.info("選択されたシーズンの有効なレースデータはありません。")
        else:
            base = scope_df.groupby("プレイヤー名").agg(出走=("順位", "count"), pt=("獲得ポイント", "sum"), 賞金=("獲得賞金", "sum"), 優勝=("順位", lambda x: (x == 1).sum())).reset_index()
            base["RANK"] = base["pt"].apply(lambda x: get_rank_info(x)[0])
            
            st.markdown(f"### 🥇 {selected_season_scope.upper()} トップ表彰台")
            top3 = base.sort_values("pt", ascending=False).head(3).reset_index(drop=True)
            for idx, row in top3.iterrows():
                m = "🥇 CHAMPION" if idx==0 else "🥈 2ND PLACE" if idx==1 else "🥉 3RD PLACE"
                c = "rank_gold" if idx==0 else "rank_silver" if idx==1 else "rank_bronze"
                b = "badge-gold" if idx==0 else "badge-silver" if idx==1 else "badge-bronze"
                st.markdown(f"""
                <div class="podium-container {c}">
                    <div>
                        <span class="podium-badge {b}">{m}</span> &nbsp;&nbsp;
                        <span class="podium-name">{row['プレイヤー名']}</span> &nbsp;
                        <span style='color:#a1a1aa; font-size:0.85rem;'>[{row['RANK']}]</span>
                    </div>
                    <div class="podium-stats">
                        {row['pt']} pt &nbsp;|&nbsp; 優勝: {row['優勝']}回 &nbsp;|&nbsp; ${row['賞金']:,}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br><hr>", unsafe_allow_html=True)
            
            st.markdown('<div class="section-title">👑 ポイントリーダーボード</div>', unsafe_allow_html=True)
            st.dataframe(base.sort_values("pt", ascending=False)[["プレイヤー名", "RANK", "pt", "優勝", "出走"]], hide_index=True, use_container_width=True)
            
            st.markdown('<div class="section-title">💰 マネーリーダーボード</div>', unsafe_allow_html=True)
            st.dataframe(base.sort_values("賞金", ascending=False)[["プレイヤー名", "RANK", "賞金", "優勝", "出走"]], hide_index=True, use_container_width=True)
                
            st.markdown('<br><div class="section-title">🔍 テレメトリーアーカイブ (過去ログ・振り返り)</div>', unsafe_allow_html=True)
            log_df = scope_df.copy()
            log_df["LABEL"] = "🏁 【" + log_df["レース日時"].str.slice(0, 16) + "】 " + log_df["レース名"] + " @ " + log_df["コース名"]
            labels = list(log_df.sort_values("レース日時", ascending=False)["LABEL"].unique())
            
            sel_label = st.selectbox("閲覧するレースを選択", labels, label_visibility="collapsed")
            if sel_label:
                st.dataframe(log_df[log_df["LABEL"] == sel_label][["順位", "プレイヤー名", "使用車種", "獲得ポイント", "獲得賞金", "コース名", "レース日時"]].sort_values("順位"), hide_index=True, use_container_width=True)

# ==========================================
# タブ：📊 サーバーデータ分析
# ==========================================
with tab_car:
    clean_df = history_df[history_df["レース名"] != "SYSTEM_SIGNUP"] if not history_df.empty else history_df
    if clean_df.empty:
        st.info("データが蓄積されていません。")
    else:
        sub_v, sub_c = st.tabs(["🏎️ 車種別・性能分析", "🛣️ コース別・最速統計"])
        with sub_v:
            v_df = clean_df.groupby("使用車種").agg(出走=("順位", "count"), 平均順位=("順位", "mean"), 優勝=("順位", lambda x: (x == 1).sum())).reset_index()
            v_df["勝率(%)"] = ((v_df["優勝"] / v_df["出走"]) * 100).round(1)
            st.dataframe(v_df.sort_values("出走", ascending=False), hide_index=True, use_container_width=True)
        with sub_c:
            c_records = []
            for c_name, c_group in clean_df.groupby("コース名"):
                win_df = c_group[c_group["順位"] == 1]
                t_racer = win_df["プレイヤー名"].value_counts().idxmax() if not win_df.empty else "データなし"
                t_car = win_df["使用車種"].value_counts().idxmax() if not win_df.empty and len(win_df["使用車種"].dropna())>0 else "データなし"
                m_car = c_group["使用車種"].value_counts().idxmax() if not c_group["使用車種"].dropna().empty else "データなし"
                c_records.append({"開催コース名": c_name, "総開催レース数": f"{c_group['レース日時'].nunique()}戦", "総エントリー数": f"{len(c_group)}台", "最多勝レーサー (得意)": t_racer, "最多選抜車両 (人気)": m_car, "最多優勝車両 (最速)": t_car})
            st.dataframe(pd.DataFrame(c_records), hide_index=True, use_container_width=True)

# ==========================================
# タブ：👤 個人成績ログ
# ==========================================
with tab_personal:
    if not player_names:
        st.info("登録されているレーサーがいません。")
    else:
        d_idx = player_names.index(st.session_state.racer_name) if st.session_state.racer_name in player_names else 0
        target = st.selectbox("確認したいレーサーを選択", player_names, index=d_idx, label_visibility="collapsed")
        
        p_data = history_df[(history_df["プレイヤー名"] == target) & (history_df["レース名"] != "SYSTEM_SIGNUP")]
        if p_data.empty:
            st.info("このレーサーの公式出走ログはまだありません。")
        else:
            cur_rank, _ = get_rank_info(p_data[p_data["シーズン"] == st.session_state.current_season]["獲得ポイント"].sum())
            st.markdown(f"<div class='section-title' style='font-size:1.8rem; margin-top:10px;'>👤 レーサー名: {target.upper()} <span style='color:#ff003c; font-size:1.1rem; font-style:italic; margin-left:15px;'>{st.session_state.current_season} / CLASS {cur_rank}</span></div>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("通算公式出走数", f"{len(p_data)} 戦")
            c2.metric("通算総獲得賞金", f"${p_data['獲得賞金'].sum():,}")
            c3.metric("全期間累計ポイント", f"{p_data['獲得ポイント'].sum()} pt")
            c4.metric("生涯平均アベレージ", f"{p_data['順位'].mean().round(1)} 位")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(p_data[["シーズン", "レース名", "コース名", "順位", "使用車種", "獲得ポイント", "獲得賞金", "レース日時"]].sort_values("レース日時", ascending=False), hide_index=True, use_container_width=True)
