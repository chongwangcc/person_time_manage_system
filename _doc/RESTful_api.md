# API接口

## 1. 获得每周的统计信息
获得每周的时间统计信息，目前总共有一下以下几种类型
- 本周开始结束时间  start_date、end_date
- 学习工作番茄时钟数量 working_and_study_tomato_nums_of_each_day
- 运动娱乐的次数 execise_nums、fun_nums
- 本周学习工作的番茄时钟总数 study_tomato_nums、working_tomato_nums
- 本周每天睡眠时长  sleep_hours
- 本周每天各类别时长明细 every_day_category_details
- 本周各类别总时间占比  each_category_time_sum
- 本周重叠时段或漏填的时段 missing_info

#### Request
- Method: **GET**
- URL: ```/api/v1/statistics/weekly/all/<date_str>```
- date_str: 日期字符串。 ```2019-01-19```
- Headers: Cookies ,用户必须已经登陆
- Body:


#### Response
- Body
```angular2html
{
    "each_category_time_sum": [
        {
            "name": "娱乐",
            "value": 30
        },
        {
            "name": "学习",
            "value": 300
        },
        {
            "name": "整理",
            "value": 380
        },
        {
            "name": "杂",
            "value": 630
        },
        {
            "name": "睡觉",
            "value": 1380
        }
    ],
    "end_date": "2019-03-09",
    "every_day_category_details": {
        "data": [
            [
                0.5,
                0
            ],
            [
                0,
                5
            ],
            [
                0,
                6.33
            ],
            [
                6.5,
                4
            ],
            [
                17,
                6
            ]
        ],
        "legends": [
            "娱乐",
            "学习",
            "整理",
            "杂",
            "睡觉"
        ],
        "sum": [
            24,
            21.33
        ],
        "xData": [
            "2019-03-03",
            "2019-03-04"
        ]
    },
    "execise_nums": 0,
    "fun_nums": 1,
    "sleep_hours": {
        "actual_hours": [
            {
                "category": "2019-03-03",
                "hours": 17
            },
            {
                "category": "2019-03-04",
                "hours": 6
            }
        ],
        "standard_hours": 8
    },
    "start_date": "2019-03-03",
    "study_tomato_nums": 10,
    "working_and_study_tomato_nums_of_each_day": 10,
    "working_tomato_nums": 0
}
```

## 2. 获得每月的统计信息
获得本月和上月的时间统计信息，目前总共有一下以下几种类型
- 本月开始结束时间  start_date、end_date
- 学习工作番茄时钟数量 study_tomato_nums,working_tomato_nums
- 活着时间占比，本月已过百分比 living_percent、during_percent
- 能力雷达 ability_redar
- 本月词云图  word_cloud
- 高效时段利用率 efficient_period_using_rate
- 活着时间走势图 living_time

#### Request
- Method: **GET**
- URL: ```/api/v1/statistics/monthly/all/<date_str>```
- date_str: 日期字符串。 ```2019-03```
- Headers: Cookies ,用户必须已经登陆
- Body:


#### Response
- Body
```angular2html
{
    "last_month": {
        "ability_redar": [
            {
                "name": "2019-02",
                "value": [
                    10,
                    3,
                    3,
                    10,
                    5
                ]
            }
        ],
        "during_percent": "100%",
        "efficient_period_using_rate": {
            "data": [
                0,
                0,
                0,
                0,
                10.91
            ],
            "name": "2019-02"
        },
        "end_date": "2019-02-28",
        "living_percent": "30%",
        "living_time": {
            "actual_hours": [
                {
                    "category": "2019-02-01",
                    "hours": 10
                },
                {
                    "category": "2019-02-02",
                    "hours": 2
                },
                {
                    "category": "2019-02-03",
                    "hours": 7.75
                },
                {
                    "category": "2019-02-04",
                    "hours": 3
                },
                {
                    "category": "2019-02-05",
                    "hours": 4.5
                },
            ],
            "standard_hours": 12
        },
        "start_date": "2019-02-01",
        "study_tomato_nums": 113.83,
        "word_cloud": [
            {
                "name": "玩游戏仙剑4",
                "value": 10
            },
            {
                "name": "玩游戏",
            },
            {
                "name": "去健身房",
                "value": 1
            }
        ],
        "working_tomato_nums": 85.33
    },
    "this_month": {
        "ability_redar": [
            {
                "name": "2019-03",
                "value": [
                    10,
                    0,
                    1,
                    10,
                    9
                ]
            }
        ],
        "during_percent": "13%",
        "efficient_period_using_rate": {
            "data": [
                34.09,
                26.67,
                0,
                18.18,
                0,
            ],
            "name": "2019-03"
        },
        "end_date": "2019-03-31",
        "living_percent": "26%",
        "living_time": {
            "actual_hours": [
                {
                    "category": "2019-03-01",
                    "hours": 7.5
                },
                {
                    "category": "2019-03-01",
                    "hours": 0.75
                },
                {
                    "category": "2019-03-01",
                    "hours": 1
                },
                {
                    "category": "2019-03-01",
                    "hours": 0.5
                }
            ],
            "standard_hours": 12
        },
        "start_date": "2019-03-01",
        "study_tomato_nums": 28.67,
        "word_cloud": [
            {
                "name": "给家里打电话",
                "value": 1
            },
            {
                "name": "记账本web界面调整",
                "value": 1
            },
            {
                "name": "读书第五项修炼",
                "value": 1
            },
            {
                "name": "时间日志调试bug",
                "value": 1
            },
            {
                "name": "时间日志调bug",
                "value": 3
            }
        ],
        "working_tomato_nums": 1.5
    }
}
```

## 3. 获得每年的统计信息
获得每年的统计信息，目前总共有一下以下几种类型
- 本年开始结束时间  start_date、end_date
- 学习工作番茄时钟数量 study_tomato_nums,working_tomato_nums
- 运动总次数 运动总时长 workout_hours、workout_nums
- 每周时长走势 every_week_category_details
- 本月词云图  word_cloud
- 各类矩形图 category_rectangle

#### Request
- Method: **GET**
- URL: ```/api/v1/statistics/yearly/all/<date_str>```
- date_str: 日期字符串。 ```2019```
- Headers: Cookies ,用户必须已经登陆
- Body:


#### Response
- Body
```angular2html
{
    "category_rectangle": {
        "娱乐": {
            "youtube": {
                "$count": 0.67
            },
            "youtube视频": {
                "$count": 1
            },
            "出去遛弯": {
                "$count": 0.67
            },
            "听新闻": {
                "$count": 0.25
            },
            "和家里打电话": {
                "$count": 1.83
            },
            "和苗苗聊天": {
                "$count": 4.67
            },
            "在家打牌": {
                "$count": 2.5
            },
            "我是大侦探": {
                "$count": 3.5
            },
            "我是米": {
                "$count": 1
            },
            "打牌": {
                "$count": 3
            },
            "玩游戏": {
                "$count": 80
            },
            "玩游戏仙剑4": {
                "$count": 1.33
            },
            "玩牌": {
                "$count": 2
            },
            "看书": {
                "$count": 1.75
            },
            "看电影": {
                "$count": 2
            },
            "看视频": {
                "$count": 1
            },
            "给家里打电话": {
                "$count": 2.92
            }
        },
        "运动": {
            "健身房走路": {
                "$count": 14
            },
            "健身房跑步": {
                "$count": 1
            },
            "出去散步": {
                "$count": 0.5
            },
            "出去遛弯": {
                "$count": 2.42
            },
            "去健身房": {
                "$count": 1
            },
            "去健身房走路": {
                "$count": 11
            },
            "去健身房跑步": {
                "$count": 3
            },
            "去外边遛弯": {
                "$count": 1
            },
            "跑步": {
                "$count": 0.5
            },
            "跑步3公里": {
                "$count": 1.5
            }
        }
    },
    "end_date": "12-31",
    "every_week_category_details": {
        "data": [
            [
                3,
                0,
                11.25,
                7.58,
                21.67,
                18.25,
                9.58,
                37.25,
                1,
                0.5
            ],
            [
                14,
                27,
                33.08,
                28.42,
                25.83,
                2,
                31.17,
                15,
                18.08,
                5
            ],
            [
                13,
                15,
                8,
                12.5,
                0,
                0,
                9.17,
                15.5,
                18.75,
                0
            ],
            [
                1.5,
                3.5,
                4.67,
                6,
                6.08,
                0,
                4.83,
                2,
                4.5,
                6.33
            ],
            [
                34.75,
                55.17,
                39.5,
                47.67,
                44.17,
                76.42,
                41.42,
                29.67,
                56.92,
                10.5
            ],
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0.5,
                0
            ],
            [
                48.75,
                62.33,
                66.5,
                63.58,
                68,
                71.33,
                65.33,
                60.33,
                64.25,
                23
            ],
            [
                5,
                5,
                5,
                2.25,
                2.17,
                0,
                6.5,
                6,
                4,
                0
            ]
        ],
        "legends": [
            "娱乐",
            "学习",
            "工作",
            "整理",
            "杂",
            "杂食",
            "睡觉",
            "运动"
        ],
        "sum": [
            120,
            168,
            168,
            168,
            167.92,
            168,
            168,
            165.75,
            168,
            45.33
        ],
        "xData": [
            "2018-12-30",
            "2019-01-06",
            "2019-01-13",
            "2019-01-20",
            "2019-01-27",
            "2019-02-03",
            "2019-02-10",
            "2019-02-17",
            "2019-02-24",
            "2019-03-03"
        ]
    },
    "study_tomato_nums": 399.17,
    "word_cloud": [
        {
            "name": "给家里打电话",
            "value": 3
        },
        {
            "name": "玩游戏仙剑4",
            "value": 12
        },
        {
            "name": "玩游戏",
            "value": 1
        },
        {
            "name": "玩游戏仙剑四",
            "value": 1
        },
        {
            "name": "玩牌",
            "value": 2
        },

    ],
    "working_tomato_nums": 183.83,
    "workout_hours": 71.83,
    "workout_nums": 40,
    "year": "2019"
}
```