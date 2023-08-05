Confusion
=========

This package defines a *TOMLParser* class which allows you to employ an extended syntax in your TOML files.

Defaults
--------

Consider this scrap of TOML::

    [A]

    [B]
    flavour = "strawberry"

Confusion_ lets you add a `DEFAULT` section just like the traditional Python `configparser module`_::

    [DEFAULT]
    flavour = "vanilla"

    [A]

    [B]
    flavour = "strawberry"

Substitution
------------

By applying the extended substitution syntax, you can define a value in only one location and reference
it elsewhere (DRY principle)::

    [A]
    flavour = "strawberry"

    [B]
    flavour = ${A:flavour}

Example
-------

Let's use this scrap of TOML for demonstration::

    text = """

    [DEFAULT]
    flavour = "vanilla"
    flake = false

    [A]
    flavour = "strawberry"

    [B]
    flavour = ${A:flavour}
    flake = true

    """

The simplest way to construct a parser is using the *from_string* class method::

    parser = TOMLParser.from_string(text)

To create a TOMLParser object from a TOML file, just use the `pathlib module`_::

    import pathlib
    from confusion import TOMLParser

    text = pathlib.Path("my.toml").read_text()
    parser = TOMLParser.from_string(text)

A TOMLParser object has all the methods of Python's standard `ConfigParser`.
There is one difference; the *sections* attribute is a property which returns a dictionary::

    print(parser.sections)
    >>> {'A': <Section: A>, 'B': <Section: B>}

The hierarchical TOML data is available via the object's *tables* property::

    print(parser.tables)
    >>> {'A': {'flavour': 'strawberry', 'flake': False}, 'B': {'flavour': 'strawberry', 'flake': True}}

.. _configparser module: https://docs.python.org/3/library/configparser.html#module-configparser
.. _confusion: https://github.com/tundish/conf_fusion
.. _pathlib module: https://docs.python.org/3/library/pathlib.html#module-pathlib
