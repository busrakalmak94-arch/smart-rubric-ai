import streamlit as st
# import anthropic
import json

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Rubrik Asistanı",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    color: #e2e8f0;
}

/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Title bar */
.title-bar {
    background: linear-gradient(90deg, rgba(0,212,170,0.15) 0%, transparent 100%);
    border-left: 4px solid #00d4aa;
    padding: 16px 24px;
    margin-bottom: 28px;
    border-radius: 0 8px 8px 0;
}
.title-bar h1 {
    margin: 0; font-size: 1.6rem; font-weight: 800; color: #fff;
}
.title-bar p { margin: 4px 0 0; color: #00d4aa; font-size: 0.85rem; }

/* Section headers */
.sec-header {
    color: #00d4aa;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 24px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(0,212,170,0.2);
}

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,212,170,0.25) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 2px rgba(0,212,170,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #0088ff) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Student card */
.student-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,212,170,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
    position: relative;
}
.student-card .student-name {
    font-weight: 700; font-size: 0.9rem; color: #00d4aa; margin-bottom: 4px;
}
.student-card .student-answer {
    color: #94a3b8; font-size: 0.85rem; font-style: italic; margin-bottom: 12px;
}

/* Score badge */
.score-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}
.score-high { background: rgba(0,212,170,0.2); color: #00d4aa; border: 1px solid #00d4aa; }
.score-mid  { background: rgba(255,179,0,0.2);  color: #ffb300; border: 1px solid #ffb300; }
.score-low  { background: rgba(255,80,80,0.2);  color: #ff5050; border: 1px solid #ff5050; }

/* Result sections */
.result-section {
    background: rgba(0,0,0,0.25);
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 8px;
    font-size: 0.82rem;
    line-height: 1.6;
}
.result-label {
    color: #64748b;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* Approved badge */
.approved-badge {
    background: rgba(0,212,170,0.15);
    border: 1px solid #00d4aa;
    color: #00d4aa;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
}

/* Steps bar */
.steps-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 32px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,212,170,0.1);
    border-radius: 10px;
    overflow: hidden;
}
.step-item {
    flex: 1;
    padding: 10px 16px;
    text-align: center;
    font-size: 0.78rem;
    font-weight: 600;
    color: #475569;
    border-right: 1px solid rgba(0,212,170,0.1);
    position: relative;
}
.step-item:last-child { border-right: none; }
.step-item.active { background: rgba(0,212,170,0.12); color: #00d4aa; }
.step-item.done { color: #22c55e; }
.step-num {
    display: inline-block;
    width: 20px; height: 20px;
    border-radius: 50%;
    background: rgba(0,212,170,0.2);
    color: #00d4aa;
    font-size: 0.7rem;
    font-weight: 800;
    line-height: 20px;
    margin-right: 6px;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,212,170,0.15) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* Slider */
.stSlider > div { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── Sample data ───────────────────────────────────────────────
SAMPLE_STUDENTS = [
    {"name": "Öğrenci #001", "answer": "Rezonansda XL = XC olur, bu yüzden empedans minimum değer olan R'ye iner ve akım maksimuma ulaşır."},
    {"name": "Öğrenci #002", "answer": "Rezonansda direnç sıfır olur ve akım maksimuma ulaşır."},
    {"name": "Öğrenci #003", "answer": "Seri RLC devresinde rezonans frekansında reaktif elemanlar birbirini götürür, impedans saf ohmik direnç değerine iner ve bu da akımı tepe noktasına çıkarır."},
    {"name": "Öğrenci #004", "answer": "Rezonansda L ve C birbirini sıfırlar, impedans R olur."},
    {"name": "Öğrenci #005", "answer": "Rezonans frekansında ω₀ = 1/√(LC) olur. XL = XC eşitliği sağlandığında devre saf resistif davranır ve akım I = V/R ile maksimum olur."},
    {"name": "Öğrenci #006", "answer": "Akım çok artar ve devre maksimum güç çeker."},
    {"name": "Öğrenci #007", "answer": "Rezonansda bobin ve kondansatör aynı reaktansı gösterir (XL = XC), bunlar birbirini götürür ve kalan empedans yalnızca R'dir. Böylece akım maksimuma ulaşır."},
    {"name": "Öğrenci #008", "answer": "Rezonans frekansında empedans en küçük değerini alır ve akım maksimum olur fakat neden olduğunu tam açıklayamıyorum."},
    {"name": "Öğrenci #009", "answer": "Kondansatör reaktansı artar, bobin reaktansı azalır, ikisi eşitlenince rezonans olur ve akım zirveye çıkar."},
    {"name": "Öğrenci #010", "answer": "Devre rezonans durumunda rezonans frekansında salınım yapar ve akım sıfır olur."},
]

SAMPLE_QUESTION = "Seri RLC devresinde rezonans durumunu tanımlayarak fiziksel sonuçlarını açıklayınız."

SAMPLE_RUBRIC = """Kriter 1 - Reaktans Eşitliği (3 puan):
- 3 puan: XL = XC eşitliğini açıkça belirtmiş ve fiziksel nedenini açıklamış.
- 1 puan: Reaktansların birbirini götürdüğünü söylemiş ama eksik ifade.
- 0 puan: Reaktans ilişkisine hiç değinmemiş.

Kriter 2 - Empedans Dengesi (3 puan):
- 3 puan: Empedansın minimuma inerek saf ohmik direnç (Z=R) olduğunu açıklamış.
- 1 puan: Empedansın azaldığını belirtmiş ama "sıfırlandı" hatası yapmış.
- 0 puan: Empedans-direnç ilişkisine değinmemiş.

Kriter 3 - Akım Tepkisi (3 puan):
- 3 puan: Akımın I=V/R ile maksimuma ulaştığını ve fiziksel gerekçesini açıklamış.
- 1 puan: Akımın arttığını söylemiş ama fiziksel gerekçeyi eksik bırakmış.
- 0 puan: Akımın azaldığını veya sıfırlandığını iddia etmiş."""

# ── Session state ─────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1
if "results" not in st.session_state:
    st.session_state.results = {}
if "approved" not in st.session_state:
    st.session_state.approved = {}
if "edited_feedback" not in st.session_state:
    st.session_state.edited_feedback = {}
if "edited_scores" not in st.session_state:
    st.session_state.edited_scores = {}

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="title-bar">
  <h1>⚡ Yapay Zekâ Destekli Rubrik Değerlendirme</h1>
  <p>Öğrenci cevaplarını rubriğe göre anında analiz et · Hataları teşhis et · Geri bildirim gönder</p>
</div>
""", unsafe_allow_html=True)

# ── Steps bar ─────────────────────────────────────────────────
s = st.session_state.step
def step_cls(n):
    if s > n: return "done"
    if s == n: return "active"
    return ""

step_icons = {1: "📝", 2: "🤖", 3: "✅"}
step_labels = {1: "Rubrik Girişi", 2: "AI Değerlendirme", 3: "Onay Paneli"}

bars = "".join([
    f'<div class="step-item {step_cls(i)}"><span class="step-num">{i}</span>{step_icons[i]} {step_labels[i]}</div>'
    for i in [1,2,3]
])
st.markdown(f'<div class="steps-bar">{bars}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# STEP 1 — Rubrik Girişi
# ══════════════════════════════════════════════════════════════
if st.session_state.step == 1:

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="sec-header">Soru & Rubrik</div>', unsafe_allow_html=True)

        question = st.text_area(
            "Soru metni",
            value=SAMPLE_QUESTION,
            height=80,
            placeholder="Soruyu buraya yazın...",
            key="question_input"
        )

        rubric = st.text_area(
            "Rubrik kriterleri",
            value=SAMPLE_RUBRIC,
            height=280,
            placeholder="Her kriteri puan aralıklarıyla açıklayın...",
            key="rubric_input"
        )

    with col2:
        st.markdown('<div class="sec-header">Öğrenci Cevapları (10 örnek)</div>', unsafe_allow_html=True)

        students = []
        for i, s_data in enumerate(SAMPLE_STUDENTS):
            with st.expander(f"{s_data['name']}", expanded=(i < 2)):
                name = st.text_input("Ad Soyad", value=s_data["name"], key=f"name_{i}", label_visibility="collapsed")
                answer = st.text_area("Cevap", value=s_data["answer"], height=80, key=f"answer_{i}", label_visibility="collapsed")
                students.append({"name": name, "answer": answer})

        st.session_state.students = students

    st.markdown("---")
    st.markdown('<div class="sec-header">API Anahtarı</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Anthropic API Anahtarı",
        type="password",
        placeholder="sk-ant-...",
        help="console.anthropic.com adresinden alabilirsiniz",
        value=st.session_state.get("api_key", "")
    )

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🤖  AI ile Değerlendir", use_container_width=True):
            if not api_key:
                st.error("Lütfen API anahtarınızı girin.")
            elif question and rubric:
                st.session_state.question = question
                st.session_state.rubric = rubric
                st.session_state.api_key = api_key
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Lütfen soru ve rubrik alanlarını doldurun.")

# ══════════════════════════════════════════════════════════════
# STEP 2 — AI Değerlendirme
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == 2:

    st.markdown('<div class="sec-header">AI Değerlendirme Motoru Çalışıyor</div>', unsafe_allow_html=True)

    client = anthropic.Anthropic(api_key=st.session_state.get("api_key"))

    progress_bar = st.progress(0, text="Değerlendirme başlıyor...")
    result_container = st.container()

    results = {}

    for idx, student in enumerate(st.session_state.students):
        progress = (idx) / len(st.session_state.students)
        progress_bar.progress(progress, text=f"📊 {student['name']} değerlendiriliyor... ({idx+1}/{len(st.session_state.students)})")

        prompt = f"""Sen bir pedagoji uzmanısın. Aşağıdaki rubriğe göre öğrenci cevabını değerlendir.

SORU:
{st.session_state.question}

RUBRİK:
{st.session_state.rubric}

ÖĞRENCİ CEVABI:
{student['answer']}

Lütfen SADECE aşağıdaki JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "scores": {{
    "kriter_1": <0|1|3>,
    "kriter_2": <0|1|3>,
    "kriter_3": <0|1|3>
  }},
  "toplam": <toplam puan 0-9>,
  "hata_teshisi": "<tespit edilen kavram yanılgısı veya eksiklik, yoksa 'Belirgin hata yok'>",
  "geri_bildirim": "<öğrenciye yönelik gelişim odaklı, motive edici 2-3 cümle geri bildirim>",
  "guclu_yanlar": "<öğrencinin doğru yazdığı kısımlar>",
  "eksikler": "<eksik veya yanlış kavramlar>"
}}"""

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.content[0].text.strip()
            # strip code fences if any
            raw = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw)
        except Exception as e:
            data = {
                "scores": {"kriter_1": 0, "kriter_2": 0, "kriter_3": 0},
                "toplam": 0,
                "hata_teshisi": f"Değerlendirme hatası: {e}",
                "geri_bildirim": "Değerlendirme yapılamadı.",
                "guclu_yanlar": "-",
                "eksikler": "-"
            }

        results[idx] = {"student": student, "result": data}

    progress_bar.progress(1.0, text="✅ Tüm değerlendirmeler tamamlandı!")

    st.session_state.results = results
    st.session_state.step = 3
    st.rerun()

# ══════════════════════════════════════════════════════════════
# STEP 3 — Onay Paneli
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == 3:

    results = st.session_state.results
    approved = st.session_state.approved

    # Summary bar
    total = len(results)
    n_approved = len([k for k in approved if approved[k]])
    avg_score = sum(results[i]["result"]["toplam"] for i in results) / total if total else 0

    m1, m2, m3, m4 = st.columns(4)
    for col, label, val, color in [
        (m1, "Toplam Öğrenci", total, "#00d4aa"),
        (m2, "Onaylanan", n_approved, "#22c55e"),
        (m3, "Bekleyen", total - n_approved, "#ffb300"),
        (m4, "Ortalama Puan", f"{avg_score:.1f}/9", "#60a5fa"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                    border-radius:10px;padding:14px;text-align:center;">
          <div style="color:{color};font-size:1.6rem;font-weight:800;">{val}</div>
          <div style="color:#64748b;font-size:0.75rem;margin-top:2px;">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Toplu işlem
    cola, colb, colc = st.columns([1,1,3])
    with cola:
        if st.button("✅ Tümünü Onayla"):
            for i in results:
                st.session_state.approved[i] = True
                if i not in st.session_state.edited_feedback:
                    st.session_state.edited_feedback[i] = results[i]["result"]["geri_bildirim"]
            st.rerun()
    with colb:
        if st.button("🔄 Baştan Başla"):
            for key in ["step","results","approved","edited_feedback","edited_scores"]:
                del st.session_state[key]
            st.rerun()

    st.markdown('<div class="sec-header">Öğrenci Değerlendirmeleri</div>', unsafe_allow_html=True)

    for idx, item in results.items():
        student = item["student"]
        result = item["result"]
        is_approved = approved.get(idx, False)
        total_score = result.get("toplam", 0)

        # Score color
        if total_score >= 7:
            badge_cls = "score-high"
        elif total_score >= 4:
            badge_cls = "score-mid"
        else:
            badge_cls = "score-low"

        approved_html = '<span class="approved-badge">✓ ONAYLANDI</span>' if is_approved else ""
        short_answer = student['answer'][:120] + ("..." if len(student['answer']) > 120 else "")

        st.markdown(f"""
        <div class="student-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <div class="student-name">{student['name']}</div>
              <div class="student-answer">"{short_answer}"</div>
            </div>
            <div style="text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
              <span class="score-badge {badge_cls}">{total_score} / 9 puan</span>
              {approved_html}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🔍 Detayları Gör / Düzenle — {student['name']}"):
            dcol1, dcol2 = st.columns([1,1], gap="large")

            with dcol1:
                st.markdown("**AI Karar Gerekçesi**")
                st.markdown(f"""
                <div class="result-section">
                  <div class="result-label">Güçlü Yanlar</div>
                  <div style="color:#86efac;margin-bottom:10px;">✓ {result.get('guclu_yanlar','-')}</div>
                  <div class="result-label">Eksikler / Hatalar</div>
                  <div style="color:#fca5a5;margin-bottom:10px;">⚠ {result.get('eksikler','-')}</div>
                  <div class="result-label">Kavram Yanılgısı Teşhisi</div>
                  <div style="color:#fdba74;">🔬 {result.get('hata_teshisi','-')}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Kriter Puanları**")
                scores = result.get("scores", {})
                for ki, (kkey, klabel) in enumerate([
                    ("kriter_1", "Reaktans Eşitliği"),
                    ("kriter_2", "Empedans Dengesi"),
                    ("kriter_3", "Akım Tepkisi"),
                ]):
                    raw_score = scores.get(kkey, 0)
                    edited_key = f"score_{idx}_{ki}"
                    if edited_key not in st.session_state.edited_scores:
                        st.session_state.edited_scores[edited_key] = raw_score

                    new_score = st.select_slider(
                        f"{klabel}",
                        options=[0, 1, 3],
                        value=st.session_state.edited_scores[edited_key],
                        key=f"slider_{idx}_{ki}"
                    )
                    st.session_state.edited_scores[edited_key] = new_score

            with dcol2:
                st.markdown("**Geri Bildirim (Düzenlenebilir)**")
                fb_key = f"fb_{idx}"
                if fb_key not in st.session_state.edited_feedback:
                    st.session_state.edited_feedback[fb_key] = result.get("geri_bildirim", "")

                edited_fb = st.text_area(
                    "Geri bildirim",
                    value=st.session_state.edited_feedback[fb_key],
                    height=150,
                    key=f"textarea_fb_{idx}",
                    label_visibility="collapsed"
                )
                st.session_state.edited_feedback[fb_key] = edited_fb

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("✅ Onayla & Gönder", key=f"approve_{idx}", use_container_width=True):
                        st.session_state.approved[idx] = True
                        st.success(f"✓ {student['name']} onaylandı!")
                        st.rerun()
                with btn_col2:
                    if is_approved:
                        if st.button("↩ Geri Al", key=f"unapprove_{idx}", use_container_width=True):
                            st.session_state.approved[idx] = False
                            st.rerun()

    # Final summary if all approved
    if n_approved == total:
        st.markdown("""
        <div style="background:rgba(0,212,170,0.1);border:1px solid #00d4aa;border-radius:12px;
                    padding:20px;text-align:center;margin-top:24px;">
          <div style="font-size:2rem;">🎉</div>
          <div style="color:#00d4aa;font-weight:800;font-size:1.1rem;margin:8px 0;">
            Tüm değerlendirmeler onaylandı!
          </div>
          <div style="color:#94a3b8;font-size:0.85rem;">
            10 öğrencinin geri bildirimi gönderilmeye hazır.
          </div>
        </div>
        """, unsafe_allow_html=True)
