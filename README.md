# wz5zPracticeAutoSign

This script will sign practice data on wz5z system use the github actions

[![auto sign at 7 55 am](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/7_55_am.yml/badge.svg)](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/7_55_am.yml)

[![auto sign 1 00 pm](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/1_00_pm.yml/badge.svg)](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/1_00_pm.yml)

[![auto sign 10 00 am](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/9_00_am.yml/badge.svg?branch=main)](https://github.com/reterrrrrr/wz5zPracticeAutoSign/actions/workflows/9_00_am.yml)

set dinguserid to env ENV_DINGUSERID or use -d to point dinguserid if you want use custom config please according the this format:

~~~json
'[{"ding_id": "xxx", "lng": "xxx", "lat": "xxx", "companyId": "xxx", "random": true, "max_delay": 1800, "str5": "xxx", "ua": "xxx"}, {"ding_id": "xxx", "lng": "xxx", "lat": "xxx", "companyId": "xxx", "random": true, "max_delay": 1800, "str5": "xxx", "ua": "xxx"}]'
~~~

[shortcuts](https://www.icloud.com/shortcuts/a052d3c868074fb8b6325602e8b5f7d0)

you can get you dinguserid via get_info.py
if you should executable file please vist the [release](https://github.com/reterrrrrr/wz5zPracticeAutoSign/releases/tag/v1.0.0a)
