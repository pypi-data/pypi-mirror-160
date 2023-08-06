# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kbodata', 'kbodata.get', 'kbodata.load', 'kbodata.parser']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.6.2,<5.0.0',
 'pandas>=1.2.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'tqdm>=4.61.1,<5.0.0']

setup_kwargs = {
    'name': 'kbodata',
    'version': '0.1.7',
    'description': 'Scraping Korea Baseball Game information',
    'long_description': "# What is kbo-data\n\nkbo-data는 한국프로야구 경기정보를 스크래핑하는 파이썬 패키지입니다.  \nkbo-data is a Python package that provides Korean professional baseball game information by scraping.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kbodata)\n[![PyPI](https://img.shields.io/pypi/v/kbodata)](https://pypi.org/project/kbodata/)\n[![GitHub license](https://img.shields.io/github/license/Hyeonji-Ryu/kbo-data)](https://github.com/Hyeonji-Ryu/kbo-data/blob/main/LICENSE)\n\n## Required\n\n이 패키지를 사용하기 위해서는 chrome driver가 필요합니다. chrome driver는 [해당 페이지](https://chromedriver.chromium.org/downloads)에서 다운로드할 수 있습니다.  \nThis package is required chrome driver. You can download it from [this page](https://chromedriver.chromium.org/downloads)\n\n## How to Use\n\n### 패키지 설치하기\n\n먼저 패키지를 설치합니다.  \nyou have to install kbodata package first.\n\n```bash\npip install kbodata\n```\n\n### 데이터 가져오기 (kbodata.get module)\n\n원하는 날짜의 경기 스케쥴을 다운로드 받습니다.  \nyou can download KBO match schedule that you want to get.\n\n```python\n    import kbodata\n\n    # 2021년 4월 20일의 KBO 경기 스케쥴을 가져옵니다.\n    # Get the KBO match schedule for April 20, 2021.\n    >>> day = kbodata.get_daily_schedule(2021,4,20,'chromedriver_path')\n\n    # 2021년 4월 KBO 경기 스케쥴을 가져옵니다.\n    # Get the KBO match schedule for April 2021.\n    >>> month = kbodata.get_monthly_schedule(2021,4,'chromedriver_path')\n\n    # 2021년 KBO 경기 스케쥴을 가져옵니다. \n    # Get the KBO match schedule for 2021.\n    >>> year = kbodata.get_yearly_schedule(2021,'chromedriver_path')\n```\n\n해당 스케쥴을 바탕으로 경기 정보를 JSON 형식으로 가져옵니다.  \nIt will be broght match information in JSON format based on the schedule.  \n\n```python\n    # 2021년 4월 20일의 KBO 경기 정보를 가져옵니다.\n    # Get the KBO match information for April 20, 2021.\n    >>> day_data = kbodata.get_game_data(day,'chromedriver_path')\n\n    # 2021년 4월 KBO 경기 정보를 가져옵니다.\n    # Get the KBO match information for April 2021.\n    >>> month_data = kbodata.get_game_data(month,'chromedriver_path')\n\n    # 2021년 KBO 경기 정보를 가져옵니다. \n    # Get the KBO match information for 2021.\n    >>> year_data = kbodata.get_game_data(year,'chromedriver_path')\n```\n\nJSON 형식은 아래와 같습니다.  \nThe JSON format is as below.\n\n```ini\n    { id: date_gameid,\n    contents: {\n      'scoreboard': []\n      'ETC_info': {}\n      'away_batter': []\n      'home_batter': []\n      'away_pitcher': []\n      'home_pitcher': []\n        }\n    }\n```\n\n## 데이터 변형하기 (kbodata.load module)\n\n가져온 데이터들을 특정 파일 타입으로 변환합니다. 지원하는 파일 타입은 아래와 같습니다.  \nThis module converts data into specific file types. The supported file types are as follows.\n\n- DataFrame(pandas)\n- Dict\n\n```python\n    # 팀 경기 정보만을 정리하여 DataFrame으로 변환합니다.\n    scoreboard = kbodata.scoreboard_to_DataFrame(day_data)\n    # 타자 정보만을 정리하여 DataFrame으로 변환합니다.\n    batter = kbodata.batter_to_DataFrame(day_data)\n    # 투수 정보만을 정리하여 DataFrame으로 변환합니다.\n    pitcher = kbodata.pitcher_to_DataFrame(day_data)\n\n    # 팀 경기 정보만을 정리하여 Dict으로 변환합니다.\n    scoreboard = kbodata.scoreboard_to_Dict(day_data)\n    # 타자 정보만을 정리하여 Dict으로 변환합니다.\n    batter = kbodata.batter_to_Dict(day_data)\n    # 투수 정보만을 정리하여 Dict으로 변환합니다.\n    pitcher = kbodata.pitcher_to_Dict(day_data)\n```\n\n변환된 데이터에 대한 정보는 아래의 링크에서 확인할 수 있습니다.  \nYou can find information about the converted data at the link below.\n\n- Scoreboard: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/scoreboard.md\n- Batter: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/batter.md\n- Pitcher: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/pitcher.md\n\n## Issues\n\nKBO 공식 홈페이지에 없는 데이터는 제공되지 않습니다. 데이터가 제공되지 않는 경기 정보는 아래와 같습니다.  \nData that is not on the KBO official website is not provided. Match information for which data is not provided are listed below.  \n\n### 경기 기준 (from game)\n\n- 2008-03-30 LTHH0\n- 2009-04-04 WOLT0\n- 2010-03-20 OBLT0\n- 2010-03-20 WOSS0\n- 2015-07-08 HTWO0\n- 2018-08-01 WOSK0\n\n### 날짜 기준 (from date)\n\n- 2013-03-09\n- 2013-03-10\n- 2013-03-11\n- 2013-03-12\n- 2013-03-13\n- 2013-03-14\n- 2013-03-15\n- 2013-03-16\n- 2013-03-17\n- 2013-03-18\n- 2013-03-19\n- 2013-03-20\n",
    'author': 'Hyeonji-Ryu',
    'author_email': 'dev.bearabbit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hyeonji-Ryu/kbo-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
