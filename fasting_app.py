import streamlit as st
from datetime import datetime, timedelta
import pytz

# Türkiye saat dilimi
tz = pytz.timezone("Europe/Istanbul")

# canlı yenileme
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
    if m>0: parts.append(f"{m} dk")
    parts.append(f"{s} sn")
    return " ".join(parts)

st.set_page_config(page_title="72 Saatlik Açlık Sayacı", page_icon="💪")

# ---- BODYBUILDING BANNER ----
st.image(
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1600",
    use_container_width=True
)

st.title("💪 Alp için 72 Saatlik Açlık Sayacı !")

# ---- SIDEBAR ----
start_str=st.sidebar.text_input("Başlangıç", "23.02.2026 20:00")
hours=st.sidebar.number_input("Süre (saat)",1,240,72)

# ---- ZAMAN HESABI ----
start=parse_dt(start_str)
if not start:
    st.error("Tarih formatı hatalı")
    st.stop()

# 🔴 KRİTİK SATIR → start'ı timezone'lu yapıyoruz
start = tz.localize(start)

finish=start+timedelta(hours=int(hours))
now=datetime.now(tz)

remaining=finish-now
elapsed=now-start

# ---- SAYAÇLAR ----
col1,col2=st.columns(2)

with col1:
    st.markdown("### ⏳ Kalan")
    if remaining.total_seconds()<=0:
        st.success("🎉 Oruç tamamlandı!")
    st.markdown(f"<h1>{format_td(remaining)}</h1>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🔥 Geçen")
    if now<start:
        st.markdown("<h1>Henüz başlamadı</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1>{format_td(elapsed)}</h1>", unsafe_allow_html=True)

# ---- PROGRESS ----
st.divider()
total=(finish-start).total_seconds()
progress=min(max(elapsed.total_seconds()/total,0),1)

st.markdown("### 📈 İlerleme")
st.progress(progress)
st.markdown(f"**%{int(progress*100)} tamamlandı**")

# ---- MOTIVASYON MESAJLARI ----
st.divider()

if progress < 0.25:
    st.info("Başlangıç zor, ama disiplin kas gibidir 💪")

elif progress < 0.5:
    st.info("Yağ yakımı başladı 🔥 devam!")

elif progress < 0.75:
    st.info("Metabolizma çalışıyor, hormonlar seninle 🧠")

elif progress < 1:
    st.info("Son düzlüğe girdin, karakter burada belli olur 👊")

else:
    st.success("🎉 Tebrikler! Refeed zamanı 💪🍽")

# ---- ALT BİLGİ ----
st.divider()
st.caption(f"Başlangıç: {start.strftime('%d.%m.%Y %H:%M')}")
st.caption(f"Bitiş: {finish.strftime('%d.%m.%Y %H:%M')}")
st.caption(f"Şu an: {now.strftime('%d.%m.%Y %H:%M:%S')}")
