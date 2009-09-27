======
Sparta
======

A Simple API for RDF by Mark Nottingham, <mnot@pobox.com>

Sparts is a simple, resource-centric API for RDF graphs, built on top of
rdflib_. 

Installation
------------

Sparta requires rdflib_ 2.4+.

To install::

  python setup.py install

For installation help::

  python setup.py install --help
  
In examples/::

  example.py: Example of use
  example-out.txt: ouput of example script
  rss.py: example RSS 1.0 feed parser
  rss_schema.xml: partial RDF Schema/OWL for RSS 1.0 example

For more information, see sparta.py and <http://github.com/mnot/sparta/>.

Getting Started
---------------

The easiest way to get started is to play with it; take a look at the example 
files above. You can also take a look through the preliminary documentation below.

Sparta is a wrapper around an rdflib_ Graph. To use it, 
you must first instantiate one or more Graphs, make any necessary prefix mappings, 
and then instantiate a ThingFactory.

Prefix bindings allow URIs to be referred to with a short name.
For example, if "http://www.example.com/foo#" is mapped to the prefix "foo",
then the URI "http://www.example.com/foo#bar" can be referred to in Sparta
with the name "foo_bar".

Prefix bindings are made by calling the normal bind(prefix,
URI) method on the rdflib graph. You can also bind a complete URI to a
string with the addAlias(alias, URI)  method on the ThingFactory
(this accommodates URIs that are awkward or impossible to map using
prefixes).

To be instantiated, a ThingFactory requires one argument; the
Graph (or store) that is to be used. Optionally, you can also give a
schema_store argument, which points to a separate store that contains the
schema hints used to help Sparta map RDF into Python datatypes and objects. If
this is not specified, the primary store will be used.

This is a common idiom for setting up Sparta::

  <pre class="example">    from rdflib.Graph import Graph
    store = Graph()
    store.parse([URI])
    store.bind([prefix], [URI])
    Thing = ThingFactory(store)</pre>

Working with Nodes
------------------

Once you've bound any prefixes you need and set up the store,
you're ready to work with RDF data.

An RDF node is represented as a Python object in Sparta, whose properties
correspond to RDF arcs. To start working with a node, you must instantiate it
with its identity; there are three ways to do this.

1. Thing("prefix_localname") - Refers to the URI indicated using the 
   prefix mapping, as described above.
2. Thing(URIRef('http://www.example.com/foo#bar')) - Refers to the 
   URI specified.
3. Thing(None) - creates a bNode_ (blank, or anonymous RDF node).

Accessing and Manipulating Data
-------------------------------

A node's properties can be accessed and changed by name,
using the prefix mapping as explained above. For example::

  print foo.rdf_type

will print the 'rdf_type' property of the 'foo' node.

There are two ways to access a property's values, depending on what Sparta
knows about it through the schema store. If it is an 
owl:FunctionalProperty_, 
or if the subject is subclassed to restrict that property with either a 
<http://www.w3.org/TR/owl-ref/#maxCardinality-def> owl:maxCardinality
or a <http://www.w3.org/TR/owl-ref/#cardinality> owl:cardinality of
"1", the property can be accessed as a normal, singular value; that is, it can
be accessed as explained above, assigned with the '=' operator, deleted with
'del', and so forth.

Otherwise, the property's value is assumed to have a cardinality greater
than one, and implements a subset of the 
<http://docs.python.org/lib/module-sets.html> sets.Set interface. For
example, you can add to the set with the add method, like this::

  foo.children.add("bob")

test for membership with the in operator, and so forth. See the PropertySet 
class for the exact methods implemented.

Datatyping
----------

An RDF predicate with one of the following as its 
<http://www.w3.org/TR/rdf-schema/#ch_range> rdfs:range (according to
the schema store) will be mapped to these Python datatypes:

* rdf:List - list
* rdf:Seq - list
* xs:string, xs:normalizedString, xs:token, xs:language - unicode
* xs:boolean - bool
* xs:decimal, xs:float, xs:double - float
* xs:integer, xs:long, xs:unsignedLong, xs:unsignedInt - long
* xs:nonPositiveInteger, xs:nonNegativeInteger, xs:positiveInteger, 
  xs:negativeInteger, xs:int, xs:short, xs:byte, xs:unsignedShort,
  xs:unsignedByte - int
* xs:anyURI - str
* xs:base64Binary - (decoded base64)


.. _rdflib: http://rdflib.net/Graph/
.. _bnode: http://www.w3.org/TR/rdf-primer/#structuredproperties 
.. _owl:FunctionProperty: http://www.w3.org/TR/owl-ref/#FunctionalProperty-def
