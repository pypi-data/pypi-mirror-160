# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isptools',
 'isptools.Ping',
 'isptools.Pool',
 'isptools.Ports',
 'isptools.discovery']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['discover = ISPTools.main:main']}

setup_kwargs = {
    'name': 'isptools',
    'version': '0.1.0',
    'description': 'Utilidades para un ISP',
    'long_description': '\n# ISPTools\nEste genial paquete de herramientas de monitoreo te ofrece realizar de una forma muy facil el monitoreo de tu red\nISP, con esto puedes detectar si alguna ip que este fuera de tus colas esta consumiendo internet.\n\n## Demo\nEntre las 4 herramientas tenemos:\n#### 1°  Detectar ip e informacion del dispositivo actual\n     En esta opcion se obtienen los datos del ordenador donde se este ejecutando el programa:\\\n     De esta forma se optiene la ip y tambien el nombre del computador actual:\n![App Screenshot](https://i.stack.imgur.com/GBHKd.jpg)\n#### 2° Detectar dispositivo en un rango especifico:\n    Para poder escanear los dispositivos en un rango especifico se debe ingresar una ip en la cual se desee obtener la informacion\n    automatiamente obtenemos el rango y comenzamos a hacer ping en un pool desde 1 a 255:\\\n![App Screenshot](https://lh3.googleusercontent.com/Fj8dkhwMISmPSfnskbCy1O1952CRhFth5jEu3uh-n2-CuWpnqd10ntBhQCpVl3V1fRBkmMo5pBBeCWGPJFQJCt7iR-Iq4yaHmVWK0NXerRYbfxGW7Emm9jVROoiAV8tG7fkrLkReLEGFUE-LaDlPAPmzQTBw6ObVlLvMGNrxkyCbMgy9j1gD-_pm1fi7J2anxBcI8jDRV54XhZDdUMyfXJ6N_3lSmjruYWVzWb4llxry0E0C_GO3o6Kzdlca3raNrGbbI7rcBYRvgez5Ut-4ZSlFfeUoOx1iVGnV_sW_gXtH_a7aq047DS_ObDUIf4I5FhSjSMqqtgrCu_wecxXV9jVS4bNRFQ4a04eOAaGg0wi5Pcg07XnPuQMSZbEk5e7wbgoTWTZTKkW96xP8t3EY1FJyABkCmSBDVEC-PQrstgXDh-WGpPI3xbxc95ApukS1Mfsdh03LjJORE5MnXE5FQda5MYJUM-k2zNy6KieP8SSISf7fJF2MZpy0qeIYsLFbTq045M_jkHghEvVO7rMZ78_-AWm7VzJ03p6EL74UurvkYGZbSWV-6o-IsNA-dMrBYks_6fyyxCe3i9Z7wpSp6PyVEFeSsLySl10oQ_GnQ4taB8-rUFtVRu7TDU3H_BbW4AxiTr6B1w5tpufl8MiOiMIKeoOzsjOsDRUdMAx18eDVDLhbzZPImONhQNx7z_5GVCV3N7WRjCFaRuWXVfMyYzasobmcvGQqBy-WMXBHuypymmukmGFFdmnkdzhorXnoJ0155-hb7Ge6RshkkbaD-MG2DVWjTw=w327-h371-no?authuser=0)\n#### 3° Hacer ping a una IP\n    En esta parte se hace ping a una unica ip que es especificada por el usuario, es muy parecido\n    a la parte anterior pero unicamente a una sola direccion IP\n![App Screenshot](https://lh3.googleusercontent.com/Qky4iszvwcw5jt8t2Uwe5nRQjuk8pRBNiT-QOONzut3E_gYZefY0eNGVZ7Yd3nLjntrlkM9PFdr8jrU6GZGj-7S0UjPowrfeToluitAIZ1Ii8rHLEnIqDol8DGC12aZwZiEAsvQGF7rdUQw7Hhu95-sD7ChhzdbXTTmGxc_TJJWt_rsouSLogrFN3VE8sTTRNowLn75TsH70L0EzFjKC46i0jTN-L4U7BQiMwZNqQDu3MCw3VG9rZqG9imHGzeRVbW3twkRHw1U7bcxmzP5uJVJVCxqRmTEMz8hk8ofsUbDR_pmrXegul5Eqmo_7kLKPuH-z_NmTV-8DMvw12SU0Zwuhayfnr35RMpgN16XZ35q5nfjtiPyp7CPvajItVwN1XNPzSCYCHiE7PejiG__UH-sAiMcotYc865CO4ahISFunFGJhQk75dG7-X7kyqmQORbzNut7ELsVDxMWHxHJwSfygjJ82AKdtw2-JeJTv1_-r0C9n4ltPU8XVBQp9gU5t4WKfsjYgZtIxln3sOIRo9OFxtCQF3KH1SCGy5YaTB-w6e34FCtI_upEG_urTx1L5nalu_CU5LQZzp1vOqmTPUu2kYlHbtOEpekcvTxg-u4gdPqcUtehJaA5BIE8Zy10U2zF5ey4jbIPxBiVGwWlPbxiaF_jAExRi8_P0WCvYOOCPRn5ZP16x2Ch2NqKmCtGimwXq9Vw3JlO-ShS7fP9FoACo2Kzk2v0nudySJpJWq7gnmtyeR3pXjO556ArRqT--ik09IXCmkhWE9N5WutMqYeRFnH5Y1A=w786-h736-no?authuser=0)\n#### 4° Detectar puertos en una IP:\n    Para la deteccion de los puertos uilizamos el modulo socket, con un rango de puertos de 1 hasta 65535\n    en los cuales unicamente los puertos abiertos seran mostrados en pantalla:\n![App Screenshot](https://lh3.googleusercontent.com/PhxHe0RNWf4_J9SXdthfdjnIVD0JQcF-Wc3TbW2oWZeoko7TP_5hvT4Cegbf2vVyvMKBcOEZdfQKe9r_puZItK8dNWt15gqjoS4718R8Ce7OHxhcHY0WJGaiKMkjme1VQQ4-Hprq_Fyg5V_wgmjfwJWdM8EHoC4YuHwpNQ4haV7gBk-QYh_NaCNje6hS1bp6TjvkgsSzIrQxmMWV4VMql2TzePuMC-OW3D0BqZ72llMRWEvu8BLDr4C7S33tKOqWw0qykgiXaoLOYtJrPfUzPJCv6Nd-92ZCkTyhzDPdD4SSG349AncY-u2SDLrd36lf4Lp4M3gtrVMpgP6dpc3xr0o_8skDrHaeO1Dxh785p5huyMlAx9xIw_6VfqYRS2Ds0qHTMb-NhSpQkB_4n7EAWGXhGRmW2TfQlbLm_87JUg8JTQzkDHm9C04U4lHrS2bju3TirNC8uXpyDuuBSHWOeDmOWsCFzj-M3sZXlt9sndY1-ppo3DZPN82ZaiuDWCcGVN2hskusnb0mCXjv-2_3Iemp2CbQ60gkFUiW7bJUbdvMcVKe_KJYcGVHWQXWAJ-ESO4nW66zBXlSpw4DOuLdFMP9M3TIYCtnGnUojuYYb_qR-KoPZp5Rmfvquqb_LeoYtO8Z_Dpy5B1YhDjo0BwQKuqIpfN-8WLdL0n4II0SqiaiV8HqTKGEtLp0Mj4y0cHUf92Bx4c4alQUv5QT24ZcWmvQpHv7Unwg-CZ_2ytM3vJxVamMNTW20M3nVvPa8drUTsHzOVSZzIR7-c8z6n_Zbqpv0QyGLg=w708-h725-no?authuser=0)\nCon esto finalizamos las herramientas disponibles en la version 1.0\n## Author\n\n- [@David Macanchi](https://github.com/mattnial)\n\n\n## Support\n\nPara cualquier duda o recomendacion puedes escribirme a: dmmacanchi@utpl.edu.ec',
    'author': 'David Macanchi',
    'author_email': 'dmmacanchi@utpl.edu.ec',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
