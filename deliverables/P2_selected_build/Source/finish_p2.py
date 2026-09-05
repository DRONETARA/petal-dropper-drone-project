import bpy,bmesh,json,struct,os,math,csv
from mathutils import Vector,Matrix
from pathlib import Path
ROOT=str(Path(__file__).resolve().parents[1])
bpy.ops.wm.open_mainfile(filepath=ROOT+'/PetalDrop_1kg_Assembly.blend')
scene=bpy.context.scene;scene.frame_set(1);bpy.context.view_layer.update()
manifest=json.load(open(ROOT+'/parts_manifest.json'));rows={r['part']:r for r in manifest}
for name,row in rows.items():
 o=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.001)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bmesh.ops.triangulate(bm,faces=list(bm.faces))
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.001)
 bmesh.ops.triangulate(bm,faces=list(bm.faces))
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 assert all(e.is_manifold for e in bm.edges),name+' manifold failure'
 assert all(f.calc_area()>1e-7 for f in bm.faces),name+' degenerate face'
 unseen=set(bm.verts);components=0
 while unseen:
  components+=1;stack=[unseen.pop()]
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    q=e.other_vert(v)
    if q in unseen:unseen.remove(q);stack.append(q)
 assert components==1,name+' disconnected'
 vol=bm.calc_volume(signed=True);row['volume_cm3']=round(vol/1000,3);row['solid_PETG_mass_g']=round(vol/1000*1.27,1)
 row['nonmanifold_edges']=0;row['connected_components']=1;row['triangles']=len(bm.faces)
 bm.verts.ensure_lookup_table();bm.verts.index_update()
 vv=[v.co.copy() for v in bm.verts];faces=[[v.index for v in f.verts] for f in bm.faces]
 lo=[min(v[i] for v in vv) for i in range(3)];dims=[max(v[i] for v in vv)-lo[i] for i in range(3)];order=sorted(range(3),key=lambda i:dims[i],reverse=True)
 if sum(order[i]>order[j] for i in range(3) for j in range(i+1,3))%2:order[0],order[1]=order[1],order[0]
 vv=[Vector([v[i] for i in order]) for v in vv];lo=Vector([min(v[i] for v in vv) for i in range(3)]);vv=[v-lo for v in vv]
 row['bbox_mm']=[round(max(v[i] for v in vv),3) for i in range(3)]
 with open(ROOT+'/STL_mm/'+row['file'],'wb') as f:
  f.write(('PETALDROP P2 | MM UNITS | '+name).encode('ascii','replace')[:80].ljust(80,b' '));f.write(struct.pack('<I',len(faces)))
  for inds in faces:
   a,b,c=[vv[i] for i in inds];normal=(b-a).cross(c-a).normalized();f.write(struct.pack('<12fH',*normal,*a,*b,*c,0))
 # Keep assembly's mesh identical to cleaned export, retaining all animation transforms.
 bm.transform(o.matrix_world.inverted());bm.to_mesh(o.data);o.data.update();bm.free()
 row['notes']+=' Mesh merged at 0.001 mm tolerance; outward STL normals verified.'
for body,size,z in [('PETAL DROP / P1',10,535),('1 kg PETALS TARGET',7,516),('PROVISIONAL 22 L FILL',6.5,500)]:
 o=bpy.data.objects[body];o.location.x=-80;o.location.z=z;o.data.size=size
bpy.data.objects['MANUAL DOOR RESET'].hide_render=True
with open(ROOT+'/parts_manifest.json','w') as f:json.dump(manifest,f,indent=2)
with open(ROOT+'/parts_manifest.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['part','STL file','quantity','X mm','Y mm','Z mm','solid PETG grams','nonmanifold edges','components','print notes'])
 for r in manifest:w.writerow([r['part'],r['file'],1,*r['bbox_mm'],r['solid_PETG_mass_g'],r['nonmanifold_edges'],r['connected_components'],r['notes']])
r=json.load(open(ROOT+'/verification.json'));r['solid_PETG_total_kg']=round(sum(x['solid_PETG_mass_g'] for x in manifest)/1000,3);r['export_cleanup_tolerance_mm']=.001
with open(ROOT+'/verification.json','w') as f:json.dump(r,f,indent=2)
# Put the readable prototype guide inside the Blender file as well.
if os.path.exists(ROOT+'/README.md'):
 t=bpy.data.texts.get('READ ME • prototype limitations');t.clear();t.write(open(ROOT+'/README.md').read())
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/PetalDrop_1kg_Assembly.blend')
print('EXPORT_REPAIR_COMPLETE',r['solid_PETG_total_kg'],flush=True)
scene.camera=bpy.data.objects['ASSEMBLY • closed'];scene.render.filepath=ROOT+'/Assembly_closed.png';bpy.ops.render.render(write_still=True)
scene.frame_set(90);scene.camera=bpy.data.objects['MECHANISM • underside']
for o in bpy.data.collections['15 • NONPRINT | stand, cover & interface references'].objects:
 if 'landing' in o.name.lower():o.hide_render=True
scene.render.filepath=ROOT+'/Mechanism_open.png';bpy.ops.render.render(write_still=True)
for o in bpy.data.collections['15 • NONPRINT | stand, cover & interface references'].objects:o.hide_render=False
scene.camera=bpy.data.objects['ASSEMBLY • closed'];scene.render.filepath=ROOT+'/Assembly_open.png';bpy.ops.render.render(write_still=True)
print('FINAL_PREVIEWS_READY',flush=True)
