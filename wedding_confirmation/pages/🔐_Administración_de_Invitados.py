"""Admin Streamlit app."""

from pathlib import Path

import streamlit as st

from wedding_confirmation.db.models import Base, Guest
from wedding_confirmation.db.session import SessionLocal, engine
from wedding_confirmation.services.guests import (
    export_guests_to_google_sheets,
    import_guests_from_google_sheets,
)

st.set_page_config(page_title="Admin – Wedding RSVP", page_icon="🔐")

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

pwd = st.text_input("Password de administración", type="password")
if pwd != ADMIN_PASSWORD:
    st.stop()


st.title("Administración – Base de Datos")

try:
    session = SessionLocal()
    st.session_state.guests = session.query(Guest).all()
    session.close()
except Exception:
    st.session_state.guests = None  # type: ignore
    st.warning("No data.")


if "guests" in st.session_state and st.session_state.guests:
    st.dataframe(
        [
            {
                "Código": g.code,
                "Nombre": g.name,
                "Número de invitaciones": g.allowed_guests,
                "Confirmación": g.confirmation,
                "Lugares confirmados": g.confirmed_guests,
            }
            for g in st.session_state.guests
        ]
    )
else:
    st.session_state["guests"] = None
    st.error("No hay invitados registrados")


st.header("Agregar invitado")

with st.form("add_guest"):
    code = st.text_input("Código único")
    name = st.text_input("Nombre / Familia")
    allowed = st.number_input("Invitados permitidos", min_value=1, value=1)

    submitted = st.form_submit_button("Agregar")

if submitted:
    session = SessionLocal()

    guest = Guest(code=code, name=name, allowed_guests=allowed)

    session.add(guest)
    session.commit()
    session.close()

    st.success(f"Invitado {name} agregado")


# st.header("Cargar invitados desde CSV")

# file = st.file_uploader("Selecciona archivo CSV", type="csv")

# if file:
#     df = pd.read_csv(file)
#     st.dataframe(df)

#     if st.button("Importar invitados"):
#         session = SessionLocal()

#         for _, row in df.iterrows():
#             guest = Guest(
#                 code=row["code"],
#                 name=row["name"],
#                 allowed_guests=int(row["allowed_guests"]),
#             )
#             session.add(guest)

#         session.commit()
#         session.close()

#         st.success("Invitados importados correctamente")

st.sidebar.header("Sincronización - Google Sheets")

st.sidebar.info(
    "Esto importará invitados desde Google Sheets.\n\n"
    "- Se crearán invitados nuevos\n"
    "- Se actualizarán solo campos permitidos\n"
    "- No se tocarán confirmaciones"
)

if st.sidebar.button("Importar desde Google Sheets"):
    session = SessionLocal()

    result = import_guests_from_google_sheets(session)
    session.close()

    st.sidebar.success(
        f"Importación completa:\n"
        f"- Creados: {result['created']}\n"
        f"- Actualizados: {result['updated']}\n"
        f"- Ignorados: {result['skipped']}\n"
        f"- Borrados: {result['deleted']}"
    )

if st.sidebar.button("Exportar a Google Sheets"):
    session = SessionLocal()
    export_guests_to_google_sheets(session)
    session.close()

    st.success("Invitados exportados correctamente a Google Sheets")

st.sidebar.header("Base de datos local")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "boda.db"

if not Path(DATA_DIR).exists() and st.sidebar.button("Crear tablas"):
    Base.metadata.create_all(engine)
    st.sidebar.success("Base de datos inicializada correctamente")

if st.sidebar.button("Resetear base de datos"):
    from wedding_confirmation.db.models import Base
    from wedding_confirmation.db.session import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    st.sidebar.success("Base de datos reseteada correctamente")
