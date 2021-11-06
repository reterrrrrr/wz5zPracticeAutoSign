# wz5zPracticeAutoSign

This script will sign practice data on wz5z system use the github actions

[![auto sign](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/github-actions.yml/badge.svg)](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/github-actions.yml)

[![auto sign d](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/main.yml/badge.svg)](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/main.yml)

set dinguserid to env ENV_DINGUSERID or use -d to point dinguserid if you want use custom config please according the this format:

~~~json
'[{"ding_id": "xxx", "lng": "xxx", "lat": "xxx", "companyId": "xxx", "random": true, "max_delay": 1800, "str5": "xxx", "ua": "xxx"}, {"ding_id": "xxx", "lng": "xxx", "lat": "xxx", "companyId": "xxx", "random": true, "max_delay": 1800, "str5": "xxx", "ua": "xxx"}]'
~~~

you can get you dinguserid via get_info.py
if you should executable file please vist the [release](https://github.com/reterrrrrr/wz5zPracticeAutoSign/releases/tag/v1.0.0a)
