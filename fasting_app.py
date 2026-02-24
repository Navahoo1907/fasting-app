import streamlit as st
from datetime import datetime, timedelta

# --- Auto refresh (every 1 second) ---
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="tick")  # 1000 ms
except Exception:
    # Fallback: no hard refresh (still updates on interaction)
    pass

def parse_dt(dt_str: str) -> datetime | None:
    dt_str = dt_str.strip()
    fmts = [
        "%d.%m.%Y %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M",
        "%d.%m.%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]
    for f in fmts:
        try:
            return datetime.strptime(dt_str, f)
        except ValueError:
            pass
    return None

def format_td_smart(td: timedelta, hide_zero_days=True, hide_zero_hours=True) -> str:
    """
    Example:
      2 gün 46 dakika 24 sn   (hours omitted if 0)
      5 saat 03 dakika 10 sn  (days omitted if 0)
      46 dakika 24 sn         (days+hours omitted if 0)
    """
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        total_seconds = 0

    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []

    if not (hide_zero_days and days == 0):
        if days > 0:
            parts.append(f"{days} gün")

    if not (hide_zero_hours and hours == 0):
        if hours > 0:
            parts.append(f"{hours} saat")

    # minutes & seconds always shown
    parts.append(f"{minutes} dakika")
    parts.append(f"{seconds} sn")

    return " ".join(parts)

st.set_page_config(page_title="72h Fast Countdown", page_icon="⏳", layout="centered")
st.title("⏳ 72h Fast Countdown")

# Sidebar
default_start = "23.02.2026 20:00"
default_hours = 72

with st.sidebar:
    st.header("Ayarlar")
    start_str = st.text_input("Başlangıç (örn: 23.02.2026 20:00)", value=default_start)
    hours = st.number_input("Süre (saat)", min_value=1, max_value=240, value=default_hours, step=1)

start_dt = parse_dt(start_str)
if not start_dt:
    st.error("Tarih formatını anlayamadım. Örn: 23.02.2026 20:00")
    st.stop()

finish_dt = start_dt + timedelta(hours=int(hours))
now = datetime.now()

remaining = finish_dt - now
elapsed = now - start_dt

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kalan")
    if remaining.total_seconds() <= 0:
        st.success("🎉 Bitti!")
    st.metric("Time remaining", format_td_smart(remaining, hide_zero_days=False, hide_zero_hours=True))

with col2:
    st.subheader("Geçen")
    if now < start_dt:
        st.info("Henüz başlamadı.")
        st.metric("Elapsed", "0 dakika 0 sn")
    else:
        # Hide "0 gün" in elapsed, hide "0 saat" too
        st.metric("Elapsed", format_td_smart(elapsed, hide_zero_days=True, hide_zero_hours=True))

st.divider()
st.write(f"**Start:** {start_dt.strftime('%d.%m.%Y %H:%M')}")
st.write(f"**Finish:** {finish_dt.strftime('%d.%m.%Y %H:%M')}")
st.write(f"**Now:** {now.strftime('%d.%m.%Y %H:%M:%S')}")