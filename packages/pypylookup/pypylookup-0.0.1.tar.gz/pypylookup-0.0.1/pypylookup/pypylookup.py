class PyPyLookup:
    def __init__(self,key_dataframe,new_dataframe):
        self.key_df = key_dataframe
        self.mapping = {}
        self.new_df = new_dataframe


    def find_col(self,df,name):
        cols = list(df.columns)
        cols = [x.lower() for x in cols]
        try:
            return cols.index(name.lower())
        except:
            print("Can not find the ", name, "column in the file")

    
    def insert_column(self,name,value=" "):
        lst = []
        col = self.find_col(self.new_df, name)
        for data in self.new_df.values:
            try:
                tmp = str(data[col]).upper()
            except:
                tmp = "Nan"
            if tmp in self.mapping:
                lst.append(self.mapping[tmp])
            else:
                print(tmp,"not there")
                lst.append(value)
        return lst
    
    def lookup_file(self,key,value):
        key_no = self.find_col(self.key_df,key)
        value_no = self.find_col(self.key_df,value)
        for data in self.key_df.values:
            name = str(data[key_no]).upper()
            self.mapping[name] = data[value_no]
    
    