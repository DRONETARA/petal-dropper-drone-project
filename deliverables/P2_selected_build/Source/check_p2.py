import bpy,math,json,struct,collections,os
from mathutils.bvhtree import BVHTree
from mathutils import Vector
from pathlib import Path
ROOT=str(Path(__file__).resolve().parents[1])
bpy.ops.wm.open_mainfile(filepath=ROOT+'/PetalDrop_1kg_Assembly.blend')
scene=bpy.context.scene
printed=[o for o in scene.objects if o.get('Manufacture','').startswith('PRINT')]
doors=[o for o in printed if o.parent and 'Door ' in o.parent.name]
keepers=[o for o in printed if o.parent and 'keeper' in o.parent.name]
fixed=[o for o in printed if not o.parent]
stand=[o for o in scene.objects if 'UNVERIFIED landing' in o.name or 'UNVERIFIED extended landing' in o.name]
def bounds(o):
 vv=[o.matrix_world@v.co for v in o.data.vertices];return [min(v[i] for v in vv) for i in range(3)],[max(v[i] for v in vv) for i in range(3)]
def bvh(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
scene.frame_set(1);bpy.context.view_layer.update();fix={o.name:bvh(o) for o in fixed+stand}
hits=[];minz=1e9
for mode,maxangle in [('keeper',90),('door',95)]:
 for angle in range(maxangle+1):
  for p in set(o.parent for o in keepers):p.rotation_euler.z=math.radians(angle if mode=='keeper' else 90)
  for p in set(o.parent for o in doors):p.rotation_euler.y=math.radians((1 if p.location.x<0 else -1)*(angle if mode=='door' else 0))
  bpy.context.view_layer.update();moving=keepers+doors;bs={o.name:bvh(o) for o in moving}
  for o in moving:
   for name,t in fix.items():
    if bs[o.name].overlap(t):hits.append([mode,angle,o.name,name])
   if o in doors:minz=min(minz,bounds(o)[0][2])
  for i,o in enumerate(moving):
   for q in moving[i+1:]:
    if o.parent!=q.parent and bs[o.name].overlap(bs[q.name]):hits.append([mode,angle,o.name,q.name])
scene.frame_set(1);bpy.context.view_layer.update()
prop=[o for o in scene.objects if 'blade' in o.name.lower() and o.type=='MESH' and o.get('Status')]
propz=min(bounds(o)[0][2] for o in prop)
printed_top=max(bounds(o)[1][2] for o in printed)
# Validate the delivered binary STLs independently of Blender topology.
stl=[]
for fn in sorted(os.listdir(ROOT+'/STL_mm')):
 if not fn.endswith('.stl'):continue
 data=open(ROOT+'/STL_mm/'+fn,'rb').read();n=struct.unpack_from('<I',data,80)[0];edges=collections.Counter();vol=0;deg=0
 for i in range(n):
  row=struct.unpack_from('<12fH',data,84+50*i);v=[tuple(round(k,4) for k in row[j:j+3]) for j in [3,6,9]];a,b,c=map(Vector,v)
  if (b-a).cross(c-a).length<1e-7:deg+=1
  vol+=a.dot(b.cross(c))/6
  for j in range(3):edges[tuple(sorted((v[j],v[(j+1)%3])))]+=1
 bad=sum(v!=2 for v in edges.values())
 stl.append({'file':fn,'triangles':n,'boundary_or_nonmanifold_edges':bad,'degenerate_triangles':deg,'signed_volume_mm3':round(vol,3),'binary_size_ok':len(data)==84+50*n})
report={'motion_step_degrees':1,'keeper_states':91,'door_states':96,'intersections':hits,'minimum_printed_door_Z_mm':round(minz,3),'ground_plane_Z_mm':-5,'door_to_ground_gap_mm':round(minz+5,3),'lowest_reference_prop_blade_Z_mm':round(propz,3),'highest_printed_part_Z_mm':round(printed_top,3),'vertical_prop_plane_to_printed_assembly_mm':round(propz-printed_top,3),'independent_STL_validation':stl,'limitations':'Surface-intersection sampling at 1-degree increments; no continuous collision proof, no flexible deformation or dynamic loads. Pin, screw, servo and electrical interfaces require physical verification. Landing stand has proposed tubular geometry; welds and structural performance untested. STL edge checks quantize coordinates to 0.0001 mm.'}
with open(ROOT+'/final_checks.json','w') as f:json.dump(report,f,indent=2)
print('FINAL_CHECKS',json.dumps({k:v for k,v in report.items() if k!='independent_STL_validation'}),flush=True)
print('STL_FAILURES',[r for r in stl if r['boundary_or_nonmanifold_edges'] or r['degenerate_triangles'] or r['signed_volume_mm3']<=0 or not r['binary_size_ok']],flush=True)
