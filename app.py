from os import name
import re
from django.shortcuts import render
from flask import Flask,redirect,render_template,request,jsonify, url_for
import firebase_admin
from firebase_admin import credentials,firestore



app = Flask(__name__)



cred = credentials.Certificate("function_form_credentials.json")  # Secret Credentials not on view
firebase_admin.initialize_app(cred)
store=firestore.client()

@app.route('/',methods=["GET"])
def home():
        st_data = store.collection("function_data").stream()
        venue_collection = []
        venue_collection_set = set()
        for doc in st_data:
            for k in doc.to_dict():
                if (k=="venue"):
                    venue_collection.append(doc.to_dict()[k])
        for i in venue_collection:
            venue_collection_set.add(i)


        docs = store.collection("venues").stream()
        v_list = []
        v_list_set = set()
        print("docs = ",docs)
        for doc in docs:
            for k in doc.to_dict():
                v_list.append(doc.to_dict()[k])
        print(v_list)
        for i in v_list:
            v_list_set.add(i)

        difference_set = v_list_set - venue_collection_set
        difference_list = []
        for i in difference_set:
            difference_list.append(i)


        print(difference_list)



        return render_template("login_form.html",venue = difference_list)


@app.route('/login_validation',methods=["GET","POST"])
def login_valid():
    log = request.form.get("login_as")
    mail_id = request.form.get("mail_id")
    staff_id = request.form.get("staff_id")


    if (log=="Admin"):
        docs = store.collection("admin_login").stream()
        for doc in docs:
            for i in doc.to_dict():
                if doc.to_dict()[i]==mail_id:
                    if doc.to_dict()["staff_id"]==staff_id:
                        func_list = []
                        ap_data = store.collection("function_data").stream()
                        for ap_doc in ap_data:
                            func_list.append(ap_doc.to_dict())
                        return render_template("admin.html",function = func_list)
                    else:
                        return render_template("login_form.html",confirmation="id_not_match")
                    

    else:
        """st_data = store.collection("function_data").stream()
        venue_collection = []
        venue_collection_set = set()
        for doc in st_data:
            for k in doc.to_dict():
                if (k=="venue"):
                    venue_collection.append(doc.to_dict()[k])
        for i in venue_collection:
            venue_collection_set.add(i)


        docs = store.collection("venues").stream()
        v_list = []
        v_list_set = set()
        print("docs = ",docs)
        for doc in docs:
            for k in doc.to_dict():
                v_list.append(doc.to_dict()[k])
        print(v_list)
        for i in v_list:
            v_list_set.add(i)

        difference_set = v_list_set - venue_collection_set
        difference_list = []
        for i in difference_set:
            difference_list.append(i)"""
        up_data = firestore.client()
        func_list = []
        #st_data = store.collection("function_data").stream()

        docs = store.collection("staff_login").stream()
        for doc in docs:
            for i in doc.to_dict():
                if doc.to_dict()[i]==mail_id:
                    if doc.to_dict()["staff_id"]==staff_id:
                        print(mail_id)
                        db=up_data.collection("function_data").where("organizer_mail_id","==",mail_id).get()
                        #db=up_data.collection("function_data").stream()
                        for data in db:
                            key = data.id
                            func = store.collection("function_data").document(key).get()
                            print(func)
                            func_list.append(func.to_dict())
                            
                        print(func_list)
                        return render_template("function_form.html",date=None,mailid=mail_id,function=func_list)
                    else:
                        return render_template("login.html",confirmation = "id_not_match")


    print(log,"\n",mail_id,"\n",staff_id)
    return render_template("login_form.html",confirmation="failure")


@app.route('/approve',methods=["GET","POST"])
def approve_cancel():
    func_name = request.form.get('func_name')
    """func_date = request.form.get('func_date')
    chief_guest_name = request.form.get('chief_guest_name')
    organizer_name = request.form.get('organizer_name')
    venue = request.form.get('venue')"""
    up_data = firestore.client()
    func_list = []
    ap_data = store.collection("function_data").stream()
    
    print(request.form.get('approve'))
    if(request.form.get('approve')=="approve"):
        docs = up_data.collection("function_data").where("func_name","==",func_name).get()
        for doc in docs:
            key = doc.id
            print(key)
            up_data.collection("function_data").document(key).update({"approval":"approved"})
            for ap_doc in ap_data:
                func_list.append(ap_doc.to_dict())
            return render_template("admin.html",function = func_list)
                


    elif(request.form.get('approve')=="cancel"):
        docs = up_data.collection("function_data").where("func_name","==",func_name).get()
        for doc in docs:
            key = doc.id
            print(key)
            up_data.collection("function_data").document(key).update({"approval":"cancelled"})
            for ap_doc in ap_data:
                func_list.append(ap_doc.to_dict())
            return render_template("admin.html",function = func_list)

    elif(request.form.get('delete_func')=="delete_func"):
        """st_data = store.collection("function_data").stream()
        venue_collection = []
        venue_collection_set = set()
        for doc in st_data:
            for k in doc.to_dict():
                if (k=="venue"):
                    venue_collection.append(doc.to_dict()[k])
        for i in venue_collection:
            venue_collection_set.add(i)


        v_docs = store.collection("venues").stream()
        v_list = []
        v_list_set = set()
        print("docs = ",v_docs)
        for doc in v_docs:
            for k in doc.to_dict():
                v_list.append(doc.to_dict()[k])
        print(v_list)
        for i in v_list:
            v_list_set.add(i)

        difference_set = v_list_set - venue_collection_set
        difference_list = []
        for i in difference_set:
            difference_list.append(i)"""

        mail_id = request.form.get('organizer_mail_id')
        func_name = request.form.get('func_name')
        print("function name ::::: ",func_name)
        func_list = []
        #store.collection("function_data").where("func_name"==func_name).get()
        docs = store.collection("function_data").where("func_name","==",func_name).get()
        print("docs--->",docs)
        for doc in docs:
            key = doc.id
            print(key)
            up_data.collection("function_data").document(key).delete()

        db=store.collection("function_data").where("organizer_mail_id","==",mail_id).get()
        print("db---->",db)
        for data in db:
            key = data.id
            func = store.collection("function_data").document(key).get()
            func_list.append(func.to_dict())
        return render_template("function_form.html",date=None,mailid=mail_id,function=func_list)



    return render_template("admin.html",error="error")


@app.route('/submit',methods=["GET","POST"])
def submit():

    s_dict = {}


    #general_details
    s_dict["dept_name"] = request.form.get('department')  
    s_dict["func_name"] = request.form.get('func_name')
    s_dict["func_date"] = request.form.get('func_date')
    s_dict["func_days"] = request.form.get('func_days')
    print("date----------->",request.form.get('func_date'))
    s_time = request.form.get('time_duration_start').split(':')
    if (int(s_time[0])<12):
        start_time = s_time[0] +":"+s_time[1] + " AM"
    else:
        if int(s_time[0])==12:
            start_time = s_time[0] +":"+s_time[1] + " PM"
        else:
            temp = int(s_time[0]) - 12
            start_time = str(temp) +":"+s_time[1] + " PM"
    s_dict["time_duration_start"] = start_time
    e_time = request.form.get('time_duration_end').split(':')
    if (int(e_time[0])<12):
        end_time = e_time[0] +":"+e_time[1] + " AM"
    else:
        if int(e_time[0])==12:
            end_time = e_time[0] +":"+e_time[1] + " AM"
        else:
            temp = int(e_time[0]) - 12
            end_time = str(temp) + ":" + e_time[1] + " PM"
    s_dict["time_duration_end"] = end_time
    s_dict["venue"] = request.form.get('venue')
    s_dict["training_type"] = request.form.get('train_type')
    s_dict["func_students"] = request.form.get('func_students')
    year_students = request.form.get('func_students_year')
    dept_students = request.form.get('func_students_dept')
    class_students = request.form.get('func_students_class')
    func_students_year_course = year_students+"-"+dept_students+"-"+class_students
    s_dict["func_students_year_course"] = func_students_year_course
    s_dict["chief_guest_name"] = request.form.get('chief_guest_name')
    s_dict["designation"] = request.form.get('designation')
    s_dict["field_type"] = request.form.get('field_type')
    s_dict["field"] = request.form.get('organizer_name')
    s_dict["organizer_name"] = request.form.get('organizer_name')
    s_dict["organizer_contact"] = request.form.get('organizer_contact')

    

    #guest_house  s_dict[""]
    if(request.form.get('guest_house_persons')=="" and request.form.get('guest_house_days'=="")):
        s_dict["guest_house"] = None 
        s_dict["guest_house_pesons"] = None
        s_dict["guest_house_days"] = None
    else:
        s_dict["guest_house"] = "Yes"
        s_dict["guest_house_pesons"] = request.form.get('guest_house_persons')
        s_dict["guest_house_days"] = request.form.get('guest_house_days')

    #refreshment
    if (request.form.get('refreshment_guest_number')==""):
        s_dict["refreshment_for_guest"] = "No"
        s_dict["refreshment_for_guest_number"] = None
    else:
        s_dict["refreshment_for_guest"] = "Yes"
        s_dict["refreshment_for_guest_number"] = request.form.get('refreshment_guest_number')

    if(request.form.get('refreshment_student_number')==""):
        s_dict["refreshment_for_student"] = "No"
        s_dict["refreshment_for_student_number"] = None
    else:
       s_dict["refreshment_for_student"] = "Yes"
       s_dict["refreshment_for_student_number"] = request.form.get('refreshment_student_number') 
    s_dict["payment_through"] = request.form.get('payment_through')
    s_dict["lunch_exact_numbers"] = request.form.get('lunch_exact_numbers')
    s_dict["tiffin"] = request.form.get('tiffin')
    s_dict["spl_lunch_veg"] = request.form.get('spl_lunch_veg')
    s_dict["spl_lunch_non_veg"] = request.form.get('spl_lunch_non_veg')
    s_dict["lunch_required_time"] = request.form.get('lunch_required_time')

    #transport
    if(request.form.get('transport_req_date')==""):
        s_dict["transport_req"] = "No"
        s_dict["transport_req_date"] = None
        s_dict["transport_pickup_time"] = None
        s_dict["transport_location"] = None
        s_dict["transport_drop_time"] = None
        s_dict["transport_pickup_person_name"] = None
        s_dict["transport_pickup_person_contact"] = None
    else:
        s_dict["transport_req"] = "Yes"
        s_dict["transport_req_date"] = request.form.get('transport_req_date')
        s_dict["transport_pickup_time"] = request.form.get('transport_pickup_time')
        s_dict["transport_location"] = request.form.get('transport_location')
        s_dict["transport_drop_time"] = request.form.get('transport_drop_time')
        s_dict["transport_pickup_person_name"] = request.form.get('transport_pickup_person_name')
        s_dict["transport_pickup_person_contact"] = request.form.get('transport_pickup_person_contact')
    
    
    #Power/System/Camera Requirement
    s_dict["mic_arrangement"] = request.form.get('mic_arrangement')
    s_dict["type_of_mic"] = request.form.get('type_of_mic')
    s_dict["mic_number"] = request.form.get('mic_number')
    s_dict["ac_arrangement"] = request.form.get('ac_arrangement')
    s_dict["lcd_projector"] = request.form.get('lcd_projector')
    s_dict["laptop"] = request.form.get('laptop')
    s_dict["photography"] = request.form.get('photography')


    #Memento/Seating/Reception/Item requirement
    s_dict["memento"] = request.form.get('memento')
    s_dict["seating_arrangement_numbers"] = request.form.get('seating_arrangement_numbers')
    s_dict["dias"] = request.form.get('dias')
    s_dict["audience"] = request.form.get('audience')
    s_dict["table_cloth_number"] = request.form.get('table_cloth_number')
    s_dict["reception_item_rec"] = request.form.get('reception_item_rec')

    #approval
    s_dict["approval"] = None

    s_dict["organizer_mail_id"] = request.form.get('mail_id')
    mail_id = request.form.get('mail_id')

    store.collection("function_data").add(s_dict)

    print("DATA SAVED TO DATABASE !!!")

    

    #difference_list = get_venue_details()

    db=store.collection("function_data").where("organizer_mail_id","==",mail_id).get()
    func_list = []
    for data in db:
        key = data.id
        func = store.collection("function_data").document(key).get()
        print(func)
        func_list.append(func.to_dict())

    return render_template("function_form.html",date=None,mailid=mail_id,function=func_list)

@app.route('/get_venue_details',methods=["GET","POST"])
def get_venue_details():
    st_data = store.collection("function_data").stream()
    #venue_collection = {}
    venue_collection_list = []
    for doc in st_data:
        venue_collection = {}
        print("doc dict=---------->",doc.to_dict())
        for k in range(1):
            print("k---------------->",k)
            venue_collection["venue"]=doc.to_dict()["venue"]
            venue_collection["func_date"]=doc.to_dict()["func_date"]
            venue_collection["time_duration_start"]=doc.to_dict()["time_duration_start"]
        venue_collection_list.append(venue_collection)


    func_date_ck = request.form.get('func_date_check')
    mail_id = request.form.get('mail_id')
    print("Mail id : ---->",mail_id)
    print("Date--------->",func_date_ck)
    #func_start_time_ck = request.form.get('time_duration_start')

    func_start_time = request.form.get('time_duration_start_check').split(':')
    if (int(func_start_time[0])<12):
        function_start_time = func_start_time[0] +":"+func_start_time[1] + " AM"
    else:
        if int(func_start_time[0])==12:
            function_start_time = func_start_time[0] +":"+func_start_time[1] + " AM"
        else:
            temp = int(func_start_time[0]) - 12
            function_start_time = str(temp) + ":" + func_start_time[1] + " PM"
    func_time = function_start_time

    docs = store.collection("venues").stream()
    v_list = []
    print("docs = ",docs)
    for doc in docs:
        for k in doc.to_dict():
            v_list.append(doc.to_dict()[k])
    print(v_list)
    print(venue_collection_list)
    for venue in venue_collection_list:
        print("venue--------->",venue)
        for k in venue:
            if(venue["func_date"]==func_date_ck):
                if(venue["time_duration_start"]==func_time):
                    print(venue["venue"])
                    v_list.remove(venue["venue"])
                break
                    #v_list.remove(venue["venue"])



    db=store.collection("function_data").where("organizer_mail_id","==",mail_id).get()
    func_list = []
    for data in db:
        key = data.id
        func = store.collection("function_data").document(key).get()
        print(func)
        func_list.append(func.to_dict())

    return render_template("function_form.html",date = func_date_ck,venue=v_list,mailid=mail_id,function=func_list)
        

if __name__=='__main__':
    app.run(debug=True)