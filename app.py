from distutils.log import debug
from os import name
import re
from flask import Flask,redirect,render_template,request,jsonify
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
        venue_collection_set.add(i for i in venue_collection)


        docs = store.collection("venues").stream()
        v_list = []
        v_list_set = set()
        print("docs = ",docs)
        for doc in docs:
            for k in doc.to_dict():
                v_list.append(doc.to_dict()[k])
        print(v_list)
        v_list_set.add(i for i in v_list)

        difference_set = v_list_set - venue_collection_set
        difference_list = [i for i in difference_set]


        print(difference_list)



        return render_template("function_form.html",venue = difference_list)

        


@app.route('/submit',methods=["GET","POST"])
def submit():

    s_dict = {}

    #general_details
    s_dict["dept_name"] = request.form.get('department')  
    s_dict["func_name"] = request.form.get('func_name') 
    s_dict["func_days"] = request.form.get('func_days')
    s_dict["time_duration"] = request.form.get('time_duration')
    s_dict["venue"] = request.form.get('venue')
    s_dict["training_type"] = request.form.get('training_type')
    s_dict["func_students"] = request.form.get('func_students')
    s_dict["chief_guest_name"] = request.form.get('chief_guest_name')
    s_dict["designation"] = request.form.get('designation')
    s_dict["field"] = request.form.get('organizer_name')
    s_dict["organizer_name"] = request.form.get('organizer_name')
    s_dict["organizer_contact"] = request.form.get('organizer_contact')

    

    #guest_house  s_dict[""]
    s_dict["guest_house"] =request.form.get('guest_house')
    s_dict["guest_house_pesons"] = request.form.get('guest_house_persons')
    s_dict["guest_house_days"] = request.form.get('guest_house_days')

    #refreshment
    s_dict["refreshment_for_guest"] = request.form.get('refreshment_for_guest')
    s_dict["refreshment_for_guest_number"] = request.form.get('refreshment_guest_number')
    s_dict["refreshment_for_student"] = request.form.get('refreshment_for_student')
    s_dict["refreshment_for_student_number"] = request.form.get('refreshment_student_number')
    s_dict["payment_through"] = request.form.get('payment_through')
    s_dict["lunch_exact_numbers"] = request.form.get('lunch_exact_numbers')
    s_dict["tiffin"] = request.form.get('tiffin')
    s_dict["spl_lunch_veg"] = request.form.get('spl_lunch_veg')
    s_dict["spl_lunch_non_veg"] = request.form.get('spl_lunch_non_veg')
    s_dict["lunch_required_time"] = request.form.get('lunch_required_time')

    #transport
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

    store.collection("function_data").add(s_dict)

    print("DATA SAVED TO DATABASE !!!")

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
    print("venue_collection_se=====>",venue_collection_set)
    print("v_list_set===>",v_list_set)
    #v_list_set.difference(venue_collection_set)

    difference_set = v_list_set - venue_collection_set
    difference_list = [i for i in difference_set]
    print("v_difference_set===============>",difference_set)
    print(difference_list)

    return render_template("function_form.html",venue=difference_list)

if __name__=='__main__':
    debug = True
    app.run()