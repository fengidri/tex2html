## nginx config

```
server {
	listen 80;
	server_name wiki.me;
    charset utf-8;
    set $type "";
    set $encoding "";

	location / {
                 index index.html;
                 root /var/www/wiki;
	}
	location /store {
                alias /home/feng/wiki;

                autoindex on;
                autoindex_format json;
	}
}
```
