#coding: utf-8
import re, json
import urllib.parse
from bs4 import BeautifulSoup


class HtmlParser(object):
    # 从响应提取连接并去重
    def parser_urls(self, response):
        pattern = re.compile(r'https://movie.mtime.com/(\d+)/')
        urls = pattern.findall(response)
        if urls is not None:
            return list(set(urls))
        else:
            return None

    # 从响应提取=到;之间的内容
    def parser_json(self, page_url, response):
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        if result is not None:
            value = json.load(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception as e:
                print(e)
                return None
            # 已上映
            if isRelease:
                if value.get('value').get('releaseType') == 1:
                    return self._parser_release(page_url, value, releaseType=1)
                if value.get('value').get('releaseType') == 3:
                    return self._parser_release(page_url, value, releaseType=3)
            # 未上映
            else:
                if value.get('value').get('releaseType') == 0:
                    return self._parser_no_release(page_url, value, releaseType=0)
                if value.get('value').get('releaseType') == 2:
                    return self._parser_no_release(page_url, value, releaseType=2)


    def _parser_release(self, page_url, value, releaseType):
        try:
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')

            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')

            ShowDays = boxOffice.get('ShowDays')
            try:
                Rank = boxOffice.get('Rank')
            except Exception:
                Rank = 0

            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal, RDirectorFinal, RStoryFinal,
                    Usercount, AttitudeCount, TotalBoxOffice+TotalBoxOfficeUnit, TodayBoxOffice+TodayBoxOfficeUnit,
                    Rank, ShowDays, releaseType)
        except Exception as e:
            print(e, page_url, value)
            return None

    def _parser_no_release(self, page_url, value, releaseType):
        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')

            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')

            try:
                Rank = value.get('value').get('hotValue').get('Ranking')
            except Exception:
                Rank = 0
            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal, RDirectorFinal, RStoryFinal,
                    Usercount, AttitudeCount, u'无', u'无', Rank, 0, releaseType)
        except Exception as e:
            print(e, page_url, value)
            return None