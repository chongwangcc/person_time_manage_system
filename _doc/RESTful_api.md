# API接口

## 获得每周的统计信息
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
- date_str: 日期字符串。 ```/api/v1/statistics/weekly/all/2019-01-19```
- Headers:
- Body:


####Response
- Body
```angular2html
{
  "each_category_time_sum": [
    {
      "name": "\u5a31\u4e50", 
      "value": 675.0
    }, 
    {
      "name": "\u5b66\u4e60", 
      "value": 1985.0
    }, 
    {
      "name": "\u5de5\u4f5c", 
      "value": 480.0
    }, 
    {
      "name": "\u6574\u7406", 
      "value": 280.0
    }, 
    {
      "name": "\u6742", 
      "value": 2370.0
    }, 
    {
      "name": "\u7761\u89c9", 
      "value": 3990.0
    }, 
    {
      "name": "\u8fd0\u52a8", 
      "value": 300.0
    }
  ], 
  "end_date": "2019-01-20", 
  "every_day_category_details": {
    "data": [
      [
        1.5, 
        0.0, 
        0.67, 
        0.75, 
        0.33, 
        2.0, 
        6.0
      ], 
      [
        4.5, 
        2.5, 
        5.0, 
        5.5, 
        8.0, 
        7.58, 
        0.0
      ], 
      [
        0.0, 
        4.0, 
        2.0, 
        1.5, 
        0.5, 
        0.0, 
        0.0
      ], 
      [
        2.17, 
        0.5, 
        0.5, 
        0.5, 
        0.5, 
        0.5, 
        0.0
      ], 
      [
        5.33, 
        6.5, 
        5.0, 
        4.92, 
        5.83, 
        5.75, 
        6.17
      ], 
      [
        10.5, 
        9.5, 
        9.83, 
        9.83, 
        8.83, 
        7.17, 
        10.83
      ], 
      [
        0.0, 
        1.0, 
        1.0, 
        1.0, 
        0.0, 
        1.0, 
        1.0
      ]
    ], 
    "legends": [
      "\u5a31\u4e50", 
      "\u5b66\u4e60", 
      "\u5de5\u4f5c", 
      "\u6574\u7406", 
      "\u6742", 
      "\u7761\u89c9", 
      "\u8fd0\u52a8"
    ], 
    "sum": [
      24.0, 
      24.0, 
      24.0, 
      24.0, 
      24.0, 
      24.0, 
      24.0
    ], 
    "xData": [
      "2019-01-13", 
      "2019-01-14", 
      "2019-01-15", 
      "2019-01-16", 
      "2019-01-17", 
      "2019-01-18", 
      "2019-01-19"
    ]
  }, 
  "execise_nums": 5, 
  "fun_nums": 6, 
  "missing_info": [], 
  "sleep_hours": {
    "actual_hours": [
      {
        "category": "2019-01-13", 
        "hours": 10.5
      }, 
      {
        "category": "2019-01-14", 
        "hours": 9.5
      }, 
      {
        "category": "2019-01-15", 
        "hours": 9.83
      }, 
      {
        "category": "2019-01-16", 
        "hours": 9.83
      }, 
      {
        "category": "2019-01-17", 
        "hours": 8.83
      }, 
      {
        "category": "2019-01-18", 
        "hours": 7.17
      }, 
      {
        "category": "2019-01-19", 
        "hours": 10.83
      }
    ], 
    "standard_hours": 7.5
  }, 
  "start_date": "2019-01-13", 
  "study_tomato_nums": 66.17, 
  "working_and_study_tomato_nums_of_each_day": 82.17, 
  "working_tomato_nums": 16.0
}
```
