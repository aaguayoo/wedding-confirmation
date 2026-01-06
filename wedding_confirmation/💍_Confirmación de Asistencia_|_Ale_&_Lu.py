"""Streamlit app."""

import base64
from pathlib import Path

import streamlit as st

from wedding_confirmation.db.session import SessionLocal
from wedding_confirmation.services.guests import (
    confirm_attendance,
    export_guests_to_google_sheets,
    get_guest_by_code,
)


def load_css() -> None:
    """Load the custom font and CSS styles for the Streamlit app.

    This function reads the font and CSS files, encodes the font, and injects
    the resulting styles into the Streamlit page.
    """
    css_path = Path("wedding_confirmation/assets/style.css")
    font1_path = Path("wedding_confirmation/assets/fonts/HuxleyVertical.otf")
    font2_path = Path("wedding_confirmation/assets/fonts/TheArtistSans.otf")

    font1_base64 = base64.b64encode(font1_path.read_bytes()).decode()
    font2_base64 = base64.b64encode(font2_path.read_bytes()).decode()

    with open(css_path) as f:
        css = f.read()

    font_face = f"""
    <style>
    @font-face {{
        font-family: 'Huxley Vertical';
        src: url(data:font/otf;base64,{font1_base64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}

    @font-face {{
        font-family: 'The Artist Sans';
        src: url(data:font/otf;base64,{font2_base64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}

    {css}
    </style>
    """

    st.markdown(font_face, unsafe_allow_html=True)


st.set_page_config(
    page_title="Confirmación de Asistencia | Ale & Lu",
    page_icon="💍",
    layout="centered",
)

load_css()

st.image(
    "wedding_confirmation/assets/lucero_y_alejandro.jpeg",  # guarda la imagen ahí
    use_container_width=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.title("Confirmación de Asistencia", anchor=False)
st.markdown(
    "## Nos hará muy felices contar contigo en este día tan especial 🫶. "
    "Por favor, ayúdanos confirmando tu asistencia y el número de lugares "
    "que utilizarás 😊."
)
st.markdown("---")

content = st.empty()
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.message = ""


if not st.session_state.submitted:
    with content.container():
        if codigo := st.text_input("Ingresa tu código de invitación"):
            session = SessionLocal()
            if invitado := get_guest_by_code(session, codigo):
                st.markdown("---")

                st.markdown(f"## Hola, {invitado.group}")
                names = invitado.names.split(", ")
                if invitado.confirmation == "Pendiente":
                    index = None
                elif invitado.confirmation == "Sí":
                    index = 0
                else:
                    index = 1
                confirmacion = st.radio(
                    f"¿Podrá{'n' if len(names) != 1 else 's'} asistir a la boda?",
                    ["Sí", "No"],
                    index=index,
                )

                if confirmacion == "Sí":
                    if len(names) != 1:
                        st.markdown(
                            f"### Invitaciones disponibles: {invitado.allowed_guests}"
                        )
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
                    "¡Gracias por respuesta 💜! Nos vemos pronto en Taxco 😊."
                    if confirmacion == "Sí"
                    else (
                        "Gracias por tu respuesta. "
                        f"{'Les vamos a extrañar ' if len(names) != 1 else 'Te vamos a extrañar '}"  # noqa
                        f"pero estará{'n' if len(names) != 1 else 's'} presente en nuestros corazones 😊."  # noqa
                    )
                )

                if st.button("Enviar confirmación"):
                    confirm_attendance(
                        session, invitado, confirmacion, num_confirmados, comentarios  # type: ignore  # noqa
                    )

                    st.session_state.submitted = True
                    st.session_state.message = message
                    content.empty()
            else:
                st.error(
                    f"Lo sentimos mucho, el código {codigo} no fue encontrado ☹️. "
                    "Revisa que el código coincida perfectamente con el que se te "
                    "compartió junto con la invitación 😊."
                )

if st.session_state.submitted:
    st.success(st.session_state.message)
    session = SessionLocal()
    export_guests_to_google_sheets(session)
    session.close()
