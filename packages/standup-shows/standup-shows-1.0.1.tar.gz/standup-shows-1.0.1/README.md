<!-- # CLI -->
# Installation
```shell
$ pip install standup-shows
````

# Basic Usage
"Search for shows in a 50-mile radius from zipcode 75201 for comics listed in ./comics.txt"

```
$ standup 75201 50 comics.txt
Ms. Pat:
    Arlington Improv - Thursday, December 01 at 08:00 PM - https://www.dead-frog.com/live-comedy/event/881867
    Arlington Improv - Friday, December 02 at 07:30 PM - https://www.dead-frog.com/live-comedy/event/881868
    Arlington Improv - Friday, December 02 at 09:45 PM - https://www.dead-frog.com/live-comedy/event/881869
    Arlington Improv - Saturday, December 03 at 07:00 PM - https://www.dead-frog.com/live-comedy/event/881870
    Arlington Improv - Saturday, December 03 at 09:30 PM - https://www.dead-frog.com/live-comedy/event/881871
    Arlington Improv - Sunday, December 04 at 07:00 PM - https://www.dead-frog.com/live-comedy/event/881872

Mark Normand:
    Dallas Comedy Club - Wednesday, July 13 at 10:00 PM - https://www.dead-frog.com/live-comedy/event/123455
    Dallas Comedy Club - Wednesday, July 13 at 11:00 PM - https://www.dead-frog.com/live-comedy/event/123456
```

The script takes a few seconds to execute because it scrapes events from the web. You can specify the number of threads to create with the `--max_threads` flag.

```
$ standup --help
NAME
    standup.py - Find stand-up comedy shows that your favorite comedians are scheduled to perform near you.

SYNOPSIS
    standup.py COMEDIANS ZIPCODE <flags>

DESCRIPTION
    Find stand-up comedy shows that your favorite comedians are scheduled to perform near you.

POSITIONAL ARGUMENTS
    COMEDIANS
        Type: str
        A filepath containing a newline-delimited list of comedians in the form of <firstname lastname>.
    ZIPCODE
        Type: int
        The zipcode to search near.

FLAGS
    --radius=RADIUS
        Type: int
        Default: 25
        The radius in miles around the zipcode to search.
    --max_threads=MAX_THREADS
        Type: int
        Default: 100
        The maximum number of threads to create. A new thread is created for each URL to scrape.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

# Further Development
- Output to email
- Find a dataset to add support for musical artists
