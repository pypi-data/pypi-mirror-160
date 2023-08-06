#!/usr/bin/env python3
"""
A Python wrapper for Kavita API bindings
"""

# handle json
import json
# regex
import re
# Data types
from typing import Dict,Any,List,Optional
# creating web requests
import requests

class api:
    """
    Kavita server instance object

    Parameters:
        url: Server URL with http:// or https://
        apikey: API key for your user account
    """
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey

        # match http:// or https://
        if re.match(r"^https?://",self.url) is None:
            raise ValueError('Please prepend "http://" or "https://" to your URL') # pylint: disable=line-too-long

        http_headers = {"accept": "application/json"}
        r = requests.post(self.url + "/api/Plugin/authenticate",
                          headers=http_headers,
                          params="apiKey=" + apikey)

        # expose status code
        self.status_code = r.status_code

        # check http status code
        if r.status_code != 200:
            raise ValueError("Please check your URL and API key are correct")

        self.raw_plugin_auth = r.json()
        self.token = "bearer " + r.json()["token"]

    ###########################################################################
    # NOTE endpoints under /api/Reader

    def reader_chapter_info(self, chapter: int):
        """
        Return information about a single chapter

        Parameters:
            chapter (int): Chapter ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Reader/chapter-info",
                         headers=http_headers,
                         params="chapterId=" + str(chapter))
        self.status_code = r.status_code
        return(r.json())

    def reader_mark_multiple_series(self, operation, series_list):
        """
        Mark all series within the list as read/unread

        Parameters:
            operation: Either "read" or "unread". Determines executed operation
            series_list: A list of series IDs
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token,
                        "Content-Type": "application/json"}
        http_data: Dict[str,List[int]] = {"seriesIds": series_list}
        r = requests.post(self.url + "/api/Reader/mark-multiple-series-"
                          + operation,
                          headers=http_headers,
                          data=json.dumps(http_data))
        self.status_code = r.status_code
        return(r.json())

    def reader_mark_multiple_series_read(self, series_list):
        """
        Mark all series within the list as read
        Wrapper for reader_mark_multiple_series

        Parameters:
            series_list: A list of series IDs
        """
        r = self.reader_mark_multiple_series("read", series_list)
        return(r)

    def reader_mark_multiple_series_unread(self, series_list):
        """
        Mark all series within the list as unread
        Wrapper for reader_mark_multiple_series

        Parameters:
            series_list: A list of series IDs
        """
        r = self.reader_mark_multiple_series("unread", series_list)
        return(r)

    def reader_get_progress(self, chapter: int):
        """
        Return the progress for a chapter

        Parameters:
            chapter (int): Chapter ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Reader/get-progress",
                         headers=http_headers,
                         params="chapterId=" + str(chapter))
        self.status_code = r.status_code
        return(r.json())

    def reader_progress(self, series: int, volume: int,
                        chapter: int, page: int, bookscroll=None):
        """
        Set reading progress against chapter

        Parameters:
            series (int): Series ID the chapter belongs to
            volume (int): Volume ID the chapter belongs to
            chapter (int): Chapter ID
            page (int): Page number progress set

        Optional Parameters:
            bookscroll: Only valid for ebooks. Sets progress within a chapter
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token,
                        "Content-Type": "application/json"}
        # this dict is later encoded using json.dumps into a json payload
        http_data: Dict[str,int|str] = {"volumeId": volume,
                                        "chapterId": chapter,
                                        "pageNum": page,
                                        "seriesId": series,
                                        "bookScrollId": bookscroll}
        r = requests.post(self.url + "/api/Reader/progress",
                          headers=http_headers,
                          data=json.dumps(http_data))
        self.status_code = r.status_code
        return(r)

    def reader_continue_point(self, series: int):
        """
        Return the current progress for a series

        Parameters:
            series (int): Series ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Reader/continue-point",
                         headers=http_headers,
                         params="seriesId=" + str(series))
        self.status_code = r.status_code
        return(r.json())

    ###########################################################################
    # NOTE endpoints under /api/Library

    def library_scan(self, library: int):
        """
        Scan the given library

        Parameters:
            library (int): Library ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token,
                        "Content-Type": "application/json"}
        # this dict is later encoded using json.dumps into a json payload
        http_data: Dict[Any,Any] = {}
        r = requests.post(self.url + "/api/Library/scan",
                          headers=http_headers,
                          params="libraryId=" + str(library),
                          data=json.dumps(http_data))
        self.status_code = r.status_code
        return(r)

    def library_libraries(self):
        """
        Return all libraries
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Library/libraries",
                         headers=http_headers)
        self.status_code = r.status_code
        return(r.json())

    def library(self):
        """
        Return all libraries
        Wrapper for library_libraries
        """
        r = self.library_libraries()
        return(r)

    def library_search(self, query):
        """
        Search series by name

        Parameters:
            query: Search string
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Library/search",
                         headers=http_headers,
                         params="queryString=" + query)
        self.status_code = r.status_code
        return(r.json())

    ###########################################################################
    # NOTE endpoints under /api/Series

    # NOTE does not support the full request body of the endpoint
    def series(self,
               library=None,
               page_number=None,
               page_size=None,
               read_status: Optional[Dict[str,bool]]=None,
               request_body: Optional[Dict[str,Any]]=None
               ):
        """
        Return all series. Allows you to specify a variety of filters

        Optional Parameters:
            library (int): ID of library you want to list
            page_number (int)
            page_size (int)
            read_status (Dict): Change values by modifying this dict:
                                {"unread": True,
                                 "in_progress": True,
                                 "read": True}
            request_body (Dict): Use this to provide the full request body.
                                 read_status will be ignore if you use this.
                                 Check the Kavita API documentation to find
                                 all available settings.
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token,
                        "Content-Type": "application/json"}
        http_parameters = {"libraryId": library,
                           "PageNumber": page_number,
                           "PageSize": page_size}
        """
        Supported request body
        This is basically the filter you can use in the UI

        {
        "formats": [
            0, # ?
            1, # .cbz
            2, # ?
            3, # .epub
            4, # .pdf
        ],
        "readStatus": { # set read status filter
            "notRead": True,
            "inProgress": True,
            "read": True
        },
        "libraries": [0], # can also be used to limit the library
        "genres": [0], # genre ids
        "writers": [0], # writer ids
        "penciller": [0], # penciller ids
        "inker": [0], # inker ids
        "colorist": [0], # colorist ids
        "letterer": [0], # letterer ids
        "coverArtist": [0], # cover artist ids
        "editor": [0], # editor ids
        "publisher": [0], # publisher ids
        "character": [0], # character ids
        "translators": [0], # translators ids
        "collectionTags": [0], # collection tag ids
        "tags": [0], # tag ids
        "rating": 0, # 1-5 for number of stars. 0 is no stars given
        "sortOptions": {
            "sortField": 1, # 1-5
            "isAscending": True # True/False
        },
        "ageRating": [0],
        "languages": ["string"], # e.g. "en"
        "publicationStatus": [
            0, # Ongoing
            1, # Hiatus
            2, # Completed
            3, # Cancelled
            4, # Ended
        ],
        "seriesNameQuery": "string" # series search name
        }
        """

        # Set default value if none is provided
        if read_status is None:
            read_status = {"unread": True,
                           "inprogress": True,
                           "read": True}

        # check value of request_body
        if request_body is None:
            http_data: Dict[str,Any] = {"readStatus": {
                                            "notRead": read_status["unread"],
                                            "inProgress": (read_status
                                                           ["inprogress"]),
                                            "read": read_status["read"]
                                        },
                                        }
        else:
            http_data = request_body

        r = requests.post(self.url + "/api/Series",
                          params=http_parameters,
                          headers=http_headers,
                          data=json.dumps(http_data))
        self.status_code = r.status_code
        return(r.json())

    def series_volumes(self, series: int):
        """
        Return all volumes, chapters and page progress for a series

        Parameters:
            series (int): Series ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Series/volumes",
                         headers=http_headers,
                         params="seriesId=" + str(series))
        self.status_code = r.status_code
        return(r.json())

    def series_volume(self, volume: int):
        """
        Return information about the given volume

        Parameters:
            volume (int): Volume ID
        """
        http_headers = {"accept": "application/json",
                        "Authorization": self.token}
        r = requests.get(self.url + "/api/Series/volume",
                         headers=http_headers,
                         params="volumeId=" + str(volume))
        self.status_code = r.status_code
        return(r.json())

    ###########################################################################
