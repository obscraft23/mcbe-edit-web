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
    
    if worldid == "dummy":
        return JsonResponse({"nbts":{},"type":typeid})

    elif typeid == "0":
        return JsonResponse({"nbts":{},"type":typeid})
    
    elif typeid == "1":
         return JsonResponse({"nbts":obj.getChoiceOfEntity(),"type":typeid})
    
    elif typeid == "2":
        return JsonResponse({"nbts":[[key[0],"cx="+str(key[2])+",cz="+str(key[3])] for key in obj.keylist if key[5]==49 and key[4]==int(dimid)],"type":typeid})

    elif typeid == "3":
        return JsonResponse({"nbts":[[key[0],key[0]] for key in obj.keylist if key[0].startswith("VILLAGE")],"type":typeid})

    elif typeid == "4":
        return JsonResponse({"nbts":[[key[0],key[0]] for key in obj.keylist if "player" in key[0]],"type":typeid})

    else:
        return JsonResponse({"nbts":{},"type":typeid})


def save_worlddata(request):
    
    worldID = str(uuid.uuid4())
    #save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data/")+worldID+"/"
    save_dir = "/tmp/"+worldID+"/"
    dirdict = json.loads(request.POST['directories'])
    #nfiles = len(file["file_field"])
    print(dirdict)
    print("###")
    print(len(request.FILES.getlist("file_field")))
    flist = [file.name for file in request.FILES.getlist("file_field")]
    print(len(flist))
    i=0
    for key in flist:
        
        print(request.FILES.getlist("file_field")[i].name)
        
        f = request.FILES.getlist("file_field")[i]
        
        fpath = save_dir+dirdict[key]
        dir = os.path.dirname(fpath)
        os.makedirs(dir,exist_ok=True)
        with open(fpath,"wb") as destination:
            bindata = f.open().read()
            destination.write(bindata)
            #for chunk in f.chunks():
            #    destination.write(chunk)
        
        i+=1
    print(i)
    
    return worldID
        
        
def create_blog_post(request):

    if request.method == 'POST':

        if request.FILES["file_field"]:
            
            worldID = save_worlddata(request)

            form1 = dimentionChoiceForm({"worldid": worldID,"choice_dim":0,"choice_type":0})

            redirect_url = reverse('testview')
            parameters = urlencode({"worldID":worldID})
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
            
            #return render(request, 'dimention_choice.html', {"form1": form1, "worldID":worldID})
            
        if "submit-form1" in request.POST:
            form1 = dimentionChoiceForm(request.POST)
            if form1.is_valid():
                print(request.POST)
                #form2 = entityChoiceForm(request.POST)
                return render(request, 'dimention_choice.html', {"form1": form1, "form2":form2})

        if "submit-form2" in request.POST:
            if form2.is_valid():
                print(request.POST)
                #form2 = entityChoiceForm(request.POST)
                return render(request, 'dimention_choice.html', {"form1": form1, "form2":form2})

    else:

        form0 = uploadForm()
        #form1 = dimentionChoiceForm()
        #form2 = entityChoiceForm()

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
                nbt = request.POST.get('nbt')
                key = request.POST.get("key")
                json_str = request.POST.get('jsondata')
                worldidpath = '/tmp/'+worldid+'/'
                worldfname = glob.glob(worldidpath+"/*/db")[0][:-3]
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