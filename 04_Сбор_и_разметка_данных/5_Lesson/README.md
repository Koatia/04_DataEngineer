1. Чтобы создать новый проект Scrapy, используем команду startproject.
За ней нужно  ввести название проекта, например news_vz и точку создания проекта:

```bash
scrapy startproject news_vz .
```

2. Чтобы создать паука используем команду genspider. За ней нужно ввести название паука, например news и домен:

```bash
scrapy genspider news vz.ru
```