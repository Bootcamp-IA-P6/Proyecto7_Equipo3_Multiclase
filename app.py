import streamlit as st
import joblib
import pandas as pd
import numpy as np
import urllib.parse
import os
from datetime import datetime

# ── Cargar variables de entorno desde .env ────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()          # busca .env en la carpeta desde donde se ejecuta
except ImportError:
    pass                   # si no está instalado, usa las variables del sistema

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Cuestionario de Incontinencia Urinaria",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Supabase integration ──────────────────────────────────────────────────────
@st.cache_resource
def get_supabase_client():
    """Crea el cliente Supabase una sola vez. Devuelve None si no está configurado."""
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()

    if not url or not key:
        return None, "❌ SUPABASE_URL o SUPABASE_KEY no encontradas en el .env"

    if url == "https://XXXXXXXXXXXX.supabase.co":
        return None, "❌ Aún tienes los valores de ejemplo en el .env — cámbialos por los reales"

    try:
        from supabase import create_client
        client = create_client(url, key)
        return client, "✅ Conectado a Supabase"
    except ImportError:
        return None, "❌ Librería 'supabase' no instalada — ejecuta: uv add supabase"
    except Exception as e:
        return None, f"❌ Error al conectar con Supabase: {e}"

def save_to_supabase(data: dict) -> tuple[bool, str]:
    """Guarda una fila en Supabase. Devuelve (éxito, mensaje)."""
    client, msg = get_supabase_client()
    if client is None:
        return False, msg
    try:
        client.table("ui_responses").insert(data).execute()
        return True, "✅ Respuestas guardadas correctamente"
    except Exception as e:
        return False, f"❌ Error al insertar en Supabase: {e}"

# ── CSS (mobile-first) ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --pink-light: #fce4ec;
    --pink-mid:   #f8bbd9;
    --pink-soft:  #f48fb1;
    --blue-light: #e3f2fd;
    --blue-mid:   #bbdefb;
    --blue-soft:  #90caf9;
    --blue-main:  #64b5f6;
    --text-dark:  #3d2c3e;
    --text-mid:   #6b5b6e;
    --text-light: #a694a8;
    --white:      #ffffff;
    --surface:    rgba(255,255,255,0.82);
    --border:     rgba(244,143,177,0.25);
    --radius:     18px;
    --shadow:     0 8px 32px rgba(180,100,150,0.12);
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #fce4ec 0%, #f3e5f5 25%, #e8eaf6 55%, #e3f2fd 100%) !important;
    min-height: 100vh;
}

.block-container {
    max-width: 560px !important;
    padding: 1.2rem 1rem 5rem !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Buttons (mobile-first: big touch targets) ── */
.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    border-radius: 14px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all .2s ease !important;
    letter-spacing: 0.01em !important;
    min-height: 48px !important;
    -webkit-tap-highlight-color: transparent !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #f06292, #64b5f6) !important;
    border: none !important;
    color: #fff !important;
    padding: 14px 24px !important;
    box-shadow: 0 4px 15px rgba(240,98,146,0.35) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:active {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(240,98,146,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-dark) !important;
    padding: 12px 16px !important;
    backdrop-filter: blur(8px) !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button[kind="secondary"]:active {
    border-color: #f48fb1 !important;
    background: rgba(252,228,236,0.9) !important;
}

/* ── Selected option highlight ── */
.option-selected .stButton > button[kind="secondary"] {
    border-color: #f06292 !important;
    background: rgba(252,228,236,0.95) !important;
    box-shadow: 0 2px 12px rgba(240,98,146,0.2) !important;
}

div[data-testid="stCheckbox"] label {
    font-size: 15px !important;
    color: var(--text-mid) !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
}
div[data-testid="stTextInput"] input {
    border-radius: 12px !important;
    font-size: 16px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface) !important;
    min-height: 48px !important;
    /* prevent iOS zoom on focus */
}
div[data-testid="stTextInput"] input:focus {
    border-color: #f48fb1 !important;
    box-shadow: 0 0 0 3px rgba(244,143,177,0.15) !important;
}

/* ── Progress ── */
.prog-wrap {
    background: rgba(244,143,177,0.2);
    border-radius: 6px;
    height: 5px;
    overflow: hidden;
    margin-bottom: 6px;
}
.prog-fill {
    height: 100%;
    background: linear-gradient(90deg, #f06292, #64b5f6);
    border-radius: 6px;
    transition: width .5s ease;
}
.step-hint {
    font-size: 12px;
    color: var(--text-light);
    text-align: right;
    margin-bottom: 16px;
    letter-spacing: .04em;
}

/* ── Question typography ── */
.q-title {
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    color: var(--text-dark);
    line-height: 1.35;
    margin: 0 0 6px;
}
.q-sub {
    font-size: 14px;
    color: var(--text-light);
    line-height: 1.6;
    margin: 0 0 18px;
}

/* ── Welcome screen ── */
.welcome-wrap {
    text-align: center;
    padding: 1.5rem 0 1rem;
    animation: fadeInUp .6s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.welcome-icon { font-size: 48px; margin-bottom: 14px; }
.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    color: var(--text-dark);
    line-height: 1.3;
    margin: 0 0 12px;
    background: linear-gradient(135deg, #e91e8c, #2196f3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.welcome-sub {
    font-size: 15px;
    color: var(--text-mid);
    line-height: 1.7;
    margin: 0 0 18px;
}
.welcome-info {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 16px 18px;
    font-size: 14px;
    color: var(--text-mid);
    line-height: 1.65;
    margin: 0 0 8px;
    backdrop-filter: blur(8px);
}

/* ── Quiz card ── */
.quiz-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 18px;
    margin-bottom: 14px;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    animation: fadeInUp .35s ease;
}

/* ── Selected check badge ── */
.sel-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, rgba(240,98,146,0.15), rgba(100,181,246,0.15));
    border: 1.5px solid rgba(240,98,146,0.4);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    color: #c2185b;
    font-weight: 600;
    margin-top: 10px;
}

/* ── Result card ── */
.result-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    animation: fadeInUp .5s ease;
}
.result-header {
    padding: 1.3rem 1.2rem 1rem;
    background: linear-gradient(135deg, rgba(252,228,236,0.8), rgba(227,242,253,0.8));
    border-bottom: 1.5px solid var(--border);
}
.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 12px;
    letter-spacing: .04em;
    text-transform: uppercase;
}
.badge-none   { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
.badge-stress { background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
.badge-mixed  { background: #fce4ec; color: #880e4f; border: 1px solid #f48fb1; }
.badge-urge   { background: #fce4ec; color: #b71c1c; border: 1px solid #ef9a9a; }
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 19px;
    color: var(--text-dark);
    line-height: 1.35;
    margin: 0 0 8px;
}
.result-desc { font-size: 14px; color: var(--text-mid); line-height: 1.7; margin: 0; }
.result-body { padding: 1.2rem; }

.section-lbl {
    font-size: 10px;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin: 0 0 12px;
    display: block;
    font-weight: 700;
}
.prob-row { margin-bottom: 12px; }
.prob-meta { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; }
.prob-name { color: var(--text-mid); }
.prob-pct  { font-weight: 700; color: var(--text-dark); }
.prob-track { height: 7px; background: rgba(244,143,177,0.15); border-radius: 4px; overflow: hidden; }
.prob-fill  { height: 100%; border-radius: 4px; transition: width .8s ease; }
.pf-none   { background: linear-gradient(90deg, #66bb6a, #43a047); }
.pf-stress { background: linear-gradient(90deg, #64b5f6, #2196f3); }
.pf-mixed  { background: linear-gradient(90deg, #f48fb1, #e91e8c); }
.pf-urge   { background: linear-gradient(90deg, #ef9a9a, #f44336); }

/* ── Habits ── */
.habit-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(244,143,177,0.15);
    font-size: 14px;
    color: var(--text-mid);
    line-height: 1.55;
}
.habit-item:last-child { border-bottom: none; }
.habit-dot {
    width: 7px; height: 7px;
    background: linear-gradient(135deg, #f06292, #64b5f6);
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 6px;
}

/* ── Prof card ── */
.prof-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    background: linear-gradient(135deg, rgba(252,228,236,0.6), rgba(227,242,253,0.6));
    border: 1.5px solid var(--border);
    border-radius: 14px;
    margin-bottom: 10px;
    cursor: pointer;
    text-decoration: none !important;
    transition: all .2s ease;
    backdrop-filter: blur(8px);
}
.prof-card:hover, .prof-card:active {
    border-color: #f48fb1;
    box-shadow: 0 4px 16px rgba(240,98,146,0.2);
}
.prof-icon { font-size: 24px; flex-shrink: 0; }
.prof-name { font-size: 14px; font-weight: 700; color: var(--text-dark); margin: 0 0 3px; }
.prof-why  { font-size: 13px; color: var(--text-mid); line-height: 1.45; margin: 0; }
.prof-cta  { font-size: 12px; color: #e91e8c; margin: 6px 0 0; font-weight: 700; }

.disclaimer {
    font-size: 12px;
    color: var(--text-light);
    line-height: 1.7;
    border-top: 1px solid var(--border);
    padding-top: 16px;
    margin-top: 8px;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(244,143,177,0.3), transparent);
    margin: 16px 0 20px;
}

/* ── Spinner text ── */
.stSpinner > div { border-top-color: #f06292 !important; }

/* ══════════════════════════════════════════════════════════════════════════
   RESPONSIVE — mobile-first adjustments
   ══════════════════════════════════════════════════════════════════════════ */
@media (max-width: 640px) {
    .block-container {
        max-width: 100% !important;
        padding: 1rem 0.8rem 5rem !important;
    }
    .q-title { font-size: 19px; }
    .welcome-title { font-size: 23px; }
    .welcome-icon { font-size: 42px; }
    .quiz-card { padding: 18px 14px; }
    .result-header { padding: 1rem; }
    .result-body { padding: 1rem; }
    .result-title { font-size: 17px; }

    /* Stack columns vertically on mobile */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── Model loading ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        scaler   = joblib.load("models/pipeline.pkl")
        ensemble = joblib.load("models/ensemble_final.pkl")
        # Try to load feature columns from training data
        try:
            X_train = pd.read_csv("data/processed/X_train_scaled.csv")
            feature_cols = list(X_train.columns)
        except Exception:
            feature_cols = None
        return scaler, ensemble, feature_cols, True
    except Exception as e:
        return None, None, None, False

scaler, ensemble, FEATURE_COLS, MODEL_LOADED = load_models()

# ── Session state defaults ────────────────────────────────────────────────────
DEFAULTS = dict(
    step=0,
    # Quiz answers
    q_tipo=None, q_frec=None, q_cant=None, q_molestia=None, q_impacto=None,
    # Personal
    edad="", peso="", altura="",
    # Medical
    diab=False, hta=False, art=False, cancer=False,
    # Lifestyle
    fumadora=None, actividad=None,
    # Demographics
    etnia=None, pais=None, status_eco=None,
    # Location
    city="Madrid",
    # Flags
    saved=False,
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Total steps (for progress) ────────────────────────────────────────────────
TOTAL_QUESTIONS = 12

# ── Helpers ───────────────────────────────────────────────────────────────────
def go(step: int):
    st.session_state.step = step
    st.rerun()

def progress(current_q: int):
    pct = round(current_q / TOTAL_QUESTIONS * 100)
    st.markdown(
        f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>'
        f'<div class="step-hint">Pregunta {current_q} de {TOTAL_QUESTIONS}</div>',
        unsafe_allow_html=True,
    )

def q_header(title: str, sub: str = None):
    sub_html = f'<p class="q-sub">{sub}</p>' if sub else ""
    st.markdown(f'<p class="q-title">{title}</p>{sub_html}', unsafe_allow_html=True)

def nav(back_step: int, next_step: int, next_disabled: bool = False, next_label: str = "Siguiente →"):
    """Navigation buttons."""
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Atrás", key=f"back_{back_step}_{next_step}_{st.session_state.step}"):
            go(back_step)
    with c2:
        if st.button(
            next_label,
            key=f"next_{next_step}_{st.session_state.step}",
            disabled=next_disabled,
            use_container_width=True,
            type="primary",
        ):
            go(next_step)

def choice_buttons(state_key: str, options: list, cols: int = 1):
    """
    Render option buttons.
    options = list of (value, icon, label)
    Sets session_state[state_key] and reruns on click.
    Shows selected value below.
    """
    current = st.session_state.get(state_key)
    if cols == 1:
        for item in options:
            val, icon, label = item[0], item[1], item[2]
            btn_label = f"{icon}  {label}"
            if st.button(btn_label, key=f"btn_{state_key}_{val}", use_container_width=True, type="secondary"):
                st.session_state[state_key] = val
                st.rerun()
    else:
        rows_needed = -(-len(options) // cols)
        for r in range(rows_needed):
            row_cols = st.columns(cols)
            for c in range(cols):
                idx = r * cols + c
                if idx < len(options):
                    item = options[idx]
                    val, icon, label = item[0], item[1], item[2]
                    with row_cols[c]:
                        if st.button(
                            f"{icon}\n{label}",
                            key=f"btn_{state_key}_{val}",
                            use_container_width=True,
                            type="secondary",
                        ):
                            st.session_state[state_key] = val
                            st.rerun()
    if current:
        sel = next((i[2] for i in options if i[0] == current), current)
        sel_icon = next((i[1] for i in options if i[0] == current), "")
        st.markdown(f'<div class="sel-badge">✓ {sel_icon} {sel}</div>', unsafe_allow_html=True)

# ── Feature builder ───────────────────────────────────────────────────────────
def build_feature_row(s: dict, imc: float) -> dict:
    """Reconstruct the full feature vector the model was trained on."""
    etnia_cols = ["etnia_asiatica", "etnia_blanca", "etnia_hisp_mex",
                  "etnia_hisp_otra", "etnia_negra", "etnia_otra"]
    etnia_map  = {
        "asiatica": "etnia_asiatica", "blanca": "etnia_blanca",
        "hisp_mex": "etnia_hisp_mex", "hisp_otra": "etnia_hisp_otra",
        "negra": "etnia_negra", "otra": "etnia_otra",
    }
    etnia_key  = etnia_map.get(s.get("etnia", "blanca"), "etnia_blanca")
    etnia_vals = {c: int(c == etnia_key) for c in etnia_cols}

    pais_cols = ["pais_mexico", "pais_otro", "pais_usa"]
    pais_map  = {"mexico": "pais_mexico", "otro": "pais_otro", "usa": "pais_usa"}
    pais_key  = pais_map.get(s.get("pais", "usa"), "pais_usa")
    pais_vals = {c: int(c == pais_key) for c in pais_cols}

    ui_otro = int(s.get("q_tipo") == "otro")

    try:    edad = float(s.get("edad") or 50)
    except: edad = 50.0

    try:    sec = float(s.get("status_eco") or 2.7)
    except: sec = 2.7

    try:    frec = float(s.get("q_frec") or 2)
    except: frec = 2.0

    try:    cant = float(s.get("q_cant") or 1)
    except: cant = 1.0

    try:    molestia = float(s.get("q_molestia") or 0)
    except: molestia = 0.0

    try:    impacto = float(s.get("q_impacto") or 0)
    except: impacto = 0.0

    row = {
        "edad_anios":                edad,
        "imc":                       imc,
        "status_economico":          sec,
        "dx_diabetes":               int(bool(s.get("diab"))),
        "dx_hipertension":           int(bool(s.get("hta"))),
        "dx_cancer":                 int(bool(s.get("cancer"))),
        "dx_artritis":               int(bool(s.get("art"))),
        "fumadora_alguna_vez":       int(s.get("fumadora") == "si"),
        "actividad_fisica_vigorosa": int(s.get("actividad") == "si"),
        "ui_frecuencia":             frec,
        "ui_cantidad":               cant,
        "ui_otro_tipo_presente":     float(ui_otro),
        "ui_molestia_percibida":     molestia,
        "ui_impacto_actividades":    impacto,
        **etnia_vals,
        **pais_vals,
    }
    return row

def classify(s: dict):
    """Return (pred_class, probs_dict). Uses real model if loaded, else heuristic."""
    try:
        peso   = float(s.get("peso")   or 70)
        altura = float(s.get("altura") or 162)
        if altura <= 0:
            raise ValueError
        imc = round(peso / (altura / 100) ** 2, 1)
    except Exception:
        peso, altura, imc = 70.0, 162.0, 26.7

    if MODEL_LOADED and scaler is not None and ensemble is not None:
        try:
            row  = build_feature_row(s, imc)
            X    = pd.DataFrame([row])
            if FEATURE_COLS:
                for col in FEATURE_COLS:
                    if col not in X.columns:
                        X[col] = 0
                X = X[FEATURE_COLS]
            X_sc      = scaler.transform(X)
            pred      = ensemble.predict(X_sc)[0]
            probs_arr = ensemble.predict_proba(X_sc)[0]
            classes   = ensemble.classes_
            probs     = {c: round(float(p) * 100) for c, p in zip(classes, probs_arr)}
            # Normalise keys to expected set
            key_map = {}
            for c in classes:
                cl = str(c).lower()
                if "none" in cl or "no" == cl or cl == "0":
                    key_map[c] = "none"
                elif "stress" in cl or "esfuerzo" in cl or cl == "1":
                    key_map[c] = "stress"
                elif "urge" in cl or "urgencia" in cl or cl == "3":
                    key_map[c] = "urge"
                elif "mix" in cl or cl == "2":
                    key_map[c] = "mixed"
                else:
                    key_map[c] = cl
            norm_probs = {}
            for c, p in probs.items():
                norm_key = key_map.get(c, str(c))
                norm_probs[norm_key] = norm_probs.get(norm_key, 0) + p
            # Fill missing keys with 0
            for k in ["none", "stress", "mixed", "urge"]:
                norm_probs.setdefault(k, 0)
            norm_pred = key_map.get(pred, str(pred))
            return norm_pred, norm_probs
        except Exception as e:
            pass  # Fall through to heuristic

    # ── Fallback heurística ──────────────────────────────────────────────
    tipo   = s.get("q_tipo", "esfuerzo")
    try: frec = int(s.get("q_frec") or 2)
    except: frec = 2
    try: cant = int(s.get("q_cant") or 1)
    except: cant = 1
    try: impact = int(s.get("q_impacto") or 0)
    except: impact = 0
    try: edad = float(s.get("edad") or 50)
    except: edad = 50.0

    sc = {"none": 10, "stress": 20, "mixed": 15, "urge": 15}

    if tipo == "esfuerzo":   sc["stress"] += 45; sc["mixed"] += 10
    elif tipo == "urgencia": sc["urge"] += 45;   sc["mixed"] += 10
    elif tipo == "mixta":    sc["mixed"] += 50;  sc["stress"] += 5; sc["urge"] += 5
    else:                    sc["urge"] += 20;   sc["none"] += 10;  sc["mixed"] += 10

    if frec <= 1:   sc["none"] += 15; sc["stress"] -= 5; sc["urge"] -= 5
    elif frec >= 4: sc["urge"] += 10; sc["mixed"] += 8;  sc["none"] -= 10

    if cant == 1:   sc["none"] += 5;  sc["stress"] += 5
    elif cant == 3: sc["mixed"] += 10; sc["urge"] += 8;  sc["none"] -= 10

    if impact >= 2:   sc["urge"] += 8;  sc["mixed"] += 8;  sc["none"] -= 10
    elif impact == 0: sc["none"] += 10

    if edad >= 60:   sc["urge"] += 12; sc["mixed"] += 8;  sc["none"] -= 10
    elif edad >= 45: sc["stress"] += 6; sc["mixed"] += 4; sc["none"] -= 5

    if imc >= 30:   sc["stress"] += 10; sc["mixed"] += 8; sc["none"] -= 8
    elif imc >= 25: sc["stress"] += 4

    if s.get("diab"):   sc["urge"] += 8;  sc["mixed"] += 5
    if s.get("hta"):    sc["urge"] += 6;  sc["mixed"] += 4
    if s.get("art"):    sc["urge"] += 8;  sc["mixed"] += 6; sc["none"] -= 5
    if s.get("cancer"): sc["urge"] += 5;  sc["mixed"] += 3

    for k in sc:
        sc[k] = max(sc[k], 1)
    total = sum(sc.values())
    probs = {k: round(sc[k] / total * 100) for k in sc}
    return max(probs, key=probs.get), probs

# ── Result content ────────────────────────────────────────────────────────────
RESULTS = {
    "none": {
        "badge_cls": "badge-none",
        "badge_txt": "Sin incontinencia aparente",
        "title": "Las pérdidas parecen leves o esporádicas",
        "desc": "Según tus respuestas, lo que describes podría estar dentro de la variabilidad normal o ser un episodio puntual. Si persiste o te preocupa, merece una consulta.",
        "profs": [
            {
                "icon": "🩺",
                "name": "Médico de cabecera o de familia",
                "why": "Primer paso siempre. Puede hacer una valoración inicial y derivarte si es necesario.",
                "search": "médico de cabecera medicina de familia",
            },
        ],
        "habits": [
            "Lleva un diario miccional una semana para detectar patrones.",
            "Reduce cafeína y alcohol — irritan la vejiga.",
            "Controla la ingesta de líquidos: 1.5–2 litros al día es lo ideal.",
        ],
    },
    "stress": {
        "badge_cls": "badge-stress",
        "badge_txt": "Incontinencia de esfuerzo",
        "title": "Lo que describes suena a incontinencia de esfuerzo",
        "desc": "Las pérdidas al toser, reír o hacer ejercicio son muy características. Suele deberse a debilitamiento del suelo pélvico y tiene tratamiento muy efectivo.",
        "profs": [
            {
                "icon": "🤸‍♀️",
                "name": "Fisioterapeuta de suelo pélvico",
                "why": "Tratamiento de primera línea. Los ejercicios de Kegel guiados tienen tasa de éxito muy alta.",
                "search": "fisioterapeuta suelo pélvico",
            },
            {
                "icon": "👩‍⚕️",
                "name": "Ginecóloga o uroginecóloga",
                "why": "Para valoración completa, especialmente si los síntomas son moderados o graves.",
                "search": "uroginecóloga ginecóloga suelo pélvico",
            },
        ],
        "habits": [
            "Practica ejercicios de Kegel: 3 series de 10 contracciones al día.",
            "Evita el sobrepeso — cada kilo extra aumenta la presión sobre el suelo pélvico.",
            "Controla el estreñimiento; el esfuerzo al defecar daña el suelo pélvico.",
            "Evita saltar a la comba o correr en superficies duras sin trabajo previo de suelo pélvico.",
        ],
    },
    "urge": {
        "badge_cls": "badge-urge",
        "badge_txt": "Vejiga hiperactiva",
        "title": "Lo que describes suena a vejiga hiperactiva",
        "desc": "La urgencia repentina y no llegar al baño a tiempo son características de la vejiga hiperactiva. Tiene tratamiento efectivo con medicación y entrenamiento vesical.",
        "profs": [
            {
                "icon": "🔬",
                "name": "Uróloga o uroginecóloga",
                "why": "Puede confirmar el diagnóstico y proponer tratamiento farmacológico o entrenamiento vesical.",
                "search": "uróloga uroginecóloga vejiga hiperactiva",
            },
            {
                "icon": "🤸‍♀️",
                "name": "Fisioterapeuta de suelo pélvico",
                "why": "Complementa el tratamiento con técnicas de control de urgencia.",
                "search": "fisioterapeuta suelo pélvico vejiga hiperactiva",
            },
        ],
        "habits": [
            "Practica el entrenamiento vesical: aguanta un poco más antes de ir al baño.",
            "Sigue un horario miccional regular (cada 2–3 h) para reeducar la vejiga.",
            "Elimina irritantes: cafeína, alcohol, bebidas carbonatadas y picante.",
            "Técnica de distracción cuando sientes urgencia: respira profundo y cuenta hasta 10.",
        ],
    },
    "mixed": {
        "badge_cls": "badge-mixed",
        "badge_txt": "Incontinencia mixta",
        "title": "Lo que describes tiene características de ambos tipos",
        "desc": "Tienes síntomas de esfuerzo y de urgencia. Esto se llama incontinencia mixta y es frecuente. Requiere una valoración más completa para decidir por dónde empezar.",
        "profs": [
            {
                "icon": "👩‍⚕️",
                "name": "Ginecóloga o uroginecóloga",
                "why": "Puede hacer una valoración urodinámica para confirmar el tipo predominante.",
                "search": "uroginecóloga valoración urodinámica incontinencia",
            },
            {
                "icon": "🤸‍♀️",
                "name": "Fisioterapeuta de suelo pélvico",
                "why": "Tratamiento coadyuvante para ambos componentes.",
                "search": "fisioterapeuta suelo pélvico incontinencia mixta",
            },
        ],
        "habits": [
            "Combina ejercicios de Kegel con entrenamiento vesical.",
            "Lleva un diario miccional para identificar cuál componente predomina.",
            "Reduce cafeína y alcohol: irritan la vejiga y empeoran la urgencia.",
            "Controla el peso corporal — el sobrepeso agrava el componente de esfuerzo.",
        ],
    },
}

PROB_META = {
    "none":   ("Sin incontinencia", "pf-none"),
    "stress": ("De esfuerzo",       "pf-stress"),
    "mixed":  ("Mixta",             "pf-mixed"),
    "urge":   ("De urgencia",       "pf-urge"),
}

def google_search_url(query: str, city: str) -> str:
    """Build a Google search URL for finding professionals in a city."""
    full_query = f"{query} en {city}"
    return f"https://www.google.com/search?q={urllib.parse.quote_plus(full_query)}"

# ════════════════════════════════════════════════════════════════════════════
# SCREENS — one question per view for mobile-friendly UX
# ════════════════════════════════════════════════════════════════════════════

step = st.session_state.step

# ── 0 · Bienvenida ────────────────────────────────────────────────────────────
if step == 0:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-icon">🌸</div>
        <p class="welcome-title">Tu bienestar íntimo importa</p>
        <p class="welcome-sub">
            No estás sola.<br>
            Esto es más común de lo que imaginas.<br>
            Te ayudamos a entender tu situación sin juicios.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-info">
        🔒 <strong>Privacidad:</strong> Tus respuestas son anónimas y se usan solo
        para orientarte. No reemplaza a un profesional de salud.<br><br>
        ⏱ <strong>Duración:</strong> Aproximadamente 3–4 minutos.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    city = st.text_input(
        "📍 ¿En qué ciudad estás?",
        value=st.session_state.city,
        placeholder="Ej: Madrid, Barcelona, Ciudad de México…",
    )
    st.session_state.city = city

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Empezar el cuestionario →", key="start", use_container_width=True, type="primary"):
        go(1)

# ── 1 · Tipo de incontinencia ─────────────────────────────────────────────────
elif step == 1:
    progress(1)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("¿Qué es lo que más se parece a lo que te pasa?")
    choice_buttons("q_tipo", [
        ("esfuerzo", "🏃‍♀️", "Se me escapa al moverme, toser o reír"),
        ("urgencia", "⚡",   "Siento urgencia repentina y no llego al baño"),
        ("mixta",    "🔀",   "Ambas cosas me ocurren"),
        ("otro",     "❓",   "Algo diferente / no sé describirlo"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(0, 2, next_disabled=not st.session_state.q_tipo)

# ── 2 · Frecuencia ────────────────────────────────────────────────────────────
elif step == 2:
    progress(2)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("¿Con qué frecuencia ocurren las pérdidas?")
    choice_buttons("q_frec", [
        ("1", "📅", "Menos de una vez al mes"),
        ("2", "📅", "Una vez al mes aproximadamente"),
        ("3", "📆", "Una vez a la semana"),
        ("4", "🔁", "Varios días a la semana"),
        ("5", "⚠️", "Todos los días"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(1, 3, next_disabled=not st.session_state.q_frec)

# ── 3 · Cantidad ──────────────────────────────────────────────────────────────
elif step == 3:
    progress(3)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("¿Cuánta orina se te escapa habitualmente?")
    choice_buttons("q_cant", [
        ("1", "💧", "Unas gotas"),
        ("2", "💦", "Un chorro pequeño"),
        ("3", "🌊", "Bastante cantidad"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(2, 4, next_disabled=not st.session_state.q_cant)

# ── 4 · Molestia ──────────────────────────────────────────────────────────────
elif step == 4:
    progress(4)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("¿Cuánta molestia te causa?", "Considera la incomodidad física y emocional.")
    choice_buttons("q_molestia", [
        ("0", "😌", "Ninguna"),
        ("1", "🙂", "Poca"),
        ("2", "😐", "Moderada"),
        ("3", "😟", "Bastante"),
        ("4", "😣", "Mucha"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(3, 5, next_disabled=st.session_state.q_molestia is None)

# ── 5 · Impacto ───────────────────────────────────────────────────────────────
elif step == 5:
    progress(5)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿Cómo afecta esto a tus actividades diarias?",
        "Piensa en si evitas salidas, llevas compresas o cambias hábitos.",
    )
    choice_buttons("q_impacto", [
        ("0", "😌", "Nada, apenas lo noto"),
        ("1", "🙂", "Un poco, no cambia mi rutina"),
        ("2", "😐", "Bastante — adapto algunas cosas"),
        ("3", "😟", "Mucho — limita cosas que me importan"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(4, 6, next_disabled=st.session_state.q_impacto is None)

# ── 6 · Datos personales ─────────────────────────────────────────────────────
elif step == 6:
    progress(6)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("Cuéntanos un poco sobre ti", "Mejora la orientación — no son obligatorios.")

    st.session_state.edad   = st.text_input("Edad (años)",  value=st.session_state.edad,   placeholder="45")
    st.session_state.peso   = st.text_input("Peso (kg)",    value=st.session_state.peso,   placeholder="68")
    st.session_state.altura = st.text_input("Altura (cm)",  value=st.session_state.altura, placeholder="162")

    try:
        imc_val = round(float(st.session_state.peso) / (float(st.session_state.altura) / 100) ** 2, 1)
        st.caption(f"✦ IMC calculado: **{imc_val}** kg/m²")
    except Exception:
        pass
    st.markdown('</div>', unsafe_allow_html=True)
    nav(5, 7)

# ── 7 · Historial médico ─────────────────────────────────────────────────────
elif step == 7:
    progress(7)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿Te han diagnosticado alguna de estas condiciones?",
        "Marca todo lo que aplique. Si no lo sabes, déjalo sin marcar.",
    )
    st.session_state.diab   = st.checkbox("Diabetes (azúcar alta en sangre)",      value=st.session_state.diab)
    st.session_state.hta    = st.checkbox("Tensión arterial alta (hipertensión)",   value=st.session_state.hta)
    st.session_state.art    = st.checkbox("Artritis o dolor articular crónico",     value=st.session_state.art)
    st.session_state.cancer = st.checkbox("Cáncer (cualquier tipo, diagnosticado)", value=st.session_state.cancer)
    st.markdown('</div>', unsafe_allow_html=True)
    nav(6, 8)

# ── 8 · Fumadora ─────────────────────────────────────────────────────────────
elif step == 8:
    progress(8)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header("¿Has fumado alguna vez en tu vida?", "Incluye aunque hayas dejado de fumar.")
    choice_buttons("fumadora", [
        ("si", "🚬", "Sí, he fumado"),
        ("no", "🚭", "No, nunca he fumado"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(7, 9, next_disabled=not st.session_state.fumadora)

# ── 9 · Actividad física ─────────────────────────────────────────────────────
elif step == 9:
    progress(9)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿Realizas actividad física vigorosa habitualmente?",
        "Ej. correr, aeróbic intenso, deportes de contacto, ciclismo rápido.",
    )
    choice_buttons("actividad", [
        ("si", "🏋️", "Sí, regularmente"),
        ("no", "🚶", "No, o solo actividad ligera / moderada"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(8, 10, next_disabled=not st.session_state.actividad)

# ── 10 · Etnia ────────────────────────────────────────────────────────────────
elif step == 10:
    progress(10)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿Con qué grupo étnico te identificas?",
        "Opcional — si prefieres no responder pulsa 'Siguiente'.",
    )
    choice_buttons("etnia", [
        ("hisp_mex",  "🌮", "Hispana mexicana"),
        ("hisp_otra", "🌎", "Hispana de otro origen"),
        ("blanca",    "🤍", "Blanca no hispana"),
        ("negra",     "✊", "Negra / afroamericana"),
        ("asiatica",  "🌸", "Asiática"),
        ("otra",      "🌍", "Otra / prefiero no decir"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(9, 11)

# ── 11 · País de nacimiento ──────────────────────────────────────────────────
elif step == 11:
    progress(11)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿En qué país naciste?",
        "Opcional — si prefieres no responder pulsa 'Siguiente'.",
    )
    choice_buttons("pais", [
        ("usa",    "🇺🇸", "Estados Unidos"),
        ("mexico", "🇲🇽", "México"),
        ("otro",   "🌐",  "Otro país"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(10, 12)

# ── 12 · Status económico ────────────────────────────────────────────────────
elif step == 12:
    progress(12)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    q_header(
        "¿Cómo describirías tu situación económica?",
        "Orientativo — ninguna respuesta afecta negativamente tu resultado.",
    )
    choice_buttons("status_eco", [
        ("1.0", "💸", "Muy por debajo del umbral de pobreza"),
        ("2.0", "🪙", "Cerca o por debajo del umbral de pobreza"),
        ("3.0", "💼", "Ingresos medios"),
        ("5.0", "🏠", "Ingresos por encima de la media"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)
    nav(11, 13, next_label="Ver resultado 🌸")

# ── 13 · Resultado ────────────────────────────────────────────────────────────
elif step == 13:
    with st.spinner("Analizando tus respuestas con cuidado... 🌸"):
        s    = dict(st.session_state)
        pred, probs = classify(s)

        # Make sure pred is a valid key
        if pred not in RESULTS:
            pred = max(probs, key=probs.get)
        if pred not in RESULTS:
            pred = "none"

        info = RESULTS[pred]

        # ── Save to Supabase (once per session) ──────────────────────────
        if not st.session_state.get("saved", False):
            record = {
                "timestamp":   datetime.utcnow().isoformat(),
                "city":        s.get("city", ""),
                "pred_class":  pred,
                "prob_none":   probs.get("none", 0),
                "prob_stress": probs.get("stress", 0),
                "prob_mixed":  probs.get("mixed", 0),
                "prob_urge":   probs.get("urge", 0),
                "q_tipo":      s.get("q_tipo", ""),
                "q_frec":      s.get("q_frec", ""),
                "q_cant":      s.get("q_cant", ""),
                "q_molestia":  s.get("q_molestia", ""),
                "q_impacto":   s.get("q_impacto", ""),
                "edad":        s.get("edad", ""),
                "peso":        s.get("peso", ""),
                "altura":      s.get("altura", ""),
                "dx_diab":     int(bool(s.get("diab"))),
                "dx_hta":      int(bool(s.get("hta"))),
                "dx_art":      int(bool(s.get("art"))),
                "dx_cancer":   int(bool(s.get("cancer"))),
                "fumadora":    s.get("fumadora", ""),
                "actividad":   s.get("actividad", ""),
                "etnia":       s.get("etnia", ""),
                "pais":        s.get("pais", ""),
                "status_eco":  s.get("status_eco", ""),
                "model_loaded": MODEL_LOADED,
            }
            ok, db_msg = save_to_supabase(record)
            if ok:
                st.session_state.saved = True
                st.session_state.db_msg = ("success", db_msg)
            else:
                st.session_state.db_msg = ("error", db_msg)

    # ── Mostrar estado de Supabase (solo para debug — quita en producción) ──
    db_status = st.session_state.get("db_msg")
    if db_status:
        kind, msg = db_status
        if kind == "success":
            st.success(msg, icon="🌸")
        else:
            with st.expander("⚠️ Diagnóstico Supabase — haz clic para ver"):
                st.error(msg)
                st.markdown("""
**Pasos para solucionar:**
1. Abre tu proyecto en [supabase.com](https://supabase.com)
2. Ve a ⚙️ **Settings → API**
3. Copia **Project URL** y la key **anon / public**
4. Pégalas en tu archivo `.env`:
```
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...
```
5. Reinicia la app: `uv run streamlit run app.py`
                """)

    # ── Probability bars ──────────────────────────────────────────────────
    prob_bars = "".join([
        f'<div class="prob-row">'
        f'<div class="prob-meta">'
        f'<span class="prob-name">{PROB_META[k][0]}</span>'
        f'<span class="prob-pct">{probs.get(k, 0)}%</span>'
        f'</div>'
        f'<div class="prob-track">'
        f'<div class="prob-fill {PROB_META[k][1]}" style="width:{probs.get(k, 0)}%"></div>'
        f'</div>'
        f'</div>'
        for k in ["none", "stress", "mixed", "urge"]
    ])

    # ── Habits ────────────────────────────────────────────────────────────
    habits_html = "".join([
        f'<div class="habit-item"><div class="habit-dot"></div><span>{h}</span></div>'
        for h in info["habits"]
    ])

    # ── Result card ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="result-card">
      <div class="result-header">
        <span class="badge {info['badge_cls']}">{info['badge_txt']}</span>
        <p class="result-title">{info['title']}</p>
        <p class="result-desc">{info['desc']}</p>
      </div>
      <div class="result-body">
        <span class="section-lbl">Probabilidad estimada por tipo</span>
        {prob_bars}
        <div style="margin-top:18px">
          <span class="section-lbl">Hábitos recomendados</span>
          {habits_html}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Professionals ─────────────────────────────────────────────────────
    city = st.session_state.get("city", "Madrid") or "Madrid"
    st.markdown(
        f'<span class="section-lbl" style="display:block;margin-top:20px;margin-bottom:10px;">'
        f'Profesionales cerca de {city}</span>',
        unsafe_allow_html=True,
    )

    for prof in info["profs"]:
        search_url = google_search_url(prof["search"], city)
        st.markdown(f"""
        <a class="prof-card" href="{search_url}" target="_blank" rel="noopener noreferrer">
          <span class="prof-icon">{prof['icon']}</span>
          <div>
            <p class="prof-name">{prof['name']}</p>
            <p class="prof-why">{prof['why']}</p>
            <p class="prof-cta">Buscar en Google →</p>
          </div>
        </a>
        """, unsafe_allow_html=True)

    # ── Disclaimer ────────────────────────────────────────────────────────
    model_note = "" if MODEL_LOADED else " Resultado basado en heurística clínica (modelo no encontrado)."
    st.markdown(f"""
    <p class="disclaimer">⚠ Esta orientación se basa en un modelo entrenado con datos de la encuesta NHANES
    (mujeres adultas EE.UU.). No es un diagnóstico médico. Solo un profesional de salud puede evaluar
    tu situación y definir el tratamiento adecuado.{model_note}</p>
    """, unsafe_allow_html=True)

    # ── Restart ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver a empezar", key="restart", use_container_width=True):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()
