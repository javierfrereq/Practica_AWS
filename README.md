# Practica_AWS
* Practica_AWS - Curso_Aplicaciones_web_avanzado

Se explicará cómo crear una VM/instancia en AWS, conectarnos a ella a través de una computadora local mediante SSH y se configurará una aplicación que enviará recordatorios a un correo especifico, basándose en la información de un archivo en Excel.

## Por qué usar AWS?
Amazon Web Services proporciona una plataforma de infraestructura escalable, de confianza y de bajo costo en la nube. [enlace](https://aws.amazon.com/es/about-aws/)

### Creación de VM/instancia en AWS y configuración necesaria para conexión remota. 

Procedemos a crear una VM con los requerimientos necesarios a través del dashboard que ofrece AWS. 
Una vez creada podremos visualizar los siguiente:
![MV](https://user-images.githubusercontent.com/32844919/57976965-c3f0f980-79b2-11e9-9f41-6b2c1cf9cd6f.PNG)

Nos conectaremos a la instancia creada a través del cliente SSH y para eso necesitamos crear un “archivo.pem”. 

Le cambiamos los permisos al archivo.pem con el siguiente comando:

```chmod 400 JavierFrere.pem ```

Nos conectamos a la instancia con el siguiente comando:

```ssh -i "JavierFrere.pem" ubuntu@ec2-52-91-101-40.compute-1.amazonaws.com```

![Terminal - Connect](https://user-images.githubusercontent.com/32844919/57977036-53e37300-79b4-11e9-8413-718998946445.PNG)

### Agregar - subir archivos en una instancia alojada en AWS 

Ya conectados a la instancia que se creó en AWS, procedemos a subir los archivos de la aplicación **recuerdalo** con la siguiente línea de comando:

```scp -i "JavierFrere.pem" ./recuerdalo.tar.gz ubuntu@ec2-52-91-101-40.compute-1.amazonaws.com:/home/ubuntu/recuerdalo.tar.gz```

Descomprimimos el archivo recuerdalo.tar.gz en AWS con el siguiente comando:

```tar -zxvf recuerdalo.tar.gz```

### Permiso para el acceso de "GOOGLE SHEETS API" desde Python

Ingresamos al siguiente [enlace](https://developers.google.com/sheets/api/quickstart/python) y luego descargamos el **archivo.json** del enlace anterior y ejecutamos el script para autorizar el acceso. 

#### Ejemplo del formato "google sheets"

[Enlace](https://docs.google.com/spreadsheets/d/1d4aPIPSW7iyF8hE-S96_Rc1Nw0ljDCGU_l86IX7Ya84/edit?usp=sharing)


### Pasos para poner en funcionamiento la aplicación **[recuerdalo](https://github.com/javierfrereq/Practica_AWS/tree/master/recuerdalo)** 

#### 1.- Instalamos las librerías necesarias para que la aplicación funciones, con los siguientes comandos:

```sh
$ sudo apt update
$ sudo apt install python3-pip
$ pip3 --version
$ pip3 install pandas
$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### 2.- Modificamos los siguientes archivos:
[Conf.py](https://github.com/javierfrereq/Practica_AWS/blob/master/recuerdalo/._conf.py)
![Configuracion_correo](https://user-images.githubusercontent.com/32844919/57977193-ceae8d00-79b8-11e9-9934-e5bd5fb5613f.PNG)

Agregamos el correo a quien le llegará los recordatorios. 
```to = "<javierfrereq@gmail.com>" ```

[drive.py](https://github.com/javierfrereq/Practica_AWS/blob/master/recuerdalo/._drive.py)
![SHA Excel](https://user-images.githubusercontent.com/32844919/57977221-75932900-79b9-11e9-9e75-a0c4a751eede.PNG)

Agregamos ***ID_HOJA_GOOGLE_SHEETS*** del archivo de EXCEL que se usará para extraer la información que se desea recordar. 
```SAMPLE_SPREADSHEET_ID = '**ID_HOJA_GOOGLE_SHEETS**'```

#### 3.- Ejecución del Script que hará iniciar la Aplicación
Escribimos la siguiente línea de comando para iniciar el script de la aplicación:
``python3 script_recuerdalo.py``

![Ejecucion_Script](https://user-images.githubusercontent.com/32844919/57977288-e2f38980-79ba-11e9-8d70-6b11841d0667.PNG)

#### 4.- Creación del Crontab para automatizar el tiempo de los envíos de los recordatorios

Creamos el ***crontab*** con la siguiente línea de comando:

```Crontab -e```

Agregamos la siguiente línea en el crontab creado:

```0 11 * * * /bin/bash /home/ubuntu/practica_aws/recuerdalo/scripts.sh > /home/ubuntu/practica_aws/log.txt 2>&1```

#### 5.- Prueba de la funcionalidad de la aplicación

En la siguiente imagen podemos verificar los correos que llegaron recordando los eventos extraídos del Excel. 

![recordatorio](https://user-images.githubusercontent.com/32844919/57977345-3b775680-79bc-11e9-8692-696c96e7d389.PNG)




