# Курсовая работа
Стукошин В. М3О-312Б-18.
  
### Постановка задачи
1. Скачать и установить веб-сервер.  
2. Настроить его на работу с localhost  
3. Реализовать форму с загрузкой файла  
4. Захостить python приложение из предыдущего семестра, при загрузке снимка рисовать в веб карту NDVI.  
  
## Ход выполнения работы:  
В работе использована CentOS 7.
Работать будем в директории ~/isak_kurs/.  
  
1. Установим пакеты для разработки.

        [stukoshin@localhost isak_kurs]$ sudo yum groupinstall "Development Tools"
        [stukoshin@localhost isak_kurs]$ sudo yum install python-pip python-devel gcc nginx  

2. Создадим приложение Flask_app  
    Установим uwsgi и flask:  

        [stukoshin@localhost isak_kurs]$ pip install uwsgi flask  

    Создадим приложение Flask:  

        [stukoshin@localhost isak_kurs]$ vi ~/isak_kurs/flask_app.py  
    Сохраним и закроем файл и сохраним его с помощью ":wq".  
  
3. Создадим точку входа WSGI.  
    Создадим файл wsgi.py:  
    
        [stukoshin@localhost isak_kurs]$ vim ~/isak_kurs/wsgi.py  
    Внутри напишем:  
    
        from isak_kurs import flask_app  
        if __name__ == "__main__":  
          flask_app.run()  
  
4. Настройка uWSGI.  
    Протестируем uWSGI:  

        [stukoshin@localhost isak_kurs]$ uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi &   

    После этого остановим uwsgi.

        [stukoshin@localhost isak_kurs]$ fg  
        uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
        ^C  
    Создадим файл конфигурации uWSGI:  
    
        [stukoshin@localhost isak_kurs]$ vi ~/isak_kurs/isak_kurs.ini  
    Введем следующее:  
    
        [uwsgi]  
        module = wsgi  
        master = true  
        socket = isak_kurs.sock  
        chmod-socket = 660  
      
5. Создадим файл службы systemd.  
    Создадим файл isak_kurs.service:  
    
        [stukoshin@localhost isak_kurs]$ sudo vi /etc/systemd/system/isak_kurs.service  
    Введем следующее: 
    
        [Unit]  
        Description=uWSGI for isak_kurs  
        After=network.target  
        [Service]  
        User=stukoshin  
        Group=nginx  
        WorkingDirectory=/home/stukoshin/isak_kurs  
        ExecStart=/home/stukoshin/isak_kurs/uwsgi --ini isak_kurs.ini  
        [Install]  
        WantedBy=multi-user.target 
    
    Запустим созданную службу:  
    
        [stukoshin@localhost isak_kurs]$ sudo systemctl start isak_kurs  
        [stukoshin@localhost isak_kurs]$ sudo systemctl enable isak_kurs  
      
6. Настроим Nginx.  
    Необходимо настроить Nginx для передачи веб-запросов в  сокет с использованием uWSGI протокола.  
    Откроем файл конфигурации:  
    
        [stukoshin@localhost isak_kurs]$ sudo vi /etc/nginx/nginx.conf  
    Найдем блок server в теле http, выше него создадим свой:  
    
        server {  
          listen 80;  
          server_name 10.0.2.15;  
          
          location / {
            include uwsgi_params;
            uwsgi_pass unix:/home/stukoshin/isak_kurs/isak_kurs.sock;
        }
    Сохраним файл и закроем его.  
    Добавим nginx пользователя в свою группу пользователей:  
    
        [stukoshin@localhost isak_kurs]$ sudo usermod -a -G stukoshin nginx  
    Предоставим группе пользователей права на выполнение в домашнем каталоге:  
    
        [stukoshin@localhost isak_kurs]$ chmod 710 /home/stukoshin  
    Запустим Nginx:  
    
        [stukoshin@localhost isak_kurs]$ sudo systemctl start nginx  
        [stukoshin@localhost isak_kurs]$ sudo systemctl enable nginx  
    
    Убедимся, что сайт работает выполнив команду:
    
        [stukoshin@localhost isak_kurs]$ curl 10.0.2.15:80 | head -n 3
    
    Получим следующий вывод в терминал:  
        \<head>  
        \<title>NDVI</title>  
        \</head>  
      
    # Вывод:  
    В ходе выполнения курсовой работы было создано приложение Flask, позволяющее загружать изображения спектров Landsat7 B3 и B4 и получать цветное изображение NDVI. 
    Также была создана и настроена точка входа WSGI, служба systemd и серверный блок Nginx. 
