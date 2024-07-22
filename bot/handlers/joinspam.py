
class JoinSpam:

    @staticmethod
    def is_in_list(user_id: str):
        with open("joinspam.txt", "r") as file:
            if user_id in file.read():
                return True
            else:
                return False
            
    @staticmethod
    def append(user_id: str, author: str):
        with open("./data/joinspam.txt", "a") as file:
            file.write("\n%s:%s" % (user_id , author))
        
    @staticmethod
    def remove(user_id: str, author: str):
        with open("./data/joinspam.txt", "r") as file:
            user_ids = [i.strip() for i in file.readlines()]

        key = lambda line: not line.startswith("%s:%s" % (user_id, author))

        new_ids = [i for i in filter(key, user_ids)]

        with open("./data/joinspam.txt", "w") as file:
            file.write("\n".join(new_ids))
    
    @staticmethod
    def user_joinspams(user_id: str):
        with open("./data/joinspam.txt", "r") as file:
            user_ids = [i.strip() for i in file.readlines()]

        key = lambda line: line.endswith(user_id)

        new_ids = [i for i in filter(key, user_ids)]

        return new_ids
    
