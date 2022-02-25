import json
import datetime
import os
from collections import namedtuple


#this function is to identify the length of the json data to set the next id of the added content...
#the only way to set the id of the next content, we must know the length of the stored data and add 1 to it to set the next one
def dataLengthCounter(dataType,deside, TopicId = None):
    if(dataType == "Topic"):
        file = open("mainData.json", "r")
        load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
        file.close()
        topicNum = len(load[0])  # this counts the length of the topics in the json file
        if(deside == True):
            topicHowTosNum = len(load[0][TopicId].howTos) # this counts the length of the howtos in the topics 
            return topicHowTosNum
        else:
            file = open("mainData.json", "r")
            load = json.load(file)
            long = len(load["Topic"])
            return long
            
    if(dataType == "HowTos"):
        file = open("mainData.json", "r")
        load = json.load(file)
        howTosNum = len(load["howTos"]) # this counts the length of HowTos in mainData.json
        file.close()
        return howTosNum



# this is the function that is called when the user needs to add a new content to the app
def contentAdder(direction, start, cont, fileName=None, draft = False, draftData = ""):    
    # Data skeleton for topics in mainData.json
    dataT = {
        "id" : "",
        "name" : "",
        "info" : "",
        "additional" : "",
        "timeStamp" : "",
        "howTos" : [ ],
        "pointer" : [], # this points to the address which the user is editing lastly and save the data as draft
                       # when user want to continue, the pointer points to the last object to be edited and can continue
        "th" :{
                "id" : "",
                "title" : "",
                "preRequest" : "",
                "content" : "",
                "info" : "",
                "timeStamp" : ""
            }
    }


    # Data skeleton for HowTos in mainData.json
    dataHowTos = {
            "id" : "0",
            "title" : "",
            "preRequest" : "",
            "info" : "",
            "timeStamp" : "",
            "pointer" : []
        }

    exit1 = False

    while(exit1 == False):
        # for draft manager this helps. when function is called from strat manger, starts args will be set to true and user will start adding from begining.
        #  but when we call it from draft manager, we set the start args to false b/c we dont need the starting part
        # so this condition will dectate the start and draft continueation
        choosen = ""
        if(start == True): 
            os.system("cls")
            print("[*]-- Welcome, Choose a Catagory to Enter your Content!")
            print("     -|T|- Topic.   -|TH|- HowTo's in Topic   -|H|- How To's/Tutorials.    ")
            choosen = input(">> ")
            #if the user choosen topic  to enter
        if(choosen != "TH" and (start == True) and (choosen != "H")):
            if(choosen == "T"):
                # os.system("cls")
                print("[*] Enter the -Topic- Name to Add. ")
                topic = input(">> ")
                if(fileName):
                    topic = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                # now create a draft file with the name of the title
                open(f"drafts/topics/{topic}.json", "x" )
                # now add the data skeleton to the draft file
                with open(f"drafts/topics/{topic}.json", "w") as file:
                    json.dump(dataT, file)
                # save the name to the draft json file
                file1 = open(f"drafts/topics/{topic}.json", "r")
                load1 = json.load(file1)
                    # now count all the topic content from mainData.json to add the id to the new content
                new = dataLengthCounter("Topic", False, None)
                newId = new
                load1["name"] = topic # assign the name object to the name
                file1.close()
                load1["id"] = int(new) # add the id to the draft
                file1 = open(f"drafts/topics/{topic}.json", "w")
                json.dump(load1, file1) # this writes the edited data
                file1.close()
                
                
                # newHowToId = new["topicHowTosNum"] + 1
                file1.close()

                print("[*] SAVED. ")

            
            if( direction == "tinfo" and (cont == True)   or (draft == False)):  # this is set from draft manager to start the draft from topic.info 
                # Inserting Info
                # os.system("cls")
                print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
                print("[*] Enter \"INFO\" about this topic.. ")
                info0 = " "
                if(draftData != ""):
                    info0 = draftData
                info = input("[*]>>  ")
                info = info0 + info
                print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
                userChoce = input("[*] >>  " )
                # now save the info to the object to the draft
                # we save the data as draft no matter the users choose to save or draft it because we save the over all 
                # finished data to the mainData.json until then every users input is saved as drafts
                if(fileName):
                    topic = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                file1 = open(f"drafts/topics/{topic}.json", "r")
                load1 = json.load(file1)
                load1["info"] = info # assign the name object to the name
                # we point the pointer object as array value. in this case pointer[0] is the first object and if there is anther object we continue as pointer[1]. this helps us to accsess the pointer by object when the user leter continues the draft
                load1["pointer"] = []
                load1["pointer"].append("info")  # this is very very important. this object helps for the user to continue editing from he left off because of this pointer telling it to where he left it in the last time
                file1.close()
                file1 = open(f"drafts/topics/{topic}.json", "w")
                json.dump(load1, file1) # this writes the edited data
                file1.close()      
                # after the data is saved as draft then we conceder users choice to continue adding or to leave and save it for letter to continue
                if(userChoce == "d" ):
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break
                if(userChoce == "c" ):
                    print("[*] Saved. ") 
                    conn = input("[*] Press Enter To Continue..") 
                else:
                    print("[*] You Enterd wrong!. taking matter in Hand..")
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break       
            
            if( direction == "tadditional" and (cont == True)  and (choosen !="H")    or (draft == False)): # this is set from draft manager to start the draft from topic.info
                # Inserting additional
                # os.system("cls")
                print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
                print("[*] Enter \"ADDITIONAL\" about this topic.. Its Optional ")
                additional0 = " "
                if(draftData != ""):
                    additional0 = draftData
                additional = input("[*]>>  ")
                additional = additional0 + additional
                print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
                userChoce = input("[*] >>  " )
                # now save the info to the object to the draft
                # we save the data as draft no matter the users choose to save or draft it because we save the over all 
                # finished data to the mainData.json until then every users input is saved as drafts
                # before finishing topic adding, we insert time of creation
                date = datetime.datetime.now
                if(fileName):
                    topic = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                file1 = open(f"drafts/topics/{topic}.json", "r")
                load1 = json.load(file1)
                load1["pointer"] = []
                load1["additional"] = additional # assign the name object to the name
                load1["timeStamp"] = str(date) # date of cration added
                load1["pointer"].append("additional") # this is very very important. this object helps for the user to continue editing from he left off because of this pointer telling it to where he left it in the last time
                file1.close()
                file1 = open(f"drafts/topics/{topic}.json", "w")
                json.dump(load1, file1) # this writes the edited data
                file1.close()      
                # after the data is saved as draft then we conceder users choice to continue adding or to leave and save it for letter to continue
                if(userChoce == "d" ):
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break
                if(userChoce == "c" ):
                    print("[*] Saved. ")
                    conn = input("[*] Press Enter To Continue..")
                else:
                    print("[*] You Enterd wrong!. taking matter in Hand..")
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break   
                # topic adding finished
                # pop a quetion for the user to exit or to add new howTos in this topic which he had created now
                                    # now save the draft file to the mainData.json file
                file3 = open(f"drafts/topics/{topic}.json", "r") # load the draft to load3
                load3 = json.load(file3)
                file3.close()
                load3.pop("pointer", None)
                load3.pop("th", None)
                file3 = open("mainData.json", "r") 
                readMain = json.load(file3)  # load the mainData.json file to readMain
                readMain["Topic"].append(load3)  # add the draft to the mainData by appending the object to the array to it
                file3.close()
                file = open("mainData.json", "w")
                json.dump(readMain, file)
                file.close()
                
                # now we delete the draft file we dont need it any more
                os.remove(f"drafts/topics/{topic}.json")
            
                print("[*] You Have Finished Adding a New \"Topic\".  ")
                print("[*] If you Want you can ADD your first \"HowTos\"/Tutorial in This Topic, Go To Homepage and use the \"Add\" Command then Choose \"How To's in Topic\". ")
                choosenN = input("[*] Press Enter To Go To Homepage. ")
                break
                    

        if( choosen == "TH" or draft == True ):
            if(choosen == "TH"):
                # os.system("cls")
                print("[*] Topic Lists..")
                file = open("mainData.json", "r")
                load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
                file.close()
                coll = load[0]
                i=0
                for each in coll:
                    print("[-",i,"-] ",each.name)
                    i+=1
                print("[*] Select a Topic to Add a Tutorial For.")
                inter = input(">> ")
                # create a draft json file to save it as draft
                key = dataLengthCounter("Topic", True, int(inter))
                fname = load[0][int(key)].id # is to select the topic id and to save at mainData.json at finish
                print("[*] Enter Name for the Tutorial")
                hName = input(">> ")
                if(fileName):
                    hName = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                open(f"drafts/topics/{hName}.json", "x")
                file = open(f"drafts/topics/{hName}.json", "w")
                json.dump(dataT, file)
                file.close()
                file = open(f"drafts/topics/{hName}.json", "r")   
                load1 = json.load(file)  
                file.close()        
                load1["th"]["title"] = hName
                thid = dataLengthCounter("Topic", True, int(inter))
                rthid = thid 
                load1["th"]["id"] = int(rthid)
                load1["tid"] = int(rthid) # so that to access the topic id from draft 
                file1 = open(f"drafts/topics/{hName}.json", "w")
                json.dump(load1, file1)
                file1.close()
                print("[*] Saved. ")   
                #this is for enterning the topic how tos after user selected topic
            if( direction == "thpreRequest" and (cont == True)  or (draft == False)):
                # Inserting preRequest
                # os.system("cls")
                print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
                print("[*] Enter -PreRequest- for This Tutorial. ")
                preR0 = " "
                if(draftData != ""):
                    preR0= draftData
                preR = input(">> ")
                preR = preR0 + preR
                print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
                userChoce = input("[*] >>  " )
                if(fileName):
                    hName = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                file1 = open(f"drafts/topics/{hName}.json", "r")
                load1 = json.load(file1) 
                load1["th"]["preRequest"] = preR
                load1["pointer"] = [] # so that at every object entery, the pointer must be empty so that if the user drafts a data, the pointer object will hold the current object
                load1["pointer"].append("howTos")
                load1["pointer"].append("preRequest")
                file1.close()
                file1 = open(f"drafts/topics/{hName}.json", "w")
                json.dump(load1, file1)
                file1.close()
                if(userChoce == "d" ):
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break
                if(userChoce == "c" ):
                    print("[*] Saved. ")
                    conn = input("[*] Press Enter To Continue..")
                else:
                    print("[*] You Enterd wrong!. taking matter in Hand..")
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break  

            if( direction == "thinfo" and (cont == True)  or (draft == False)):
                # Insert info
                # os.system("cls")
                print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
                print("[*] Enter -INFO- for This Tutorial. ")
                info0 = " "
                if(draftData != ""):
                    info0= draftData
                info1 = input(">> ")
                info1 = info0 + info1
                print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
                userChoce = input("[*] >>  " )
                if(fileName):
                    hName = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                file1 = open(f"drafts/topics/{hName}.json", "r")
                load1 = json.load(file1) 
                date1 = datetime.datetime.now
                load1["th"]["info"] = info1
                load1["th"]["timeStamp"] = str(date1) # date when the tutoral is created
                load1["pointer"] = []
                load1["pointer"].append("howTos")
                load1["pointer"].append("info")
                file1.close()
                file1 = open(f"drafts/topics/{hName}.json", "w")
                json.dump(load1, file1)
                file1.close()
                if(userChoce == "d" ):
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break
                if(userChoce == "c" ):
                    print("[*] Saved. ")
                    conn = input("[*] Press Enter To Continue..")
                else:
                    print("[*] You Enterd wrong!. taking matter in Hand..")
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break  

            if( direction == "thcontent" and (cont == True) or (draft == False)):
                # Inserting the main content
                # os.system("cls")
                print("[*] HERE INSERT Every Step by Step Concepts of The Tutorials. ")
                
                print("[*] Start Typing.................................................") 
                content0 = " "
                if(draftData != ""):
                    content0= draftData
                content = input(">>-- ")
                content = content0 + content
                print("[$] After you insert your data, Press \"F\" TO Finish and Save all. \n or you can save it as DRAFT by pressing \"d\" ")
                userChoce = input("[*] >>  " )
                if(fileName):
                    hName = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                file1 = open(f"drafts/topics/{hName}.json", "r")
                load1 = json.load(file1) 
                load1["th"]["content"] = content
                load1["pointer"] = []
                load1["pointer"].append("howTos") 
                load1["pointer"].append("content")
                file1.close()
                file1 = open(f"drafts/topics/{hName}.json", "w")
                json.dump(load1, file1)
                file1.close()
                if(userChoce == "d" ):
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break
                if(userChoce == "F" ):
                    # now save the draft file to the mainData.json file
                    file3 = open(f"drafts/topics/{hName}.json", "r") # load the draft to load3
                    load3 = json.load(file3)
                    file3.close()
                    how = load3["th"]

                    file3 = open("mainData.json", "r") 
                    readMain = json.load(file3)  # load the mainData.json file to readMain
                    idd = load3["tid"]-1 # b/c index starts from zero. if we dont decrease 1, it will have out of index error
                    readMain["Topic"][int(idd)]["howTos"].append(how)  # add the draft to the mainData by appending the object to the array to it
                    file3.close()
                    file = open("mainData.json", "w")
                    json.dump(readMain, file)
                    file.close()
                    # now we delete the draft file we dont need it any more
                    os.remove(f"drafts/topics/{hName}.json")
                    print("[*] Saved. ")
                    print("[***] You Have Finished Adding a New Tutorial for this TOPIC. \n [*] You Can Edit Your Content by Going to Edit Content from Home Page...")
                    home = input("[***] Press Enter Key to go to HomePage...")
                    break
                else:
                    print("[*] You Enterd wrong!. taking matter in Hand..")
                    print("[*] Saved As Draft. ")
                    conn = input("[*] Press Enter To Continue..")
                    break       

            
        # now for the howto inserting logic        
        if(choosen == "H" ):
            if( start == True): # this is setted from start manager. when the user selects to add new howtos
                # os.system("cls")
                print("[*] Enter the -How To Tutorial- Name to Add. ")
                hName2 = input(">> ")
                if(fileName):
                    hName2 = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
                # opening a json draft file for the howtos tutorials with the howtos name
                with open(f"drafts/howTos/{hName2}.json", "x") as file2:
                    json.dump(dataHowTos, file2)
                hid = dataLengthCounter("HowTos", False)  # the count of the howto array from the mainData.json and add 1 to set new content
                file1 = open(f"drafts/howTos/{hName2}.json", "r")
                load1 = json.load(file1)
                load1["title"] = hName2
                load1["id"] = hid
                file1.close()
                file1 = open(f"drafts/howTos/{hName2}.json", "w")
                json.dump(load1, file1)
                file1.close()
                print("[*] Saved. ")

        if( direction == "hpreRequest" and (cont == True) or (draft == False)):
            # Inserting preRequest
            # os.system("cls")
            print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
            print("[*] Enter -PreRequest- for This Tutorial. ")
            preR0 = " "
            if(draftData != ""):
                preR0= draftData
            preR = input(">> ")
            preR = preR0 + preR
            if(fileName):
                hName2 = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
            print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
            userChoce = input("[*] >>  " )
            file1 = open(f"drafts/howTos/{hName2}.json", "r")
            load1 = json.load(file1)
            load1["preRequest"] = preR
            load1["pointer"] = []
            load1["pointer"].append("preRequest")
            file1.close()
            file1 = open(f"drafts/howTos/{hName2}.json", "w")
            json.dump(load1, file1)
            file1.close()
            if(userChoce == "d" ):
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break
            if(userChoce == "c" ):
                print("[*] Saved. ")
            else:
                print("[*] You Enterd wrong!. taking matter in Hand..")
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break  

        if( direction == "hinfo" and (cont == True)  or (draft == False)):
            # Insert info
            # os.system("cls")
            print("[$] After you insert your data, you can CONTINUE by pressing \"c\" \n or you can save it as DRAFT by pressing \"d\" ")
            print("[*] Enter -INFO- for This Tutorial. ")
            info0 = " "
            if(draftData != ""):
                info0= draftData
            info1 = input(">> ")
            info1 = info0 + info1
            if(fileName):
                hName2 = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
            print("[*] Press \"d\" to Save AS Draft or Press \"c\" to Continue ")
            userChoce = input("[*] >>  " )
            file1 = open(f"drafts/howTos/{hName2}.json", "r")
            load1 = json.load(file1)
            date1 = datetime.datetime.now
            load1["info"] = info1
            load1["timeStamp"] = str(date1) # date when the tutoral is created
            load1["pointer"] = []
            load1["pointer"].append("info")
            file1.close()
            file1 = open(f"drafts/howTos/{hName2}.json", "w")
            json.dump(load1, file1)
            file1.close()
            if(userChoce == "d" ):
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break
            if(userChoce == "c" ):
                print("[*] Saved. ")
                conn = input("[*] Press Enter To Continue..")
            else:
                print("[*] You Enterd wrong!. taking matter in Hand..")
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break  

        if( direction == "hcontent" and (cont == True)  or (draft == False)):
            # Inserting the main content
            # os.system("cls")
            print("[*] HERE INSERT Every Step by Step Concepts of The Tutorials. ")
            print("[$] After you insert your data, Press \"F\" TO Finish and Save all. \n or you can save it as DRAFT by pressing \"d\" ")
            print("[*] Start Typing.................................................")
            content0 = " "
            if(draftData != ""):
                content0= draftData
            content = input(">>-- ")
            content = content0 + content
            print("[*] Press \"d\" to Save AS Draft or Press \"F\" to Finish. ")
            userChoce = input("[*] >>  " )
            if(fileName):
                hName2 = fileName # if the fileName is set from the draft function in order to contiune editing and to save the data this function must have the file name w/c is provided from draft function
            file1 = open(f"drafts/howTos/{hName2}.json", "r")
            load1 = json.load(file1)
            load1["content"] = content
            load1["pointer"] = []
            load1["pointer"].append("content") 
            file1.close()
            file1 = open(f"drafts/howTos/{hName2}.json", "w")
            json.dump(load1, file1)
            file1.close()
            if(userChoce == "d" ):
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break
            if(userChoce == "F" ):
                # now save the draft file to the mainData.json file
                file3 = open(f"drafts/howTos/{hName2}.json", "r") # load the draft to load3
                load3 = json.load(file3)
                file3.close()
                file3 = open("mainData.json", "r") 
                readMain = json.load(file3)  # load the mainData.json file to readMain
                hid = dataLengthCounter("HowTos", False, None)
                load3.pop("pointer")
                readMain["howTos"].append(load3)  # add the draft to the mainData by appending the object to the array to it
                file3.close()
                file = open("mainData.json", "w")
                json.dump(readMain, file)
                file.close()
                # now we delete the draft file we dont need it any more
                os.remove(f"drafts/howTos/{hName2}.json")
                print("[*] Saved. ")
                print("[***] You Have Finished Adding a New Tutorial for ",hName2,". \n[*] You Can Edit Your Content by Going to Edit Content from Home Page...")
                home = input("[***] Press Enter Key to go to HomePage...")
                break
            else:
                print("[*] You Enterd wrong!. taking matter in Hand..")
                print("[*] Saved As Draft. ")
                conn = input("[*] Press Enter To Continue..")
                break   
    return 



def draftManager():
    import os
    import os.path
    # now let the user choose the drafts from
    print("[*] List Drafts from.. ")
    print("[*]   \"T\" FROM TOPICS      OR      \"H\" FROM HOWTO'S")
    c = input(">> ")
    if(c == "T" ): # block for handling the topic drafts
        # NOW list the drafts from drafts directory
        drafts = os.listdir("drafts/topics")
        i = 0
        if(len(drafts) == 0):
            print("[*] There are No Drafts at this Moment.")
            bb = input("[*] Press Enter To Continue..")
            return
        print("[*] Select The Number to which you want to continue the Draft.")
        for each in drafts:
            print("     [",i,"] ",each,"") # to list all the drafts by id
            i += 1
        select = input(">> ")
        selected = drafts[int(select)]
        basename = os.path.splitext(selected)
        rbasename = os.path.splitext(selected)[0]
        # now open the file and load it. to find the pointer
        file = open(f"drafts/topics/{selected}", "r")
        load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
        file.close()
        pointer = load[6]
        if(pointer[0] == "info"):
            # os.system("cls")
            print(load["info"]) # to make it user friendly, we will out put the last data that the user enterd 
            contentAdder("tinfo", False, True, rbasename, draft = True, draftData= load["info"]) # this will call the adder function. then the arguments will deside where the user starts continuing adding
            return
        if(pointer[0] == "additional"):
            # os.system("cls")
            print(load["additional"])
            contentAdder("tadditional", False, True, rbasename, draft = True, draftData= load["additional"] )
            return
        if(pointer[1] == "preRequest"):
            # os.system("cls")
            print(load[7].preRequest)
            contentAdder("thpreRequest", False, True, rbasename, draft = True, draftData=load[7].preRequest)
            return
        if(pointer[1] == "info"):
            # os.system("cls")
            print(load[7].info)
            contentAdder("thinfo", False, True, rbasename, draft = True, draftData=load[7].info)
            return
        if(pointer[1] == "content"):
            # os.system("cls")
            print("-----------------------------------------------------CONTENT")
            print(load[7].content)
            contentAdder("thcontent", False, True, rbasename, draft = True, draftData=load[7].content)
            return
        else:
            print("[[ some error occored! try agin ]]")
            return
    if(c == "H" ): # block to handle the howtos drafts
        # NOW list the drafts from drafts directory
        drafts = os.listdir("drafts/howTos")
        i = 0
        if(len(drafts) == 0):
            print("[*] There are No Drafts at this Moment.")
            bb = input("[*] Press Enter To Continue..")
            return
        print("[*] Select The Number to which you want to continue the Draft.")
        for each in drafts:
            print("     [",i,"] ",each,"") # to list all the drafts by id
            i += 1
        select = input(">> ")
        selected = drafts[int(select)]
        base = os.path.splitext(selected)
        rbase = os.path.splitext(selected)[0]
        # now open the file and load it. to find the pointer
        file = open(f"drafts/howTos/{selected}", "r")
        load = json.load(file)
        file.close()
        pointer = load["pointer"]
        if(pointer[0] == "info"):
            os.system("cls")
            print(load["info"])
            contentAdder("hinfo", False, True, rbase, draft = True, draftData= load["info"]) # this will call the adder function. then the arguments will deside where the user starts continuing adding
            return
        if(pointer[0] == "preRequest"):
            os.system("cls")
            print(load["preRequest"])
            contentAdder("hpreRequest", False, True, rbase, draft = True, draftData=load["preRequest"])
            return
        if(pointer[0] == "content"):
            os.system("cls")
            print("-------------------------------------------------")
            print(load["content"])
            contentAdder("hcontent", False, True, rbase, draft = True, draftData=load["content"])
            return
        else:
            print("[[ some error occored! try agin ]]")
            return        
    return



def contentLister(contentObject):
    lop = True
    while(lop == True):
        if(contentObject["Topic"] == True):
            # open the selected objects
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
            file.close()
            info11 = load[0][int(str(contentObject["index2"]))].info
            add = load[0][int(str(contentObject["index2"]))].additional
            name = load[0][int(str(contentObject["index2"]))].name
            x=True
            while( x == True):
                os.system("cls")
                print("[*] You Have Choosen --", name, "--")
                print("[*] Enter the Option you want To Open it.")
                howToNum = dataLengthCounter("Topic", True, int(str(contentObject["index2"])))
                print("     -i- Info    -a- Additional    -list- To List HowTo's in This Topic [",howToNum,"]     -quit- To Exit")
                ch = input(">> ")
                if(ch == "list"):
                    file = open("mainData.json", "r")
                    load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))# this object hook will make the dict data accessable as an object or by . 
                    collection = []
                    collection = load[0][int(contentObject["index2"])].howTos # this selects the first 0 is entering to 'Topic' object... w/c has the array of the objects..
                    file.close()
                    print("[*] These is list of All The HowTo's in This Topic. ")
                    i = 0
                    for each in collection:
                        print("     [-",i,"-] ",each.title,) # in other words this is equal to load[0][0].howTos[1] ...the second 0 is for intering the first array in the "Topic" array. then .howtos is to get in to howtos array and [1] is to access the objects in howtos
                        i += 1
                    print("[*] To Select Topic use this command.. \"list -number of the topic\". \n [*] Eg: list -44  ")
                    choice = input(">> ")
                    choosenNum = ""
                    for each in choice: # this loop is for filtering the number from "list -number"
                        choosenNum = choosenNum + each
                        if(choosenNum == "list -"): # after the loop gets to list - then this condition will met and set it to empty string and on the next loop, what left will be the pure id number we need that the user choosed 
                            choosenNum = ""
                    # open file to access howtos in topics
                    file = open("mainData.json", "r")
                    load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
                    file.close()
                    howToname = load[0][int(str(contentObject["index2"]))].howTos[int(choosenNum)].title # the first 0 is to go in topics array, the second contentobject.index2 is from the previos function that chose the title and the last choosnum is the user choosing howtos from the topics
                    info = load[0][int(str(contentObject["index2"]))].howTos[int(choosenNum)].info
                    content = load[0][int(str(contentObject["index2"]))].howTos[int(choosenNum)].content
                    preRequest = load[0][int(str(contentObject["index2"]))].howTos[int(choosenNum)].preRequest
                    inhowto = True
                    while(inhowto == True):
                        os.system("cls")
                        print("[*] You Have Choosen --", howToname, "--")
                        print("[*] Enter the Option you want To Open it.")
                        print("     -i- Info    -p- PreRequest   -C- Content    -exit- To Exit")
                        ch = input(">> ")
                        if(ch == "i"):
                            os.system("cls")
                            print("--------------------------------------INFO")
                            print(info)
                            clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                            os.system("cls")
                        if(ch == "p"):
                            os.system("cls")
                            print("--------------------------------------PRE-REQUEST")
                            print(preRequest) 
                            clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                            os.system("cls")
                        if(ch == "C" or ch == "c"):         
                            os.system("cls")          
                            print("--------------------------------------CONTENT")
                            print(content)
                            clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                            os.system("cls")
                        if(ch == "exit"):
                            break
                        else:
                            print("[*] Please Enter the correct command.")
                            
                   
                if(ch == "a"):
                    os.system("cls")
                    print("--------------------------------------ADDITIONAL")
                    print(add)
                    clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                    os.system("cls")
                if(ch == "i"):
                    os.system("cls")
                    print("--------------------------------------INFO")
                    print(info11)
                    clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                    os.system("cls")
                if(ch == "quit"):
                    break
                else:
                    print("[*] Please Enter the correct command.")
        
                
        if(contentObject["Topic"] == False ):
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
            file.close()
            howToname = load[int(str(contentObject["index1"]))][int(str(contentObject["index2"]))].title # the first 0 is to go in topics array, the second contentobject.index2 is from the previos function that chose the title and the last choosnum is the user choosing howtos from the topics
            info = load[int(str(contentObject["index1"]))][int(str(contentObject["index2"]))].info
            content = load[int(str(contentObject["index1"]))][int(str(contentObject["index2"]))].content
            preRequest = load[int(str(contentObject["index1"]))][int(str(contentObject["index2"]))].preRequest
            os.system("cls")
            loop = True
            while(loop == True):
                print("[*] You Have Choosen --", howToname, "--")
                print("[*] Enter the Option you want To Open it.")
                print("     -i- Info    -p- PreRequest  -C- Content    -exit- To Exit")
                ch = input(">> ")
                if(ch == "i"):
                    os.system("cls")
                    print("--------------------------------------INFO")
                    print(info)
                    clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                    os.system("cls")
                if(ch == "p"):
                    os.system("cls")
                    print("--------------------------------------PRE-REQUEST")
                    print(preRequest) 
                    clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                    os.system("cls")
                if(ch == "C" or ch == "c"):                  
                    os.system("cls") 
                    print("--------------------------------------CONTENT")
                    print(content)
                    clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                    os.system("cls")
                if(ch == "exit"):
                    break
            else:
                print("[*] Please Enter the correct command.")
        else:
            print("[*] Please Enter the correct command3.")
        return
    return

                



def lister(selector):
    loop = True
    while(loop == True):
        # here at the begining when the user wants to list topics or howtos. the selected will pass through the selector args
        if(selector == "list -T"):
            # now access the mainData.json to list the objects
            os.system("cls")
            with open("mainData.json", "r") as file:
                load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys() ) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
            collection = [] 
            collection = load[0] # this selects the first 0 is entering to 'Topic' object... w/c has the array of the objects
            file.close()
            print("[*] These is list of All The Topics. ")
            i = 0
            for each in collection:
                print("     [-",i,"-] ",each.name,) # in other words this is equal to load[0].name ...
                i += 1
            print("[*] To Select Topic use this command.. \"list -number of the topic\". \n[*] Eg: list -44   -exit- To Go Back. ")
            choice = input(">> ")
            if(choice == "exit"):
                break
            else:
                print("[*] Please Enter the correct command.")
            choosenNum = ""
            for each in choice: # this loop is for filtering the number from "list -number"
                choosenNum = choosenNum + each
                if(choosenNum == "list -"): # after the loop gets to list - then this condition will met and set it to empty string and on the next loop, what left will be the pure id number we need that the user choosed 
                    choosenNum = ""
            obj = {
                "Topic" : True, # this helps in the contentLister function to tell it that there is a howtos in the topic you have to list
                "index1" : "0", # to get in Topics array in mainData.json
                "index2" : choosenNum # goes to the topic id that the user chooses
            }
            return obj
        if(selector == "list -H"):
            os.system("cls")
            # now access the mainData.json to list the objects
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
            collection = []
            collection = load[1] # this selects the first 0 is entering to 'Topic' object... w/c has the array of the objects
            file.close()
            print("[*] These is list of All The Topics. ")
            i = 0
            for each in collection:
                print("     [-",each.id,"-] ",each.title,) # in other words this is equal to load[0].name ...
                i += 1
            print("[*] To Select Topic use this command.. \"list -number of the topic\". \n[*] Eg: list -44   -exit- To Go Back. ")
            choice = input(">> ")
            if(choice == "exit"):
                break
            # else:
            #     print("[*] Please Enter the correct command1.")
            choosenNum = ""
            for each in choice: # this loop is for filtering the number from "list -number"
                choosenNum = choosenNum + each
                if(choosenNum == "list -"): # after the loop gets to list - then this condition will met and set it to empty string and on the next loop, what left will be the pure id number we need that the user choosed 
                    choosenNum = ""
            obj = {
                "Topic" : False, # this helps in the contentLister function to tell it that there is only howtos in here
                "index1" : "1", # to get in to Howtos array in mainData.json
                "index2" : choosenNum
            }
            return obj
        else:
            print("[*] Please Enter the correct command2!")
    return

        
            

def editor():
    print("[*] In what catagori do you want to edit?")
    print("     -T- Topic     |        -H- HowTo's")
    ch = input(">> ")
    if(ch == "T"):
        index = lister("list -T")
        int(index["index1"])
        int(int(index["index2"]))
        
        # open the file besed on the index from lister function
        file = open("mainData.json", "r")
        load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
        file.close()
        name = load[0][int(index["index2"])].name
        info = load[0][int(index["index2"])].info
        additional = load[0][int(index["index2"])].additional
        print("[*] Topic to Edit is \"",name,"\"")
        print("[*] Select Option to Edit..")
        print("     -i- INFO    -a- ADDITIONAL    -list- To Edit HowTos")
        ch = input(">> ")
        # eziga nek.... objectun set mareg silmayichal sel wust mulu howtos objectun ketek edit argewe
        if(ch == "i"):
            print(info,"\n [*] Edit here..")
            edit = input(">> ")
            file = open("mainData.json", "r")
            load = json.load(file)
            load["Topic"][int(index["index2"])]["info"] = edit
            # sel = load["Topic"][int(index["index2"])]["howTos"] # the whole howto object in the selected howto will be saved to sel. then the sel object will get modifide and reattache it to the howtos in the mainData.json
            # sel["info"] = edit  # here the info is edited separetly 
            # load["Topic"][int(index["index2"])]["howTos"] = sel 
            file = open("mainData.json", "w")
            json.dump(load, file)
            file.close()
            print("[*] File Edited.")
            clear = input("\n\n\n\n\n[*] Press Enter To Continue..")

        if(ch == "a"):
            print(additional,"\n [*] Edit here..")
            edit = input(">> ")
            file = open("mainData.json", "r")
            load = json.load(file)
            load["Topic"][int(index["index2"])]["additional"]= edit
            file = open("mainData.json", "w")
            json.dump(load, file)
            file.close()
            print("[*] File Edited.")
            clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            
        if(ch == "list"):
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values())) # this object hook will make the dict data accessable as an object or by . 
            collection = []
            collection = load[0][int(index["index2"])].howTos # this selects the first 0 is entering to 'Topic' object... w/c has the array of the objects..
            file.close()
            print("[*] These is list of All The HowTo's in This Topic. ")
            i = 0
            for each in collection:
                print("     [-",i,"-] ",each.title,) # in other words this is equal to load[0][0].howTos[1] ...the second 0 is for intering the first array in the "Topic" array. then .howtos is to get in to howtos array and [1] is to access the objects in howtos
                i += 1
            print("[*] To Select Topic use this command.. \"list -number of the topic\". \n [*] Eg: list -44  ")
            choice = input(">> ")
            choosenNum = ""
            for each in choice: # this loop is for filtering the number from "list -number"
                choosenNum = choosenNum + each
                if(choosenNum == "list -"): # after the loop gets to list - then this condition will met and set it to empty string and on the next loop, what left will be the pure id number we need that the user choosed 
                    choosenNum = ""
            int(choosenNum)
            # open file to access howtos in topics
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys() ) (*obj.values()))
            file.close()
            howToname = load[0][int(index["index2"])].howTos[int(choosenNum)].title # the first 0 is to go in topics array, the second contentobject.index2 is from the previos function that chose the title and the last choosnum is the user choosing howtos from the topics
            info = load[0][int(index["index2"])].howTos[int(choosenNum)].info
            content = load[0][int(index["index2"])].howTos[int(choosenNum)].content
            preRequest = load[0][int(index["index2"])].howTos[int(choosenNum)].preRequest
            print("[*] You Have Choosen --", howToname, "--")
            print("[*] Enter the Option you want To Edit it.")
            print("     -i- Info    -p- PreRequest   -C- Content")
            ch = input(">> ")
            if(ch == "i"):
                print(info, " \n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load1 = json.load(file)
                sel = load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] # the whole howto object in the selected howto will be saved to sel. then the sel object will get modifide and reattache it to the howtos in the mainData.json
                sel["info"] = edit  # here the info is edited separetly 
                load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] = sel 
                file = open("mainData.json", "w")
                json.dump(load1, file)
                file.close()
                print("[*] File Edited.")
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            if(ch == "p"):
                print(preRequest ," \n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load1 = json.load(file)
                sel = load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] # the whole howto object in the selected howto will be saved to sel. then the sel object will get modifide and reattache it to the howtos in the mainData.json
                sel["preRequest"] = edit  # here the info is edited separetly 
                load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] = sel 
                file = open("mainData.json", "w")
                json.dump(load1, file)
                file.close()
                print("[*] File Edited.")
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            if(ch == "c" or ch == "C"):
                print(content ," \n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load1 = json.load(file)
                sel = load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] # the whole howto object in the selected howto will be saved to sel. then the sel object will get modifide and reattache it to the howtos in the mainData.json
                sel["content"] = edit  # here the info is edited separetly 
                load1["Topic"][int(index["index2"])]["howTos"][int(choosenNum)] = sel 
                file = open("mainData.json", "w")
                json.dump(load1, file)
                file.close()
                print("[*] File Edited.")
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            else:
                return
    if(ch == "H"):
        index = lister("list -H")
        file = open("mainData.json", "r")
        load = json.loads(file.read(), object_hook= lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
        file.close()
        # howToname = load[0][int(index["index2"])].howTos[choosenNum].title 
        # the first 0 is to go in topics array, the second contentobject.index2 is from the previos function that chose the title and the last choosnum is the user choosing howtos from the topics
        # info = load[0]][int(index["index2"])].howTos[choosenNum].info
        # preRequest = load[0]][int(index["index2"])].howTos[choosenNum].preRequest
        # content = load[0]][int(index["index2"])].howTos[choosenNum].content
        howToname = load[1][int(index["index2"])].title 
        info = load[1][int(index["index2"])].info
        preRequest = load[1][int(index["index2"])].preRequest
        content = load[1][int(index["index2"])].content
        loop = True
        while(loop == True):
            print("[*] You Have Choosen --", howToname, "--")
            print("[*] Enter the Option you want To Edit it.")
            print("     -i- Info    -p- PreRequest  -C- Content")
            ch = input(">> ")
            if(ch == "i"):
                print(info, "\n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load = json.load(file)
                bla = load["howTos"][int(index["index2"])]
                bla["info"]= edit
                load["howTos"][int(index["index2"])] = bla
                file = open("mainData.json", "w")
                json.dump(load, file)
                file.close()
                print("[*] File Edited.")
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            if(ch == "p"):
                print(preRequest, "\n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load = json.load(file)
                bla = load["howTos"][int(index["index2"])]
                bla["preRequest"]= edit
                load["howTos"][int(index["index2"])] = bla            
                file = open("mainData.json", "w")
                json.dump(load, file)
                file.close()
                print("[*] File Edited.")
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
            if(ch == "c" or ch == "C"):
                print(content ,"\n [*] Edit here..")
                edit = input(">> ")
                file = open("mainData.json", "r")
                load = json.load(file)
                bla = load["howTos"][int(index["index2"])]
                bla["content"]= edit
                load["howTos"][int(index["index2"])] = bla
                file = open("mainData.json", "w")
                json.dump(load, file)
                file.close()
                print("[*] File Edited.")        
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")  
            else:
                break
   
    return


def search(word, direction):
    # get file to be searched
    file = open("mainData.json", "r")
    load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
    file.close()
    thowTos = load[0]
    howTos = load[1]
    # user sentence will be separted and each word is placed in an array
    userWord = []
    single = ""
    v = 1
    # for loop to go through the words of the user sentence
    for each in word:
        if(each != " "): # when the loop gets to space, it stops adding to the userword array
            single = single + each
        if(each == " "): # when the loop gets to space, it adds the string in the single to the userword array 
            userWord.append(single)
            single = "" # this empty the single variable for a new word to be enterd to the single var agin like the first one
        if(len(word) == v):
            userWord.append(single)
        v += 1
    toBeSearched = []
    if(direction == "thowTos"):
        i=0
        names =[]
        collect = []
        for each in thowTos: # loops through the topics
            tidd = each.id
            for ht in each.howTos:
                names.append(ht.title) # singles out the name of the howtos in the topic
                obj = {} # object to store the important object of each data in the loop
                collect = []
                obj["index1"] = 0
                obj["index2"] = ht.id
                obj["index3"] = True
                obj["index4"] = ht.title # to show me the name of howtos in the topic howtos
                obj["index5"] = int(tidd)
                collect.append(obj) # the object will be placed in a single array to be hold for each howto name this array holdes all the objects and the separated words to be organized
                # [ [{obj}, word1, word2, word3], [{obj}, word1, word2, word3]] each array is differnt howtos name 
                toBeSearched.append(collect)
                # print(toBeSearched)
        i+=1
        x = ""
        y = 0
        inn = 1
        for sel in names:
            for se in sel:
                if(se != " "):
                    x = x + se
                if(se == " "):
                    toBeSearched[y].append(x)
                    x = ""
                if(len(sel) == inn):
                    toBeSearched[y].append(x)
                inn +=1
            y += 1
        foundMatch = []
        # print(names)
        for sel in userWord:
            for each in toBeSearched:
                # print(each)
                object = each[0]
                for each1 in each:
                    if(each1 != "How" or each1 != "is" or each1 != "to"):
                        if(sel == each1):
                            foundMatch.append(object) # each[0] is the first array element w/c is the object dict that holds the needed key values to access the found matched
        # print(foundMatch)
        return foundMatch
    if(direction == "howTos"):
        i = 0
        for each in howTos: # loops through the howtoes only
            if(len(howTos) > i):
                name = each.title # singles out the name of the howtos in the topic
                obj = {} # object to store the important object of each data in the loop
                collect = []
                x = ""
                obj["index1"] = 1
                obj["index2"] = each.id
                obj["index3"] = False
                obj["index4"] = 0  # to show me the id of howtos in the howtos
                collect.append(obj) # the object will be placed in a single array to be hold for each howto name this array holdes all the objects and the separated words to be organized
                # [ [{obj}, word1, word2, word3], [{obj}, word1, word2, word3]] each array is differnt howtos name 
                h = 1
                for sel in each.title:
                    if(sel != " "):
                        x = x + sel
                    if(sel == " "):
                        collect.append(x)
                        x = ""
                    if(len(each) == h):
                        collect.append(x)
                    h += 1
                toBeSearched.append(collect)
            foundMatch = []
            for sel in userWord:
                for each in toBeSearched:
                    object = each
                    for each in each:
                        if(each != "How" or each != "is" or each != "to"):
                            if(sel == each):
                                foundMatch.append(object[0]) 
                                # each[0] is the first array element w/c is the object dict that holds the needed key values to access the found matched
            # print(foundMatch)
    return foundMatch
        

        

def searchResultLister(direction):
    if(len(direction) > 0):
        if(direction[0]["index3"] == True): # True indicates there is a 'howTos' object
            x = direction[0]
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook = lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
            file.close()
            result = []
            result = load[0][x["index5"]].howTos[x["index2"]] # these indexes came frame the search function
            print("[*] Match Found [",len(direction),"]")
            for each in direction: # loop to list the matchfound array w/c we get from search function
                y = each
                print("--> [-",load[0][y["index5"]].howTos[y["index2"]].id,"-] ",load[0][y["index5"]].howTos[y["index2"]].title)


            print("[*] These are The HowTo's That FounMatch!! ")

            print("[*] To Select Topic use this command.. \"list -number of the topic\". \n [*] Eg: list -44  ")
            choice = input(">> ")
            choosenNum = ""
            for each in choice: # this loop is for filtering the number from "list -number"
                choosenNum = choosenNum + each
                if(choosenNum == "list -"): # after the loop gets to list - then this condition will met and set it to empty string and on the next loop, what left will be the pure id number we need that the user choosed 
                    choosenNum = ""
            # open file to access howtos in topics
            file = open("mainData.json", "r")
            load = json.loads(file.read(), object_hook= lambda obj: namedtuple("obj", obj.keys()) (*obj.values()))
            file.close()
            howToname = load[0][x["index5"]].howTos[int(choosenNum)].title # the first 0 is to go in topics array, the second contentobject.index2 is from the previos function that chose the title and the last choosnum is the user choosing howtos from the topics
            info = load[0][x["index5"]].howTos[int(choosenNum)].info
            content = load[0][x["index5"]].howTos[int(choosenNum)].content
            preRequest =  load[0][x["index5"]].howTos[int(choosenNum)].preRequest
            print("[*] You Have Choosen --", howToname, "--")
            print("[*] Enter the Option you want To Open it.")
            print("     -i- Info    -a- PreRequest   -C- Content")
            ch = input(">> ")
            if(ch == "i"):
                os.system("cls")
                print("--------------------------------------INFO")
                print(info)
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                os.system("cls")
            if(ch == "a"):
                os.system("cls")
                print("--------------------------------------PRE-REQUEST")
                print(preRequest) 
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                os.system("cls")
            if(ch == "C" or "c"):                   
                os.system("cls")
                print("--------------------------------------CONTENT")
                print(content)
                clear = input("\n\n\n\n\n[*] Press Enter To Continue..")
                os.system("cls")
            else:
                return

        if(direction[0]["index3"] == False):
            print("[*] Match Found [",len(direction),"]")
            file = open("mainData.json", "r")
            load = json.load(file)
            file.close()
            lists = load["howTos"][int(direction[0]["index2"])]
            for each in direction:
                print("[- ",lists["id"]," -] ",lists["title"])
            print("[*] Select a Tutorial to view.")
            mm = input(">> ")
            contentLister({
                "Topic" : False,
                "index1" : 1,
                "index2" : mm
            })
    else:
        print("[*] No Mactch Found.")
        conn = input("[*] Press Enter To Continue..")
    return




    
