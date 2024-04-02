from . import generic


class Relation(object):
    """Relation is a common representation of a relation between two ci."""

    def __init__(self, sys_id, relation_type_id, target_sys_id):
        self.sys_id = sys_id
        self.rel_type = relation_type_id
        self.target_sys_id = target_sys_id


class CmdbRelation(Relation):
    """
        CmdbRelation is an opiniated representation of the relation from CMDB Instance API.
        Please refer to: https://developer.servicenow.com/dev.do#!/reference/api/utah/rest/cmdb-instance-api#cmdb-POST-instance-relation
    """

    def __init__(self, value):
        if "sys_id" not in value:
            raise ValueError("Relation has no sys_id")
        if "type" not in value or not isinstance(value["type"], dict):
            raise ValueError("Relation has no type or type is not a dictionary")
        elif "value" not in value["type"] or not value["type"]["value"]:
            raise ValueError("Relation type has no value")
        if "target" not in value or not isinstance(value["type"], dict):
            raise ValueError("Relation has no target or target is not a dictionary")
        elif "value" not in value["target"] or not value["target"]["value"]:
            raise ValueError("Relation target has no value")

        super(CmdbRelation, self).__init__(
            value["sys_id"],
            value["type"]["value"],
            value["target"]["value"]
        )

    @classmethod
    def from_values(cls, type_sys_id, target_sys_id):
        d = dict(
            sys_id=None,
            type=dict(value=target_sys_id),
            target=dict(value=target_sys_id),
        )
        return cls(d)


class RelationClient(generic.GenericClient, object):
    def __init__(self, configuration_item, client):
        super(RelationClient, self).__init__(client, 1000)
        self.ci = configuration_item
        self.outbound = []
        self.inbound = []

    def __iter__(self):
        for relation in self.outbound:
            yield "outbound", relation
        for relation in self.inbound:
            yield "inbound", relation

    def __sizeof__(self):
        return len(self.inbound) + len(self.outbound)

    def add(self, direction, relation):
        if not isinstance(relation, Relation) and not issubclass(relation, Relation):
            raise ValueError("Provided value is not of type 'Relation'")
        if direction == "outbound":
            self.outbound.append(relation)
        elif direction == "inbound":
            self.inbound.append(relation)

