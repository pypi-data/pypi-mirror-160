# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['losaunideireccional']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'losaunideireccional',
    'version': '0.1.2',
    'description': 'Diseño de carga de losa alivianada',
    'long_description': 'Proyecto Final de Python \nSegundo Bimestre \n\n## Objetivos de aprendizaje\n- Aplicar de modulos y paquetes \n- Aplicación de funciones utilizando las diferentes normativas \n- \n\n## Herramientas\n- git\n- github\n- python\n- poetry\n- numpy\n\n\n## Organización de carpetas\n> TODO: Actualizar, revisar uso de comando [tree](https://stackoverflow.com/questions/23989232/is-there-a-way-to-represent-a-directory-tree-in-a-github-readme-md) y [documento](https://github.com/kriasoft/Folder-Structure-Conventions/blob/master/README.md) de referencia\n\n\n\n```\npoetry-demo\n├── pyproject.toml              \n├── README.md                   # Documentación del proyecto \n├── pyproject.toml\n├── propuesta.txt\n├── poetry.lock       \n├── __init__.py  \n├── main.py  \n├── LosaUnideireccional\n│   └── __init__.py\n│   └── armaduralongitudinal.py\n│   └── controlDeflexión.py\n│   └── determinación_de_Cargas.py\n│   └── determinaciónMomentos_Ultimos.py\n└── img\n```\n> TODO: Actualizar la lista de archivos.\n\n## Descripción\n> Diseño de Losa alivianada \n\nEste Programa nos permite calcular la carga que soportara la losa que esta pensada para diseñarse\nEs un losa de funciones basicas que se la utiliza para viviendas o escaleras, de construcción alivianada ya sea en su eje x o en su eje y \n\n### Fuente de datos\n> TODO: Detallar la fuente de datos sólo en el caso que su aplicación utilice datos externos. Agregar URLs.\n\nSe indica las normativas estandarizadas para la construcción en el ecuador \n\n> TODO: Actualizar captura y enlace  a video en youtube\n<div align="center">\n<a href="https://www.habitatyvivienda.gob.ec/documentos-normativos-nec-norma-ecuatoriana-de-la-construccion/" target="_blank">\n<img src="./img/FormulaNormativa.png" >\n</a>\n<p>Normativas NEC</p>\n</div>\n\n<br/><br/>\n\n## Versiones y evoluciones del producto\n> TODO: Completar\n\nVersión 0.1.2 Julio 2022\n\n- Cálculo  de diseño de losa \n- Cálculo de momento flector negativo \n- Cálculo de momento flector positivo \n- Correlación de grafica de pandeo para analisis \n \n- ....  \n',
    'author': 'Imanazco',
    'author_email': 'ivanna_ao97@outlook.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
