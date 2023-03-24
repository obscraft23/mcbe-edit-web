import pybedrock as pb
import numpy as np

class beworld:

    def __init__(self,path):
        self.worldfname = path
        self.keylist = pb.listkeys(self.worldfname)
    
    def getChoiceFromSubChunk(self,SubChunkPrefix):

        SubChunkkeylist = [key[0] for key in self.keylist if key[0].startswith(SubChunkPrefix)]

        SubchunkChoice = []
        if len(SubChunkkeylist) >0:

            for key in SubChunkkeylist:

                if key[5] == 49:
                    SubchunkChoice.append([key[0],"BlockEntity"])
                
                elif key[5] == 51:
                    SubchunkChoice.append([key[0],"PendingTicks"])
                
                elif key[5] == 57:
                    SubchunkChoice.append([key[0],"HardCodedSpawnAreas"])
                
                elif key[5] == 58:
                    SubchunkChoice.append([key[0],"BlockEntity"])
                
                elif key[5] == 43:
                    SubchunkChoice.append([key[0],"Data3D"])
                
                elif key[5] == 47:
                    SubchunkChoice.append([key[0],"SubChunk"])
        
        return SubchunkChoice

    def getChoiceOfEntity(self):

        actorkeylist = [key[0] for key in self.keylist if key[0].startswith("actorprefix")]

        entityChoice = []
        if len(actorkeylist) > 0:
            for key in actorkeylist:
                id = pb.readNBT(pb.loadbinary(self.worldfname,key))[0]["value"]["identifier"]["value"]
                #entityChoice.append((key,id+":"+key.replace("actorprefix","")))
                entityChoice.append([key,id+":"+key.replace("actorprefix","")])

        #return tuple(entityChoice)
        return entityChoice
    
    def getexistingChunks(self,dimentionid):

        SubChunkskeylist = [["@"+str(key[2])+":"+str(key[3])+":"+str(dimentionid),"@"+str(key[2])+":"+str(key[3])+":"+str(dimentionid)] for key in self.keylist if (key[0].startswith("@") and key[4] == dimentionid)]
        SubChunkPrefixlist = np.unique(SubChunkskeylist,axis=0).tolist()

        return SubChunkPrefixlist
    
    def getDictfromkey(self,key):
        bindata = pb.loadbinary(self.worldfname,key)
        return pb.readNBT(bindata)