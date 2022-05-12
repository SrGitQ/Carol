import requests, json
from licenses import getSchDB, getNotionHeaders

# This just contain useful manipulation data for dinamikos_team
# Data used:
#   title
#   formula
#   rich_text
#   select
#   deadline

def getNotionDatabase():
    readUrl = f"https://api.notion.com/v1/databases/{getSchDB()}/query"

    res = requests.post(readUrl, headers=getNotionHeaders())
    data = res.json()
    return data['results']

# DATABASE
class NotionDatabase:
    '''
    This function will make a fetch to the database url to get its json data
    it needs headers with the toke to access.
    '''
    def __init__(self, dbId:str, headers:str):
        readUrl = f"https://api.notion.com/v1/databases/{getSchDB()}/query"
        res = requests.post(readUrl, headers=headers)
        self.cData = res.json()
        self.results = self.cData['results']
        self.objects = self.cData['object']
        self.rows = self.__getRows(self.results)
    
    def __getRows(self, results):
        rows = []
        for result in results:
            rows.append(NotionDBRow(result))
        return rows

    def getRows(self):
        for row in self.rows:
            print(row)

# DATA TYPES
class NotionDBRow:
    def __init__(self, row):
        self.rowData = self.__getRowData(row)
        self.columns = self.__setInitColumns(row['properties'])
    
    def __getRowData(self, props):
        keys = props.keys()
        rowData = {}
        for key in keys:
            if key != 'properties':
                rowData[key] = props[key]
        return rowData

    def __setInitColumns(self, props):
        keys = props.keys()
        formalColumns = {}
        for key in keys:
            propFeature = props[key]
            name = key
            idV = propFeature['id']
            typeV = propFeature['type']
            propData = propFeature[typeV]

            formalColumns[key] = Prop(key, idV, typeV, propData)
        return formalColumns
    
    def setProperty(self, prop, value):
        self.columns[prop] = value

    def getProperty(self, prop):
        return self.columns[prop]
    
    def __str__(self):
        text = ''
        for col in self.columns:
            text += col.__str__() + ' '
        return f'{text}\n '

class Prop:
    def __init__(self, name:str, idV:str, typeV:str, propData):
        self.name = name
        self.idV = idV
        self.typeV = typeV
        self.propData = self.__propParser(typeV,propData)
    
    def __propParser(self, typeV, propData):
        if typeV == 'title':
            return Title(propData)
        elif typeV == 'formula':
            return Formula(propData)
        elif typeV == 'rich_text':
            return Rich_text(propData)
        elif typeV == 'select':
            return Select(propData)
        elif typeV == 'deadline':
            return Deadline(propData)
        else:
            return []

    def __str__(self):
        return f'{self.typeV}'

class Rich_text:
    def __init__(self, prop):
        try:
            prop = prop[0]
        
            self.type = prop['type']
            self.text = Text(prop['text'])
            self.annotations = Annotations(prop['annotations'])
            self.plain_text = prop['plain_text']
            self.href = prop['href']
        except:
            self.prop = prop

class Title(Rich_text):
    def __init__(self, prop):
        super().__init__(prop)

class Formula:
    def __init__(self, prop):
        self.type = prop['type']
        self.number = prop[self.type]

class Text:
    def __init__(self, text):
        self.content = text['content']
        self.link = text['link']

class Annotations:
    def __init__(self, annotations):
        self.bold = annotations['bold']
        self.italic = annotations['italic']
        self.strikethrough = annotations['strikethrough']
        self.underline = annotations['underline']
        self.code = annotation['code']
        self.color = annotation['color']


class Select:
    def __init__(self, prop):
        self.id = prop['id']
        self.name = prop['name']
        self.color = prop['color']

class Deadline:
    def __init__(self, prop):
        self.start = prop['start']
        self.end = prop['end']
        self.time_zone = prop['time_zone']










#from licenses import getSchDB, getNotionHeaders

#database = NotionDatabase(getSchDB(), getNotionHeaders())

#print(database.getRows())














