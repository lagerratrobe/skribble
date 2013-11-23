skribble
========

Hackathon project to create a simple Mapserver templating tool.  The basic idea is that a current mapfile can be used as a template to create new mapfiles that are similar, but whose styles and certain other atttributes have been modified based on the contents of a config file.

Envisioned workflow is something like this:
  "$ skribble.py template.map config.mst"

The output would be new directory named "config", with a mapfile in it named "config.map"
