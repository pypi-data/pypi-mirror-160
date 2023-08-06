"""
This module provides functions and classes for performing
operations on local csv data files.
"""
import ajcore as core
from ajcore import MP, MPList, Movie, Speak, get_conf_vod_link

__all__ = [
    "core",
    "MP",
    "MPList",
    "Conference",
    "Conferences",
    "Movie",
    "Speak"
]


class Conference:
    """Conference from local data."""

    __slots__ = "angun_base", "sami", "minutes", "ct1", "ct2", "ct3", "menu", "type", "movie_list", "open_time", "week", "hand_lang", "date", "mc", "minutes_type", "audio_service", "title", "angun", "qvod"

    def __init__(
        self,
        angun_base: str,
        sami: str,
        minutes: str,
        ct1: str,
        ct2: str,
        ct3: str,
        menu: str,
        type: str,
        movie_list: list[dict],
        open_time: str,
        week: str,
        hand_lang: str,
        date: str,
        mc: str,
        minutes_type: str,
        audio_service: int,
        title: str,
        angun: list[dict],
        qvod: int
    ):
        self.angun_base: str = angun_base
        self.sami: str = sami
        self.minutes: str = minutes
        self.ct1: str = ct1
        self.ct2: str = ct2
        self.ct3: str = ct3
        self.menu: str = menu
        self.type: str = type
        self.movie_list: list = movie_list
        self.open_time: str = open_time
        self.week: str = week
        self.hand_lang: str = hand_lang
        self.date: str = date
        self.mc: str = mc
        self.minutes_type: str = minutes_type
        self.audio_service: int = audio_service
        self.title: str = title
        self.angun: list[dict] = angun
        self.qvod: int = qvod

    def __repr__(self) -> str:
        _type: str = "" if self.type in (None, "") else f" <{self.type}> "
        return f"<{self.date}, {self.open_time}, {self.week}, {self.title}{_type}({len(self.movies)} movies)>"

    @property
    def vod_link(self) -> str:
        return get_conf_vod_link(self)

    @property
    def local_csv_file_name(self) -> str:
        return f"{self.date}_gen{self.ct1}.{self.ct2}.{self.ct3}.{self.mc}_{self.open_time}({len(self.movies)}movies).csv"

    @property
    def default_file_name(self) -> str:
        return self.local_csv_file_name.replace(".csv", "")

    @property
    def confer_num_and_pdf_file_id(self) -> tuple[str, str]:
        pdf_link = self.minutes
        if pdf_link in ("", None):
            from sys import stderr

            print(
                f"This conference:\n{self.title!r}\nhas no valid PDF link, check\n{self.vod_link}\nfor details.",
                file=stderr,
            )
            return ("", "")
        import re

        try:
            confer_num: str = (
                re.search(r"conferNum=[^&]*", pdf_link)
                .group(0)
                .replace("conferNum=", "")
            )
        except:
            confer_num: str = ""
            from sys import stderr

            print(
                f"confer number not found\n{self.title!r}\n{pdf_link!r}\nhas no valid confer number, check\n{self.vod_link}\nfor details.",
                file=stderr,
            )
        try:
            pdf_file_id: str = (
                re.search(r"pdfFileId=[^&]*", pdf_link)
                .group(0)
                .replace("pdfFileId=", "")
            )
        except:
            pdf_file_id: str = ""
            from sys import stderr

            print(
                f"pdf id not found\n{self.conf_title!r}\n{pdf_link!r}\nhas no valid pdf ID, check\n{self.vod_link}\nfor details.",
                file=stderr,
            )
        return (confer_num, pdf_file_id)

    @property
    def confer_num(self) -> str:
        return self.confer_num_and_pdf_file_id[0]

    @property
    def pdf_file_id(self) -> str:
        return self.confer_num_and_pdf_file_id[1]

    def download_pdf(self, to: str = ".") -> bool:
        """
        Downloads pdf file to some path, defaults to '.'
        returns True if succeed, else False
        """
        with open(f"{to}/{self.default_file_name}.pdf", "wb") as output_pdf:
            output_pdf.write(self.pdf)
            return True
        return False

    @property
    def pdf(self) -> bytes:
        """Returns PDF raw bytes data"""
        action: str = "http://likms.assembly.go.kr/record/mhs-10-040-0040.do"
        import requests
        from faker import Faker
        # # # # # # # # # # #
        # HTTP POST method  #
        # # # # # # # # # # #
        respond = requests.post(
            action,
            data={
                "target": "I_TARGET",
                "enctype": "multipart/form-data",
                "conferNum": self.confer_num,
                "fileId": self.pdf_file_id,
            },
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": Faker().user_agent(),
            },
        )
        # # # # # # # # # # # #
        # returns binary data #
        # # # # # # # # # # # #
        return respond.content

    @property
    def movies(self) -> list:
        return self.movie_list

    def __iter__(self):
        return iter(self.movies)


class Conferences:
    """Load data from local disk"""
    __slots__ = "generation", "files", "conferences"

    def __init__(self, nth: int):
        self.generation: int = nth
        suffix: str = "" if self.generation > 9 else "0"
        # print(len(core.Local.files))
        print("Loading data... ", end="", flush=True)
        self.files = []
        for file in core.Local.files:
            if f"gen{suffix}{nth}" in str(file):
                self.files.append(file)
        self.conferences = []
        import csv
        import json
        for file in self.files:
            with open(file, "r") as conf_file:
                reader = csv.reader(conf_file)
                for line in reader:
                    current_raw_data = json.loads(line[0])
                    # import pprint
                    # pprint.pp(current_raw_data)
                    # self.conferences.append(
                    current_conf_movies_dict_data_list: list = current_raw_data['movieList']
                    current_conf_movies_list: list = []
                    for current_movie in current_conf_movies_dict_data_list:
                        current_movie_speak_list: list = current_movie.get('subList')
                        current_conf_movies_list.append(
                            Movie(
                                current_movie.get('realTime'),
                                current_movie['playTime'],
                                current_movie['speakType'],
                                current_movie['no'],
                                [
                                    Speak(
                                        d.get('realTime'),
                                        d.get('playTime'),
                                        d.get('speakType'),
                                        d.get('no'),
                                        d.get('movieTitle'),
                                        d.get('wv')
                                    )
                                    for d in current_movie_speak_list
                                ] if current_movie_speak_list is not None else []
                            )
                        )
                    current_conf = Conference(
                            current_raw_data['angunBase'],
                            current_raw_data['sami'],
                            current_raw_data['minutes'],
                            current_raw_data['ct1'],
                            current_raw_data['ct2'],
                            current_raw_data['ct3'],
                            current_raw_data['menu'],
                            current_raw_data['type'],
                            # current_raw_data['movieList'],
                            current_conf_movies_list,
                            current_raw_data['confOpenTime'],
                            current_raw_data['confWeek'],
                            current_raw_data['handlang'],
                            current_raw_data['confDate'],
                            current_raw_data['mc'],
                            current_raw_data['munitesType'],
                            current_raw_data['audioService'],
                            current_raw_data['confTitle'],
                            current_raw_data['angun'],
                            current_raw_data['qvod'],
                    )
                    self.conferences.append(current_conf)
        import os
        print("Done.\r", end="")
        print(" " * os.get_terminal_size().columns + "\r", end="")

    def __iter__(self):
        return iter(self.conferences)

    def __repr__(self) -> str:
        return f"<class '{self.generation}{core.suffix_of(self.generation)} Assembly conferences' ({len(self.conferences)} local records in {str(core.LOCAL_DATA_PATH)!r})>"
