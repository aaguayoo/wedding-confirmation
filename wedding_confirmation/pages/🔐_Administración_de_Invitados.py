"""Admin Streamlit app."""

import streamlit as st

from wedding_confirmation.db.models import Base, Guest
from wedding_confirmation.db.session import SessionLocal, engine
from wedding_confirmation.services.guests import (
    export_guests_to_google_sheets,
    import_guests_from_google_sheets,
)
from wedding_confirmation.utils.utils import generate_random_id

st.set_page_config(page_title="Admin – Wedding RSVP", page_icon="🔐")

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]


st.title("Administración – Base de Datos")


pwd = st.text_input("Password de administración", type="password")
if pwd != ADMIN_PASSWORD:
    st.stop()

st.markdown("---")

try:
    session = SessionLocal()
    st.session_state.guests = session.query(Guest).all()
    session.close()
except Exception:
    st.session_state.guests = None  # type: ignore
    st.error("No existe la tabla de SQL.")

if "guests" in st.session_state and st.session_state.guests:
    st.dataframe(
        [
            {
                "Código": g.code,
                "Nombres": g.names,
                "Grupo": g.group,
                "Número de invitaciones": g.allowed_guests,
                "Confirmación": g.confirmation,
                "Lugares confirmados": g.confirmed_guests,
                "Comentarios": g.comments,
            }
            for g in st.session_state.guests
        ]
    )
else:
    st.session_state["guests"] = None
    st.warning("No hay invitados registrados")

st.header("Agregar invitado")

with st.container(border=True):
    code = generate_random_id()

    type_ = "Familia"

    label = "Nombre" if type_ == "Invitado" else "Familia"
    name = st.text_input(label)

    allowed = (
        st.number_input("Invitados permitidos", min_value=1, value=1)
        if type_ == "Familia"
        else 1
    )

    group = name
    names = []
    with st.container(border=True):
        for _ in range(allowed):
            guest_name = st.text_input(f"Invitado {_ + 1}")
            names.append(guest_name)
    submitted = st.button("Agregar")
    session = SessionLocal()
    export_guests_to_google_sheets(session)
    session.close()


if submitted:
    session = SessionLocal()

    guests = Guest(
        code=code, names=", ".join(names), group=group, allowed_guests=allowed
    )

    session.add(guests)
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

#    if st.sidebar.button("Exportar a Google Sheets"):
#        session = SessionLocal()
#        export_guests_to_google_sheets(session)
#        session.close()
#
#        st.success("Invitados exportados correctamente a Google Sheets")

st.sidebar.header("Base de datos")

if st.sidebar.button("Borrar base de datos"):
    Base.metadata.drop_all(engine)
    st.sidebar.warning("Se ha borrado la base de datos.")

Base.metadata.create_all(engine)
