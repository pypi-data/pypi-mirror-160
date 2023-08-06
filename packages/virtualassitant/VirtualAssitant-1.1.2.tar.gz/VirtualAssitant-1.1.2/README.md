# Proyecto Final, PYTHON BÁSICO

## Objetivos de aprendizaje
- Aplicar nuevas habilidades a un problema del mundo real
- Sintetizar las técnicas aprendidas

## Herramientas
- git
- github
- python
- poetry
- pandas
- numpy
- click
- speechrecognition
- google_auth
- PyAudio

> TODO: Actualizar la lista de herramientas si utilizo algún librería adicional.

## Organización de carpetas
> TODO: Actualizar, revisar uso de comando [tree](https://stackoverflow.com/questions/23989232/is-there-a-way-to-represent-a-directory-tree-in-a-github-readme-md) y [documento](https://github.com/kriasoft/Folder-Structure-Conventions/blob/master/README.md) de referencia



```
proyecto-bimestral-sb-a-drleon4
├── pyproject.toml   
├── poetry.lock 
├── propuesta.txt         
├── README.md                      
├── plantilla_doc.md            # Documentación del proyecto 
├── src
│   └── VirtualAssitant
│   │   ├── __init__.py
│   │   ├── assistent.py
│   │   ├── calendar_doc.py
│   │   └── credentials.json
│   ├── __init__.py
│   └── creative_event.py
├── img                         #archivos .png que se han ido añadiendo
├── dist                        #archivos generados por poetry
```

## Descripción

AgendAssistant es una aplicación desarrollada mediante la librería Speech Recognition y el api de google calendar, las cuales nos va a servir para desarrollar un mini asistente para
agendamiento de tareas (titulo de la tarea, descripción de la tarea, fecha de inicio y fecha de finalización de la tarea), para esto la api de google nos ayuda a registrar
las tareas dentro del calendario mediante el correo electrónico configurado y si tenemos ese correo electrónico sincronizado en nuestro dispositivo móvil, la tarea aparecerá 
dentro del calendario del móvil. Todo esto se lo registrará mediante comandos de voz luego de ejecutar la aplicación.

### Fuente de datos
> TODO: Detallar la fuente de datos sólo en el caso que su aplicación utilice datos externos. Agregar URLs.

A continuación se muestra un registro de actividades manualmente con google calendar

<div align="center">
<a href="https://www.youtube.com/watch?v=HnDE6X5ugSs&t=428s&ab_channel=Novax" target="_blank">
<img src="./img/conexion.png" >
</a>
<p>Conexion con google calendar</p>
</div>

<br/><br/>

Fuente confiable la cual indica como se realiza la instalación y descarga del archivo PyAudio

<div align="center">
<a href="https://www.youtube.com/watch?v=-3am_5jMzJ4&ab_channel=CodeWithHarry" target="_blank">
<img src="./img/pyaudio.png" >
</a>
<p>Instalacion de PyAudio</p>
</div>

<br/><br/>

Aquí se presenta como se puede crear un proyecto de google y como se genera el archivo .json para realizar la conexión
<div align="center">
<a href="https://www.youtube.com/watch?v=OwE6EjKn4oM&t=0s&ab_channel=Novax" target="_blank">
<img src="./img/proyectoGoogle.png" >
</a>
<p>Crear projectos en Google</p>
</div>

<br/><br/>

Aquí dejo el comando de como instalar las 3 librerias de google

> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

> NOTA: en caso de que el comando no funcione instalar cada una manualmente

## Versiones y evoluciones del producto

Versión 1.0.1 Julio 2022

- Recibe el título del evento
- Recibe la descripción del evento 
- Recibe la fecha de inicio del evento
- Recibe la fecha de fin del evento
- Envía el evento a la API de google auth
- Crea el evento dentro del calendario de google
