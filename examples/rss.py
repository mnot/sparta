#!/usr/bin/env python

from rdflib.Graph import Graph
from rdflib.URIRef import URIRef as URI
from sparta import ThingFactory
import textwrap
indent = textwrap.TextWrapper(initial_indent="  ", subsequent_indent="  ").fill

def main(rss_url, blog_uri):
    store, schema_store = Graph(), Graph()
    store.parse(rss_url)
    store.bind('rss', 'http://purl.org/rss/1.0/')
    schema_store.parse('file:rss_schema.xml')
    Thing = ThingFactory(store, schema_store)
    
    blog = Thing(URI(blog_uri))
    for item in blog.rss_items:
        print "*", item.rss_title
        print indent(item.rss_description)
    
    
if __name__ == '__main__':        
    import sys
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        sys.stderr.write("Usage: %s [RSS feed URL] [Blog URI]\n" % sys.argv[0])
        sys.exit(1)
