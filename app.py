#!/usr/bin/env python
from flask import Flask, jsonify
from flask import request,make_response,abort
import sys
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hey welcome to release v1.0"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No results'}), 404)

@app.route('/api/v1.0/data', methods=['GET'])
def get_data():
    return jsonify(FILE_DATA)

@app.route('/api/v1.0/search/<string:name>', methods=['GET'])
def Search_by_all(name):
    r_list1 = [r_list for r_list in FILE_DATA if r_list['name'] == name]
    r_list2 = [r_list for r_list in FILE_DATA if r_list['location'] == name]
    r_list3 = [r_list for r_list in FILE_DATA if r_list['cuisine'] == name]
    r_list = sum([r_list1,r_list2,r_list3],[])
    if len(r_list) == 0:
        abort(404)
    return jsonify({'RESTRAUNTS': r_list})

@app.route('/api/v1.0/search/<string:res_name>/<int:capacity>', methods=['GET'])
def capacity_search(res_name,capacity):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == res_name]
    new_list = res_list[0]["tables"]
    new_list1 = convert_keys_to_string(new_list)
    t_list = {key:value for key,value in new_list1.iteritems() if value['capacity'] == capacity}

    if len(t_list) == 0:
        abort(404)
    return jsonify({'Tables': t_list})

@app.route('/api/v1.0/remove_restraunt/<string:res_name>', methods=['GET'])
def remove_restraunt(res_name):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == res_name]
    if len(res_list) == 0:
        return jsonify({'result': "Not found"})
    FILE_DATA.remove(res_list[0])
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    return jsonify({'result': "succesfully removed"})

@app.route('/api/v1.0/add_restraunt/<string:res_name>/<string:cuisine>/<string:location>', methods=['GET'])
def add_restraunt(res_name,cuisine,location):

    restraunt_list = {}
    restraunt_list["name"] = res_name
    restraunt_list["cuisine"] = cuisine
    restraunt_list["location"] = location
    restraunt_list["tables"] = {}
    restraunt_list["reviews"] = ""
    FILE_DATA.append(restraunt_list);
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)

    return jsonify({'result': 'Succesfully added restraunt'})

@app.route('/api/v1.0/<string:what>/<string:re_name>/<string:table>', methods=['GET'])
def book_restaurant(what,re_name,table):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    new_list1 = res_list[0]["tables"]
    flag = 0
    for key,value in new_list1.iteritems():
        if key == table:
            flag += 1
            if what == "book":
                if value['book'] == False:
                    value['book'] = True
                else:
                    return jsonify({'Result': 'Already Booked'})
            elif what == "cancel":
                if value['book'] == True:
                    value['book'] = False
                else:
                    return jsonify({'Result': 'No Booking'})
            else:
                return jsonify({'Result': 'You mis-spelled'})

    for a in FILE_DATA:
        if a["name"] == re_name:
            a["tables"] = new_list1
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    if flag == 0:
        abort(404)
    return jsonify({'Result': 'Succesfully Changed'})

@app.route('/api/v1.0/add_table/<string:re_name>/<string:table>/<int:capacity>', methods=['GET'])
def add_table(re_name,table,capacity):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    new_list1 = res_list[0]["tables"]
    my_data = {u'book':False,u'capacity':capacity,u'availability':True}
    new_list1[u'table3'] = my_data
    for a in FILE_DATA:
        if a["name"] == re_name:
            a["tables"] = new_list1
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    return jsonify({'Result': 'Succesfully added table'})

@app.route('/api/v1.0/remove_table/<string:re_name>/<string:table>', methods=['GET'])
def remove_table(re_name,table):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    new_list1 = res_list[0]["tables"]
    data = new_list1.pop(table)

    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    return jsonify({'Result': 'Succesfully removed table'})

@app.route('/api/v1.0/modify/<string:re_name>/<string:table>/capacity=<int:capacity>', methods=['GET'])
def modify_data(re_name,table,capacity):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    new_list1 = res_list[0]["tables"]
    flag = 0

    for key,value in new_list1.iteritems():
        if key == table:
            flag += 1
            if(capacity):
                value['capacity']= capacity

    for a in FILE_DATA:
        if a["name"] == re_name:
            a["tables"] = new_list1
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    if flag == 0:
        abort(404)
    return jsonify({'Result': 'Succesfully Changed'})

@app.route('/api/v1.0/modify/<string:re_name>/<string:table>/availability=<string:availability>', methods=['GET'])
def modify_data1(re_name,table,availability):

    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    new_list1 = res_list[0]["tables"]
    flag = 0

    for key,value in new_list1.iteritems():
        if key == table:
            flag += 1
            if(availability):
                value['availability']= availability

    for a in FILE_DATA:
        if a["name"] == re_name:
            a["tables"] = new_list1
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    if flag == 0:
        abort(404)
    return jsonify({'Result': 'Succesfully Changed'})

@app.route('/api/v1.0/reviews/<string:re_name>/<string:review>', methods=['GET'])
def write_review(re_name,review):
    res_list = [res_list for res_list in FILE_DATA if res_list['name'] == re_name]
    res_list[0]["reviews"] = review

    for a in FILE_DATA:
        if a["name"] == re_name:
            a = res_list
    with open(FILE, "w") as wfile:
        json.dump(FILE_DATA, wfile)
    return jsonify({'Result': 'Succesfully written review'})

def get_file_data():
    try:
        with open(FILE) as rfile:
            return json.load(rfile)
    except Exception as ie:
        return {
         "error":"Can't able to load file"
        }

def main():
    global FILE,FILE_DATA
    FILE = 'restraunt.json'
    FILE_DATA = get_file_data()
    app.run(debug=True)

def convert_keys_to_string(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

if __name__ == '__main__':
    main()
