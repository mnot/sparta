#!/usr/bin/env python2.4

from sparta import ThingFactory
from rdflib.Graph import Graph

store = Graph()
store.bind("contact", "http://www.example.com/contact#")
store.bind("person", "http://www.example.com/person#")
store.bind("xs", "http://www.w3.org/2001/XMLSchema#")
store.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
store.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
store.bind("owl", "http://www.w3.org/2002/07/owl#")

Thing = ThingFactory(store)
Thing.addAlias("special", "http://www.example.com/my-unmappable-stuff#special-thing")

### these should be loaded externally...
Thing("person_employment_history", 
      rdfs_range=[Thing("rdf_List")],
      rdf_type=[Thing("owl_FunctionalProperty")]
)
Thing("person_age", rdfs_range=[Thing("xs_int")])
Thing("person_picture", rdfs_range=[Thing("xs_base64Binary")])
Thing("contact_phone", rdf_type=[Thing("owl_FunctionalProperty")])
Thing("person_wife", rdf_type=[Thing("owl_FunctionalProperty")])
Thing("person_name", rdf_type=[Thing("owl_FunctionalProperty")])
Thing("contact_www", rdf_type=[Thing("owl_FunctionalProperty")])
Thing("person_age", rdf_type=[Thing("owl_FunctionalProperty")])

bob = Thing("person_bob")
Person = Thing("person_Person")
bob.rdf_type.add(Person)
bob.contact_phone = "555-1212"
bob.person_name = "Bob"
bob.contact_address.add(Thing(None, 
                            contact_street = ["314159 There Street"],
                            contact_city = ["EveryVille"],
                            contact_state = ["NA"],
                            contact_zip = ["12345"],
                       ))

bob.person_childname.add("joe")
bob.person_childname.add("jim")
bob.person_childname.add("bob")
if "jim" in bob.person_childname:
    print "Yes, Bob has a child named jim."
if "george" not in bob.person_childname:
    print "But he doesn't have one named george."
bob.person_childname.remove("jim")
if "jim" not in bob.person_childname:
    print "And in fact, jim isn't any more."
bob.person_childname.discard("nonexistant")

bob.person_employment_history = ["7-11", "Wal-Mart", "Goldman Sachs"]

bob.special.add("testing...")
print "This should be 1:", len(bob.special)

mary = Thing("person_mary",
             person_name="Mary",
             person_hair=["blue"], 
             person_age=23
            )

bob.person_wife = mary

mary.person_childname = bob.person_childname
print "Mary has", len(mary.person_childname), "kids."

mary.contact_phone = "123-4567"
bob.person_wife.contact_www = "http://www.example.org/~mary"

print "Bob's phone is", bob.contact_phone
# print "Bob's zip code is", bob.contact_address.contact_zip
print "Bob's wife is", bob.person_wife.person_name
print "Mary's phone is", mary.contact_phone
print "Bob's wife's phone is", bob.person_wife.contact_phone
print "Mary's web site is", mary.contact_www
print "their", len(bob.person_childname), "kids' names are:"
for kid in bob.person_childname: print "  ", kid
print "Bob has worked at:", bob.person_employment_history

print "Mary's age is", mary.person_age
bob.person_age = bob.person_wife.person_age + 4
print "Bob's age is", bob.person_age, type(bob.person_age)

f = open('/dev/random')
bob.person_picture.add(f.read(25))
f.close()

print "Bob's properties:", ", ".join(map(str, bob.properties()))
print "Bob has a wife?", hasattr(bob, "person_wife")
print "Her name?", getattr(bob, "person_wife").person_name

print
print store.serialize(format="xml")
