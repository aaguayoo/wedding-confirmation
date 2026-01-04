"""Admin Streamlit app."""

import pandas as pd  # type: ignore
import streamlit as st

from wedding_confirmation.db.models import Base, Guest
from wedding_confirmation.db.session import SessionLocal, engine

st.set_page_config(page_title="Admin – Wedding DB")

st.title("Administración – Base de Datos")

st.header("Inicializar base de datos")

if st.button("Crear tablas"):
    Base.metadata.create_all(engine)
    st.success("Base de datos inicializada correctamente")

if st.button("Resetear base de datos"):
    from wedding_confirmation.db.models import Base
    from wedding_confirmation.db.session import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    st.success("Base de datos reseteada correctamente")

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


st.header("Cargar invitados desde CSV")

file = st.file_uploader("Selecciona archivo CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.dataframe(df)

    if st.button("Importar invitados"):
        session = SessionLocal()

        for _, row in df.iterrows():
            guest = Guest(
                code=row["code"],
                name=row["name"],
                allowed_guests=int(row["allowed_guests"]),
            )
            session.add(guest)

        session.commit()
        session.close()

        st.success("Invitados importados correctamente")

st.header("Invitados registrados")

try:
    session = SessionLocal()
    guests = session.query(Guest).all()
    session.close()
except Exception:
    guests = None  # type: ignore
    st.warning("No data.")

if guests:
    st.dataframe(
        [
            {
                "code": g.code,
                "name": g.name,
                "allowed": g.allowed_guests,
                "confirmation": g.confirmation,
                "confirmed": g.confirmed_guests,
            }
            for g in guests
        ]
    )
else:
    st.info("No hay invitados registrados")

if st.secrets.get("ADMIN_PASSWORD"):
    pwd = st.text_input("Password", type="password")
    if pwd != st.secrets["ADMIN_PASSWORD"]:
        st.stop()
