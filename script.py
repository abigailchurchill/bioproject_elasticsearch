import json

with open('static/output.json') as f:
    archives = json.loads(f.read())


def edit_dataset():
    docs=[]
    archive_ids=[]
    desc=[]
    titles=[]
    names=[]
    documents=archives['PackageSet']['Package']
    for i in documents:
        a_id=i['Project']['Project']['ProjectID']['ArchiveID']['@id']
        archive_ids.append(a_id)
        if 'Name' not in i['Project']['Project']['ProjectDescr']:
            name='N/A'
        else:
            name=i['Project']['Project']['ProjectDescr']['Name']
        names.append(name)
        if 'Title' not in i['Project']['Project']['ProjectDescr']:
            title='N/A'
        else:
            title =i['Project']['Project']['ProjectDescr']['Title']
        titles.append(title)
        if 'Description' not in i['Project']['Project']['ProjectDescr']:
            description='N/A'
        else:
            description=i['Project']['Project']['ProjectDescr']['Description']
        desc.append(description)
        doc={
            "name":name,
            "title":title,
            "description":description,
            "archive_id":a_id
        }
        docs.append(doc)
    return docs


with open('static/changed_dataset.json', 'w') as json_file:
    json.dump(edit_dataset(), json_file)