# !/usr/bin/python
import re
import uuid

STOP_WORDS = set("tis, 'twas, a, able, about, across, after, ain't, all, almost, also, am, "
                 "among, an, and, any, are, aren't, as, at, be, because, been, but, by, can, can't, "
                 "cannot, could, could've, couldn't, dear, did, didn't, do, does, doesn't, don't, either, else, ever, "
                 "every, for, from, get, got, had, has, hasn't, have, he, he'd, he'll, he's, her, hers, him, his, "
                 "how, how'd, how'll, how's, however, i, i'd, i'll, i'm, i've, if, in, into, is, isn't, it, it's, "
                 "its, just, least, let, like, likely, may, me, might, might've, mightn't, most, must, must've, "
                 "mustn't, my, neither, no, nor, not, of, off, often, on, only, or, other, our, own, rather, "
                 "said, say, says, shan't, she, she'd, she'll, she's, should, should've, shouldn't, since, so,"
                 "some, than, that, that'll, that's, the, their, them, then, there, there's, these, they, they'd, "
                 "they'll, they're, they've, this, tis, to, too, twas, us, wants, was, wasn't, we, we'd, we'll, "
                 "we're, were, weren't, what, what'd, what's, when, when, when'd, when'll, when's, where, where'd, "
                 "where'll, where's, which, while, who, who'd, who'll, who's, whom, why, why'd, why'll, why's, will,"
                 "with, won't, would, would've, wouldn't, yet, you, you'd, you'll, you're, you've, your".split(', '))


WORD_RE = re.compile("[a-z']{2,}")
QUERY_RE = re.compile("[+-]?[a-z']{2,}")


def tokenize(content):
    """
    对content进行标计划处理
    """
    words = set()
    for match in WORD_RE.finditer(content.lower()):
        word = match.group().strip("'")
        if len(word) > 2:
            words.add(word)
    return words - STOP_WORDS


def index_document(conn, docid, content):
    """
     生成正确的索引集合
    """
    words = tokenize(content)
    pipeline = conn.pipeline(True)
    for word in words:
        pipeline.sadd('idx:' + word, docid)
    return len(pipeline.execute())


def set_comm(conn, method, names, ttl=30, execute=True):
    uid = str(uuid.uuid4())
    pipeline = conn.pipeline(True) if execute else conn
    idx_names = ['idx:' + name for name in names]
    getattr(pipeline, method)('idx:' + uid, *idx_names)
    pipeline.expire('idx:' + uid, ttl)
    if execute:
        pipeline.execute()
    return uid


def intersect(conn, items, ttl=30, execute=True):
    return set_comm(conn, 'sinterstore', items, ttl, execute)


def union(conn, items, ttl=30, execute=True):
    return set_comm(conn, 'sunionstore', items, ttl, execute)


def difference(conn, items, ttl=30, execute=True):
    return set_comm(conn, 'sdiffstore', items, ttl, execute)


def parse(query):
    unwanted = set()
    all_word = []
    current = set()
    for match in QUERY_RE.finditer(query.lower()):
        word = match.group()
        prefix = word[:1]
        if prefix in '+-':
            word = word[1:]
        else:
            prefix = None
        word = word.strip("'")
        if len(word) < 2 or word in STOP_WORDS:
            continue
        if prefix is '-':
            unwanted.add(word)
            continue
        if current and not prefix:
            all_word.append(list(current))
            current = set()
        current.add(word)

        if current:
            all_word.append(list(current))
    return all_word, list(unwanted)

