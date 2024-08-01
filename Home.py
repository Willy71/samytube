import streamlit as st
from googleapiclient.discovery import build

# Configuración de la página
st.set_page_config(page_title="YouTube Playlist Player", page_icon="▶️")

# Clave de la API de YouTube
API_KEY = st.secrets["youtube"]["api_key"]

# Crear el cliente de la API de YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Función para centrar el texto
def centrar_texto(texto, tamanho, color):
    st.markdown(f"<h{tamanho} style='text-align: center; color: {color}'>{texto}</h{tamanho}>",
                unsafe_allow_html=True)

def get_playlists():
    # Recuperar listas de reproducción del canal
    request = youtube.playlists().list(
        part='snippet',
        channelId='UCpVi9NfcKzRmNyVFkbsq3lA',
        maxResults=25
    )
    response = request.execute()
    return response['items']

def get_videos(playlist_id):
    # Recuperar videos dentro de una lista de reproducción
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    return response['items']

def main():
    centrar_texto("SamyTube Player")
    st.sidebar.title("Opciones")

    playlists = get_playlists()
    playlist_titles = [playlist['snippet']['title'] for playlist in playlists]
    selected_playlist = st.sidebar.selectbox("Selecciona una lista de reproducción", playlist_titles)

    if selected_playlist:
        playlist_id = next(playlist['id'] for playlist in playlists if playlist['snippet']['title'] == selected_playlist)
        videos = get_videos(playlist_id)
        video_ids = [video['snippet']['resourceId']['videoId'] for video in videos]

        # Generar la lista de reproducción en formato JavaScript
        playlist = ','.join(video_ids)

        # Insertar el reproductor de YouTube con la lista de reproducción
        # Insertar el reproductor de YouTube centrado
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <iframe id="player" type="text/html" width="640" height="390"
            src="https://www.youtube.com/embed/{video_ids[0]}?playlist={playlist}&autoplay=1&controls=1&loop=1"
            frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
