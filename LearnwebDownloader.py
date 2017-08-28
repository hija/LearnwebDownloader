"""
Learnweb Downloader
Downloads the course resources which are not put into a learnweb directory.
"""

import os
import sys
import re
import requests
import lxml

from requests.auth import HTTPDigestAuth #Required for sso-auth
from bs4 import BeautifulSoup #Required for parsing website data
from urllib import parse

class LearnwebDownloader:
    """Downloading course resources of the learnweb of the university of Münster"""

    URL = "https://sso.uni-muenster.de/LearnWeb/learnweb2/course/resources.php"

    def __init__(self, username, password, courseid):
        self.username = username
        self.password = password
        self.courseid = courseid

        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username, self.password)

    def _login_and_receive(self):
        """Does login to the learnweb course and returns the website source"""
        data = self.session.get(LearnwebDownloader.URL,
                                params={'id': self.courseid})
        return data.text

    def download(self):
        """Downloads the resources of the learnweb course"""
        source = self._login_and_receive()
        page_data = BeautifulSoup(source, 'lxml')
        _course_title = page_data.title.string.split(':')[0]

        files = page_data.find_all('td', class_='cell')

        _dir_title = "unknown"
        for _file in files:

            _text = _file.get_text()
            # Parsing directory title
            if 'c0' in _file['class']: #Search for new title
                if _text:
                    _dir_title = LearnwebDownloader.slugify(_text)
            elif 'c1' in _file['class'] and _file.find('a'): #Search for a file
                _file_url = _file.find('a')['href']
                if _file_url:
                    _real_file_url = self._get_real_url(_file_url)
                    if _real_file_url.endswith('pdf'):
                        self._download_file(_real_file_url, _course_title + '/' + _dir_title)


    def _get_real_url(self, url):
        """The learnweb uses short urls, hiding the real filename.
        This method returns the real url"""
        _real_url = self.session.get(url, allow_redirects=False)
        if 'Location' in _real_url.headers:
            return _real_url.headers['Location']
        return url

    @staticmethod
    def slugify(value):
        """
        Code by Django Framework! It's used to create os-accepted directory names
        """
        stmp = str(value).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', stmp)

    def _download_file(self, download_url, directory_name):
        """
        Downloads a file
        """
        os.makedirs(directory_name, exist_ok=True) # Create the directory structure where the files shall be stored
        file_name = parse.unquote(download_url[download_url.rfind('/')+1:])
        with open(directory_name + '/' + file_name, "wb") as file:
            response = self.session.get(download_url) # Download the image
            file.write(response.content) # Write it into the file

if __name__ == "__main__":
    LearnwebDownloader(sys.argv[1], sys.argv[2], sys.argv[3]).download()
