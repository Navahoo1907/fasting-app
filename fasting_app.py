import streamlit as st
from datetime import datetime, timedelta

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="tick")
except:
    pass

def parse_dt(s):
    for f in ("%d.%m.%Y %H:%M","%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s,f)
        except:
            pass
    return None

def format_td(td):
    s=int(max(td.total_seconds(),0))
    d,s=divmod(s,86400)
    h,s=divmod(s,3600)
    m,s=divmod(s,60)

    parts=[]
    if d>0: parts.append(f"{d} gün")
    if h>0: parts.append(f"{h} saat")
    parts.append(f"{m} dakika")
    parts.append(f"{s} saniye")
    return " ".join(parts)

st.set_page_config(page_title="72 Saat Açlık Sayacı", page_icon="⏳")

st.title("⏳ 72 Saatlik Açlık Sayacı")

start_str=st.sidebar.text_input("Başlangıç", "23.02.2026 20:00")
hours=st.sidebar.number_input("Süre (saat)",1,240,72)

start=parse_dt(start_str)
if not start:
    st.error("Tarih formatı hatalı")
    st.stop()

finish=start+timedelta(hours=int(hours))
now=datetime.now()

remaining=finish-now
elapsed=now-start

# --- Sayaçlar ---
col1,col2=st.columns(2)

with col1:
    st.subheader("Kalan Süre")
    if remaining.total_seconds()<=0:
        st.success("🎉 Süre tamamlandı!")
    st.metric("Kalan", format_td(remaining))

with col2:
    st.subheader("Geçen Süre")
    if now<start:
        st.metric("Geçen","Henüz başlamadı")
    else:
        st.metric("Geçen", format_td(elapsed))

# --- Grafik ---
st.divider()

total_seconds=(finish-start).total_seconds()
progress=min(max(elapsed.total_seconds()/total_seconds,0),1)

st.subheader("İlerleme")
st.progress(progress)

st.caption(f"% {int(progress*100)} tamamlandı")

# --- Alt bilgiler ---
st.divider()
st.write(f"Başlangıç: {start.strftime('%d.%m.%Y %H:%M')}")
st.write(f"Bitiş: {finish.strftime('%d.%m.%Y %H:%M')}")
st.write(f"Şu an: {now.strftime('%d.%m.%Y %H:%M:%S')}")
