import argparse
import logging
import time
import requests
import sys
import sqlite3
from bs4 import BeautifulSoup
from functools import wraps

"""
Cambridge is a terminal version of Cambridge Dictionary. 
The dictionary data comes from https://dictionary.cambridge.org.
"""

CAMBRIDGE_URL = "https://dictionary.cambridge.org"
DICT_BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"  # if no result found in cambridge, response.url is this.
SPELLCHECK_BASE_URL = "https://dictionary.cambridge.org/spellcheck/english/?q="

RESQUEST_URL = ""
RESPONSE_WORD = ""
RESPONSE_URL = ""
RESPONSE_TEXT = ""

OP = ["FETCHING", "PARSING"]

def list_words(args, con, cur):
    # The subparser i.e. the sub-command isn't in the namespace of args
    if args.delete:
        word = " ".join(args.delete)
        if delete_word(con, cur, word):
            print("'" + word + "'" + " got deleted from cache successfully")
        else:
            logger.error("No such word '%s' in cache", word)
    elif args.random:
        try:
            # data is something like [('hello',), ('good',), ('world',)]
            data = get_random_words(cur)
        except sqlite3.OperationalError:
            logger.error("You may haven't searched any word yet")
        else:
            for i in data:
                print(i[0])
    else:
        try:
            # data is something like [('hello',), ('good',), ('world',)]
            data = get_response_words(cur)
        except sqlite3.OperationalError:
            logger.error("You may haven't searched any word yet")
        else:
            if args.time:
                data.sort(reverse=True, key=lambda tup: tup[1])
            else:
                data.sort()
            for i in data:
                print(i[0])

def search_words(args, con, cur):
    global REQUEST_URL
    global RESPONSE_WORD
    global RESPONSE_URL
    global RESPONSE_TEXT

    input_word, query_word = get_query_word(args)
    REQUEST_URL = DICT_BASE_URL + query_word

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if len(check_table(cur)) == 0:
        logger.debug("Searching %s for '%s'", CAMBRIDGE_URL, input_word)
        if request_and_print(REQUEST_URL, args):
            logger.debug("Caching search result of '%s'", input_word)
            create_table(con, cur)
            insert_into_table(con, cur, input_word, RESPONSE_WORD, RESPONSE_URL,RESPONSE_TEXT)
            logger.debug("Done caching search result of '%s'", input_word)
    else:
        data = get_cache(cur, input_word, RESQUEST_URL)
        if  data is None:
            logger.debug("Searching %s for '%s'", CAMBRIDGE_URL, input_word)
            if request_and_print(REQUEST_URL, args):
                try:
                    logger.debug("Caching search result of '%s'", input_word)
                    insert_into_table(con, cur, input_word, RESPONSE_WORD, RESPONSE_URL,RESPONSE_TEXT)
                # If a user inputs a word with plural form, it won't get cached again
                except sqlite3.IntegrityError:
                    logger.debug("Cancel caching word of '%s' because it already exists", RESPONSE_WORD)
                else:
                    logger.debug("Done caching search result of '%s'", input_word)
        else:
            logger.debug("Already cached '%s' before. Use cache", input_word)
            RESPONSE_URL, RESPONSE_TEXT = data[0], data[1]
            print_dict(url)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Terminal Version of Cambridge Dictionary"
    )
    
    # Add sub-command capability that can identify different sub-command name 
    sub_parsers = parser.add_subparsers(dest='subparser_name')

    # Add sub-command l
    parser_lw = sub_parsers.add_parser("l", help="list all the words you've successfully searched in alphabetical order")

    # Make sub-command l run default funtion of "list_words"
    parser_lw.set_defaults(func=list_words)

    # Add optional argument for deleting a word from word list
    parser_lw.add_argument(
        "-d",
        "--delete",
        nargs="+",
        help="delete a word or phrase from cache",
    )

    # Add optional argument for listing all words by time
    parser_lw.add_argument(
        "-t",
        "--time",
        action="store_true",
        help="list all the words you've successfully searched in reverse chronological order",
    )

    # Add optional argument for listing words randomly chosen 
    parser_lw.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="randomly list the words you've successfully searched",
    )

    # Add sub-command s
    parser_sw = sub_parsers.add_parser("s", help="search a word or phrase")

    # Make sub-command s run default function of "search_words"
    parser_sw.set_defaults(func=search_words)

    # Add positional arguments with n args
    parser_sw.add_argument(
        "words",
        nargs="+",
        help="A word or phrase you want to search",
    )
    # Add optional arguments
    parser_sw.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="search a word or phrase in verbose mode",
    )

    # If it is for help
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(0)

    # If it is to search words
    elif sys.argv[1] != "l" and len(sys.argv) > 1:
        if "-v" in sys.argv or "--verbose" in sys.argv:
            args = parser_sw.parse_args(["-v",  " ". join([i for i in sys.argv[1:] if not "-v" in i])])
        elif "-h" in sys.argv or "--help" in sys.argv:
            parser_sw.print_help()
            sys.exit(0)
        else:
            args = parser_sw.parse_args([" ". join(sys.argv[1:])])

    # If it is not to search words
    else:
        args = parser.parse_args()

    return args


def get_query_word(args):
    input_word = args.words[0]
    query_word = args.words[0].replace(" ", "-").replace("/", "-")
    return input_word, query_word


def fetch(url, session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36"
    }
    session.headers.update(headers)
    attempt = 0 

    while True:
        try:
            r = session.get(url, timeout=9.05)
        except requests.exceptions.HTTPError as e:
            attempt = call_on_error(e, url, attempt, OP[0])
        except requests.exceptions.ConnectTimeout as e:
            attempt = call_on_error(e, url, attempt, OP[0])
        except requests.exceptions.ConnectionError as e:
            attempt = call_on_error(e, url, attempt, OP[0])
        except requests.exceptions.ReadTimeout as e:
            attempt = call_on_error(e, url, attempt, OP[0])
        except Exception as e:
            attempt = call_on_error(e, url, attempt, OP[0])
        else:
            if r.status_code != 200:  # only a 200 response has a response body
                attempt = call_on_error(r.status_code, url, attempt, OP[0])
            return r

def call_on_error(error, url, attempt, op):
    attempt += 1
    logger.debug(
        "%s HTML from %s %d times",
        op,
        url,
        attempt,
    )
    if attempt == 3:
        logger.debug("Maximum %s retries reached. Exit", op)
        logger.error(str(error))
        sys.exit()
    return attempt

def parse_spellcheck(args, session):
    word = " ".join(args.words)
    query_word = "+".join(args.words)
    url = SPELLCHECK_BASE_URL + query_word
    response = fetch(url, session)
    soup = BeautifulSoup(response.text, "lxml")
    content = soup.find("div", "hfl-s lt2b lmt-10 lmb-25 lp-s_r-20")
    print()
    console.print("[bold #3C8DAD on #DDDDDD]" + word)
    title = content.h1.text.strip()
    console.print("[bold]" + "\n" + title)
    for ul in content.find_all("ul", "hul-u"):
        notice = ul.find_previous_sibling().text
        console.print("[bold #3C8DAD]" + "\n" + notice)
        for i in ul.find_all("li"):
            suggestion = replace_all(i.text)
            console.print("[#b2b2b2]" + "  • " + suggestion)

def parse_first_dict(url):
    global RESPONSE_TEXT
    global RESPONSE_URL
    global RESPONSE_WORD

    if "isn’t in the Cambridge Dictionary yet. You can help!" in RESPONSE_TEXT or "404. Page not found" in RESPONSE_TEXT:
        print("\n" + str(NoResultError()) + "\n")
        sys.exit()

    soup = BeautifulSoup(RESPONSE_TEXT, "lxml")
    attempt = 0

    while True:
        try:
            first_dict = soup.find("div", "pr dictionary")
        except Exception as e:
            attempt = call_on_error(e, url, attempt, OP[1])
        else:
            if not first_dict: 
                attempt = call_on_error(ParsedNoneErrors(), url, attempt, OP[0])

            RESPONSE_WORD = soup.find("title").text.split("|")[0].strip().lower()
            return first_dict

def parse_dict_blocks(url):
    first_dict = parse_first_dict(url)
    try:
        result = first_dict.find(
            "div", ["pr entry-body__el", "entry-body__el clrd js-share-holder"]
        )
    except AttributeError:
        print("\n" + str(NoResultError()) + "\n")
        sys.exit()
    else:
        if result:
            blocks = first_dict.find_all(
                "div", ["pr entry-body__el", "entry-body__el clrd js-share-holder"]
            )
        else:
            blocks = first_dict.find_all("div", "pr idiom-block")
        return blocks, first_dict

# ----------parse dict head----------
def parse_head_title(title_block):
    if title_block.find("div", "di-title"):
        word = title_block.find("div", "di-title").text
        return word

def parse_head_type(head):
    if head.find("span", "anc-info-head danc-info-head"):
        w_type = (
            head.find("span", "anc-info-head danc-info-head").text
            + head.find(
                "span",
                attrs={
                    "title": "A word that describes an action, condition or experience."
                },
            ).text
        )
        w_type = replace_all(w_type)
    elif head.find("div", "posgram dpos-g hdib lmr-5"):
        posgram = head.find("div", "posgram dpos-g hdib lmr-5")
        w_type = replace_all(posgram.text)
    else:
        w_type = None
    return w_type


def parse_head_pron(head):
    w_pron_uk = head.find("span", "uk dpron-i").find("span", "pron dpron")
    if w_pron_uk:
        w_pron_uk = replace_all(w_pron_uk.text)
    # In bs4, not found element returns None, not raise error, so try block is not right
    w_pron_us = head.find("span", "us dpron-i").find("span", "pron dpron")
    if w_pron_us:
        w_pron_us = replace_all(w_pron_us.text)
        console.print(
            "[bold]UK [/bold]" + w_pron_uk + "[bold] US [/bold]" + w_pron_us, end="  "
        )
    else:
        console.print("[bold]UK [/bold]" + w_pron_uk, end="  ")


def parse_head_tense(head):
    w_tense = replace_all(head.find("span", "irreg-infls dinfls").text)
    console.print("[bold]" + w_tense, end="  ")


def parse_head_domain(head):
    domain = replace_all(head.find("span", "domain ddomain").text)
    console.print("[bold]" + domain, end="  ")


def parse_head_usage(head):
    if head.find("span", "lab dlab"):
        w_usage = replace_all(head.find("span", "lab dlab").text)
        console.print("[bold]" + w_usage, end="  ")
    if head.find_next_sibling("span", "lab dlab"):
        w_usage = replace_all(head.find_next_sibling("span", "lab dlab").text)
        console.print("[bold]" + w_usage, end="  ")


def parse_head_var(head):
    if head.find("span", "var dvar"):
        w_var = replace_all(head.find("span", "var dvar").text)
        console.print("[bold]" + w_var, end="  ")
    if head.find_next_sibling("span", "var dvar"):
        w_var = replace_all(head.find_next_sibling("span", "var dvar").text)
        console.print("[bold]" + w_var, end="  ")


def parse_head_spellvar(head):
    for i in head.find_all("span", "spellvar dspellvar"):
        spell_var = replace_all(i.text)
        console.print("[bold]" + spell_var, end="  ")


def parse_dict_head(block):
    head = block.find("div", "pos-header dpos-h")
    word = parse_head_title(block)
    if head:
        head = block.find("div", "pos-header dpos-h")
        w_type = parse_head_type(head)
        if not word:
            word = parse_head_title(head)
        if w_type:
            print()
            console.print("[bold #3C8DAD on #DDDDDD]" + word + " " + w_type)
        else:
            print()
            console.print("[bold #3C8DAD on #DDDDDD]" + word)

        if head.find("span", "uk dpron-i"):
            if head.find("span", "uk dpron-i").find("span", "pron dpron"):
                parse_head_pron(head)

        if head.find("span", "irreg-infls dinfls"):
            parse_head_tense(head)

        if head.find("span", "domain ddomain"):
            parse_head_domain(head)

        parse_head_usage(head)
        parse_head_var(head)

        if head.find("span", "spellvar dspellvar"):
            parse_head_spellvar(head)

        print()
        print()
    else:
        console.print("[bold #3C8DAD on #DDDDDD]" + word)


# ----------parse dict body----------
def parse_def_title(block):
    d_title = replace_all(block.find("h3", "dsense_h").text)
    console.print("[bold #3C8DAD]" + "\n" + d_title)


def parse_ptitle(block):
    p_title = block.find("span", "phrase-title dphrase-title").text
    if block.find("span", "phrase-info dphrase-info"):
        phrase_info = "  - " + replace_all(
            block.find("span", "phrase-info dphrase-info").text
        )
        print(f"\n\033[1m  {p_title} {phrase_info}\033[0m")
    else:
        print(f"\n\033[1m  {p_title}\033[0m")


def parse_def_info(def_block):
    def_info = replace_all(def_block.find("span", "def-info ddef-info").text)
    if def_info == " ":
        def_into = ""
    if def_info:
        if "phrase-body" in def_block.parent.attrs["class"]:
            print("  " + "\033[1m" + def_info + " " + "\033[0m", end="")
        else:
            print(def_info + " ", end="")


def parse_meaning(def_block):
    meaning_b = def_block.find("div", "def ddef_d db")
    if meaning_b.find("span", "lab dlab"):
        usage_b = meaning_b.find("span", "lab dlab")
        usage = replace_all(usage_b.text)
        meaning_words = replace_all(meaning_b.text).split(usage)[-1]
        print(usage + "\033[33m" + meaning_words + "\033[0m")
    else:
        meaning_words = replace_all(meaning_b.text)
        print("\033[33m" + meaning_words + "\033[0m")


def parse_pmeaning(def_block):
    meaning_b = def_block.find("div", "def ddef_d db")
    if meaning_b.find("span", "lab dlab"):
        usage_b = meaning_b.find("span", "lab dlab")
        usage = replace_all(usage_b.text)
        meaning_words = replace_all(meaning_b.text).split(usage)[-1]
        print("  " + usage + "\033[33m" + meaning_words + "\033[0m")
    else:
        meaning_words = replace_all(meaning_b.text)
        print("  " + "\033[33m" + meaning_words + "\033[0m")


def parse_example(def_block):
    # NOTE:
    # suppose the first "if" has already run
    # and, the second is also "if", rather than "elif"
    # then, codes under "else" will also be run
    # meaning two cases took effect at the same time, which is not wanted
    # so, for exclusive cases, you can't write two "ifs" and one "else"
    # it should be one "if", one "elif", and one "else"
    # or three "ifs"
    for e in def_block.find_all("div", "examp dexamp"):
        if e is not None:
            example = replace_all(e.find("span", "eg deg").text)
            if e.find("span", "lab dlab"):
                lab = replace_all(e.find("span", "lab dlab").text)
                console.print(
                    "[#b2b2b2]"
                    + "  • "
                    + "[/#b2b2b2]"
                    + lab
                    + " "
                    + "[#b2b2b2]"
                    + example
                )
            elif e.find("span", "gram dgram"):
                gram = replace_all(e.find("span", "gram dgram").text)
                console.print(
                    "[#b2b2b2]"
                    + "  • "
                    + "[/#b2b2b2]"
                    + gram
                    + " "
                    + "[#b2b2b2]"
                    + example
                )
            elif e.find("span", "lu dlu"):
                lu = replace_all(e.find("span", "lu dlu").text)
                console.print(
                    "[#b2b2b2]"
                    + "  • "
                    + "[/#b2b2b2]"
                    + lu
                    + " "
                    + "[#b2b2b2]"
                    + example
                )
            else:
                console.print("[#b2b2b2]" + "  • " + example)


def parse_synonym(def_block):
    if def_block.find("div", "xref synonym hax dxref-w lmt-25"):
        s_block = def_block.find("div", "xref synonym hax dxref-w lmt-25")
    if def_block.find("div", "xref synonyms hax dxref-w lmt-25"):
        s_block = def_block.find("div", "xref synonyms hax dxref-w lmt-25")
    s_title = s_block.strong.text.upper()
    console.print("[bold #b2b2b2]" + "\n  " + s_title)
    for s in s_block.find_all(
        "div", ["item lc lc1 lpb-10 lpr-10", "item lc lc1 lc-xs6-12 lpb-10 lpr-10"]
    ):
        s = s.text
        console.print("[#b2b2b2]" + "  • " + s)


def parse_see_also(def_block):
    if def_block.find("div", "xref see_also hax dxref-w"):
        see_also_block = def_block.find("div", "xref see_also hax dxref-w")
    if def_block.find("div", "xref see_also hax dxref-w lmt-25"):
        see_also_block = def_block.find("div", "xref see_also hax dxref-w lmt-25")
    see_also = see_also_block.strong.text.upper()
    console.print("[bold #b2b2b2]" + "\n  " + see_also)
    for word in see_also_block.find_all("div", "item lc lc1 lpb-10 lpr-10"):
        word = word.text
        console.print("[#b2b2b2]" + "  • " + word)


def parse_compare(def_block):
    if def_block.find("div", "xref compare hax dxref-w lmt-25"):
        compare_block = def_block.find("div", "xref compare hax dxref-w lmt-25")
    if def_block.find("div", "xref compare hax dxref-w"):
        compare_block = def_block.find("div", "xref compare hax dxref-w")
    compare = compare_block.strong.text.upper()
    console.print("[bold #b2b2b2]" + "\n  " + compare)
    for word in compare_block.find_all(
        "div", ["item lc lc1 lpb-10 lpr-10", "item lc lc1 lc-xs6-12 lpb-10 lpr-10"]
    ):
        item = word.a.text
        usage = word.find("span", "x-lab dx-lab")
        if usage:
            usage = usage.text
            console.print("[#b2b2b2]" + "  • " + item + "[/#b2b2b2]" + usage)
        else:
            console.print("[#b2b2b2]" + "  • " + item)


def parse_usage_note(def_block):
    usage_block = def_block.find("div", "usagenote dusagenote daccord")
    usagenote = usage_block.h5.text
    console.print("[bold #b2b2b2]" + "\n  " + usagenote)
    for item in usage_block.find_all("li", "text"):
        item = item.text
        console.print("[#b2b2b2]" + "    " + item)


def parse_def(def_block):
    parse_def_info(def_block)
    if "phrase-body" in def_block.parent.attrs["class"]:
        parse_pmeaning(def_block)
    else:
        parse_meaning(def_block)
    parse_example(def_block)

    if def_block.find(
        "div", ["xref synonym hax dxref-w lmt-25", "xref synonyms hax dxref-w lmt-25"]
    ):
        parse_synonym(def_block)
    if def_block.find(
        "div", ["xref see_also hax dxref-w", "xref see_also hax dxref-w lmt-25"]
    ):
        parse_see_also(def_block)
    if def_block.find(
        "div", ["xref compare hax dxref-w lmt-25", "xref compare hax dxref-w"]
    ):
        parse_compare(def_block)
    if def_block.find("div", "usagenote dusagenote daccord"):
        parse_usage_note(def_block)


def parse_idiom(block):
    if block.find("div", "xref idiom hax dxref-w lmt-25 lmb-25"):
        idiom_block = block.find("div", "xref idiom hax dxref-w lmt-25 lmb-25")
    if block.find("div", "xref idioms hax dxref-w lmt-25 lmb-25"):
        idiom_block = block.find("div", "xref idioms hax dxref-w lmt-25 lmb-25")
    idiom_title = idiom_block.h3.text.upper()
    console.print("[bold #b2b2b2]" + "\n" + idiom_title)
    for idiom in idiom_block.find_all(
        "div",
        [
            "item lc lc1 lpb-10 lpr-10",
            "item lc lc1 lc-xs6-12 lpb-10 lpr-10",
        ],
    ):
        idiom = idiom.text
        console.print("[#b2b2b2]" + "  • " + idiom)


def parse_phrasal_verb(block):
    if block.find("div", "xref phrasal_verbs hax dxref-w lmt-25 lmb-25"):
        pv_block = block.find("div", "xref phrasal_verbs hax dxref-w lmt-25 lmb-25")
    if block.find("div", "xref phrasal_verb hax dxref-w lmt-25 lmb-25"):
        pv_block = block.find("div", "xref phrasal_verb hax dxref-w lmt-25 lmb-25")
    pv_title = pv_block.h3.text.upper()
    console.print("[bold #b2b2b2]" + "\n" + pv_title)
    for pv in pv_block.find_all(
        "div",
        ["item lc lc1 lc-xs6-12 lpb-10 lpr-10", "item lc lc1 lpb-10 lpr-10"],
    ):
        pv = pv.text
        console.print("[#b2b2b2]" + "  • " + pv)


def parse_dict_body(block):
    for subblock in block.find_all("div", ["pr dsense", "pr dsense dsense-noh"]):
        if subblock.find("h3", "dsense_h"):
            parse_def_title(subblock)

        for child in subblock.find("div", "sense-body dsense_b").children:
            try:
                if child.attrs["class"] == ["def-block", "ddef_block"]:
                    parse_def(child)

                if (
                    child.attrs["class"]
                    == [
                        "pr",
                        "phrase-block",
                        "dphrase-block",
                        "lmb-25",
                    ]
                    or child.attrs["class"] == ["pr", "phrase-block", "dphrase-block"]
                ):
                    parse_ptitle(child)

                    for i in child.find_all("div", "def-block ddef_block"):
                        parse_def(i)
            except:
                pass

    if block.find(
        "div",
        [
            "xref idiom hax dxref-w lmt-25 lmb-25",
            "xref idioms hax dxref-w lmt-25 lmb-25",
        ],
    ):
        parse_idiom(block)

    if block.find(
        "div",
        [
            "xref phrasal_verbs hax dxref-w lmt-25 lmb-25",
            "xref phrasal_verb hax dxref-w lmt-25 lmb-25",
        ],
    ):
        parse_phrasal_verb(block)


def parse_dict_name(first_dict):
    dict_info = replace_all(first_dict.small.text).replace("(", "").replace(")", "")
    dict_name = dict_info.split("©")[0]
    dict_name = dict_name.split("the")[-1]
    console.print(dict_name + "\n", justify="right")

def request_and_print(url, args):
    with requests.Session() as session:
        session.trust_env = False
        response = fetch(url, session)
        if response.url == DICT_BASE_URL:
            parse_spellcheck(args, session)
            return False
        else:
            global RESPONSE_URL
            global RESPONSE_TEXT
            RESPONSE_URL = parse_from_url(response.url)
            RESPONSE_TEXT = response.text
            logger.debug("Fetched html from %s successfully", RESPONSE_URL)
            print_dict(url)
            return True

def print_dict(url):
    blocks, first_dict = parse_dict_blocks(url)
    for block in blocks:
        parse_dict_head(block)
        parse_dict_body(block)
    parse_dict_name(first_dict)


# ----------main----------
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = time.time()
        f = func(*args, **kwargs)
        time_taken = round((time.time() - start_at), 2)
        print("Time taken: {} seconds".format(time_taken))
        return f

    return wrapper

# @timer
def main():
    try:
        con = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = con.cursor()

        args = parse_args()
        args.func(args, con, cur)

        cur.close()
        con.close()

    except KeyboardInterrupt:
        print("\nStopped by user")


if __name__ == "__main__":
    from log import logger
    from utils import replace_all, parse_from_url
    from console import console
    from errors import ParsedNoneError, NoResultError
    from cache import DB, create_table, insert_into_table, get_cache, get_response_words, get_random_words, delete_word, check_table

    main()


else:
    from .log import logger
    from .utils import replace_all, parse_from_url
    from .console import console
    from .errors import ParsedNoneError, NoResultError
    from .cache import DB, create_table, insert_into_table, get_cache, get_response_words, get_random_words, delete_word, check_table
