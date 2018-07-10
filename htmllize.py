#! /usr/bin/env python3
"""
htmllize.py: Read logs from a text file and generate a simple HTML output.

This scripts expects the logs to be in a very specific format:

A sample of the log is below:

```
----BEGIN CLASS----
[04:46] <maxking> #startclass
[04:46] <maxking> THis is a class
[04:46] <maxking> There should be some logs
[04:46] <maxking> #endclass
----END CLASS----
```

The name of the file is also very specific: Logs-2018-06-18-04-46.txt

"""
import sys
from pathlib import Path
from string import Template
import re

DATE_DELIM = "/"
BASE_TEMPLATE = "logs-template.tmpl"
HTML_FILE_HEADER = """\
<!doctype html>

<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>#dgplug Summer Training Logs - $date</title>
    <meta name="description" content="DGPLUG Summer Training Logs">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style re="css/stylesheet">
      table { border: none; border-collapse: collapse; }
      table td { border-left: 1px solid #000; }
      table td:first-child { border-left: none; }
    </style>
  </head>
  <body>
    <h2> DGPLUG Summer Training Logs for $date </h2>
    <table class="table table-hover table-condensed">
"""
HTML_FILE_FOOTER = """\
    </table>
  </body>
</html>
"""

HTML_LOG_TEMPLATE = """\
      <tr>
        <td> <span class="text-muted"> {time} </span>: <span class="text-danger"> {nick} </span></td>
        <td class="text-success">{message}</td>
      </tr>
"""

# Here is the link to git gist with rail road diagram for web url regex
# https://gist.github.com/RatanShreshtha/76063f21ddbfb0335a341ce1c272170e

WEB_URL_REGEX = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})'
WEB_URL_REP_REGEX = r'<a href="\1" target="_blank">\1</a>'


def get_metadata(log_file_name):
    """Parse the log file name to get the data and time.

    :param str log_file_name: Name of the log file to parse.
    :returns: A tuple of date and time in which date is a list of
        [YYYY, MM, DD] and time is [HH, MM]
    :rtype: A tuple of lists.
    """
    metdata = log_file_name.replace('.txt', '').split('-')
    date = metdata[1:4]
    time = metdata[5:]
    return (date, time)


def parse_log_line(line):
    """Given a log line, parse and return all parts.

    A typical line looks like this:

       [04:46] <maxking> #startclass

    The first part is the date, 2nd part is nick of the user and finally the
    last part is the message.

    :param str line: A single message line.
    :returns: Tuple of (time, nick, message)
    :rtype: (str, str, str)
    """
    time, nick, *message = line.split(" ")
    # Strip the [ ] from the time.
    time = time[1:-1].strip()
    # Strip the < > from the nick.
    nick = nick[1:-1].strip()

    message = " ".join(message)
    message = re.sub(WEB_URL_REGEX, WEB_URL_REP_REGEX, message)

    return (time, nick, message)


def generate_html(log_file):
    """Generate the output HTML file from the text log file.

    .. note:: This overwrites if there is an HTML file that already exists.

    :param Path log_file: Log file to convert to HTML.
    """
    date, time = get_metadata(log_file.name)
    html_file = log_file.parent / log_file.name.replace('.txt', '.html')

    with html_file.open(mode='w') as output_file:
        output_file.write(
            Template(HTML_FILE_HEADER).safe_substitute(
                date=DATE_DELIM.join(date)
            )
        )
        with log_file.open(mode='r') as input_file:
            prev_nick = None
            for line in input_file.readlines():
                if "BEGIN CLASS" in line or "END CLASS" in line:
                    continue
                try:
                    time, nick, message = parse_log_line(line)
                    if prev_nick == nick:
                        nick = ''
                    output_file.write(HTML_LOG_TEMPLATE.format(time=time, nick=nick, message=message))  # noqa: E501
                    prev_nick = nick if nick != '' else prev_nick
                except ValueError:
                    # This usually means that the line is not of the format we
                    # executed. This is fine for the first and last line with
                    # --BEGIN CLASS-- and --END CLASS--.
                    print(f"skipping line: {line}")

        output_file.write(HTML_FILE_FOOTER)


def usage():
    """Print usage of the current script and exit."""
    print("Usage: python3 htmlize.py Logs-file.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    log_file = sys.argv[1]
    generate_html(Path(log_file))
