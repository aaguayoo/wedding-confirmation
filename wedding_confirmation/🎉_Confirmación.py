"""Streamlit app."""

import streamlit as st

from wedding_confirmation.db.session import SessionLocal
from wedding_confirmation.services.guests import confirm_attendance, get_guest_by_code

st.title("Confirmación de Asistencia")

if codigo := st.text_input("Ingresa tu código de invitación"):
    session = SessionLocal()
    if invitado := get_guest_by_code(session, codigo):
        st.success(f"Hola {invitado.name}")
        st.write(f"Invitados permitidos: {invitado.allowed_guests}")

        confirmacion = st.radio(
            "¿Confirmas tu asistencia?",
            ["si", "no"],
            index=0 if invitado.confirmation == "si" else 1,
        )

        num_confirmados = (
            st.number_input(
                "¿Cuántas personas asistirán?",
                min_value=1,
                max_value=invitado.allowed_guests,
                value=invitado.confirmed_guests or 1,
            )
            if confirmacion == "si"
            else None
        )
        comentarios = st.text_area(
            "Comentarios (opcional)", value=invitado.comments or ""
        )

        if st.button("Guardar confirmación"):
            confirm_attendance(
                session, invitado, confirmacion, num_confirmados, comentarios
            )
            st.success("¡Gracias por confirmar!")

    else:
        st.error("Código no encontrado")
