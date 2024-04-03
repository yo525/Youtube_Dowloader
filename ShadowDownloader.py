import dearpygui.dearpygui as dpg
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from os.path import exists
from pytube import YouTube, Playlist
from datetime import datetime
from hashlib import sha256
import os, sys
from mutagen.easyid3 import EasyID3
import mutagen


def resolver_ruta(ruta_relativa):   
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)

dpg.create_context()
dpg.create_viewport(title='ShadowDownloader',small_icon=resolver_ruta('icono.ico'),large_icon=resolver_ruta('icono.ico'),width=1000,height=482,max_width=1000,min_width=1000,max_height=482,min_height=482) 
 
logs = [str(datetime.now())]

#video o playlist
tipo = ''

urlll = ''
url = ''
formato = ''
idioma = ''
calidad = ''
nombre = ''
artista = ''
album = ''
ano = ''
genero = ''
path_descarga = ''

calidades_audio = ['MP4']#,'Wav', 'FLAC', 'MP3', 'M4a'
calidades_video = ['MP4', 'MOV', 'WMV', 'AVI']

lista_elementos = []
ids_tabla = []

exit_comodin = False

def elegir_ruta_descarga():
    global path_descarga
    path_descarga = askdirectory(mustexist=True,title='Download Path')
    dpg.set_value('path_descarga',path_descarga)


def nombre_change(sender,app_data):
    global nombre
    nombre = app_data

def artista_change(sender,app_data):
    global artista
    artista = app_data

def album_change(sender,app_data):
    global album
    album = app_data

def ano_change(sender,app_data):
    global ano
    ano = app_data

def genero_change(sender,app_data):
    global genero
    genero = app_data

def separar_entre_video_playlis(sender,app_data):
    global tipo, url
    url = app_data
    if 'watch' in app_data:
        tipo = 'video'
        dpg.configure_item('anadir',show=True)
        dpg.configure_item('anadir_videos_playlist',show=False)
        dpg.configure_item('anadir_playlist',show=False)
        try:
            video = YouTube(app_data)
            obtener_nombre = video.title
            dpg.configure_item('nombre_tag',default_value=str(obtener_nombre))
            nombre_change(None,obtener_nombre)
        except:
            pass
        try:
            video = YouTube(url)
            obtener_artista = video.author   
            dpg.configure_item('artista_tag',default_value=str(obtener_artista))         
            artista_change(None, obtener_artista)
        except:
            pass
    elif 'playlist' in app_data:
        tipo = 'playlist'
        dpg.configure_item('anadir',show=False)
        dpg.configure_item('anadir_videos_playlist',show=True)
        dpg.configure_item('anadir_playlist',show=True)
    else:
        tipo = ''
        dpg.configure_item('anadir',show=True)
        dpg.configure_item('anadir_videos_playlist',show=False)
        dpg.configure_item('anadir_playlist',show=False)
        try:
            video = YouTube(app_data)
            obtener_nombre = video.title
            dpg.configure_item('nombre_tag',default_value=str(obtener_nombre))
            nombre_change(None,obtener_nombre)
        except:
            pass
        
        try:
            video = YouTube(url)
            obtener_artista = video.author   
            dpg.configure_item('artista_tag',default_value=str(obtener_artista))         
            artista_change(None, obtener_artista)
        except:
            pass
        
    
def cambio_formato(sender,app_data):
    global formato
    formato = app_data
    if 'video' in formato:
        dpg.configure_item("select_box_calidad",default_value='Calidad del video',items=calidades_video,enabled = True)
    elif 'audio' in formato:
        dpg.configure_item("select_box_calidad",default_value='MP4',items=calidades_audio, enabled=True)
        cambio_calidad(None,'MP4')
    else:
        dpg.configure_item("select_box_calidad",default_value='', enabled=False)
    
    if 'subtitulos' in formato:
        dpg.configure_item("select_box_idioma",default_value='Idioma de los subtitulos',enabled = True)
    else:
        dpg.configure_item("select_box_idioma",default_value='',enabled = False)

    try:
        if 'video' in formato:
            dpg.configure_item("select_box_calidad_playlist",default_value=calidad,items=calidades_video,enabled = True)
        elif 'audio' in formato:
            dpg.configure_item("select_box_calidad_playlist",default_value=calidad,items=calidades_audio, enabled=True)
        else:
            dpg.configure_item("select_box_calidad_playlist",default_value='', enabled=False)
    
        if 'subtitulos' in formato:
            dpg.configure_item("select_box_idioma_playlist",default_value='Idioma de los subtitulos',enabled = True)
        else:
            dpg.configure_item("select_box_idioma_playlist",default_value='',enabled = False)
    except:
        anadir_log('not_know')


def cambio_idioma(sender,app_data):
    global idioma
    idioma = app_data


def cambio_calidad(sender,app_data):
    global calidad
    print('control')
    calidad = app_data

def url_video_exist(urll):
    try:
        YouTube(urll)
        return True
    except:
        return False
    
def url_playlist_exist(urll):
    try:
        Playlist(urll)
        return True
    except:
        return False


def anadir_log(log):
    global logs
    print(str(log))
    if len(logs) >= 1000:
        while (len(logs) >= 1000):
            logs.pop(0)
    logs.append(str(str(datetime.now())+':\t'+' '+str(log)))


def anadir_uno_x_uno(sender,app_data):
    global videos_lista, urlll
    if url_playlist_exist(url) == True:
        urlll = url
        videos = Playlist(url)
    else:
        showinfo(title='Error',message='Por favor introduce un url de youtube valido')
        anadir_log('URL de la playlist de youtube invalido')
        return None
    
    if exists(path_descarga) != True:
        showinfo(title='Error',message='Por favor introduce un directorio de descarga existente')
        anadir_log(log=('Download Path invalid or not exist '+str(url)))
        return None
    
    if formato == '':
        showinfo(title='Error',message='Por favor introduce una acción para hacer')
        anadir_log(log=('Invalid action '+str(url)))
        return None
    
    with dpg.window(tag='window_playlist',width=dpg.get_viewport_width()-15,height=dpg.get_viewport_height()-30,pos=[0,0],no_close=True,no_collapse=True,no_move=True,no_title_bar=True,no_background=True,no_resize=True,modal=True):
        dpg.add_input_text(tag="url_input_playlist",parent='window_playlist',width=970,readonly=True)
    
        dpg.add_spacer()

        with dpg.group(horizontal=True,parent='window_playlist',tag='grupo_formato_playlist'):
            
            dpg.add_combo(tag="select_box_formato_playlist",parent='grupo_formato_playlist',default_value=formato,
                          items=[#'Descargar video(+audio)',
                                 'Descargar audio', 
                                 #'Descargar Info', 
                                 #'Descargar subtitulos', 
                                 #'Descargar video(+audio) + informacion', 
                                 #'Descargar audio + informacion', 
                                 #'Descargar video(+audio) + subtitulos', 
                                 #'Descargar audio + subtitulos', 
                                 #'Descargar Info + subtitulos', 
                                 #'Descargar video(+audio) + informacion + subtitulos', 
                                 #'Descargar audio + informacion + subtitulos'
                                 ],
                          callback=cambio_formato,
                          width=333     
                          )

            dpg.add_combo(tag="select_box_idioma_playlist",parent='grupo_formato_playlist',default_value=idioma,
                          callback=cambio_idioma,
                          width=310,   
                          )


            dpg.add_combo(tag="select_box_calidad_playlist",parent='grupo_formato_playlist',default_value='MP4',
                      callback=cambio_calidad,
                      width=310    
                      )
        
            cambio_formato(None,'Descargar audio')
            cambio_calidad(None,'MP4')

        dpg.add_spacer()
        dpg.add_text(default_value='Tags (opcional):',parent='window_playlist')
        with dpg.group(horizontal=True,tag='grupo_tags_playlist',parent='window_playlist'):
            tamano_input_tags = 132
            dpg.add_text(parent='grupo_tags_playlist',default_value='Nombre:')
            dpg.add_input_text(parent='grupo_tags_playlist',hint='Nombre',tag='nombre_tag_playlist',width=tamano_input_tags,callback=nombre_change)
            dpg.add_text(parent='grupo_tags_playlist',default_value='Artista:')
            dpg.add_input_text(parent='grupo_tags_playlist',hint='Artista/s',tag='artista_tag_playlist',width=tamano_input_tags,callback=artista_change)
            dpg.add_text(parent='grupo_tags_playlist',default_value='Albúm:')
            dpg.add_input_text(parent='grupo_tags_playlist',hint='Albúm',tag='album_tag_playlist',width=tamano_input_tags,callback=album_change)
            dpg.add_text(parent='grupo_tags_playlist',default_value='Año:')
            dpg.add_input_text(parent='grupo_tags_playlist',hint='Año',tag='ano_tag_playlist',width=tamano_input_tags,callback=ano_change)
            dpg.add_text(parent='grupo_tags_playlist',default_value='Género:')
            dpg.add_input_text(parent='grupo_tags_playlist',hint='Género',tag='genero_tag_playlist',width=tamano_input_tags,callback=genero_change)

        dpg.add_spacer()
        dpg.add_spacer()
        dpg.add_spacer()
        with dpg.group(horizontal=True,parent='window_playlist',tag='grupo_path_playlist'):
            dpg.add_input_text(tag="path_descarga_playlist",parent='grupo_path_playlist',hint='Ruta de descarga...',readonly=True,width=910)
            dpg.add_button(tag='path_descarga_boton_playlist',parent='grupo_path_playlist',label='Browse',width=52,callback=elegir_ruta_descarga)

        dpg.add_spacer()

        with dpg.group(horizontal=True,parent='window_playlist',tag='botones_grupo_playlist'):
            dpg.add_button(tag='boton_cancelar_playlist',parent='botones_grupo_playlist',label='Salir/Cancelar',callback=salir_window_playlist)
            dpg.add_button(tag='boton_eliminar_playlist',parent='botones_grupo_playlist',label='Eliminar',callback=change_video_unoxuno)
            dpg.add_button(tag='boton_ok_playlist',parent='botones_grupo_playlist',label='Añadir',callback=anadir_video_unoxuno)

    cambio_formato(None,formato)
    
    videos_lista = [i for i in videos.video_urls]
    change_video_unoxuno()

def salir_window_playlist(sender,app_data):
    anadir_log('saliendo window_playlist')
    dpg.delete_item('window_playlist')
    separar_entre_video_playlis(None,urlll)

def change_video_unoxuno():
    global url
    if len(videos_lista) == 0:
        dpg.delete_item('window_playlist')
        anadir_log('lista_videos_playlist_finish')
        separar_entre_video_playlis(None,urlll)
        return None
    video = videos_lista.pop(0)
    url = video
    dpg.configure_item('url_input_playlist',default_value=str(video))
    dpg.configure_item('path_descarga_playlist',default_value=path_descarga)
    try:
        video = YouTube(url)
        obtener_nombre = video.title
        dpg.configure_item('nombre_tag_playlist',default_value=str(obtener_nombre))
        nombre_change(None,obtener_nombre)
        
    except:
        print('erro')
    
    try:
        video = YouTube(url)
        obtener_artista = video.author   
        dpg.configure_item('artista_tag_playlist',default_value=str(obtener_artista))         
        artista_change(None, obtener_artista)
        
    except:
        print('erro2')

def anadir_video_unoxuno(sender,app_data):
    anadir_video(None,None)
    change_video_unoxuno()


def anadir_elementos_playlist(sender,app_data):
    global url, exit_comodin
    if url_playlist_exist(url) == True:
        urll = url
        videos = Playlist(urll)
    else:
        showinfo(title='Error',message='Por favor introduce un url de youtube valido')
        anadir_log('URL de la playlist de youtube invalido')
        return None
    
    if exists(path_descarga) != True:
        showinfo(title='Error',message='Por favor introduce un directorio de descarga existente')
        anadir_log(log=('Download Path invalid or not exist '+str(url)))
        return None
    
    if formato == '':
        showinfo(title='Error',message='Por favor introduce una acción para hacer')
        anadir_log(log=('Invalid action '+str(url)))
        return None
    
    with dpg.window(tag='window_playlist_loading',width=dpg.get_viewport_width()-15,height=dpg.get_viewport_height()-30,pos=[0,0],no_close=True,no_collapse=True,no_move=True,no_title_bar=True,no_background=True,no_resize=True,modal=True):
        dpg.add_loading_indicator(tag='loading_playlist',parent='window_playlist_loading',style=0,circle_count=10,radius=25,pos=[100,100])
        dpg.add_input_text(parent='window_playlist_loading',tag='info_playlist_loading',multiline=True,readonly=True)

    info=[]
    videos_lista = videos.video_urls
    longitud = len(videos_lista)
    for url in videos_lista:
        #if exit_comodin == True:
         #   exit_comodin = False
          #  showinfo(title='Info',message='La operación a sido cancelada')
           # anadir_log('El añadimiento de videos a la tabla desde una playlist a sido cancelado')
            #break
        #Eror el boton no cancela

        try:
            video = YouTube(url)
            obtener_nombre = video.title
            nombre_change(None,obtener_nombre)
        except:
            pass
        try:
            video = YouTube(url)
            obtener_artista = video.author            
            artista_change(None, obtener_artista)
        except:
            pass
            

        info.append(url)
        dpg.set_value(item='info_playlist_loading',value=str('\n'.join(info)+'\t'+str(len(info))+' de: '+str(longitud)))
    
        anadir_video(None,None)

    dpg.delete_item('window_playlist_loading')


def anadir_video(sender,app_data):
    global lista_elementos, ids_tabla, tipo, nombre, url
    lista = []
    tags = [nombre,artista,album,ano,genero]

    if url_video_exist(url) == True:
        lista.append(url)
    else:
        showinfo(title='Error',message='Por favor introduce un url de youtube valido')
        anadir_log('URL de youtube invalido')
        return None
    
    for i in tags:
        if i == '' or i == ' ' or i == None or len(i) == 0:
            lista.append('-')
        else:
            lista.append(i)
    
    if exists(path_descarga) == True:
        lista.append(path_descarga)
    else:
        showinfo(title='Error',message='Por favor introduce un directorio de descarga existente')
        anadir_log(('Download Path invalid or not exist: '+str(url)))
        return None
    
    if formato != '':
        lista.append(formato)
    else:
        showinfo(title='Error',message='Por favor introduce una acción para hacer')
        anadir_log(('Invalid action',url))
        return None
    
    if idioma != '':
        lista.append(idioma)
    else:
        lista.append('-')
    
    if calidad != '':
        lista.append(calidad)
    else:
        if 'video' in formato:
            lista.append('MP4')
        elif 'audio' in formato:
            lista.append('MP3')
        else:
            lista.append('-')

    
    info = sha256(str(''.join(lista)).encode('utf-8')).hexdigest()
    if info not in ids_tabla:
        lista_elementos.append(lista)
        ids_tabla.append(str(info))

        with dpg.table_row(parent='tabla',tag=str(info)):
            dpg.add_selectable()
            for i in lista:
                dpg.add_text(default_value=i)
    else:
        showinfo('Info','El elemento ya existe')
        anadir_log('The element alredy exist')
        return None
    
    url = ''
    tipo = ''
    nombre = ''
    dpg.configure_item('url_input',default_value='')
    dpg.configure_item('nombre_tag',default_value='')
    


def descargar(sender,app_data):
    #URL/Nombre/Artista/Album/Año/género/Path_download/Accion/Idioma/Calidad
    anadir_log('Iniciando proceso_descaraga')
    
    with dpg.window(tag='window_download_loading',width=dpg.get_viewport_width()-15,height=dpg.get_viewport_height()-30,pos=[0,0],no_close=True,no_collapse=True,no_move=True,no_title_bar=True,no_background=True,no_resize=True,modal=True):
        dpg.add_loading_indicator(tag='loading_download',parent='window_download_loading',style=0,circle_count=10,radius=25,pos=[100,100])
        dpg.add_input_text(parent='window_download_loading',tag='info_download_loading',multiline=True,readonly=True)
    
    info=[]
    longitud=len(lista_elementos)
    abc = ' ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-1234567890()'
    for i in lista_elementos:
        url_download = i[0]
        nombre_download = i[1]
        nombre_download2 = ''
        for j in nombre_download:
            if j not in abc:
                nombre_download2 += ''
            else:
                nombre_download2 += j
        artista_download = i[2]
        album_download = i[3]
        ano_download = i[4]
        genero_download = i[5]
        path_download = i[6]
        accion_download = i[7]
        if i[8] != '-':
            idioma_download = i[8]
        else:
            idioma_download = ''

        if i[9] !='-':
            calidad_download = i[9]
        else:
            icalidad_download = ''
        
        info.append(url_download)
        dpg.set_value(item='info_download_loading',value=str('\n'.join(info)+'\t'+str(len(info))+' de: '+str(longitud)))
        
        yt = YouTube(url_download)

        yt.streams.filter(only_audio=True, mime_type="audio/mp4")
        stream = yt.streams.get_audio_only()
        stream.download(output_path=path_download,filename=nombre_download2+'.mp4')
        path = path_descarga+'\\'+nombre_download2+'.mp4'

        try:
            tags = EasyID3(path)
        except mutagen.id3.ID3NoHeaderError:    
            tags = mutagen.File(path, easy=True)
            tags.add_tags()
            

        tags['title'] = nombre_download2
        tags['artist'] = artista_download
        tags['album'] = album_download
        tags['date'] = ano_download
        tags['genre'] = genero_download
        tags['comment'] = 'Download with ShadowDownloader from: '+url_download
        tags['copyright'] = 'Copyright song to his artist'
        tags.save(path)
        
    anadir_log('Descarga_finalizada')
    for i in ids_tabla:
        dpg.delete_item(i)
    dpg.delete_item('window_download_loading')

def mostrar_logs(sender,app_data):
    showinfo('LOGS',message=str('\n'.join(logs)))

with dpg.window(tag='window',width=dpg.get_viewport_width()-15,height=dpg.get_viewport_height()-30,pos=[0,0],no_close=True,no_collapse=True,no_move=True,no_title_bar=True,no_background=True,no_resize=True):
    dpg.add_button(width=970,height=1,callback=mostrar_logs)
    with dpg.table(parent='window',tag='tabla',scrollY=True,height=200,sortable=True,header_row=True,resizable=True,borders_innerV=True,row_background=True,borders_innerH=True,freeze_rows=True):
        dpg.add_table_column(label='',init_width_or_weight=0.1175)
        dpg.add_table_column(label=' Enlace de descarga')
        dpg.add_table_column(label=' Nombre')
        dpg.add_table_column(label=' Artista')
        dpg.add_table_column(label=' Álbum')
        dpg.add_table_column(label=' Año')
        dpg.add_table_column(label=' Género')
        dpg.add_table_column(label=' Ruta de descarga')
        dpg.add_table_column(label=' Acción')
        dpg.add_table_column(label=' Idioma')
        dpg.add_table_column(label=' Calidad')


    dpg.add_spacer()
    dpg.add_separator()
    dpg.add_spacer()

    dpg.add_input_text(tag="url_input",parent='window',width=970,callback=separar_entre_video_playlis, hint="Introduce la url del video o playlist a descargar")
    
    dpg.add_spacer()
    
    with dpg.group(horizontal=True,parent='window',tag='grupo_formato'):
        
        dpg.add_combo(tag="select_box_formato",parent='grupo_formato',default_value='Descargar audio',
                      items=[#'Descargar video(+audio)',
                             'Descargar audio', 
                             #'Descargar Info', 
                             #'Descargar subtitulos', 
                             #'Descargar video(+audio) + informacion', 
                             #'Descargar audio + informacion', 
                             #'Descargar video(+audio) + subtitulos', 
                             #'Descargar audio + subtitulos', 
                             #'Descargar Info + subtitulos', 
                             #'Descargar video(+audio) + informacion + subtitulos', 
                             #'Descargar audio + informacion + subtitulos'
                             ],
                      callback=cambio_formato,
                      width=333 
                      )
        
        dpg.add_combo(tag="select_box_idioma",parent='grupo_formato',default_value='Idioma de los subtitulos',
                      callback=cambio_idioma,
                      width=310,
                      enabled= False    
                      )
        
        dpg.add_combo(tag="select_box_calidad",parent='grupo_formato',default_value='MP4',
                      callback=cambio_calidad,
                      width=310,
                      enabled= False    
                      )
        
        cambio_formato(None,'Descargar audio')
        cambio_calidad(None,'MP4')

    dpg.add_spacer()
    dpg.add_text(default_value='Tags (opcional):',parent='window')
    with dpg.group(horizontal=True,tag='grupo_tags',parent='window'):
        tamano_input_tags = 132
        dpg.add_text(parent='grupo_tags',default_value='Nombre:')
        dpg.add_input_text(parent='grupo_tags',hint='Nombre',tag='nombre_tag',width=tamano_input_tags,callback=nombre_change)
        dpg.add_text(parent='grupo_tags',default_value='Artista:')
        dpg.add_input_text(parent='grupo_tags',hint='Artista/s',tag='artista_tag',width=tamano_input_tags,callback=artista_change)
        dpg.add_text(parent='grupo_tags',default_value='Albúm:')
        dpg.add_input_text(parent='grupo_tags',hint='Albúm',tag='album_tag',width=tamano_input_tags,callback=album_change)
        dpg.add_text(parent='grupo_tags',default_value='Año:')
        dpg.add_input_text(parent='grupo_tags',hint='Año',tag='ano_tag',width=tamano_input_tags,callback=ano_change)
        dpg.add_text(parent='grupo_tags',default_value='Género:')
        dpg.add_input_text(parent='grupo_tags',hint='Género',tag='genero_tag',width=tamano_input_tags,callback=genero_change)
    
    dpg.add_spacer()
    dpg.add_spacer()
    dpg.add_spacer()
    with dpg.group(horizontal=True,parent='window',tag='grupo_path'):
        dpg.add_input_text(tag="path_descarga",parent='grupo_path',hint='Ruta de descarga...',readonly=True,width=910)
        dpg.add_button(tag='path_descarga_boton',parent='grupo_path',label='Browse',width=52,callback=elegir_ruta_descarga)
        
    
    dpg.add_spacer()
    with dpg.group(horizontal=True,tag='grupo_anadir'):
        dpg.add_button(tag='anadir_playlist',show=False,parent='grupo_anadir',label='Modificar los atributos de cada video de la playlist',width=480,height=25,callback=anadir_uno_x_uno)
        dpg.add_button(tag='anadir',parent='grupo_anadir',label='Añadir',width=970,height=25,callback=anadir_video)
        dpg.add_button(tag='anadir_videos_playlist',show=False,parent='grupo_anadir',label='Añadir',width=483,height=25,callback=anadir_elementos_playlist)

    dpg.add_spacer()
    dpg.add_separator()
    dpg.add_spacer()

    dpg.add_button(tag='descargar',parent='window',label='Descargar',width=970,height=30,callback=descargar)
        

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
