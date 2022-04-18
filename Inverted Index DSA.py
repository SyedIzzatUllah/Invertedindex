
# coding: utf-8

# In[2]:


import re  
class Appearance:
    #represnts the appearnce anf frequency of the word in a document.
    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency 
        
    #string represntion  
    def __repr__(self):

        return str(self.__dict__)
#database shows the index words
class Database:
    def __init__(self):
        self.db = dict()
    #string represntation of the object in database
    def __repr__(self):
        
        return str(self.__dict__)
    
    def get(self, id):
        return self.db.get(id, None)
    
#adding a document in database    
    def add(self, document):
        return self.db.update({document['id']: document})
#apperantly removes the document from database
    def remove(self, document): 
        
        return self.db.pop(document['id'], None)
    
#now, the inverted index class

class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db
#string represntion of the inverted index class object
    def __repr__(self):
        
        return str(self.index)
    
#proccess and saves the document
        
    def index_document(self, document):
        
        # Remove punctuation from the text.
        clean_text = re.sub(r'[^\w\s]','', document['text'])
        terms = clean_text.split(' ')
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
            
        # Update the inverted index
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

#Returns the dictionary of terms with their correspondent Appearances.
#it is a naive search[It checks for all character of the main string to the pattern.], and apperas the term where they are.
    def lookup_query(self, query):
        return { term: self.index[term] for term in query.split(' ') if term in self.index }
def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    return " in database {id}: {replaced}".format(id=id, replaced=replaced_text)
def main():
    db = Database()
    index = InvertedIndex(db)
    document1 = {
        'id': '1',
        'text': 'inverted index is a data type.'
    }
    document2 = {
        'id': '2',
        'text': 'inverted index is very easy to develop'
    }
    index.index_document(document1)
    index.index_document(document2)
    
    
    search_term = input("Enter the term you want to search: ")
    result = index.lookup_query(search_term)
    
    for term in result.keys():
        for appearance in result[term]:
            # Belgium: { docId: 1, frequency: 1}
            document = db.get(appearance.docId)
            print(highlight_term(appearance.docId, term, document['text']))
        print("-----------------------------")    
    
main()

