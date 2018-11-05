from pymongo import MongoClient
from bson.code import Code

client = MongoClient('localhost', 27017)
db = client.twitterdb
collection = db.testcollection1


mapper = Code("""
            function() {

                var date = this.user.created_at;
                var user = this.user.id_str;
                date = date.split(" ");
                var day = String(date[2]);
                var month = String(date[1]);
                var year = String(date[5]);
                
                emit(month.concat(year), user);
            }
            """)

reducer = Code("""
            function(key, values) {
                var total = 0;
                var user_list = [];
                var result = '';
                for (var i = 0; i < values.length; i++) {
                    result = result.concat(values[i]).concat(',');
                } 
                
                return result
            }
            """)

result = collection.map_reduce(mapper, reducer, "myresults")