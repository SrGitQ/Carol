import requests, json
from licenses import getSchDB, getNotionHeaders

# This just contain useful manipulation data for dinamikos_team
# Data used:
#   title
#   formula
#   rich_text
#   select
#   deadline

def saveJson(data):
    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

# DATABASE
class NotionDatabase:
    '''
    This function will make a fetch to the database url to get its json data
    it needs headers with the toke to access.
    '''
    def __init__(self, dbId:str, headers:str):
        readUrl = f"https://api.notion.com/v1/databases/{dbId}/query"
        res = requests.post(readUrl, headers=headers)
        self.cData = res.json()
        self.results = self.cData['results']
        self.objects = self.cData['object']
        #saveJson(self.results)
        self.rows = self.__getRows(self.results)
    
    def __getRows(self, results):
        rows = []
        for result in results:
            row = NotionDBRow(result)
            
            rows.append(row)
        return rows

    def printRows(self):
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
        text =''
        for col in self.columns.keys():
            coltext = self.columns[col].__str__()
            # print(coltext)
            text += coltext + ' '
        return f'{text}\n '

class Prop:
    def __init__(self, name:str, idV:str, typeV:str, propData):
        self.name = name
        self.idV = idV
        self.typeV = typeV
        self.propData = self.propParser(typeV,propData)
        self.value = self.propData.__str__()
    
    def propParser(self, typeV, propData):
        if typeV == 'title':
            return Title(propData)
        elif typeV == 'formula':
            return Formula(propData)
        elif typeV == 'rich_text':
            return Rich_text(propData)
        elif typeV == 'select':
            return Select(propData)
        elif typeV == 'date':
            return Deadline(propData)
        else:
            return []

    def __repr__(self):
        return self.propData.__str__()

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
            self.type = ''
            self.text = ''
            self.annotations = ''
            self.plain_text = ''
            self.href = ''
    def __str__(self):
        return f'{self.text}'

class Title(Rich_text):
    def __init__(self, prop):
        super().__init__(prop)

class Formula:
    def __init__(self, prop):
        self.type = prop['type']
        self.number = prop[self.type]
    def __str__(self):
        return f'{self.number}'

class Text:
    def __init__(self, text):
        self.content = text['content']
        self.link = text['link']
    def __str__(self):
        return f'{self.content}'

class Annotations:
    def __init__(self, annotations):
        self.bold = annotations['bold']
        self.italic = annotations['italic']
        self.strikethrough = annotations['strikethrough']
        self.underline = annotations['underline']
        self.code = annotations['code']
        self.color = annotations['color']

class Select:
    def __init__(self, prop):
        self.id = prop['id']
        self.name = prop['name']
        self.color = prop['color']
    def __str__(self):
        return f'{self.name}'

class Deadline:
    def __init__(self, prop):
        self.start = prop['start']
        self.end = prop['end']
        self.time_zone = prop['time_zone']
    def __str__(self):
        return f'{self.start}={self.end}'
