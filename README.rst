=========
ValleyText
=========

This tool can be used to extract keywords from sentences without chunks or word boundaries (for example, Chinese).
It is based on trie tree optimized by AhoCorasick Automation.


Installation
------------
::

    $ pip install valleytext




Usage
-----
Extract keywords
    >>> from valleytext import create_trie
    >>> words_dict = {'设备': ['GPS', '设备']}
    >>> extractor = create_trie(words_dict, False)
    >>> extracts = extractor.extract_keywords_from_text('我有一台gps设备')
    >>> extracts
    >>> # [(4, 7, 'gps', '设备'), (7, 9, '设备', '设备')]


License
-------

The project is licensed under the MIT license.
