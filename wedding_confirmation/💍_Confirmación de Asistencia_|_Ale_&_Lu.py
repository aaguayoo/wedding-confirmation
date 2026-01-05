"""Streamlit app."""

import streamlit as st

from wedding_confirmation.db.session import SessionLocal
from wedding_confirmation.services.guests import confirm_attendance, get_guest_by_code


def load_css() -> None:
    """Load and apply the custom CSS styles for the confirmation app.

    This function reads the CSS file from the assets directory and injects its
    contents into the Streamlit page so that the confirmation UI uses the
    customized styling.
    """
    with open("wedding_confirmation/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Confirmación de Asistencia | Ale & Lu",
    page_icon="💍",
    layout="centered",
)
load_css()

st.image(
    "wedding_confirmation/assets/cover.png",  # guarda la imagen ahí
    use_container_width=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("# Confirmación de Asistencia")
st.markdown(
    "## Nos hará muy felices poder contar contigo en este día tan especial. "
    "Por favor, ayudannos confirmando tu asistencia, el número de "
    "invitaciones que utilizarás, y si reservarás habitación en el hotel donde "
    "se realizará la boda. 😊"
)
st.markdown("---")


if codigo := st.text_input("Ingresa tu código de invitación"):
    session = SessionLocal()
    if invitado := get_guest_by_code(session, codigo):
        st.markdown("---")

        st.markdown(f"### Hola, {invitado.group}")
        names = invitado.names.split(", ")
        confirmacion = st.radio(
            f"¿Podrá{'n' if len(names) != 1 else 's'} asistir a la boda?",
            ["Sí", "No"],
            index=0 if invitado.confirmation == "Sí" else 1,
        )

        if confirmacion == "Sí":
            st.markdown(f"### Invitaciones disponibles: {invitado.allowed_guests}")

            if len(names) != 1:
                num_confirmados = st.number_input(
                    "¿Cuántas personas asistirán?",
                    min_value=1,
                    max_value=invitado.allowed_guests,
                    value=invitado.confirmed_guests or 1,
                )
            else:
                num_confirmados = 1
        else:
            num_confirmados = None  # type: ignore

        st.markdown("---")
        comentarios = st.text_area(
            "Algo más que quisieras compartir con nosotros (opcional):",
            value=invitado.comments or "",
        )

        message = (
            "¡Gracias por respuesta💜! Nos vemos pronto en Taxco 😊."
            if confirmacion == "Sí"
            else (
                "Gracias por tu respuesta. Qué lástima que no nos podrás "
                "acompañar, pero estarás presente en nuestros corazones 😊"
            )
        )

        if st.button("Enviar confirmación"):
            confirm_attendance(
                session, invitado, confirmacion, num_confirmados, comentarios
            )
            st.success(message)

    else:
        st.error(
            f"Lo sentimos mucho, el código {codigo} no fue encontrado ☹️. Revisa "
            "que el código coincida perfectamente con el que se te compartió junto "
            "con la invitación 😊."
        )
