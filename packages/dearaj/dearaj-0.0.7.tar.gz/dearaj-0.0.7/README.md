<div align="center">

  <img src="https://raw.githubusercontent.com/anzhi0708/dearAJ/main/img/logo.png" />

</div>

<br>

<div align="center">

  [![last-commit](https://img.shields.io/github/last-commit/anzhi0708/dearAJ?style=social)](https://github.com/anzhi0708/yeongnok/commits/main)    ![pypi-version](https://img.shields.io/pypi/v/dearaj?color=blue&style=flat-square) ![license](https://img.shields.io/github/license/anzhi0708/dearAJ?color=blue&style=flat-square)    ![repo-size](https://img.shields.io/github/repo-size/anzhi0708/dearAJ?style=social)

</div>


# dearAJ

**Data analysis tool for Korean National Assembly**

- [Installation](https://github.com/anzhi0708/dearAJ#install)
- [Usage](https://github.com/anzhi0708/dearAJ#usage)
  - mod `core`  
    - [MP](https://github.com/anzhi0708/dearAJ#mplist)
    - [MPList](https://github.com/anzhi0708/dearAJ#mplist)
    - [Speak](https://github.com/anzhi0708/dearAJ#speak)
    - [Movie](https://github.com/anzhi0708/dearAJ#movie)
    - Conference
    - Conferences
  - mod `local`
    - [Conference](https://github.com/anzhi0708/dearAJ#conferences)
    - [Conferences](https://github.com/anzhi0708/dearAJ#conferences)
- [License](https://github.com/anzhi0708/dearAJ#license)

## Install

```bash
pip3 install dearaj
```
or
```bash
git clone https://github.com/anzhi0708/dearAJ
cd dearAJ
make install
```

## Usage

```python
from dearaj import *
```

### MPList

Collection of single `MP`s using data from [열린국회정보](https://open.assembly.go.kr/portal/assm/search/memberHistSchPage.do).

```python
>>> MPList(20)
MPList(male=267, female=53, total=320)
```
```python
>>> for mp in MPList(19):
...     if mp.name == '문재인':
...             print(mp)
...
MP(generation=19, name='문재인', party='민주통합당', committee=[], region='부산 사상구', gender='남', n='초선', how='지역구')
```

### Conferences

`Conferences(n)` is the collection of the `n`th assembly's conferences. `Conference`s are the children of `Conferences`s.

```python
>>> for conf in Conferences(20):
...     print(conf)
...     print(conf.movies)
...     break
...
<2017-11-30, 10:14, 목, 제354회 국회(정기회) 제10차 법제사법위원회(1 movies)>
[Movie(real_time='10:14:00', play_time='02:28:19', speak_type='전체보기', no=423436, sublist=[Speak(real_time='10:14:01', play_time='00:01:12', speak_type='개의', no=423470, movie_title='권성동 위원장(자유한국당)  개의, 발언, 의사일정 제1항~제30항 상정', wv=0), Speak(real_time='10:15:13', play_time='00:04:25', speak_type='보고', no=423471, movie_title='금태섭 위원(더불어민주당)  보고', wv=0), Speak(real_time='10:19:39', play_time='00:03:11', speak_type='법안', no=423472, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제1항~제30항 의결', wv=0), Speak(real_time='10:22:50', play_time='00:04:21', speak_type='질의', no=423473, movie_title='윤상직 위원(자유한국당)  질의 / 김소영 처장(법원행정처)  답변 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:27:12', play_time='00:03:05', speak_type='질의', no=423474, movie_title='김진태 위원(자유한국당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:30:17', play_time='00:03:40', speak_type='질의', no=423475, movie_title='조응천 위원(더불어민주당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:33:58', play_time='00:03:57', speak_type='질의', no=423476, movie_title='주광덕 위원(자유한국당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='10:37:55', play_time='00:02:35', speak_type='질의', no=423477, movie_title='노회찬 위원(정의당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:40:30', play_time='00:03:05', speak_type='질의', no=423478, movie_title='이용주 위원(국민의당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='10:43:36', play_time='00:03:07', speak_type='질의', no=423479, movie_title='박주민 위원(더불어민주당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='10:46:43', play_time='00:04:24', speak_type='질의', no=423480, movie_title='박지원 위원(국민의당)  질의 / 김소영 처장(법원행정처)  답변 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:51:08', play_time='00:02:51', speak_type='질의', no=423481, movie_title='금태섭 위원(더불어민주당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='10:53:59', play_time='00:00:35', speak_type='발언', no=423482, movie_title='권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='10:54:35', play_time='00:04:07', speak_type='질의', no=423483, movie_title='이춘석 위원(더불어민주당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='10:58:42', play_time='00:02:54', speak_type='발언', no=423484, movie_title='권성동 위원장(자유한국당)  발언 / 김소영 처장(법원행정처)  발언', wv=0), Speak(real_time='11:01:36', play_time='00:01:34', speak_type='발언', no=423485, movie_title='이춘석 위원(더불어민주당)  발언 / 권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='11:03:11', play_time='00:03:05', speak_type='질의', no=423486, movie_title='백혜련 위원(더불어민주당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='11:06:17', play_time='00:00:47', speak_type='발언', no=423487, movie_title='권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='11:07:04', play_time='00:02:10', speak_type='발언', no=423488, movie_title='김진태 위원(자유한국당)  발언 / 김소영 처장(법원행정처)  발언', wv=0), Speak(real_time='11:09:15', play_time='00:03:22', speak_type='질의', no=423489, movie_title='박지원 위원(국민의당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='11:12:38', play_time='00:02:32', speak_type='질의', no=423490, movie_title='윤상직 위원(자유한국당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='11:15:10', play_time='00:02:48', speak_type='질의', no=423491, movie_title='주광덕 위원(자유한국당)  질의 / 김소영 처장(법원행정처)  답변', wv=0), Speak(real_time='11:17:59', play_time='00:01:59', speak_type='질의', no=423492, movie_title='백혜련 위원(더불어민주당)  질의 / 박상기 장관(법무부)  답변', wv=0), Speak(real_time='11:19:59', play_time='00:00:58', speak_type='법안', no=423493, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제31항~제39항 상정', wv=0), Speak(real_time='11:20:57', play_time='00:00:46', speak_type='보고', no=423494, movie_title='김진태 위원(자유한국당)  보고', wv=0), Speak(real_time='11:21:44', play_time='00:02:57', speak_type='법안', no=423495, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제31항~제39항 의결', wv=0), Speak(real_time='11:24:41', play_time='00:04:14', speak_type='질의', no=423496, movie_title='조응천 위원(더불어민주당)  질의 / 홍남기 실장(국무조정실)  답변 / 손병석 차관(국토교통부)  답변', wv=0), Speak(real_time='11:28:56', play_time='00:03:48', speak_type='질의', no=423497, movie_title='주광덕 위원(자유한국당)  질의 / 손병석 차관(국토교통부)  답변 / 홍남기 실장(국무조정실)  답변', wv=0), Speak(real_time='11:32:44', play_time='00:00:43', speak_type='발언', no=423498, movie_title='권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='11:33:28', play_time='00:02:18', speak_type='질의', no=423499, movie_title='정성호 위원(더불어민주당)  질의 / 김영록 장관(농림축산식품부)  답변', wv=0), Speak(real_time='11:35:47', play_time='00:02:12', speak_type='질의', no=423500, movie_title='윤상직 위원(자유한국당)  질의 / 손병석 차관(국토교통부)  답변', wv=0), Speak(real_time='11:37:59', play_time='00:01:11', speak_type='발언', no=423501, movie_title='권성동 위원장(자유한국당)  발언 / 손병석 차관(국토교통부)  발언', wv=0), Speak(real_time='11:39:11', play_time='00:04:10', speak_type='질의', no=423502, movie_title='조응천 위원(더불어민주당)  질의 / 도종환 장관(문화체육관광부)  답변 / 김영록 장관(농림축산식품부)  답변', wv=0), Speak(real_time='11:43:21', play_time='00:02:03', speak_type='질의', no=423503, movie_title='이용주 위원(국민의당)  질의 / 도종환 장관(문화체육관광부)  답변', wv=0), Speak(real_time='11:45:25', play_time='00:03:30', speak_type='질의', no=423504, movie_title='박지원 위원(국민의당)  질의 / 손병석 차관(국토교통부)  답변', wv=0), Speak(real_time='11:48:56', play_time='00:00:28', speak_type='발언', no=423505, movie_title='권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='11:49:24', play_time='00:02:29', speak_type='질의', no=423506, movie_title='박주민 위원(더불어민주당)  질의 / 도종환 장관(문화체육관광부)  답변', wv=0), Speak(real_time='11:51:54', play_time='00:00:39', speak_type='법안', no=423507, movie_title='금태섭 위원장대리(더불어민주당)  발언, 의사일정 제41항~제46항 상정', wv=0), Speak(real_time='11:52:33', play_time='00:00:51', speak_type='보고', no=423508, movie_title='전문위원  보고', wv=0), Speak(real_time='11:53:25', play_time='00:00:21', speak_type='발언', no=423509, movie_title='여상규 위원(자유한국당)  발언', wv=0), Speak(real_time='11:53:46', play_time='00:00:44', speak_type='법안', no=423510, movie_title='금태섭 위원장대리(더불어민주당)  발언, 의사일정 제41항~제46항 의결', wv=0), Speak(real_time='11:54:31', play_time='00:04:23', speak_type='질의', no=423511, movie_title='정갑윤 위원(자유한국당)  질의 / 김상곤 장관(교육부)  답변', wv=0), Speak(real_time='11:58:54', play_time='00:02:34', speak_type='질의', no=423512, movie_title='이용주 위원(국민의당)  질의 / 김상곤 장관(교육부)  답변', wv=0), Speak(real_time='12:01:29', play_time='00:04:19', speak_type='질의', no=423513, movie_title='주광덕 위원(자유한국당)  질의 / 김상곤 장관(교육부)  답변', wv=0), Speak(real_time='12:05:48', play_time='00:02:57', speak_type='질의', no=423514, movie_title='윤상직 위원(자유한국당)  질의 / 김상곤 장관(교육부)  답변', wv=0), Speak(real_time='12:08:45', play_time='00:00:34', speak_type='법안', no=423515, movie_title='금태섭 위원장대리(더불어민주당)  발언, 의사일정 제47항~제65항 상정', wv=0), Speak(real_time='12:09:20', play_time='00:02:39', speak_type='보고', no=423516, movie_title='전문위원  보고', wv=0), Speak(real_time='12:12:00', play_time='00:01:45', speak_type='발언', no=423517, movie_title='김진태 위원(자유한국당)  발언', wv=0), Speak(real_time='12:13:45', play_time='00:00:28', speak_type='발언', no=423518, movie_title='금태섭 위원(더불어민주당)  발언', wv=0), Speak(real_time='12:14:13', play_time='00:02:24', speak_type='법안', no=423519, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제47항~제58항, 제60항~제65항 의결 / 이진규 차관(과학기술정보통신부)  발언', wv=0), Speak(real_time='12:16:37', play_time='00:00:52', speak_type='질의', no=423520, movie_title='윤상직 위원(자유한국당)  질의 / 김용환 위원장(원자력안전위원회)  답변', wv=0), Speak(real_time='12:17:30', play_time='00:00:37', speak_type='법안', no=423521, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제66항~제80항 상정 / 이진규 차관(과학기술정보통신부)  발언', wv=0), Speak(real_time='12:18:07', play_time='00:02:19', speak_type='보고', no=423522, movie_title='전문위원  보고', wv=0), Speak(real_time='12:20:27', play_time='00:00:32', speak_type='발언', no=423523, movie_title='여상규 위원(자유한국당)  발언', wv=0), Speak(real_time='12:21:00', play_time='00:00:53', speak_type='발언', no=423524, movie_title='권성동 위원장(자유한국당)  발언 / 박능후 장관(보건복지부)  발언', wv=0), Speak(real_time='12:21:53', play_time='00:00:46', speak_type='발언', no=423525, movie_title='윤상직 위원(자유한국당)  발언', wv=0), Speak(real_time='12:22:39', play_time='00:00:10', speak_type='법안', no=423526, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제71항 의결', wv=0), Speak(real_time='12:22:50', play_time='00:01:00', speak_type='질의', no=423527, movie_title='이용주 위원(국민의당)  질의 / 박능후 장관(보건복지부)  답변', wv=0), Speak(real_time='12:23:51', play_time='00:02:30', speak_type='질의', no=423528, movie_title='조응천 위원(더불어민주당)  질의 / 박능후 장관(보건복지부)  답변', wv=0), Speak(real_time='12:26:21', play_time='00:01:46', speak_type='발언', no=423529, movie_title='김진태 위원(자유한국당)  발언', wv=0), Speak(real_time='12:28:07', play_time='00:01:35', speak_type='발언', no=423530, movie_title='박주민 위원(더불어민주당)  발언', wv=0), Speak(real_time='12:29:43', play_time='00:01:49', speak_type='발언', no=423531, movie_title='권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='12:31:32', play_time='00:00:53', speak_type='발언', no=423532, movie_title='조응천 위원(더불어민주당)  발언 / 권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='12:32:25', play_time='00:01:31', speak_type='질의', no=423533, movie_title='윤상직 위원(자유한국당)  질의 / 박능후 장관(보건복지부)  답변 / 권성동 위원장(자유한국당)  발언', wv=0), Speak(real_time='12:33:57', play_time='00:01:46', speak_type='질의', no=423534, movie_title='정갑윤 위원(자유한국당)  질의 / 박능후 장관(보건복지부)  답변', wv=0), Speak(real_time='12:35:43', play_time='00:02:02', speak_type='질의', no=423535, movie_title='윤상직 위원(자유한국당)  질의 / 박능후 장관(보건복지부)  답변', wv=0), Speak(real_time='12:37:45', play_time='00:03:20', speak_type='법안', no=423536, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제73항, 제78항 의결 / 박능후 장관(보건복지부)  발언 /    전문위원  발언 / 금태섭 위원(더불어민주당)  발언', wv=0), Speak(real_time='12:41:06', play_time='00:01:08', speak_type='산회', no=423537, movie_title='권성동 위원장(자유한국당)  발언, 의사일정 제66항~제68항, 제70항, 제72항, 제74항~제77항, 제79항, 제80항 의결, 산회', wv=0)])]
```

### Movie

A `Movie` object contains multuple `Speak`s, and other meta info. Sometimes a single `Conference` has multuple `Movie`s.

```python
>>> for conf in Conferences(10):
...     for movie in conf:
...             for speak in movie:
...                     print(speak)
...     break
...
Speak(real_time=None, play_time='00:05:58', speak_type='보고', no=106739, movie_title='구범모의원', wv=0)
Speak(real_time=None, play_time='00:02:15', speak_type='인사', no=106740, movie_title='부총리겸경제기획원장관', wv=0)
Speak(real_time=None, play_time='00:04:31', speak_type='기타', no=106741, movie_title='위원장', wv=0)
```

<div align="center">

  <img src="https://raw.githubusercontent.com/anzhi0708/dearAJ/main/img/actual_kr_conf_site_page.png" />
  A 'Movie' object contains multiple 'Speak' objects.

</div>

### Speak

Info about some specific `MP`'s speech, such as `speak_type` etc. A `Movie` can hold multuple `Speak`s.

## License

Copyright Anji Wong, 2022.

Distributed under the terms of the Apache 2.0 license.
