#!/usr/bin/env python

import sys
import os
import getopt

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
import ast

PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

##############################################################################
##############################################################################

_BASE_URL = "https://wl11gp.neu.edu/udcprod8/"

# requests base+endpoint via get/post with provided parameters
# should NOT be called directly
def _call(endpoint, method, params):
    return getattr(requests,method)(urljoin(_BASE_URL, endpoint), data=params)

# get an endpoint with provided parameters
def _get(endpoint, params={}):
    return _call(endpoint, "get", params)

# post to an endpoint with provided parameters
def _post(endpoint, params={}):
    return _call(endpoint, "post", params)

##############################################################################
##############################################################################

# parses all the options in a select
# returns {value:string}
def _parse_select(select):
    return {str(option["value"]):str(option.string).strip() for option in select.find_all("option")}

# an (imperfect) Banner form parser
# provides a dictionary...
#  title: page title
#  action: form action
#  method: form method (e.g. get/post)
#  params: {
#    key: value (hidden fields and selects)
# }
def _parse_form(html):
    retval = { "params":{} }
    soup = BeautifulSoup(html, "html.parser")

    retval["title"] = str(soup.title.string)

    form = soup.find("div", {"class":"pagebodydiv"}).find("form")

    retval["action"] = str(form["action"])
    retval["method"] = str(form["method"])

    for hidden in form.find_all("input", {"type":"hidden"}):
        retval["params"][str(hidden["name"])] = str(hidden["value"])
        
    for select in form.find_all("select"):
        retval["params"][str(select["name"])] = _parse_select(select)
        
    return retval

##############################################################################
##############################################################################

# parses the term-selection form
# params include {term_code:term_name}
def termform():
    return _parse_form(_get("NEUCLSS.p_disp_dyn_sched").text)

# given the output of termform(),
# returns a term code given a term name
def term_to_code(termform, term):
    terms = termform['params']['STU_TERM_IN']
    inv_terms = {v:k for k,v in terms.items()}
    if term in inv_terms:
        return inv_terms[term]
    else:
        return None

##############################################################################
##############################################################################

# parses the empy course-search form
# for a particular term
def searchform(termcode):
    return _parse_form(_post("NEUCLSS.p_class_select", {"STU_TERM_IN":termcode}).text)

# given the output of searchform(),
# returns an instructor code given an instructor name
def instructor_to_code(searchform, instructor):
    instructors = searchform['params']['sel_instr']
    inv_instructors = {v:k for k,v in instructors.items()}
    if instructor in inv_instructors:
        return inv_instructors[instructor]
    else:
        return None

##############################################################################
##############################################################################

# parses the html of a course search, returns...
# TODO: DOCUMENT RETURN WITH EXAMPLES HERE (must be a tuple)
def _parse_course_listing(html):
    retval = { "courses":{} }
    soup = BeautifulSoup(html, "html.parser")

    # retval["title"] = str(soup.title.string)

    pagebody = soup.find("div", {"class":"pagebodydiv"})
    # class_info = pagebody.find_all("TH", {"CLASS":"ddtitle"})
    # class_info = pagebody.find_all(["th", {"class":"ddtitle"}, "form"])
    class_info = pagebody.find_all(["th", {"class":"ddtitle"}, "a"])
    # class_info = pagebody.find_all("a")
    # class_info = pagebody.find_all("TH")
    # class_info = pagebody.find_all("TH")
    # print('pagebody: ', pagebody)
    # print('class_info: ', class_info)
    # print('class_info length: ', len(class_info))
    # print(class_info[0])
    # print(class_info[0]['class'])
    # if class_info[0]['class'] == ['ddtitle']:
    #     print('hello world!!!!!')
    # There is a repeated class name due to find all th and a, filter them out
    class_info = [info for info in class_info if not (info.name == 'th' and info['class'] == ['ddtitle'])]
    # Filter out Syllabus Available link tag
    class_info = [info for info in class_info if not info.text == 'Syllabus Available']
    # print('class_info: ', class_info)
    cur_prerequestLst = {}
    class_num_label_set = set()
    # class_num should be unique
    # e.g CS_5001 [ label="CS 5001\n" ]; and CS_5001 [ label="CS 5001\nIntensive Foundations of Computer Science" ];
    # we only want to take the latter
    class_num_set_class_num_label_set = {}
    # class_num_label_lst = []
    i = 0
    new_class = True
    # for info in class_info:
    for i in range(len(class_info)):
        if new_class and class_info[i].text != 'Return to Previous':
            name, crn, class_num, class_num_hyphenated, section_campus, credits = _parse_class_str(class_info[i].text)
            cur_prerequestLst[class_num_hyphenated] = []
            # class_num_set.add(class_num_hyphenated)
            # if (class_num_hyphenated in class_num_set_class_num_label_set):
            class_num_set_class_num_label_set[class_num_hyphenated] = '{} [ label="{}\\n{}" ];'.format(class_num_hyphenated, class_num, name)
            # else:

            # class_num_label_set.add('{} [ label="{}\n{}" ];'.format(class_num_hyphenated, class_num, name))
            # class_num_label_lst.append('{} [ label="{}\n{}" ]'.format(class_num_hyphenated, class_num, name))
            new_class = False
            while i < len(class_info) - 1:
                if class_info[i+1].text != 'Type':
                    i += 1
                    prereq = '_'.join(class_info[i].text.strip().split(' '))
                    cur_prerequestLst[class_num_hyphenated].append(prereq)
                    if prereq not in class_num_set_class_num_label_set:
                        # class_num_label_set.add('{} [ label="{}\n{}" ];'.format(prereq, class_info[i].text.strip(), ''))
                        class_num_set_class_num_label_set[prereq] = '{} [ label="{}\\n{}" ];'.format(prereq, class_info[i].text.strip(), '')
                    # class_num_label_lst.append('{} [ label="{}\n{}" ]'.format(prereq, class_info[i].text.strip(), ''))
                else:
                    break
        if class_info[i].text == 'Room Size':
            new_class = True
        # print(type(class_info[i].text))
        # print(i, class_info[i].text)
        i += 1
    # for info in class_info:
    # class_num_label_lst = sorted(list(class_num_label_set))
    class_num_label_lst = sorted(list(class_num_set_class_num_label_set.values()))

    # print('cur_prerequestLst: ', cur_prerequestLst)
    # print('class_num_label_lst: ', class_num_label_lst)

    return cur_prerequestLst, class_num_label_lst

    # retval["action"] = str(form["action"])
    # retval["method"] = str(form["method"])

    # for hidden in form.find_all("input", {"type":"hidden"}):
    #     retval["courses"][str(hidden["name"])] = str(hidden["value"])

    # for select in form.find_all("select"):
    #     retval["courses"][str(select["name"])] = _parse_select(select)

    # return (None, None, None) # TODO: replace with your code

def _parse_class_str(class_str):
    # print(class_str.strip().split(' - '))
    name, crn, class_num, section_campus, credits = class_str.strip().split(' - ')
    class_num_hyphenated = '_'.join(class_num.split(' '))
    # print(name, crn, class_num, section_campus, credits)
    return name, crn, class_num, class_num_hyphenated, section_campus, credits

# execute a course search request
# returns the parsed result: format of your choice (must be a tuple)
# (see _parse_course_listing for details)
def coursesearch(termcode, 
                 sel_day=[], sel_subj=["%"], sel_attr=["%"],
                 sel_schd=["%"], sel_camp=["%"], sel_insm=["%"], 
                 sel_ptrm=["%"], sel_levl=["%"], sel_instr=["%"], sel_seat=[],
                 sel_crn="", sel_crse="", sel_title="", sel_from_cred="", sel_to_cred="",
                 begin_hh="0", begin_mi="0", begin_ap="a",
                 end_hh="0", end_mi="0", end_ap="a"):
    
    # required parameters
    # (or Banner gets unhappy)
    params = [
        ("STU_TERM_IN", termcode),
        ("sel_day", "dummy"),
        ("sel_subj", "dummy"),
        ("sel_attr", "dummy"),
        ("sel_schd", "dummy"),
        ("sel_camp", "dummy"),
        ("sel_insm", "dummy"),
        ("sel_ptrm", "dummy"),
        ("sel_levl", "dummy"),
        ("sel_instr", "dummy"),
        ("sel_seat", "dummy"),
        ("p_msg_code", "You can not select All in Subject and All in Attribute type."),
        
        ("sel_crn", sel_crn),
        ("sel_crse", sel_crse),
        ("sel_title", sel_title),
        ("sel_from_cred", sel_from_cred),
        ("sel_to_cred", sel_to_cred),
        
        ("begin_hh", begin_hh),
        ("begin_mi", begin_mi),
        ("begin_ap", begin_ap),
        ("end_hh", end_hh),
        ("end_mi", end_mi),
        ("end_ap", end_ap),
    ]

    # print('here', sel_subj)
    # print('here2', sel_levl)

    # if sel_attr != ["%"]:
    #     for attr in sel_attr:
    #         params.append(("sel_attr", attr))
    # else:
    #     params.append(("sel_attr", attr))
    for attr in sel_attr:
        params.append(("sel_attr", attr))

    # if sel_subj != ["%", "%"]:
    #     for sub in sel_subj:
    #         params.append(("sel_subj", sub))
    # else:
    #     params.append(("sel_subj", sub))
    for sub in sel_subj:
        params.append(("sel_subj", sub))

    # if sel_levl != ["%"]:
    #     for level in sel_levl:
    #         params.append(("sel_levl", level))
    # else:
    #     params.append(("sel_levl", level))
    for level in sel_levl:
        params.append(("sel_levl", level))

    # if sel_instr != ["%"]:
    #     for ins in sel_instr:
    #         params.append(("sel_instr", ins))
    # else:
    #     params.append(("sel_instr", ins))
    for ins in sel_instr:
        params.append(("sel_instr", ins))

    # print('params: ', params)
    
    # TODO
    # 1. Take function parameters and add to params
    # 2. Submit form with parameters
    # 3. Call _parse_course_listing to parse, return
    # print(_post("NEUCLSS.p_class_search", params))
    course_listing = _post("NEUCLSS.p_class_search", params).text
    # print('course_listing:', course_listing)
    return _parse_course_listing(course_listing)

##############################################################################
##############################################################################

# takes in output of coursesearch
# and outputs to the console a digraph of related courses
# in DOT format
def print_course_dot(cur_prerequestLst, class_num_label_lst):
    # print("TODO")
    # print('class_num_label_lst: ', '\n'.join(class_num_label_lst))

    # print('class_num_label_lst: ', class_num_label_lst)

    # class_num_label_lst = '\n'.join(repr(line) for line in class_num_label_lst if line)
    # class_num_label_str = ast.literal_eval(class_num_label_lst)
    # print('class_num_label_str: ', class_num_label_str)
    arrowLst = []
    for cur, prerequestLst in cur_prerequestLst.items():
        for prereq in sorted(prerequestLst):
            arrowLst.append('{} -> {};'.format(prereq, cur))
    res = []
    res.append('digraph G {')
    res.append('rankdir="LR";')
    res.append('node [width=5, height=1];')
    res += class_num_label_lst
    res += sorted(arrowLst)
    res.append('}')
    # print([line for line in res if line])
    resStr = '\n'.join(res)
    # resStr = '\n'.join(repr(line) for line in res if line)
    # resStr = '\n'.join(ast.literal_eval(line) for line in res if line)

    # print(type(resStr))
    # resStr = ast.literal_eval(resStr)
    print(resStr)

##############################################################################
##############################################################################

# outputs usage statement and exits
def usage():
    print("usage:", PROG_NAME, "(--level)*", "(--instructor)*", "(--subject)*", "[--course]", "<term code>")
    print(" ()* can occur 0 or more times")
    print(" [] can occur 0 or 1 time")
    print(" <> must be provided")
    sys.exit(2)

# 1. parses command-line parameters
#    - uses term form to validate term
#    - uses search form to validate level, instructor, subject
# 2. performs a course search
# 3. outputs information in DOT format
def main(argv):
    opts,args = getopt.getopt(argv,"",["level=", "instructor=", "subject=", "course="])
    
    #####
    
    if len(args) != 1:
        usage()
        
    term = args[0]
    termcode = term_to_code(termform(), term)
    if termcode is None:
        print("ERROR: invalid term")
        usage()
        
    #####
        
    sform = searchform(termcode)
        
    levels = []
    instructors = []
    subjects = []
    course = None

    for opt in opts:
        if opt[0] == "--course":
            if course is not None:
                print("ERROR: only one course allowed")
                usage()
            else:
                course = opt[1]
                
        elif opt[0] == "--level":
            if opt[1] in sform['params']['sel_levl'].keys():
                levels.append(opt[1])
            else:
                print("ERROR: invalid level '{}'".format(opt[1]))
                usage()
                
        elif opt[0] == "--instructor":
            instructorcode = instructor_to_code(sform, opt[1])
            if instructorcode is not None:
                instructors.append(instructorcode)
            else:
                print("ERROR: invalid instructor '{}'".format(opt[1]))
                usage()
                
        elif opt[0] == "--subject":
            if opt[1] in sform['params']['sel_subj'].keys():
                subjects.append(opt[1])
            else:
                print("ERROR: invalid subject '{}'".format(opt[1]))
                usage()
    
    if not len(levels):
        levels = ["%"]
        
    if not len(instructors):
        instructors = ["%"]
        
    if not len(subjects):
        subjects = ["%", "%"]
        
    if course is None:
        course = ""
        
    # print('termcode: ', termcode)
    # print('levels: ', levels)
    # print('instructors: ', instructors)
    # print('subjects: ', subjects)
    # print('termcode: ', termcode)

    info = coursesearch(termcode,
        sel_levl=levels,
        sel_instr=instructors,
        sel_subj=subjects,
        sel_crse=course
    )
    
    #####
    
    print_course_dot(*info)
    
if __name__ == "__main__":
    main(sys.argv[1:])
