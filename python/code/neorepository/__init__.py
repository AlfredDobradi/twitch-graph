from py2neo import Graph, Node, Relationship

neo = Graph(host="neo", user="twitch", password="twitch")


class Neorepository:
    def findOrCreateUser(self, user):
        existing = neo.find_one(label="User",
                                property_key="twitch_id",
                                property_value=user["_id"])
        if existing is None:
            u = Node('User',
                     name=user["name"],
                     twitch_id=user["_id"])
            neo.create(u)
            return u
        else:
            return existing

    def findUser(self, user):
        existing = neo.find_one(label="User",
                                property_key="twitch_id",
                                property_value=user["_id"])
        if existing is None:
            return False
        else:
            return existing

    def findOrCreateRelation(self, user_from, user_to):
        existing = neo.match_one(start_node=user_from,
                                 rel_type="FOLLOWS",
                                 end_node=user_to)
        if existing is None:
            r = Relationship(user_from, "FOLLOWS", user_to)
            neo.create(r)
            return r
        else:
            return existing
