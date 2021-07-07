
import modules
import os

on = True
while(on == True):
    os.system("cls")
    print( """
        WELCOME, To Yourcyclopedia. 

                --> Type [ list -T ]  to List [TOPIC'S].
                --> Type [ list -H ]  to List [HOW TO'S Tutorials].
                --> Type [ Edit ]     to Edit Contents.
                --> Type [ Add ]      to Add New CONTENT.
                --> Type [ Cont ]     to Conuinue Drafts.
        --> Type [ sT ] to search in [HowTO-TOPIC'S].
        --> Type [ sH ] to search in [HOW TO'S Tutorials].
    """)
   
    searchIn = ""
    print("[----------------------------------------------------------]")
    user = input(">> ")
    command = ""

    for each in user:
        command = command + each
        if(command == "list -"):
            command = ""
    if(command == "T"):
        modules.contentLister(modules.lister("list -T"))
    if(command == "H"):
        modules.contentLister(modules.lister("list -H"))
    if(user == "Edit"):
        modules.editor()
    if(user == "sT"):
        searchIn = "Topic's"
        print("[*] Search in [",searchIn,"].")
        iner = input(">> ")
        modules.searchResultLister(modules.search(iner, "thowTos"))
    if(user == "sH"):
        searchIn = "HowTo's"
        print("[*] Search in [",searchIn,"].")
        iner = input(">> ")
        modules.searchResultLister(modules.search(iner, "howTos"))
    if(user == "Add"):
        modules.contentAdder("none", True, True)
    if(user == "Cont"):
        modules.draftManager()
    else:
        print("[*] Please Enter The Correct Command.")
    

    
