# Procedural sources

The root P2 assembly and exports are the deliverables. This folder contains editable regeneration sources and the preserved P1 mechanism seed used by P2. `P1_base` is reconstruction input only; do not print or build from its older specifications.

Work in a COPY of the package: regeneration overwrites output files. Run in this order using Blender 5.2 (factory startup avoids user add-ons in background):

1. Blender `--background --factory-startup --python Source/build_p2.py`
2. Python 3 `Source/write_p2_docs.py`
3. Blender `--background --factory-startup --python Source/finish_p2.py`
4. Blender `--background --factory-startup --python Source/finalize_p2.py`
5. Blender `--background --factory-startup --python Source/check_p2.py`

Geometry builders use millimetres. Manufacturer reference envelopes are explicitly labeled. Edit the geometry and docs together. Regenerated files need a fresh inspection and verification; do not reuse old checksums or claim a modified part is qualified because this version passed topology checks. Scripts depend on Blender's bundled bpy/bmesh; they are not ordinary standalone Python CAD programs.
