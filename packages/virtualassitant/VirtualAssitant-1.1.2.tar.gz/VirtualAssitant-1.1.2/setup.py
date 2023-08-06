# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['virtualassitant']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['asistente = '
                     'src.VirtualAssitant.create_event:create_event']}

setup_kwargs = {
    'name': 'virtualassitant',
    'version': '1.1.2',
    'description': 'Agendamiento de actividades mediante comandos de voz en google calendar',
    'long_description': '# Proyecto Final, PYTHON BÁSICO\n\n## Objetivos de aprendizaje\n- Aplicar nuevas habilidades a un problema del mundo real\n- Sintetizar las técnicas aprendidas\n\n## Herramientas\n- git\n- github\n- python\n- poetry\n- pandas\n- numpy\n- click\n- speechrecognition\n- google_auth\n- PyAudio\n\n> TODO: Actualizar la lista de herramientas si utilizo algún librería adicional.\n\n## Organización de carpetas\n> TODO: Actualizar, revisar uso de comando [tree](https://stackoverflow.com/questions/23989232/is-there-a-way-to-represent-a-directory-tree-in-a-github-readme-md) y [documento](https://github.com/kriasoft/Folder-Structure-Conventions/blob/master/README.md) de referencia\n\n\n\n```\nproyecto-bimestral-sb-a-drleon4\n├── pyproject.toml   \n├── poetry.lock \n├── propuesta.txt         \n├── README.md                      \n├── plantilla_doc.md            # Documentación del proyecto \n├── src\n│   └── VirtualAssitant\n│   │   ├── __init__.py\n│   │   ├── assistent.py\n│   │   ├── calendar_doc.py\n│   │   └── credentials.json\n│   ├── __init__.py\n│   └── creative_event.py\n├── img                         #archivos .png que se han ido añadiendo\n├── dist                        #archivos generados por poetry\n```\n\n## Descripción\n\nAgendAssistant es una aplicación desarrollada mediante la librería Speech Recognition y el api de google calendar, las cuales nos va a servir para desarrollar un mini asistente para\nagendamiento de tareas (titulo de la tarea, descripción de la tarea, fecha de inicio y fecha de finalización de la tarea), para esto la api de google nos ayuda a registrar\nlas tareas dentro del calendario mediante el correo electrónico configurado y si tenemos ese correo electrónico sincronizado en nuestro dispositivo móvil, la tarea aparecerá \ndentro del calendario del móvil. Todo esto se lo registrará mediante comandos de voz luego de ejecutar la aplicación.\n\n### Fuente de datos\n> TODO: Detallar la fuente de datos sólo en el caso que su aplicación utilice datos externos. Agregar URLs.\n\nA continuación se muestra un registro de actividades manualmente con google calendar\n\n<div align="center">\n<a href="https://www.youtube.com/watch?v=HnDE6X5ugSs&t=428s&ab_channel=Novax" target="_blank">\n<img src="./img/conexion.png" >\n</a>\n<p>Conexion con google calendar</p>\n</div>\n\n<br/><br/>\n\nFuente confiable la cual indica como se realiza la instalación y descarga del archivo PyAudio\n\n<div align="center">\n<a href="https://www.youtube.com/watch?v=-3am_5jMzJ4&ab_channel=CodeWithHarry" target="_blank">\n<img src="./img/pyaudio.png" >\n</a>\n<p>Instalacion de PyAudio</p>\n</div>\n\n<br/><br/>\n\nAquí se presenta como se puede crear un proyecto de google y como se genera el archivo .json para realizar la conexión\n<div align="center">\n<a href="https://www.youtube.com/watch?v=OwE6EjKn4oM&t=0s&ab_channel=Novax" target="_blank">\n<img src="./img/proyectoGoogle.png" >\n</a>\n<p>Crear projectos en Google</p>\n</div>\n\n<br/><br/>\n\nAquí dejo el comando de como instalar las 3 librerias de google\n\n> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib\n\n> NOTA: en caso de que el comando no funcione instalar cada una manualmente\n\n## Versiones y evoluciones del producto\n\nVersión 1.0.1 Julio 2022\n\n- Recibe el título del evento\n- Recibe la descripción del evento \n- Recibe la fecha de inicio del evento\n- Recibe la fecha de fin del evento\n- Envía el evento a la API de google auth\n- Crea el evento dentro del calendario de google\n',
    'author': 'Danilo',
    'author_email': 'drleon416@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
