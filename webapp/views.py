from django.shortcuts import render

# Create your views here.
from .forms import dimentionChoiceForm, uploadForm, NBTeditForm
import os
import json
import uuid
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect

from .editbeworld import beworld

import glob
from django.http.response import JsonResponse
import pybedrock as pb
from django.http import FileResponse
import shutil


def getnbtinfo(request):

    worldid = request.POST.get('worldid')
    typeid = request.POST.get('type')
    dimid = request.POST.get('choice_dim')
    
    worldidpath = "/tmp/"+worldid+'/'
    worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]
    obj = beworld(worldfname)
    existingChunks = obj.getexistingChunks(dimid)
    
    if dimid == "dummy" and typeid == "2":
        return JsonResponse({"nbts":"dummy","type":typeid})

    elif typeid == "0":
        return JsonResponse({"nbts":"none","type":typeid})
    
    elif typeid == "1":
         return JsonResponse({"nbts":obj.getChoiceOfEntity(),"type":typeid})
    
    elif typeid == "2":
        return JsonResponse({"nbts":[[key[0],"cx="+str(key[2])+",cz="+str(key[3])] for key in obj.keylist if key[5]==49 and key[4]==int(dimid)],"type":typeid})

    elif typeid == "3":
        return JsonResponse({"nbts":[[key[0],key[0]] for key in obj.keylist if key[0].startswith("VILLAGE")],"type":typeid})

    elif typeid == "4":
        return JsonResponse({"nbts":[[key[0],key[0]] for key in obj.keylist if "player" in key[0]],"type":typeid})

    elif typeid == "5":
        return JsonResponse({"nbts":"none","type":typeid})
    
    elif typeid == "6":
        return JsonResponse({"nbts":[[key[0],key[0]] for key in obj.keylist if not (key[0].startswith("@"))],"type":typeid})
    
    else:
        return JsonResponse({"nbts":"none","type":typeid})


def save_worlddata(request):
    
    worldID = str(uuid.uuid4())
    #save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data/")+worldID+"/"
    save_dir = "/tmp/"+worldID+"/"
    dirdict = json.loads(request.POST['directories'])
    #nfiles = len(file["file_field"])
    #print(dirdict)
    #print("###")
    #print(len(request.FILES.getlist("file_field")))
    flist = [file.name for file in request.FILES.getlist("file_field")]
    #print(len(flist))
    i=0
    for key in flist:
        
        #print(request.FILES.getlist("file_field")[i].name)
        
        f = request.FILES.getlist("file_field")[i]
        
        fpath = save_dir+dirdict[key]
        dir = os.path.dirname(fpath)
        os.makedirs(dir,exist_ok=True)
        with open(fpath,"wb") as destination:
            bindata = f.open().read()
            destination.write(bindata)
        
        i+=1
    
    return worldID
        
        
def create_blog_post(request):

    if request.method == 'POST' and 'directories' in request.POST:
            
        worldID = save_worlddata(request)
        redirect_url = reverse('testview')
        parameters = urlencode({"worldID":worldID})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    
    elif request.method == 'POST' and request.FILES["file_field"]:

        f = request.FILES.getlist("file_field")[0]
        
        worldID = str(uuid.uuid4())
        save_dir = "/tmp/"+worldID+"/"
        os.makedirs(save_dir,exist_ok=True)
        fpath = save_dir+f.name
        with open(fpath,"wb") as destination:
            bindata = f.open().read()
            destination.write(bindata)
        
        shutil.unpack_archive(fpath,save_dir+f.name.replace(".zip",""))
        if len(glob.glob(save_dir+"*/db")) == 0:
            os.system("mv "+save_dir+f.name.replace(".zip","")+" "+save_dir+"3f33756f-76c8-4caf-a18e-8c8a47bde0")
            worldfname = glob.glob(save_dir+"*/*/db")[0][:-3]
            os.system("mv "+worldfname+" "+save_dir)
            os.system("rm -rf "+save_dir+"3f33756f-76c8-4caf-a18e-8c8a47bde0")
        os.system("rm -rf "+fpath)
        redirect_url = reverse('testview')
        parameters = urlencode({"worldID":worldID})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
            
    else:

        form0 = uploadForm()
        return render(request, 'index.html', {"form0": form0})

###
def testview(request):
    
    if request.method == 'POST':

        if "submit-form1" in request.POST:
            
            form1 = dimentionChoiceForm({"worldid": request.POST.get('worldid'),"key":request.POST.get('nbt'),"choice_dim":request.POST.get("choice_dim"),"choice_type":request.POST.get("choice_type")})
            if form1.is_valid():

                worldid = request.POST.get('worldid')
                nbt = request.POST.get('nbt')
                worldidpath = '/tmp/'+worldid+'/'
                worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]
                if nbt == "level.dat":
                    with open(worldfname+"/level.dat","rb") as f:
                        bindata = f.read()
                    header = bindata[0:8]
                    NBTdict = pb.readNBT(bindata[8:])
                    json_str = json.dumps(NBTdict)
                    form1 = dimentionChoiceForm({"worldid": worldid,"key":nbt,"choice_dim":request.POST.get("choice_dim"),"choice_type":request.POST.get("choice_type")})
                    form2 = NBTeditForm({"jsondata":json_str})
                
                else:
                    obj = beworld(worldfname)
                    NBTdict = obj.getDictfromkey(nbt)
                    json_str = json.dumps(NBTdict)
                    form1 = dimentionChoiceForm({"worldid": worldid,"key":nbt,"choice_dim":request.POST.get("choice_dim"),"choice_type":request.POST.get("choice_type")})
                    form2 = NBTeditForm({"jsondata":json_str})

                return render(request, 'nbt_edit.html', {"form1":form1,"form2":form2})

        if "submit-form2" in request.POST:
            form1 = dimentionChoiceForm({"worldid": request.POST.get('worldid'),"key":request.POST.get('key'),"choice_dim":request.POST.get("choice_dim"),"choice_type":request.POST.get("choice_type")})

            if form1.is_valid():
                
                worldid = request.POST.get('worldid')
                worldidpath = '/tmp/'+worldid+'/'
                worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]
                key = request.POST.get("key")

                if key == "level.dat":
                    json_str = request.POST.get('jsondata')
                    json_dict = json.loads(json_str)
                    bindata = pb.writeNBT(json_dict)
                    size = len(bindata)
                    header = b'\n\x00\x00\x00'+size.to_bytes(4, 'little')
                    with open(worldfname+"/level.dat","wb") as f:
                        f.write(header+bindata)
                
                else:
                    json_str = request.POST.get('jsondata')
                    json_dict = json.loads(json_str)
                    bindata = pb.writeNBT(json_dict)
                    pb.writebinary(worldfname,key,bindata)
                
                form2 = NBTeditForm({"jsondata":json_str})
                return render(request, 'nbt_edit.html', {"form1":form1,"form2":form2})
        
        if "download" in request.POST:
            worldid = request.POST.get('worldid')
            worldidpath = '/tmp/'+worldid+'/'
            worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]

            shutil.make_archive(worldidpath+worldid, format='zip', root_dir=worldfname)
            os.system("mv "+worldidpath+worldid+".zip "+worldidpath+worldid+".mcworld")
            
            file_path = worldidpath+worldid+".mcworld"
            filename = worldid+".mcworld"
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)
            
    else:
        worldID = request.GET.get("worldID")
        form1 = dimentionChoiceForm({"worldid": worldID,"key":"None","choice_dim":0,"choice_type":0})
        json_str = "[]"
        form2 = NBTeditForm({"jsondata":json_str})
        return render(request, 'nbt_edit.html', {"form1": form1,"form2": form2})