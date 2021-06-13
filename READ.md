# <center> Курсовая работа 
## <center> по дисциплине 
## <center> "Информационные системы аэрокосмических комплексов" 
### <center> Выполнил: ст. группы М3О-312б-18 Рысистов А.В

## Постановка задачи:
  
1. Скачать и установить веб-сервер.  
2. Настроить его на работу с localhost  
3. Реализовать форму с загрузкой файла  
3.1 Захостить приложение для расчета NDVI, при загрузке снимка рисовать в веб карту. 
## Описание инструментальных средств
Работа выполнена на операционной системе Ubuntu 16.04, код программы расчет нормализованного индекса растительности реализован на языке программирования высокого уровня Python. Веб-приложение реализовано с помощью фреймворка Flask, в качестве web-сервера использовался Nginx в сочетании с сервером web-приложений uWSGI <p>
Исходный код проекта представлен в репозитории на GitHub: https://github.com/AndreyRysistov/NDVI-web

### Установка инструментов
В первую очередь установим необходимые для работы интрументы: <p>
    1. andrey@andrey-VirtualBox:~$ sudo apt update
    2. andrey@andrey-VirtualBox:~$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
    3. andrey@andrey-VirtualBox:~$ sudo apt install nginx

## Установка пакетов Python:
    1. andrey@andrey-VirtualBox:~$ pip install numpy
    2. andrey@andrey-VirtualBox:~$ pip install opencv-python
    3. andrey@andrey-VirtualBox:~$ pip install Flask, uwsgi
## Создание приложения Flask
Исходный код приложения представлен в репозитории проекта. Запустаемый файл - app.py <p>
Web-приложение представляет собой веб-форму для загрузки снимков со стутника landsat-7 в формате .tif, а так же текстового описания данных снимков для расчета местоположения города. В результате на выходе мы получаем снимок местности с размеченными  по значению нормализованного индекса раститетельности (NDVI),с помощью цветовых диапазонов, объектов. <P>
В рамках тестирования приложения использовался снимок со спутника, пролетающего над городом Сидней.
Результат работы приложения представлен на рисунке:
## Создание точки входа UWSGI и ее настройка
Теперь создадим файл, который будет служить точкой входа в наше приложение. Это покажет серверу uWSGI, как с ним взаимодействовать.

Мы назовем этот файл wsgi.py: <p>
andrey@andrey-VirtualBox:~$ nano ~/myproject/wsgi.py <p>

		from myproject import app

		if __name__ == "__main__":

    		app.run()

Т
Проверим способность uWSGI обслуживать наше приложение.

Укажем сокет, чтобы запуск осуществлялся через общедоступный интерфейс, а также протокол, чтобы использовать протокол HTTP вместо двоичного протокола uwsgi. Мы будем использовать номер порта 5000, который предварительно откроем:

     1. andrey@andrey-VirtualBox:~$ sudo ufw allow 5000
     2. andrey@andrey-VirtualBox:~$ wsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

## Создание файла конфигураций uWSGI
Создадим файл конфигураций ndvi.ini: <p>
andrey@andrey-VirtualBox:~$ nano NDVI-web-master/ndvi.ini

    [uwsgi]
    module = wsgi:app
    master = true
    processes = 5
    socket = myproject.sock
    chmod-socket = 660
    vacuum = true
    die-on-term = true

Заголовок uwsgi указывает на необходимость применить настройки. По ссылке указываем точку входа и испоняемый файл. Затем мы указываем uWSGI начать работу в режиме мастера и создать пять рабочих процессов для обслуживания фактических запросов. Для обработки фактических клиентских подключений мы будем использовать веб-сервер Nginx, который будет передавать запросы uWSGI. Поскольку эти компоненты работают на одном компьютере, предпочтительно будет использовать сокет Unix, так как он быстрее и безопаснее. Назовем этот сокет ndvi.sock и разместим его в этом каталоге.

## Создание файла элементов systemd

Далее мы созадим файл служебных элементов systemd. Создание файла элементов systemd позволит системе инициализации Ubuntu автоматически запускать uWSGI и обслуживать приложение Flask при загрузке сервера.

Для начала создаем файл службы: <p>

andrey@andrey-VirtualBox:~$ sudo nano /etc/systemd/system/NDVI-web.service


	[Unit]
	Description=uWSGI instance to serve NDVI-web
	After=network.target

	[Service]
    User=andrey
    Group=www-data
    WorkingDirectory=/home/andrey/NDVI-web
    ExecStart=/usr/bin/uwsgi --ini ndvi.ini

    [Install]
    WantedBy=multi-user.target
Теперь мы запустим созданную службу uWSGI и активируем ее запуск при загрузке системы: <p>

    1. andrey@andrey-VirtualBox:~$ sudo systemctl start NDVI-web.service 
    2. andrey@andrey-VirtualBox:~$ sudo systemctl enable NDVI-web.service 
    3. andrey@andrey-VirtualBox:~$ sudo systemctl status NDVI-web.service 
    ● NDVI-web.service - uWSGI instance to serve NDVI-web
         Loaded: loaded (/etc/systemd/system/NDVI-web.service; enabled; vendor preset: enabled)
         Active: active (running) since Sun 2021-06-13 16:42:57 EET; 11s ago
       Main PID: 6224 (uwsgi)
          Tasks: 6 (limit: 4648)
         Memory: 3.2M
         CGroup: /system.slice/NDVI-web.service
                 ├─6224 /usr/bin/uwsgi --ini ndvi.ini
                 ├─6225 /usr/bin/uwsgi --ini ndvi.ini
                 ├─6226 /usr/bin/uwsgi --ini ndvi.ini
                 ├─6227 /usr/bin/uwsgi --ini ndvi.ini
                 ├─6228 /usr/bin/uwsgi --ini ndvi.ini
                 └─6229 /usr/bin/uwsgi --ini ndvi.ini
## Настройка Nginx для работы с запросами прокси-сервера

Сервер приложений uWSGI должен быть запущен и ожидать запросы файла сокета в каталоге проекта. Настроим Nginx для передачи веб-запросов на этот сокет с помощью протокола uwsgi.

Вначале мы создадим новый файл конфигурации серверных блоков в каталоге Nginx sites-available. Назовем его NDVI-web для соответствия остальным именам в этом модуле:

		andrey@andrey-VirtualBox:~$ sudo nano /etc/nginx/sites-available/NDVI-web
        
Содержимое файла:

        server {
            listen 90;
            server_name andrey-VirtualBox www.andrey-VirtualBox;

            location / {
                include uwsgi_params;
                uwsgi_pass unix:/home/andrey/NDVI-web/ndvi.sock;
            }
        }
Доменное имя получаем с помощью команды
	
    	andrey@andrey-VirtualBox:~$ hostname
	
Чтобы активировать созданную конфигурацию серверных блоков Nginx, необходимо привязать файл к каталогу sites-enabled:

		andrey@andrey-VirtualBox:~$ sudo ln -s /etc/nginx/sites-available/NDVI-web /etc/nginx/sites-enabled

Перезапустим процесс Nginx для чтения новой конфигурации: 

		andrey@andrey-VirtualBox:~$ sudo systemctl restart nginx

В заключение снова изменим настройки брандмауэра. Нам больше не потребуется доступ через порт 5000, и мы можем удалить это правило. Затем мы сможем разрешить доступ к серверу Nginx:

    	andrey@andrey-VirtualBox:~$ sudo ufw delete allow 5000
    	andrey@andrey-VirtualBox:~$ sudo ufw allow 'Nginx Full'

Теперь мы можем обращаться к приложению через доменное имя

		http://andrey-VirtualBox 
        
## Вывод

В процессе выполнения курсовой работы было реализовано web-приложение для расчета NDVI по загружаемым спутниковым снимкам. Была создана точка входа uWSGI, а также настроен автоматический запуск службы приложение systemd. Наконец приложение было развернуто на web-сервере Nginx, который позволяет пользователям по доменному имени подключаться к ресурсу.



