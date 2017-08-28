# Learnweb-Downloader
This tool can be used to download resources from WWU Münster courses.

If your teacher does not put the files into separate folders, one cannot download the course materials easily. With this tool, these files can be downloaded.

# Requirements
Please install the following packages in order to use this tool:
    requests
    bs4
    lxml

# Usage
You can use the tool the following way

    python3 LearnwebDownloader.py [ZIV-ID] [ZIV-Password] [Course-ID]

# Limitations
Right now, the tool only downloads .pdf files. However, this should be sufficient for the most tasks.
Otherwise, just adjust the line 55 of the sourcecode.

https://github.com/hija/LearnwebDownloader/blob/master/LearnwebDownloader.py#L55
