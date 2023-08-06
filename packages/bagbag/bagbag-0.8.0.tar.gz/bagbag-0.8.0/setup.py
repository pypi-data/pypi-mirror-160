# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bagbag', 'bagbag.Tools']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.3,<3.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'langid>=1.1.6,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orator>=0.9.9,<0.10.0',
 'redis>=4.3.4,<5.0.0',
 'selenium>=4.3.0,<5.0.0',
 'telethon>=1.24.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'bagbag',
    'version': '0.8.0',
    'description': 'An all in one python library',
    'long_description': '# bagbag\n\nAn all in one python library\n\n# Install \n\n```bash\npip3 install bagbag --upgrade\n```\n\n# Library\n\n* Lg 日志模块\n  * Lg.SetLevel(level:日志级别:str)\n  * Lg.SetFile(path:日志路径:str, size:文件大小，MB:int, during:日志保留时间，天:int, color:是否带ANSI颜色:bool=True, json:是否格式化为json:bool=False):\n  * Lg.Debug(message:日志内容)\n  * Lg.Trace(message:日志内容)\n  * Lg.Info(message:日志内容)\n  * Lg.Warn(message:日志内容)\n  * Lg.Error(message:日志内容)\n* String(string:str) 一些字符串处理函数\n  * HasChinese() -> bool 是否包含中文\n  * Language() -> str 语言\n* Time 时间\n  * Strftime(format:str, timestamp:float|int) -> str\n  * Strptime(format:str, timestring:str) -> int\n* Re 正则\n  * FindAll(pattern: str | Pattern[str], string: str, flags: _FlagsType = ...) -> list\n* Tools 一些工具\n  * Selenium(SeleniumServer:str=None)\n    * Get(url:str)\n    * PageSource() -> str\n    * Close()\n  * Telegram(appid:str, apphash:str, sessionString:str=None)\n    * SessionString() -> str\n    * ResolvePeerByUsername(username:str) -> TelegramPeer\n      * History(limit:int=100, offset:int=0) -> list\n      * Resolve() -> None # 如果手动根据ID初始化一个TelegramPeer实例, 调用这个函数可以补全这个ID对应的Peer的信息\n  * ProgressBar(iterable_obj, startfrom=0, total=None, title=None, leave=False)\n  * Redis(host: str, port: int = 6379, database: int = 0, password: str = "")\n    * Set(key:str, value:str, ttl:int=None) -> (bool | None)\n    * Get(key:str) -> (str | None)\n    * Del(key:str) -> int\n    * Lock(key:str) -> RedisLock\n      * Acquire()\n      * Release()\n  * MySQL(host: str, port: int, user: str, password: str, database: str, prefix:str = "")\n  * SQLite(path: str, prefix:str = "")\n    * Execute(self, sql: str) -> (bool | int | list)\n    * Table(self, tbname: str) -> MySQLSQLiteTable\n      * AddColumn(self, colname: str, coltype: str, default=None, nullable:bool = True) -> MySQLSQLiteTable\n      * AddIndex(self, *cols: str) -> MySQLSQLiteTable\n      * Fields(self, *cols: str) -> MySQLSQLiteTable\n      * Where(self, key:str, opera:str, value:str) -> MySQLSQLiteTable\n      * WhereIn(self, key:str, value: list) -> MySQLSQLiteTable\n      * WhereNotIn(self, key:str, value: list) -> MySQLSQLiteTable\n      * WhereNull(self, key:str) -> MySQLSQLiteTable\n      * WhereNotNull_WillNotImplement(self, key:str)\n      * OrWhere(self, key:str, opera:str, value:str) -> MySQLSQLiteTable\n      * OrWhereIn_WillNotImplement(self, key:str, value: list)\n      * OrderBy(self, *key:str) -> MySQLSQLiteTable\n      * Limit(self, num:int) -> MySQLSQLiteTable\n      * Paginate(self, size:int, page:int) -> MySQLSQLiteTable\n      * Data(self, value:map) -> MySQLSQLiteTable\n      * Offset(self, num:int) -> MySQLSQLiteTable\n      * Insert(self)\n      * Update(self)\n      * Delete(self)\n      * InsertGetID(self) -> int\n      * Exists(self) -> bool\n      * Count(self) -> int\n      * Find(self, id:int) -> map\n      * First(self) -> map\n      * Get(self) -> list\n',
    'author': 'Darren',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/darren2046/bagbag',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
